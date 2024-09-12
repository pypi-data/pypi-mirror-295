WITH tx_data AS (
    SELECT 
        group_number,
        CAST('TX' AS CHAR(2)) AS state,
        CAST(tx_insurer AS CHAR(34)) AS carrier_name,
        CAST(tx_carrier_number AS CHAR(9)) AS carrier_fein,
        CAST('' AS CHAR(10)) AS carrier_zip 
    FROM client
    WHERE tx_insurer IS NOT NULL 
        OR tx_carrier_number IS NOT NULL
), or_data AS (
    SELECT 
        group_number,
        CAST('OR' AS CHAR(2)) AS state,
        CAST(or_insurer AS CHAR(34)) AS carrier_name,
        CAST('' AS char(9)) AS carrier_fein,
        CAST('' AS CHAR(10)) AS carrier_zip 
    FROM client
    WHERE or_insurer IS NOT NULL
), nc_data AS (
    SELECT 
        group_number,
        CAST('NC' AS CHAR(2)) AS state,
        CAST('' AS CHAR(34)) AS carrier_name,
        CAST(nc_insurer AS char(9)) AS carrier_fein,
        CAST('' AS CHAR(10)) AS carrier_zip 
    FROM client
    WHERE nc_insurer IS NOT NULL 
), ca_data AS (
    SELECT 
        group_number,
        CAST('CA' AS CHAR(2)) AS state,
        CAST(ca_insurer AS CHAR(34)) AS carrier_name,
        CAST('' AS char(9)) AS carrier_fein,
        CAST('' AS CHAR(10)) AS carrier_zip 
    FROM client
    WHERE ca_insurer IS NOT NULL
), fl_data AS (
    SELECT 
        group_number,
        CAST('FL' AS CHAR(2)) AS state,
        CAST(fl_insurer AS CHAR(34)) AS carrier_name,
        CAST(fl_insurer_code AS CHAR(9)) AS carrier_fein,
        CAST('' AS CHAR(10)) AS carrier_zip 
    FROM client
    WHERE fl_insurer IS NOT NULL
        OR fl_insurer_code IS NOT NULL
), sr_data AS (
    SELECT * FROM tx_data
    UNION ALL
    SELECT * FROM or_data
    UNION ALL
    SELECT * FROM nc_data
    UNION ALL
    SELECT * FROM ca_data 
    UNION ALL
    SELECT * FROM fl_data)
SELECT * FROM sr_data; 
