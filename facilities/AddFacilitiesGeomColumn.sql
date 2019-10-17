BEGIN TRANSACTION;

SELECT AddGeometryColumn ("a_schools_private", "geom", 2263, "POINT", "XY");

UPDATE a_schools_private
SET geom = MakePoint(xcoord, ycoord, 2263);

SELECT AddGeometryColumn ("a_schools_public", "geom", 2263, "POINT", "XY");

UPDATE a_schools_public
SET geom = MakePoint(xcoord, ycoord, 2263);

SELECT AddGeometryColumn ("a_colleges", "geom", 2263, "POINT", "XY");

UPDATE a_colleges
SET geom = MakePoint(xcoord, ycoord, 2263);

SELECT AddGeometryColumn ("a_libraries", "geom", 2263, "POINT", "XY");

UPDATE a_libraries
SET geom = MakePoint(xcoord, ycoord, 2263);

SELECT AddGeometryColumn ("a_hospitals", "geom", 2263, "POINT", "XY");

UPDATE a_hospitals
SET geom = MakePoint(xcoord, ycoord, 2263);

COMMIT;
