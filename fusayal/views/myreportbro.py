# coding: utf-8
"""
Fecha de creacion 5/25/19
@autor: mjapon
"""
import logging

from fusayal.logica.cuotas.reportrequest_dao import ReportRequestDao
from fusayal.utils.pyramidutil import DbComunView
from pyramid import httpexceptions
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, BLOB, Boolean, DateTime, Integer, String, Text, MetaData
from sqlalchemy import func
from reportbro import Report, ReportBroError
import datetime, decimal, json, os, uuid

log = logging.getLogger(__name__)

'''
myreportbro server example
'''


MAX_CACHE_SIZE = 500 * 1024 * 1024  # keep max. 500 MB of generated pdf files in sqlite db

"""
engine = create_engine('sqlite:///:memory:', echo=False)
db_connection = engine.connect()
metadata = MetaData()
report_request = Table('report_request', metadata,
    Column('id', Integer, primary_key=True),
    Column('key', String(36), nullable=False),
    Column('report_definition', Text, nullable=False),
    Column('data', Text, nullable=False),
    Column('is_test_data', Boolean, nullable=False),
    Column('pdf_file', BLOB),
    Column('pdf_file_size', Integer),
    Column('created_on', DateTime, nullable=False))

metadata.create_all(engine)
"""

def jsonconverter(val):
    if isinstance(val, datetime.datetime):
        return '{date.year}-{date.month}-{date.day}'.format(date=val)
    if isinstance(val, decimal.Decimal):
        return str(val)

@view_defaults(route_name='reportbro')
class ReportBroView(DbComunView):


    def __init__(self, request):
        DbComunView.__init__(self, request)
        self.additional_fonts = []


        #self.initialize(db_connection)

    """
    def initialize(self, db_connection):
        self.db_connection = db_connection
        # if using additional fonts then add to this list
        self.additional_fonts = []
    """

    def set_access_headers(self):
        headers_dict = dict()
        headers_dict['Access-Control-Allow-Origin'] = '*'
        headers_dict['Access-Control-Allow-Methods'] = 'GET, PUT, OPTIONS'
        headers_dict['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept, Z-Key'
        return headers_dict

    @view_config(request_method='OPTIONS')
    def options_logic(self):
        headers = self.set_access_headers()
        res = Response(headers=headers, body="options response")
        return res

    @view_config(request_method='PUT')
    def put_logic(self):

        headers = self.set_access_headers()
        res = Response(headers=headers, body="put response")

        json_data = json.loads(self.request.body.decode('utf-8'))
        report_definition = json_data.get('report')
        output_format = json_data.get('outputFormat')
        if output_format not in ('pdf', 'xlsx'):
            raise httpexceptions.HTTPBadRequest(detail='outputFormat parameter missing or invalid')
        data = json_data.get('data')
        is_test_data = bool(json_data.get('isTestData'))

        try:
            report = Report(report_definition, data, is_test_data, additional_fonts=self.additional_fonts)
        except Exception as e:
            raise httpexceptions.HTTPBadRequest(detail='failed to initialize report: ' + str(e))

        if report.errors:
            print "Errores al generar el reporte"
            print report.errors
            return Response(json.dumps(dict(errors=report.errors)))
        try:
            now = datetime.datetime.now()

            # delete old reports (older than 3 minutes) to avoid table getting too big
            """
            self.db_connection.execute(report_request.delete().where(
                report_request.c.created_on < (now - datetime.timedelta(minutes=3))))

            total_size = self.db_connection.execute(select([func.sum(report_request.c.pdf_file_size)])).scalar()
            if total_size and total_size > MAX_CACHE_SIZE:
                # delete all reports older than 10 seconds to reduce db size for cached pdf files
                self.db_connection.execute(report_request.delete().where(
                    report_request.c.created_on < (now - datetime.timedelta(seconds=10))))
            """

            report_file = report.generate_pdf()

            key = str(uuid.uuid4())
            # add report request into sqlite db, this enables downloading the report by url (the report is identified
            # by the key) without any post parameters. This is needed for pdf and xlsx preview.

            dao = ReportRequestDao(self.dbsession)

            dao.crear(
                key=key, report_definition=json.dumps(report_definition),
                data=json.dumps(data, default=jsonconverter), is_test_data=False,
                pdf_file=report_file)

            #self.write('key:' + key)
            res.body ="key:"+key
            return res
        except ReportBroError as e:
            print "error en put logic"
            print e
            return json.dumps(dict(errors=report.errors))

        #return Response("PUT response")






    @view_config(request_method='GET')
    def get_logic(self):

        headers = self.set_access_headers()
        res = Response(headers=headers, body="get response")

        output_format = self.request.params['outputFormat']
        assert output_format in ('pdf', 'xlsx')
        key = self.request.params['key']
        report = None
        report_file = None
        if key and len(key) == 36:
            # the report is identified by a key which was saved
            # in an sqlite table during report preview with a PUT request
            dao = ReportRequestDao(self.dbsession)
            row = dao.get(key= key)
            if not row:
                raise httpexceptions.HTTPBadRequest(detail='report not found (preview probably too old), update report preview and try again')
            if output_format == 'pdf' and row.pdf_file:
                report_file = row.pdf_file
            else:
                report_definition = json.loads(row.report_definition)
                data = json.loads(row.data)
                is_test_data = row.is_test_data
                report = Report(report_definition, data, False, additional_fonts=self.additional_fonts)
                if report.errors:
                    raise httpexceptions.HTTPBadRequest(detail='error generating report')
        else:
            json_data = json.loads(self.request.body.decode('utf-8'))
            report_definition = json_data.get('report')
            data = json_data.get('data')
            is_test_data = bool(json_data.get('isTestData'))
            if not isinstance(report_definition, dict) or not isinstance(data, dict):
                raise httpexceptions.HTTPBadRequest(detail='report_definition or data missing')
            report = Report(report_definition, data, False, additional_fonts=self.additional_fonts)
            if report.errors:
                raise httpexceptions.HTTPBadRequest(detail='error generating report')

        try:
            now = datetime.datetime.now()
            if output_format == 'pdf':
                if report_file is None:
                    report_file = report.generate_pdf()

                res.content_type = 'application/pdf'
                res.content_disposition ='inline; filename="{filename}"'.format(
                    filename='report-' + str(now) + '.pdf')
            else:
                report_file = report.generate_xlsx()
                res.content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                res.content_disposition ='inline; filename="{filename}"'.format(
                    filename='report-' + str(now) + '.xlsx')
            res.body = report_file
            return res
        except ReportBroError as e:
            print "Error al generar reporte"
            raise httpexceptions.HTTPBadRequest(detail='error generating report')