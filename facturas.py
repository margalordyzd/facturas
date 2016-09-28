__author__ = 'Dante'

# Codigo para leer facturas y sacar los insumos para la declaracion mensual del SAT

import untangle
import pandas as pn
from os import listdir
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
    except (AttributeError, IndexError):
        the_dict['impuesto'] = u'IVA'
        the_dict['importe'] = factura.cfdi_Comprobante.cfdi_Impuestos.get_attribute('totalImpuestosTrasladados')
    es.append(the_dict)

# Dataframe the list of dictionaries
data_facturas = pn.DataFrame(es)
# Change the columns to the correct data types
data_facturas['fecha'] = data_facturas.fecha.map(lambda x: pn.to_datetime(x, format='%Y-%m-%dT%H:%M:%S'))
for my_col in ['subtotal', 'total', 'importe']:
    data_facturas[my_col] = data_facturas[my_col].astype(float)

# data_hist_columns = data_facturas.columns.tolist()
# data_hist_columns.append('for_isr')
# facturas_hist = pn.DataFrame(columns=data_hist_columns)
# facturas_hist.to_pickle('facturas_hist.pkl')

facturas_hist = pn.read_pickle('facturas_hist.pkl')

nuevas_facturas = data_facturas.loc[~data_facturas.nombre.isin(facturas_hist.nombre)]


resp = raw_input('Deseas classificar las {quant} nuevas facturas?'.format(quant=len(nuevas_facturas)))

def include_nuevas(facturas_hist, nuevas_facturas):
    for_isr = pn.Series(index=nuevas_facturas.index)
    for index_number in nuevas_facturas.index:
        xml_name = nuevas_facturas.loc[index_number, 'nombre']
        emisor = nuevas_facturas.loc[index_number, 'emisor'].encode('utf-8')
        is_this_isr = raw_input('file: {file_name} \nemisor: {emisor}\n'.format(file_name=xml_name, emisor=emisor))
        for_isr[index_number] = is_this_isr != ''
    nuevas_facturas['for_isr'] = for_isr
    return facturas_hist.append(nuevas_facturas)

if resp == 'y':
    facturas_hist = include_nuevas(facturas_hist, nuevas_facturas)
    facturas_hist.to_pickle('facturas_hist.pkl')

