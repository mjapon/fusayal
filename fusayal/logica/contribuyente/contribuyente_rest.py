# coding: utf-8
"""
Fecha de creacion 3/25/19
@autor: mjapon
"""

from cornice.resource import resource

from fusayal.logica.contribuyente.contribuyente_dao import TContribuyenteDao
from fusayal.utils.pyramidutil import DbComunView


@resource(path="/rest/contribuyente/{cnt_id}",
          collection_path="/rest/contribuyente", cors_origins=('*',))
class ContribuyenteRest(DbComunView):

    def collection_get(self):
        contrib_dao = TContribuyenteDao(self.dbsession)
        contribs = contrib_dao.listar()
        cols = [{'field': 'cnt_ruc', 'header': 'RUC'},
                {'field': 'cnt_razonsocial', 'header': 'Razón social'},
                {'field': 'cnt_telf', 'header': 'Telf.'},
                {'field': 'cnt_email', 'header': 'Email'},
                {'field': 'cls_nombre', 'header': 'Tipo'},
                {'field': 'cnt_nrocntespecial', 'header': 'Cont. Especial'},
                {'field': 'ocontab', 'header': 'Obl contab.'}]

        accion = None
        if 'accion' in self.request.params:
            accion = self.request.params['accion']
            if accion == 'find':
                ruc = self.request.params['ruc']
                contrib = contrib_dao.find_by_ruc(ruc)
                if contrib is None:
                    return {'estado': 404}
                else:
                    return {'estado': 200, 'contrib': contrib}

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
                        'tiposcontrib': tipos_contrib}

    def post(self):
        contrib_dao = TContribuyenteDao(self.dbsession)
        cnt_id = self.get_request_matchdict('cnt_id')
        msg = 'Operación exitosa'
        if int(cnt_id) == 0:
            contrib_dao.crear(form=self.get_json_body(), user_crea=self.get_userid())
            return {'estado': 200, 'msg': msg}
        else:
            contrib_dao.editar(form=self.get_json_body(), user_edit=self.get_userid())
            return {'estado': 200, 'msg': msg}
