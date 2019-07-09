# coding: utf-8
"""
Fecha de creacion 6/1/19
@autor: mjapon
"""
import logging

log = logging.getLogger(__name__)

import os
from pyreportjasper import JasperPy


def processing():
    input_file = os.path.dirname(os.path.abspath(__file__)) + \
                 '/facturaA4.jasper'

    print 'ruta del archivo es:'
    print input_file

    output = os.path.dirname(os.path.abspath(__file__)) + '/output'
    jasper = JasperPy()
    jasper.process(
        input_file,
        output_file=output,
        format_list=["pdf"],
        parameters={'NroFactura':'12121212'}
    )

def main():
    print("python main function")
    processing()
    print "fin-->"

if __name__ == '__main__':
    main()