from json2html import *

def htmlConvert(x, y):
    classDef = 'class=\"' + y + '\"'
    result = json2html.convert(json = x, table_attributes = classDef, clubbing=False)
    return result