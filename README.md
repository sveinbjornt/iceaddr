# iceaddr
[![Build Status](https://travis-ci.org/sveinbjornt/iceaddr.svg?branch=master)](https://travis-ci.org/sveinbjornt/iceaddr)
### Look up Icelandic street addresses and postcodes

Python (2 and 3) module to look up and get information about Icelandic street addresses and postcodes. The underlying data is taken from [Staðfangaskrá](https://opingogn.is/dataset/stadfangaskra), the official Icelandic Address Registry maintained by [Registers Iceland](https://www.skra.is) ([CC-BY](http://opendefinition.org/licenses/cc-by/)), [IS 50V Örnefni](https://opingogn.is/dataset/is-50v-ornefni-isn93) from the [National Land Survey of Iceland](https://www.lmi.is), and from the postcode table provided by [Postur.is](https://www.postur.is/einstaklingar/posthus/postnumer/gagnaskrar/).



## Installation

```
$ pip install iceaddr
```

## Examples

### Look up address with postcode:

```python
>>> from iceaddr import iceaddr_lookup
>>> a = iceaddr_lookup('Austurstræti', number=14, postcode=101)
>>> pprint.pprint(a)
[{'bokst': '',
  'byggd': 1,
  'heiti_nf': 'Austurstræti',
  'heiti_tgf': 'Austurstræti',
  'hnitnum': 10083839,
  'husnr': 14,
  'landnr': 100852,
  'lat_wgs84': 64.147529217656,
  'long_wgs84': -21.9389394651385,
  'postnr': 101,
  'serheiti': '',
  'stadur_nf': 'Reykjavík',
  'stadur_tgf': 'Reykjavík',
  'svaedi': 'Höfuðborgarsvæðið',
  'svfnr': 0,
  'tegund': 'Þéttbýli',
  'vidsk': '',
  'x_isn93': 356999.259090909,
  'y_isn93': 408290.561363636}]
```

### Look up address with place name

```python
>>> from iceaddr import iceaddr_lookup
>>> a = iceaddr_lookup('Öldugötu', number=4, placename='Reykjavík')
>>> pprint.pprint(a)
[{'bokst': '',
  'byggd': 1,
  'heiti_nf': 'Öldugata',
  'heiti_tgf': 'Öldugötu',
  'hnitnum': 10017023,
  'husnr': 4,
  'landnr': 100570,
  'lat_wgs84': 64.1484874806941,
  'long_wgs84': -21.9452072913341,
  'postnr': 101,
  'serheiti': '',
  'stadur_nf': 'Reykjavík',
  'stadur_tgf': 'Reykjavík',
  'svaedi': 'Höfuðborgarsvæðið',
  'svfnr': 0,
  'tegund': 'Þéttbýli',
  'vidsk': '',
  'x_isn93': 356699.479545455,
  'y_isn93': 408411.468181818}]
```

Street and place names can be provided in either nominative or dative case (e.g. both 'Öldugata' and 'Öldugötu' will work, as will both 'Selfoss' and 'Selfossi').

Please note that`iceaddr_lookup()` returns a list of zero or more addresses matching the criterion.

```python
>>> from iceaddr import iceaddr_lookup
>>> iceaddr_lookup('Dúfnahólar', number=10)
[]
>>> res = iceaddr_lookup('Öldugata', number=9)
>>> [(a['postnr'], a['stadur_nf']) for a in res]
[(101, 'Reykjavík'), (220, 'Hafnarfjörður'), (621, 'Dalvík')]
```

For natural search string queries, the module provides `iceaddr_suggest()`:

```python
>>> from iceaddr import iceaddr_suggest
>>>
>>> a = iceaddr_suggest('Öldugata 4, Rey')
>>> [n['stadur_tgf'] for n in a]
['Reykjavík', 'Reyðarfirði']
>>> a = iceaddr_suggest('Öldugö', limit=200)
>>> len(a)
151
```

The default limit on results from both functions is 50.

### Keys

| Key           |                                                         |
| ------------- |---------------------------------------------------------|
| bokst         | House letter                                            |
| byggd         |                                                         |
| heiti_nf      | Street name (nominative case), e.g. 'Öldugata'          |
| heiti_tgf     | Street name (dative case), e.g. 'Öldugötu'              |
| hnitnum       |                                                         |
| husnr         | House number                                            |
| landnr        |                                                         |
| lat_wgs84     | Latitude (WGS84 coordinates)                            |
| long_wgs84    | Longitude (WGS84 coordinates)                           |
| postnr        | Postcode (e.g. 101)                                     |
| serheiti      | Special name                                            |
| stadur_nf     | Place name (nominative case), e.g. 'Selfoss'            |
| stadur_tgf    | Place name (dative case), e.g. 'Selfossi'               |
| svaedi        | Area (e.g. 'Höfuðborgarsvæðið', 'Norðurland')           |
| svfnr         |                                                         |
| tegund        | Type (either 'Þéttbýli' (urban) or 'Dreifbýli' (rural)) |
| vidsk         | Additional information                                  |
| x_isn93       | Coordinate X (ISN93)                                    |
| y_isn93       | Coordinate Y (ISN93)                                    |

### Postcodes

```python
>>> from iceaddr import postcodes_for_placename
>>> postcodes_for_placename('Ísafjörður')
[400, 401]
>>> postcodes_for_placename('Kópavogi')
[200, 201, 202, 203]
>>> postcodes_for_placename('kópav', partial=True)
[200, 201, 202, 203]
>>>
```

```python
>>> from iceaddr import postcodes
>>> postcodes.get(400)
{   'svaedi': 'Vesturland og Vestfirðir', 
    'stadur_nf': 'Ísafjörður', 
    'stadur_tgf': 'Ísafirði', 
    'tegund': 'Þéttbýli' }
```

### Placenames ("örnefni")

```python
>>> from iceaddr import placename_lookup
>>> placename_lookup('Meðalfellsvatn')
[{'flokkur': 'Vatnaörnefni Mið',
  'id': 2339,
  'lat_wgs84': 64.3112049,
  'long_wgs84': -21.5997926,
  'nafn': 'Meðalfellsvatn'}]
```

If more than one placename match is found, the results are ordered by size, with precedence given to municipalities and densely populated areas.

## Version History

* 0.3.3: Minor placename additions, smarter ordering of placename lookup results (08/01/2019)
* 0.3.2: Added municipalities and various BÍN placenames to ornefni database (02/01/2019)
* 0.3.1: Added more placenames from LMÍ data, support for multithreaded use
* 0.3: Added `placename_lookup` to look up coordinates for Icelandic placenames + minor fixes (10/12/2018)
* 0.2: Added `iceaddr_suggest`, result limit, changed key names for postcode dicts (22/10/2018)
* 0.1.2: Initial release (10/10/2018)

## BSD License 

Copyright (C) 2018 Sveinbjorn Thordarson

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or other
materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may
be used to endorse or promote products derived from this software without specific
prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

