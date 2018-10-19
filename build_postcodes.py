# -*- encoding: utf-8 -*-
"""
    Fetch list of postcodes from the Icelandic postal service,
    create and print dict mapping postcode to placename and
    other related information. Also adds placenames in the 
    nominative case (nefnifall) since the source data only 
    includes placenames in dative (þágufall).
    
    https://www.postur.is/gogn/Gotuskra/postnumer.txt
"""

import unicodecsv
import requests
from contextlib import closing
import pprint
from reynir import Reynir

POSTCODES_REMOTE_URL = "https://www.postur.is/gogn/Gotuskra/postnumer.txt"

def read_rows(dsv_file, delimiter="|", encoding="utf8"):    
    reader = unicodecsv.DictReader(dsv_file, delimiter=delimiter, encoding=encoding)    
    for row in reader:
        yield row

if __name__ == "__main__":    
    pc = dict()
    reynir = Reynir()
    pp = pprint.PrettyPrinter(indent=4)
    
    with closing(requests.get(POSTCODES_REMOTE_URL, stream=True)) as r:
        for r in read_rows(r.iter_lines(), delimiter=";", encoding="ISO-8859-1"):
            
            # CSV file from postur.is only contains postcode placenames in
            # the dative form (þgf.). Try to lemmatise to nominative (nf.) using Reynir.
            s = reynir.parse_single("Hann bjó í " + r['Staður'] + ".")
            try:
                placename_nominative = s.tree.S.IP.VP_SEQ.PP.NP.lemmas[0].replace('-', '')
            except Exception as e:
                print('Failed to generate nominative form of placename: ' + r['Staður'])
                placename_nominative = r['Staður']
            
            pc[int(r['Póstnúmer'])] = {
                'placename_nf': placename_nominative,
                'placename_tgf': r['Staður'],
                'area': r['Svæði'],
                'type': r['Tegund']
            }
    
    pp.pprint(pc)
