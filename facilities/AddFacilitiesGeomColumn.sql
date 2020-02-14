BEGIN TRANSACTION;

SELECT AddgeometryetryColumn ("a_schools_private", "geometry", 2263, "POINT", "XY");

UPDATE a_schools_private
SET geometry = MakePoint(xcoord, ycoord, 2263);

SELECT AddgeometryetryColumn ("a_schools_public", "geometry", 2263, "POINT", "XY");

UPDATE a_schools_public
SET geometry = MakePoint(xcoord, ycoord, 2263);

SELECT AddgeometryetryColumn ("a_colleges", "geometry", 2263, "POINT", "XY");

UPDATE a_colleges
SET geometry = MakePoint(xcoord, ycoord, 2263);

SELECT AddgeometryetryColumn ("a_libraries", "geometry", 2263, "POINT", "XY");

UPDATE a_libraries
SET geometry = MakePoint(xcoord, ycoord, 2263);

SELECT AddgeometryetryColumn ("a_hospitals", "geometry", 2263, "POINT", "XY");

UPDATE a_hospitals
SET geometry = MakePoint(xcoord, ycoord, 2263);

COMMIT;
