# coding: utf-8
"""
Fecha de creacion 3/27/19
@autor: mjapon
"""
import logging

from fusayal.logica.autorizacion.autorizacion_dao import TAutorizacionDao
from fusayal.logica.contribuyente.contribuyente_dao import TContribuyenteDao
from fusayal.logica.jobs.job_dao import TJobDao
from fusayal.utils.pyramidutil import DbComunView
from cornice.resource import resource

log = logging.getLogger(__name__)


@resource(path="/rest/job/{job_id}", collection_path="/rest/job")
class TJobRest(DbComunView):

    def collection_get(self):
        tjobdao = TJobDao(self.dbsession)

        accion = self.get_request_param('accion')
        if accion is not None:
            return {'estado': 201, 'msg': 'Ninguna accion realizada'}
        else:
            items = tjobdao.listar()
            cols = [{'name': 'aut_numero', 'displayName': u'Autorización'},
                    {'name': 'cnt_ruc', 'displayName': 'RUC'},
                    {'name': 'cnt_razonsocial', 'displayName': u'Razón Social'},
                    {'name': 'aut_fechaautorizacion', 'displayName': u'Fecha Autorización'},
                    {'name': 'serie', 'displayName': u'Serie'},
                    {'name': 'td_nombre', 'displayName': u'Tipo Documento'},
                    {'name': 'aut_secuencia_ini', 'displayName': u'Desde'},
                    {'name': 'aut_secuencia_fin', 'displayName': u'Hasta'},
                    {'name': 'job_nrocopias', 'displayName': u'Copias'},
                    {'name': 'sjb_nombre', 'displayName': u'Estado'}]
            return {'estado': 200, 'items': items, 'cols': cols}

    def post(self):
        job_id = self.get_request_matchdict('job_id')
        accion = self.get_request_param('accion')

        if job_id is not None:
            job_id = int(job_id)

        tjobdao = TJobDao(self.dbsession)
        if job_id == 0:
            tjobdao.crear(form=self.get_json_body(), user_crea=self.get_userid())
            return {'estado': 200, 'msg': u'Registro exitoso'}

        if accion == 'cambiar_estado':
            form = self.get_json_body()
            tjobdao.actualizar_estado(job_id=job_id, estado=form['newestado'], user_actualiza=self.get_userid())
            return {'estado': 200, 'msg': u'Actualización exitosa'}

        if accion == 'put_reporte':
            form = self.get_json_body()
            tjobdao.actualizar_plantilla(job_id=job_id, temp_id= form['temp_id'])
            return {'estado': 200, 'msg': u'Reporte asignado correctamente'}


        return {'estado': 200, 'msg': 'Ninguna accion realizada'}

    def get(self):
        accion = self.get_request_param('accion')
        tjobdao = TJobDao(self.dbsession)
        if accion == 'form':
            contribdao = TContribuyenteDao(self.dbsession)
            contribuyentes = contribdao.listar()
            return {'estado': 200, 'form': tjobdao.get_form(), 'contribs': contribuyentes}
