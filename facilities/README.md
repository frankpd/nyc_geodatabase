# NYC Facilities Data Downloader

This folder contains two Python / Pandas notebooks that each pull data from the New York City Department of Planning Facilities dataset and create spatial features for five facility categories.  The script retrieves the full facilities dataset from an API and dumps it to a JSON file, so that if the script has to be rerun from the beginning the API doesn't have to be called again.

Each Python script has no input files.  Five tables are generated from data pulled from the API: hospitals, colleges, libraries, public schools and private schools.  The 'Facilities to Shapefiles' script takes these five data frames and creates an ESRI Shapefile for it which is saved to disk in the 'outputs' folder. 

The 'Facilities to SQLite Database' script takes each of the five tables and inserts them into a SQLite database with columns representing the x and y coordinates for each point location projected in State Plane CRS.  This test database is saved to disk in the 'outputs' folder as 'facilities.sqlite'.

Once the data is created in the test database from the notebook, the following steps are: run the database utilities comparison script compare_tables.py to verify completeness and correctness relative to the previous year's data, if the data appears solid run the database utility sqlite_to_sqlite.py to copy the data from the test database to the actual NYC Geodatabase that will serve as the next published version, and then build the geometry for the facilities.  To do that, open the Spatialite GUI and connect to the NYC geodatabase. Execute the SQL script 'AddFacilitiesGeomColumn.sql' by clicking Files -> Advanced -> Execute SQL Script.  This script builds a geometry column from the xy coordinates for each feature.  After executing this query, save your changes.  You now have a spatialite geodatabase containing all facilities subgroups.

