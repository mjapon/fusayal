# coding: utf-8
"""
Fecha de creacion 3/25/19
@autor: mjapon
"""
import logging

from fusayal.logica.contribuyente.contribuyente_dao import TContribuyenteDao
from fusayal.utils.pyramidutil import DbComunView
from cornice.resource import resource


@resource(path="/rest/contribuyente/{cnt_id}", collection_path="/rest/contribuyente")
class ContribuyenteRest(DbComunView):

    def collection_get(self):
        contrib_dao = TContribuyenteDao(self.dbsession)
        contribs = contrib_dao.listar()
        cols = [{'name': 'cnt_ruc', 'displayName': 'RUC'},
                {'name': 'cnt_razonsocial', 'displayName': 'Razón social'},
                {'name': 'cnt_telf', 'displayName': 'Telf.'},
                {'name': 'cnt_email', 'displayName': 'Email'},
                {'name': 'cls_nombre', 'displayName': 'Tipo'},
                {'name': 'cnt_nrocntespecial', 'displayName': 'Cont. Especial'},
                {'name': 'ocontab', 'displayName': 'Obl contab.'}]

        return {'estado': 200, 'items': contribs, 'cols': cols}

    def get(self):
        contrib_dao = TContribuyenteDao(self.dbsession)
        accion = self.get_request_param('accion')
        cnt_id = self.get_request_matchdict('cnt_id')
        if accion is not None:
            if accion == 'form':
                form = contrib_dao.get_form()
                tipos_contrib = contrib_dao.get_tipos_contribuyentes()
                if int(cnt_id) != 0:
                    form = contrib_dao.get_form_edit(cnt_id=cnt_id)

                return {'estado': 200,
                        'form': form,
                        'tiposcontrib':tipos_contrib}

    def post(self):
        contrib_dao = TContribuyenteDao(self.dbsession)
        cnt_id = self.get_request_matchdict('cnt_id')
        msg = 'Operación exitosa'
        if int(cnt_id) == 0:
            contrib_dao.crear(form=self.get_json_body())
            return {'estado': 200, 'msg': msg}
        else:
            contrib_dao.editar(form=self.get_json_body())
            return {'estado': 200, 'msg': msg}
