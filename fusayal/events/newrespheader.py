# coding: utf-8
"""
Fecha de creacion 7/8/19
@autor: mjapon
"""
import logging

log = logging.getLogger(__name__)

from pyramid.events import NewResponse, subscriber

"""
@subscriber(NewResponse)
def add_cors_headers(event):
    if event.request.is_xhr:
        event.response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Methods': 'PUT'
        })
"""