# -*- encoding: utf-8 -*-
"""
    
    iceaddr: Look up information about Icelandic street addresses and postcodes
    Copyright (c) 2018 Sveinbjorn Thordarson
    
"""

from __future__ import unicode_literals
from __future__ import print_function

import re
from .db import shared_db
from .postcodes import postcodes, postcodes_for_placename

def _add_postcode_info(a):
    """ Look up info about postcode, add keys to address dictionary """
    if a['postnr']:
        info = postcodes[a['postnr']]
        a['stadur_nf'] = info['placename_nf']
        a['stadur_tgf'] = info['placename_tgf']
        a['svaedi'] = info['area']
        a['tegund'] = info['type']
    return a

def _run_query(q, qargs):
    db_conn = shared_db.connection()
    res = db_conn.cursor().execute(q, qargs)

    return [_add_postcode_info(dict(row)) for row in res]

def iceaddr_lookup(street_name, number=None, letter=None, 
    postcode=None, placename=None, limit=100):
    """ Look up all addresses matching criterion """
    
    # Look up postcodes for placename if no postcode is provided
    pc = [postcode] if postcode else []
    if placename and not postcode:
        pc = postcodes_for_placename(placename)        
        
    q = 'SELECT * FROM stadfong WHERE (heiti_nf=? OR heiti_tgf=?)'
    l = [street_name, street_name]
    if number:
        q += ' AND husnr=? '
        l.append(number)
    if letter:
        q += ' AND bokst=? '
        l.append(letter)
    if len(pc):
        qp = ' OR '.join([' postnr=?' for p in pc])
        l.extend(pc)
        q += ' AND (%s) ' % qp
    
    # Ordering by postcode may in fact be a reasonable proxy
    # for delivering by order of match likelihood since the
    # lowest postcodes are generally more densely populated
    q += ' ORDER BY postnr ASC, husnr ASC, bokst ASC LIMIT ?'
    l.append(limit)
    
    return _run_query(q, l)

def iceaddr_suggest(search_str, limit=100):
    """ Parse search string and fetch matching addresses. 
        Made to handle partial and full text queries in 
        the following formats:

        Öldug
        Öldugata
        Öldugata 4
        Öldugata 4, 101
        Öldugata 4, Reykjavík
        Öldugata 4, 101 Reykjavík
    """
    search_str = search_str.strip()
    if not search_str or len(search_str) < 3:
        return []
    
    items = [s.strip().split() for s in search_str.split(',')]
    
    if not [l for l in items if len(l)]:
        return []
    
    q = 'SELECT * FROM stadfong WHERE '
    qargs = list()

    # Street name component
    addr = items[0]
    
    # Handle street names with more than one word
    # E.g. "Stærri Bær 1"
    if re.match('\d+$', addr[-1]): # Has house number
        addr = [' '.join(addr[:-1]), int(addr[-1])]
    else:
        addr = [' '.join(addr)]
        
    street_name = addr[0]
    if len(addr) == 1: # "Ölduga"
        q += ' (heiti_nf LIKE ? OR heiti_tgf LIKE ?) '
        qargs.extend([street_name + '%' , street_name + '%'])
    elif len(addr) == 2: # "Öldugötu 4"
        q += ' (heiti_nf=? OR heiti_tgf=?) '
        qargs.extend([street_name, street_name])
        street_num = int(addr[1])
        q += ' AND husnr=? '
        qargs.append(street_num)
    
    # Place name component
    if len(items) > 1 and items[1]:
        pns = items[1]
        if re.match('\d\d\d$', pns[0]):
            # We have a postcode
            q += ' AND postnr=? '
            qargs.append(pns[0])
        else:
            # Try to look up place name
            pc = postcodes_for_placename(pns[0], partial=True)
            if pc:
                qp = ' OR '.join([' postnr=? ' for p in pc])
                q += ' AND (%s) ' % qp
                qargs.extend(pc)
    
    q += ' ORDER BY postnr ASC, husnr ASC, bokst ASC LIMIT ?'
    qargs.append(limit)
    
    # print(q)
    # print(qargs)
    
    return _run_query(q, qargs)
