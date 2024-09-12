from cpsar.runtime import db
from cpsar.util import imemoize

import cpsar.ws as W

class Program(W.MakoProgram):
    def main(self):
        cursor = db.cursor()
        req = self._req
        res = self._res

    @property
    @imemoize
    def file_data(self):
        cursor = db.dict_cursor()
        cursor.execute("""
            SELECT 
                patient.first_name || ' ' || patient.last_name AS patient_name,
                state_report_entry.ack_code,
                sr_rejection.trans_id,
                trans.group_number,
                drug.name as drug,
                trans.quantity,
                trans.total as price,
                array_to_string(state_report_entry.response_desc, '<br>') AS response_desc,
                state_report_entry.response_date,
                sr_rejection.entry_id,
                state_report_file.file_name as file_name,
                state_report_file.send_date send_date,
                state_report_entry.reportzone as reportzone
            FROM (
                SELECT
                    MAX(entry_id) as entry_id,
                    trans_id
                FROM state_report_entry 
                WHERE (
                    (ack_code = 'R' AND cancel_ack_code IS NULL)
                    OR cancel_ack_code = 'R' 
                    OR (file_id IS NOT NULL AND ack_code is NULL)
                    OR (cancel_file_id IS NOT NULL AND cancel_ack_code IS NULL))
                AND reportzone IS NOT NULL 
                GROUP BY trans_id
            ) AS sr_rejection
            JOIN state_report_entry using(entry_id)
            JOIN trans ON state_report_entry.trans_id = trans.trans_id
            JOIN patient ON trans.patient_id = patient.patient_id
            JOIN drug using(drug_id)
            JOIN state_report_file using(file_id)
            WHERE freeze_sr_entry != True
        """)
        recs = cursor.fetchall()

        file_data={}

        for rec in recs:
            if rec['file_name'] not in file_data:
                file_data[rec['file_name']] = {
                    'file_name' :rec['file_name'],
                    'reportzone' :rec['reportzone'],
                    'send_date' :rec['send_date'],
                    'files' : []
                    }
            file_data[rec['file_name']]['files'].append(dict(rec))

        for data in file_data.values():
            data['trans_count'] =  len(data['files'])

        retval = file_data.values()
        return sorted(retval, key=lambda x: x['file_name'])

application = Program.app
