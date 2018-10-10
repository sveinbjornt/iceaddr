# iceaddr
 
### Look up Icelandic street addresses and postcodes

Python module to look up and get information about Icelandic street addresses and postcodes. The underlying data is taken from [Staðfangaskrá](https://opingogn.is/dataset/stadfangaskra) (the National Icelandic Address Registry) maintained by [Registers Iceland](https://www.skra.is) ([CC-BY](http://opendefinition.org/licenses/cc-by/)).

## Examples

### Look up address with postcode:

```python
>>> from iceaddr import iceaddr_lookup
>>> a = iceaddr_lookup('Öldugata', number=4, postcode=101)
>>> pprint.PrettyPrinter().pprint(a)
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

### Look up address with placename

```python
>>> from iceaddr import iceaddr_lookup
>>> a = iceaddr_lookup('Öldugötu', number=4, placename='Reykjavík')
>>> pprint.PrettyPrinter().pprint(a)
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
Street names and place names can be provided in either nominative or dative case (e.g. both 'Öldugata' and 'Öldugötu' will work, as will both 'Selfoss' and 'Selfossi').

### Keys

| Key           |                                                |
| ------------- |------------------------------------------------|
| bokst         | House letter                                   |
| byggd         |                                                |
| heiti_nf      | Street name (nominative case), e.g. 'Öldugata' |
| heiti_tgf     | Street name (dative case), e.g. 'Öldugötu'     |
| hnitnum       |                                                |
| husnr         | House number                                   |
| landnr        |                                                |
| lat_wgs84     | Latitude (WGS84 coordinates)                   |
| long_wgs84    | Longtitude (WGS84 coordinates)                 |
| postnr        | Postcode (e.g. 101)                            |
| serheiti      | Special name                                   |
| stadur_nf     | Placename (nominative case), e.g. 'Selfoss'    |
| stadur_tgf    | Placename (dative case), e.g. 'Selfossi'       |
| svaedi        | Area (e.g. 'Höfuðborgarsvæðið', 'Norðurland')  |
| svfnr         |                                                |
| tegund        | Postcode (e.g. 101)                            |
| vidsk         | Additional information                         |
| x_isn93       | Coordinate X (ISN93)                           |
| y_isn93       | Coordinate Y (ISN93)                           |


### Postcodes

```python
>>> from iceaddr import postcodes_for_placename
>>> postcodes_for_placename('Kópavogur')
[200, 201, 202, 203]
```

```python
>>> from iceaddr import postcodes
>>> postcodes[401]
{   'area': 'Vesturland og Vestfirðir', 
    'placename_nf': 'Ísafjörður', 
    'placename_tgf': 'Ísafirði', 
    'type': 'Dreifbýli' }
```

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

