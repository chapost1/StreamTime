DROP TABLE IF EXISTS schema_on_provision_test;

CREATE TABLE schema_on_provision_test (id NUMERIC NOT NULL);

INSERT INTO
    schema_on_provision_test (id)
VALUES
    (1),
    (2),
    (3),
    (4);