# coding: utf-8
"""
Fecha de creacion 3/25/19
@autor: mjapon
"""
import logging

from fusayal.logica.autorizacion.autorizacion_dao import TAutorizacionDao
from fusayal.logica.contribuyente.contribuyente_dao import TContribuyenteDao
from fusayal.utils.pyramidutil import DbComunView

log = logging.getLogger(__name__)
from cornice.resource import resource


@resource(path="/rest/autorizacion/{aut_id}", collection_path="/rest/autorizacion")
class AutorizacionRest(DbComunView):

    def collection_get(self):
        taudao = TAutorizacionDao(self.dbsession)
        accion = self.get_request_param("accion")

        if accion == None:
            items = taudao.listar_all()
            cols = [{'name': 'aut_numero', 'displayName': 'Número'},
                    {'name': 'cnt_razonsocial', 'displayName': 'Razón social'},
                    {'name': 'cnt_ruc', 'displayName': 'RUC'},
                    {'name': 'td_nombre', 'displayName': 'Documento'},
                    {'name': 'serie', 'displayName': 'Serie'},
                    {'name': 'aut_secuencia_ini', 'displayName': 'Desde'},
                    {'name': 'aut_secuencia_fin', 'displayName': 'Hasta'},
                    {'name': 'aut_fechaautorizacion', 'displayName': 'Fecha autorización'},
                    {'name': 'aut_fechacaducidad', 'displayName': 'Fecha caducidad'}]
            return {'estado': 200, 'items': items, 'cols': cols}
        elif accion == 'contribauts':
            cnt_id = self.get_request_param("cnt_id")
            contribauts = taudao.listar(cnt_id=cnt_id)
            return {'estado': 200, 'items': contribauts}

    def post(self):
        aut_id = self.get_request_matchdict("aut_id")
        if aut_id is not None:
            aut_id = int(aut_id)

        taudao = TAutorizacionDao(self.dbsession)
        if int(aut_id) == 0:
            form = self.get_json_body()
            taudao.crear(form=form)
            return {'estado': 200, 'msg': 'Registro exitoso'}
        else:
            return {'estado': 200, 'msg': 'Ninguna acción realizada'}

    def get(self):
        aut_id = self.get_request_matchdict("aut_id")
        cnt_id = self.get_request_param("cnt_id")
        accion = self.get_request_param("accion")

        taudao = TAutorizacionDao(self.dbsession)

        if aut_id is not None:
            aut_id = int(aut_id)

        contribuyentes = []
        tipos_doc = []
        contribdao = TContribuyenteDao(self.dbsession)

        if accion is None:
            if aut_id == 0:
                contribuyentes = contribdao.listar()
                tipos_doc = taudao.listar_tiposdoc()

                form = taudao.get_form(cnt_id=cnt_id)
                return {'estado': 200, 'form': form, 'contribs': contribuyentes, 'tiposdoc': tipos_doc}

        return {'estado': 201, 'msg': 'Ninguna accion realizada'}
