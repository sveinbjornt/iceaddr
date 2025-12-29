
# TODO for `iceaddr`

* `iceaddr_sql_query` for direct SQL queries to the underlying database
* Provide placenames, street names, etc. in all cases (nf, þf, þgf, ef) using BÍN data
* Better automation of geo data processing in db build scripts, should not be a separate step
* iceaddr_suggest relies on comma separator to separate street address and place name. Could be made smarter.
* Function to find region of a given pair of coordinates, e.g. which_region(lat,lon) == "Norðurland"
* Add function to parse Icelandic address strings in a robust, forgiving way (see Greynir geo.py impl.)
* Add preposition functions from Greynir (e.g. "í Reykjavík", "á Dalvík", etc.)
* Dative case for placenames?
* Add MANNVIRKI gpkg data from LMÍ?
* Canonical address formatting utility function?
