ALTER TABLE state_report_entry ADD COLUMN fl_response_file_id INTEGER;
ALTER TABLE state_report_entry ALTER COLUMN control_number TYPE STR(16);

CREATE TABLE fl_sr_response (
    response_file_id SERIAL PRIMARY KEY,
    file_data TEXT,
    file_name VARCHAR(100)
    );
CREATE INDEX response_file_key on fl_sr_response (response_file_id)
