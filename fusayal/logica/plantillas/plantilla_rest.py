# coding: utf-8
"""
Fecha de creacion 2019-06-07
@autor: mjapon
"""
import logging

from fusayal.logica.plantillas.plantilla_dao import TPlantillasDao
from fusayal.utils.pyramidutil import DbComunView
from cornice.resource import resource

log = logging.getLogger(__name__)

@resource(path="/rest/cuotas/{socioid}", collection_path="/rest/cuotas")
class PlantillasRest(DbComunView):

    def __init__(self, request):
        DbComunView.__init__(self, request)
        self.plantillas_dao = TPlantillasDao(self.dbsession)

    def get(self):
        if 'form' in self.request.params:
            pass

        items = self.plantillas_dao.listar()
        return {'status':200, 'items':items}

    def post(self):
        form = self.get_json_body()
        res = self.cuotas_dao.registrar_cuota(
            socio_id=form['socio_id'],
            tipo_cuota=form['tipo'],
            anio=form['anio'],
            mes=form['mes'],
            monto=form['monto'],
            socio_id_reg=self.gsession('socioid'),
            path_compro='',
            obs=form['obs']
        )

        return {'status':200, 'res':res}