[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Release](https://shields.io/github/v/release/sveinbjornt/iceaddr?display_name=tag)](https://github.com/sveinbjornt/iceaddr/releases)
[![PyPI](https://img.shields.io/pypi/v/iceaddr)](https://pypi.org/project/iceaddr/)
[![Build](https://github.com/sveinbjornt/iceaddr/actions/workflows/python-package.yml/badge.svg)](https://github.com/sveinbjornt/iceaddr/actions)

# iceaddr

<img src="https://raw.githubusercontent.com/sveinbjornt/iceaddr/refs/heads/master/iceaddr_logo.svg" width="192" height="192" align="right" style="float: right; margin-left: 30px;" alt="iceaddr logo">

### Look up Icelandic street addresses, postcodes and placenames

`iceaddr` is a pure Python >= 3.9 package to look up information about
Icelandic streets, addresses, placenames, landmarks, locations and postcodes.
The underlying data is contained in a local SQLite database assembled
from the following sources:

* [Staðfangaskrá](https://opingogn.is/dataset/stadfangaskra), the official Icelandic address registry maintained by [Registers Iceland](https://www.skra.is) (*Þjóðskra*, [license](https://vefsafn.is/is/20170111023510/http://www.skra.is/?PageId=401e3483-e1ac-48c9-aec0-5159581d2222))
* [IS 50V Örnefni](https://opingogn.is/dataset/is-50v-ornefni-isn93) from the [National Land Survey of Iceland](https://www.lmi.is) (*Landmælingar Íslands*, [CC BY 4.0](https://www.natt.is/is/midlun/opin-gogn))
* The postcode table provided by [Postur.is](https://www.postur.is/gogn/Gotuskra/postnumer.txt), with supplementary data from [Icelandic Wikipedia](https://is.wikipedia.org/wiki/Listi_yfir_%C3%ADslensk_p%C3%B3stn%C3%BAmer)
* Municipality data provided by the [Icelandic Government](https://www.government.is/lisalib/getfile.aspx?itemid=4289e993-446d-11eb-812c-005056bc8c60)

Since no networking takes place, lookups are very fast and can be performed
offline. The package is useful for geocoding and reverse geocoding of Icelandic
addresses and placenames, as well as validating addresses and postcodes.
No external dependencies are required.

## Installation

The latest version of `iceaddr` is available via [PyPI](https://pypi.org/project/iceaddr/).

```bash
pip install iceaddr
```

## Examples

### Look up address with postcode

```python
>>> from iceaddr import iceaddr_lookup
>>> a = iceaddr_lookup('Austurstræti', number=14, postcode=101)
>>> pprint(a)
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
  'svaedi_nf': 'Höfuðborgarsvæðið',
  'svaedi_tgf': 'Höfuðborgarsvæðinu',
  'svfheiti': 'Reykjavíkurborg',
  'svfnr': 0,
  'tegund': 'Þéttbýli',
  'vidsk': ''}]
```

### Look up address with placename

```python
>>> from iceaddr import iceaddr_lookup
>>> a = iceaddr_lookup('Öldugötu', 4, 'Reykjavík')
>>> pprint(a)
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
  'svaedi_nf': 'Höfuðborgarsvæðið',
  'svaedi_tgf': 'Höfuðborgarsvæðinu',
  'svfheiti': 'Reykjavíkurborg',
  'svfnr': 0,
  'tegund': 'Þéttbýli',
  'vidsk': ''}]
```

Street and place names can be provided in either nominative (nf.) or
dative (þgf.) case (e.g. both 'Öldugata' and 'Öldugötu' will work, as
will both 'Selfoss' and 'Selfossi').

Please note that `iceaddr_lookup()` returns a list of zero or more
addresses matching the criterion.

```python
>>> from iceaddr import iceaddr_lookup
>>> iceaddr_lookup('Dúfnahólar', 10)
[]
>>> res = iceaddr_lookup('Öldugata', 9)
>>> [(a['postnr'], a['stadur_nf']) for a in res]
[(101, 'Reykjavík'), (220, 'Hafnarfjörður'), (621, 'Dalvík')]
```

For natural search string queries, the module provides `iceaddr_suggest()`:

```python
>>> from iceaddr import iceaddr_suggest
>>> a = iceaddr_suggest('Öldugata 4, Rey')
>>> [n['stadur_tgf'] for n in a]
['Reykjavík', 'Reyðarfirði']
>>> a = iceaddr_suggest('Öldugö', limit=200)
>>> len(a)
151
```

The default limit on results from both functions is 50.

### Find closest address

Given a set of WGS84 coordinates, the `nearest_addr()` function returns
a list of the nearest addresses in the database:

```python
>>> from iceaddr import nearest_addr
>>> addr = nearest_addr(64.148446, -21.944933)[0]
>>> print(f"{addr['heiti_nf']} {addr['husnr']}")
Öldugata 4
```

### Address Keys

| Key           | Value description                                       |
| ------------- |---------------------------------------------------------|
| bokst         | House letter, e.g. "A", "b"                             |
| byggd         | Byggðarnúmer in municipality                            |
| heiti_nf      | Street name (nominative case, nf.), e.g. 'Öldugata'     |
| heiti_tgf     | Street name (dative case, þgf.), e.g. 'Öldugötu'        |
| hnitnum       | Hnitnúmer staðfangahnits                                |
| husnr         | House number                                            |
| landnr        | Hlaupandi sex stafa auðkennisnúmer í landeignaskrá HMS  |
| lat_wgs84     | Latitude (WGS84 coordinates)                            |
| long_wgs84    | Longitude (WGS84 coordinates)                           |
| postnr        | Postcode (e.g. 101)                                     |
| serheiti      | Special name                                            |
| stadur_nf     | Placename (nominative case), e.g. 'Selfoss'             |
| stadur_tgf    | Placename (dative case), e.g. 'Selfossi'                |
| svaedi_nf     | Region (nominative case), e.g. 'Höfuðborgarsvæðið'      |
| svaedi_tgf    | Region (dative case), e.g. 'Höfuðborgarsvæðinu'         |
| svfheiti      | Municipality name (e.g. 'Borgarbyggð')                  |
| svfnr         | Municipality code (e.g. 3609)                           |
| tegund        | Type (either 'Þéttbýli' (urban) or 'Dreifbýli' (rural)) |
| vidsk         | Additional information                                  |

### Postcodes

#### Info about a given postcode

```python
>>> from iceaddr import postcode_lookup
>>> postcode_lookup(400)
{   "svaedi_nf": "Vesturland og Vestfirðir",
    "svaedi_tgf": "Vesturlandi og Vestfjörðum",
    "stadur_nf": "Ísafjörður",
    "stadur_tgf": "Ísafirði",
    "tegund": "Þéttbýli"}
# Accepts string or int
>>> postcode_lookup("107")
{   "svaedi_nf": "Höfuðborgarsvæðið",
    "svaedi_tgf": "Höfuðborgarsvæðinu",
    "stadur_nf": "Reykjavík",
    "stadur_tgf": "Reykjavík",
    "tegund": "Þéttbýli",
    "lysing": "Vesturbær"}
```

```python
>>> from iceaddr import POSTCODES
>>> pprint(POSTCODES[101])
{   "svaedi_nf": "Höfuðborgarsvæðið",
    "svaedi_tgf": "Höfuðborgarsvæðinu",
    "stadur_nf": "Reykjavík",
    "stadur_tgf": "Reykjavík",
    "tegund": "Þéttbýli",
    "lysing": "Miðborg"}
```

#### Get postcodes for a placename ("örnefni")

```python
>>> from iceaddr import postcodes_for_placename
>>> postcodes_for_placename('Ísafjörður')
[400, 401]
>>> postcodes_for_placename('Kópavogi')
[200, 201, 202, 203]
>>> postcodes_for_placename('kópav', partial=True)
[200, 201, 202, 203]
```

#### Get postcodes for a region ("svæði")

```python
>>> from iceaddr import postcodes_for_region
>>> postcodes_for_region('Norðurland')
[530, 531, 540, 541, 545, ...]
>>> postcodes_for_region('Höfuðborgarsvæðið')
[101, 102, 103, 104, 105, ...]
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

If more than one placename match is found, the results are ordered by size,
with precedence given to municipalities and densely populated areas.

```python
>>> placename_lookup("Egilsstað", partial=True)
[{'flokkur': 'Þéttbýli',
  'id': 63208,
  'lat_wgs84': 65.2637152,
  'long_wgs84': -14.3931143,
  'nafn': 'Egilsstaðir'},
 {'flokkur': 'Landörnefni Lítið',
  'id': 108285,
  'lat_wgs84': 65.3516154,
  'long_wgs84': -20.610947,
  'nafn': 'Egilsstaðir'}]
```

### Find closest placenames ("örnefni")

Given a set of WGS84 coordinates, the `nearest_placenames()` function
returns a list of the nearest placenames in the database:

```python
>>> from iceaddr import nearest_placenames
>>> pn = nearest_placenames(64.148446, -21.944933, limit=1)[0]
>>> print(pn["nafn"])
Landakotsvöllur
```

### Metadata

Get information about the database version, etc.:

```python
>>> from iceaddr import iceaddr_metadata
>>> meta = iceaddr_metadata()
>>> pprint(meta["date_created"].date())
'2025-11-22'
```

## Build process

To build your own version of the package, you need to have
Python >=3.9 installed. Then, after (optionally) creating a virtual
environment, run the following command from the repository root to
install dependencies:

```bash
pip install ".[dev,build]"
```

Then run the following command to build the database:

```bash
bash build.sh
```

This creates an SQLite3 database in the repo root named `iceaddr.db`.
Move this file to `src/iceaddr/` and you can now install your own
freshly built version of the package:

```bash
pip install .
```

## Version History

* 0.6.1: Updated address and placename data. Added `iceaddr_metadata` function. Better package metadata. (29/12/2025)
* 0.6.0: `nearest_*` functions now use R-Trees for much faster lookups. Added `nearest_*_with_dist` functions. Updated address and placename data. (22/11/2025)
* 0.5.10: Updated address and placename data. Added `region_for_postcode` function. Minor optimizations (07/11/2025)
* 0.5.9: Updated address and placename data. Fixed bug in `placename_lookup` function (31/07/2025)
* 0.5.8: Updated address and placename data. Added municipality name data to address records. Now requires Python 3.9+ (26/02/2025)
* 0.5.7: Updated address and placename data. Now requires Python 3.8+ (20/09/2024)
* 0.5.6: Updated address and placename data (11/08/2023)
* 0.5.5: Updated address and placename data. Removed ISN93 coords. Now requires Python 3.7+ (11/12/2022)
* 0.5.4: Updated address and placename data (09/11/2022)
* 0.5.3: Updated address, postcode and placename data, various minor fixes (19/05/2022)
* 0.5.2: Updated address and placename data, fixed issue with installing on Windows (25/06/2021)
* 0.5.1: Fixes and additions in placename data (16/10/2020)
* 0.5.0: Support for address number ranges, fix in house number lookup, new `nearest_addr` and `nearest_placenames` functions, updated data (15/10/2020)
* 0.4.0: Updated address, placename and postcode data. Better handling of house letters in address lookup (06/05/2020)
* 0.3.3: Minor placename additions, smarter ordering of placename lookup results (08/01/2019)
* 0.3.2: Added municipalities and various [BÍN](https://bin.arnastofnun.is/) placenames to ornefni database (02/01/2019)
* 0.3.1: Added more placenames from LMÍ data, support for multithreaded use
* 0.3.0: Added `placename_lookup` to look up coordinates for Icelandic placenames + minor fixes (10/12/2018)
* 0.2.0: Added `iceaddr_suggest`, result limit, changed key names for postcode dicts (22/10/2018)
* 0.1.2: Initial public release (10/10/2018)

## BSD License

Copyright (C) 2018-2025 [Sveinbjorn Thordarson](mailto:sveinbjorn@sveinbjorn.org)

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
