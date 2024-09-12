from cpsar.runtime import db
import cpsar.ws as W

class Program(W.MakoProgram):
    def main(self):
        cursor = db.cursor()
        req = self._req
        res = self._res 
        self._trans_id = None 
        self._data_837  = None
        self._data_837_fname = None
        self._data_824 = None
        self._data_824_fname = None
        self._data_997 = None
        self._data_997_fname = None


        entry_id = int(req.params.get('entry_id'))
        cursor.execute("""
            SELECT reportzone from state_report_entry
            WHERE entry_id = %s;
            """, (entry_id,))
        reportzone, = cursor.fetchone()

        if reportzone == 'TX':
            # Get file data
            cursor.execute("""
                SELECT DISTINCT
                    trans_id,
                    state_report_file.file_data as data_837,
                    state_report_file.file_name as data_837_fname,
                    state_report_824.file_data as data_824,
                    state_report_824.file_name as data_824_fname,
                    state_report_997.file_data as data_997,
                    state_report_997.file_name as data_997_fname
                FROM state_report_entry
                JOIN state_report_file using(file_id)
                LEFT JOIN state_report_824 using(file_824_id)
                LEFT JOIN state_report_997 using(file_997_id)
                WHERE entry_id = %s;
                """, (entry_id,))
            assert cursor.rowcount == 1
            (self._trans_id, 
            self._data_837, 
            self._data_837_fname, 
            self._data_824, 
            self._data_824_fname, 
            self._data_997, 
            self._data_997_fname,) = cursor.fetchall()[0]

        elif reportzone == 'FL':
            # Get file data
            cursor.execute("""
                SELECT DISTINCT
                    trans_id,
                    state_report_file.file_data as data_837,
                    state_report_file.file_name as data_837_fname,
                    fl_sr_response.file_data as data_824,
                    fl_sr_response.file_name as data_824_fname,
                    ''  as data_997,
                    ''  as data_997_fname
                FROM state_report_entry
                JOIN state_report_file using(file_id)
                LEFT JOIN fl_sr_response ON state_report_entry.fl_response_file_id = fl_sr_response.response_file_id
                WHERE entry_id = %s;
                """, (entry_id,))
            assert cursor.rowcount == 1
            (self._trans_id, 
            self._data_837, 
            self._data_837_fname, 
            self._data_824, 
            self._data_824_fname, 
            self._data_997, 
            self._data_997_fname,) = cursor.fetchall()[0]

        self.tmpl['trans_id'] = self._trans_id 

        self.tmpl['data_837'] = self._data_837
        self.tmpl['data_837_fname'] = self._data_837_fname

        self.tmpl['data_824'] = self._data_824
        self.tmpl['data_824_fname'] = self._data_824_fname

        self.tmpl['data_997'] = self._data_997
        self.tmpl['data_997_fname'] = self._data_997_fname

application = Program.app
