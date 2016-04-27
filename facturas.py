__author__ = 'Dante'

# Codigo para leer facturas y sacar los insumos para la declaracion mensual del SAT

import untangle
import pandas as pn
from os import listdir

# file_path = "150427.UM.0001628.GAN141105UK1.OAAD900808Q32.xml"
# file_path = "/Users/Dante/Dropbox/Recibos Honorarios/2015/Facturas Abril" \
#             "/FacturaXMLOAAD900808Q32D8J88GApr272015174919.xml"

# # Read all the xml files in the directory
# my_directory = "/Users/Dante/Dropbox/Recibos Honorarios/2015/Facturas Abril/"
# all_xmls = [xml_file for xml_file in listdir(my_directory) if xml_file.endswith(".xml")]
#
#
# from os import listdir
# from os.path import isfile, join
# onlyfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]


from os import walk
my_path = "xmls/"
all_xmls = []
for (dirpath, dirnames, filenames) in walk(my_path):
    all_xmls.extend([xml_file for xml_file in filenames if xml_file.endswith('.xml')])

# Iterate
es = []
for xml_name in all_xmls:
    factura = untangle.parse(my_path + xml_name)
    # Write a dictionary with this stuff
    the_dict = {}
    the_dict['nombre'] = xml_name
    the_dict['fecha'] = factura.cfdi_Comprobante.get_attribute('fecha')
    the_dict['subtotal'] = factura.cfdi_Comprobante.get_attribute('subTotal')
    the_dict['total'] = factura.cfdi_Comprobante.get_attribute('total')
    the_dict['emisor'] = factura.cfdi_Comprobante.cfdi_Emisor.get_attribute('nombre')
    try:
        the_dict['impuesto'] = factura.cfdi_Comprobante.cfdi_Impuestos.cfdi_Traslados.cfdi_Traslado.get_attribute('impuesto')
        the_dict['importe'] = factura.cfdi_Comprobante.cfdi_Impuestos.cfdi_Traslados.cfdi_Traslado.get_attribute('importe')
    except AttributeError:
        the_dict['impuesto'] = u'IVA'
        the_dict['importe'] = factura.cfdi_Comprobante.cfdi_Impuestos.get_attribute('totalImpuestosTrasladados')
    es.append(the_dict)

# Dataframe the list of dictionaries
data_facturas = pn.DataFrame(es)
# Change the columns to the correct data types
data_facturas['fecha'] = data_facturas.fecha.map(lambda x: pn.to_datetime(x, format='%Y-%m-%dT%H:%M:%S'))
for my_col in ['subtotal', 'total', 'importe']:
    data_facturas[my_col] = data_facturas[my_col].astype(float)




