# NYC Geodatabase 
This repository includes a collection of scripts used to generate layers and census data tables for the NYC Geodatabase, which is a collection of spatial layers and attributes for mapping and analyzing city-level features and data in New York City.

https://www.baruch.cuny.edu/confluence/display/geoportal/NYC+Geodatabase

Most of the database layers are relatively static and only need to be updated once every ten years, as they are based on the decennial TIGER Line files and census data.  Some features are updated on an annual basis, where older data is swapped for the most recent release.  Scripts for these layers are included in this repo:

1) Point features from the NYC facilities database that include colleges, libraries, hospitals, private schools, and public schools.

2) 5-year Census American Community Survey data for census tracts, Zip Code Tabulation Areas (ZCTAs) and Public Use Microdata Areas (PUMAs).

3) Census ZIP Code Business Patterns data that includes total counts of establishments, employees, and wages, and counts of establishments by two-digit sector level NAICS codes at the ZCTA level (the script aggregates source data from ZIP Code-level).

Subway stops, complexes, and ridership from the NYC MTA and NYNJ Port Authority are also updated annually but are not part of this repo - see alternate repos for mass transit layers and ridership.

Geodatabase features and tables that are meant to be updated every ten years were created manually. 
