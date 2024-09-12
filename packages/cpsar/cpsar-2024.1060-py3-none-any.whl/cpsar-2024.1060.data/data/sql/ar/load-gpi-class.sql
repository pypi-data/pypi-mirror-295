DROP TABLE gpi_class;

CREATE TABLE gpi_class (
    line TEXT, prefix VARCHAR(6),
    description VARCHAR(50)
);
\copy gpi_class ( line ) from /home/jeremy/x

UPDATE gpi_class SET
  prefix=substring(line FROM 1 FOR 6),
  description=substring(line FROM 7 FOR 50);

ALTER TABLE gpi_class DROP COLUMN line;
ALTER TABLE gpi_class ADD PRIMARY KEY (prefix);

