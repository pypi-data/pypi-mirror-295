import datetime
import itertools

from cpsar.util import insert_sql

class DataService(object):
    """ Service Interface for the state reporting data model. Use me unless you
    need fine grain control at the cost of more coupling.
    """
    def __init__(self, db, reportzone):
        self.reportzone = reportzone
        self._db = db
        self._trans_factory = TransFactory(db)
        self._history_factory = HistoryFactory(db)
        self._drug_factory = DrugFactory(db)
        self._claim_factory = ClaimFactory(db)
        self._patient_factory = PatientFactory(db)
        self._pharmacy_factory = PharmacyFactory(db)
        self._doctor_factory = DoctorFactory(db)
        self._employer_factory = EmployerFactory(db)

        self._client_factory = ClientFactory(db, reportzone)

        self._sr_factory = StateReportEntryFactory(db)
        self._invoice_factory = InvoiceFactory(db)
        self._item_factory = StateReportItemFactory(
            self._trans_factory,
            self._history_factory,
            self._drug_factory,
            self._claim_factory,
            self._patient_factory,
            self._invoice_factory,
            self._pharmacy_factory,
            self._doctor_factory,
            self._employer_factory,
            self._client_factory)
        self._state_report_file_factory = StateReportFileFactory(db)

    @property
    def state_report_entry_factory(self):
        return self._sr_factory

    def unreported_items(self, maxRecords=50):
        """ Provide an item set of all of the unreported entries for the given
        reportzone
        """
        entries = (self._sr_factory.entries_pending_report(self.reportzone))[:maxRecords]
        return self._item_factory.for_entries(entries)

    def new_state_report_file(self, file_name, file_type):
        return self._state_report_file_factory.new(file_name, file_type, self.reportzone)

## Object Interface

class IdentityAttrMixIn(object):
    """ Adds feature to class to test for equality against a single identity
    field. To use, specify an idattr attribute on the class. The value of this
    attribute will be used to test for equality for other objects.
    
    class Cat(IdentityAttrMixIn):
        idattr = 'name'
        def __init__(self, name):
            self.name = name

    felix1 = Cat('felix')
    felix2 = Cat('felix')
    assert felix1 == felix2
    """

    idattr = 'id'

    def __eq__(self, other):
        id = getattr(self, self.idattr)
        if isinstance(other, type(self)):
            oid = getattr(other, self.idattr)
            return id == oid
        else:
            return id == other

    def __repr__(self):
        id = getattr(self, self.idattr)
        return '<%s %s=%s>' % (type(self).__name__, self.idattr, id)

class CursorGetFactoryMixIn(object):
    """ Gives factories a get() method. The implementation class must provide:
     - _object_class attribute which is a callable to produce a new instance
            to return.
     - _populate_cursor_with method which is provided a cursor and the key
            value (provided to get()).
     
     Implementors can also provide a _null_object_class which will used to
     provide an object if the cursor has no records. If it is not specified
     and the cursor is empty, a DataError exception is raised.
    """

    _object_class = None
    _null_object_class = None

    def __init__(self, db):
        self._db = db
        self._cache = {}

    def get(self, key):
        if key in self._cache:
            return self._cache[key]
        self._populate_cache(key)
        return self._cache[key]

    def _populate_cache(self, key):
        cursor = self._db.dict_cursor()
        self._populate_cursor_with(cursor, key)
        if cursor.rowcount == 0:
            if self._null_object_class:
                self._cache[key] = self._null_object_class()
            else:
                raise DataError("No key match for %s on %s" %
                                (key, type(self).__name__))
        else:
            dbrec = cursor.fetchone()
            self._cache[key] = self._object_class(dbrec)

    def _populate_cursor_with(self, cursor, key):
        raise RuntimeError("Implement Me in Subclass")

class Client(IdentityAttrMixIn):
    idattr = 'group_number'
    def __init__(self, dbrec):
        self.address_1 = dbrec['address_1']
        self.address_2 = dbrec['address_2'] 
        self.billing_name = dbrec['billing_name']
        self.client_name = dbrec['client_name']
        self.city = dbrec['city']
        self.group_number = dbrec['group_number']
        self.invoice_processor_code = dbrec['invoice_processor_code']
        self.invoice_multiplier = dbrec['invoice_multiplier']
        self.print_multiplier_invoice = dbrec['print_multiplier_invoice']
        self.print_nonmultiplier_invoice = dbrec['print_nonmultiplier_invoice']
        self.savings_formula = dbrec['savings_formula']
        self.show_awp_on_invoice = dbrec['show_awp_on_invoice']
        self.show_sfs_on_invoice = dbrec['show_sfs_on_invoice']
        self.show_copay_on_invoice = dbrec['show_copay_on_invoice']
        self.show_savings_on_invoice = dbrec['show_savings_on_invoice']
        self.state = dbrec['state']
        self.tin = dbrec['tin']
        self.zip_code = dbrec['zip_code']
        self.insurer = dbrec['insurer'].strip() 
        self.insurer_tin = dbrec['insurer_tin']
        self.insurer_zip = dbrec['insurer_zip']
        self.claim_admin_name = dbrec['claim_admin_name'].strip()
        self.claim_admin_fein = dbrec['claim_admin_fein']
        self.claim_admin_zip = dbrec['claim_admin_zip']

        if self.client_name:     
            self.client_name = dbrec['client_name'][0:34].strip()

        if self.claim_admin_name: 
            self.claim_admin_name = dbrec['claim_admin_name'][0:34].strip()

        if dbrec['carrier_name']:
            self.insurer =  dbrec['carrier_name'][0:34].strip()
        if dbrec['carrier_fein']:
            self.insurer_tin =  dbrec['carrier_fein']
        if dbrec['carrier_zip']:
            self.insurer_zip =  dbrec['carrier_zip']

class ClientFactory(CursorGetFactoryMixIn):
    def __init__(self, db, reportzone):
        CursorGetFactoryMixIn.__init__(self, db)
        self._reportzone = reportzone
        self._object_class = Client 

    def _populate_cursor_with(self, cursor, group_number):
        cursor.execute("""
            SELECT *
            FROM client
            LEFT JOIN sr_carrier USING(group_number)
            WHERE group_number=%s
            AND sr_carrier.state=%s
            """, (group_number, self._reportzone,))

class Transaction(IdentityAttrMixIn):
    idattr = 'trans_id'
    def __init__(self, dbrec):
        self.adjustments = dbrec['adjustments']
        self.batch_date = dbrec['batch_date']
        self.create_date = dbrec['create_date']
        self.paid_date = dbrec['paid_date']
        self.awp = dbrec['awp']
        self.eho_network_copay = dbrec['eho_network_copay']
        self.cost_allowed = dbrec['cost_allowed']
        self.dispense_fee = dbrec['dispense_fee']
        self.invoice_id = dbrec['invoice_id']
        self.line_no = dbrec['line_no']
        self.paid_amount = dbrec['paid_amount']
        self.processing_fee = dbrec['processing_fee']
        self.sales_tax = dbrec['sales_tax']
        self.state_fee = dbrec['state_fee']
        self.trans_id = dbrec['trans_id']
        self.tx_type = dbrec['tx_type']
        self.history_id = dbrec['history_id']
        self.writeoff_total = dbrec['writeoff_total']
        self.date_written = dbrec['date_written'] 
        self._dbrec = dbrec

    @property
    def create_date_yyyymmdd(self):
        return self.create_date.strftime("%Y%m%d")

    @property
    def paid_date_yyyymmdd(self):
        if self.paid_date:
            return self.paid_date.strftime("%Y%m%d")
        else:
            return ''

    @property
    def received_bill_date_yyyymmdd(self):
        rd = self.create_date + datetime.timedelta(days=1)
        return rd.strftime("%Y%m%d")

    @property
    def total(self):
        return (self.cost_allowed + self.dispense_fee + self.sales_tax +
                self.processing_fee - self.eho_network_copay)

    @property
    def paid(self):
        return self.balance == 0

    @property
    def adj_total(self):
        return self.total - self.adjustments 

    @property
    def balance(self):
        return self.adj_total - self.paid_amount

class TransFactory(CursorGetFactoryMixIn):
    _object_class = Transaction

    def _populate_cursor_with(self, cursor, trans_id):
        cursor.execute("""
            SELECT *
            FROM trans
            WHERE trans_id=%s
            """, (trans_id,))

class Invoice(IdentityAttrMixIn):   
    idattr = 'invoice_id'
    def __init__(self, dbrec):
        self.invoice_id = dbrec['invoice_id']

class InvoiceFactory(CursorGetFactoryMixIn):
    _object_class = Invoice

    def _populate_cursor_with(self, cursor, invoice_id):
        cursor.execute("""
            SELECT *
            FROM invoice
            WHERE invoice_id=%s
            """, (invoice_id,))

class Doctor(IdentityAttrMixIn):
    idattr = 'doctor_id'
    def __init__(self, dbrec):
        self.doctor_id = dbrec['doctor_id']
        self.name = dbrec['name']

class NullDoctor(object):
    doctor_id = None
    name = None

class DoctorFactory(CursorGetFactoryMixIn):
    _object_class = Doctor
    _null_object_class = NullDoctor
    def _populate_cursor_with(self, cursor, doctor_id):
        cursor.execute("""
            SELECT *
            FROM doctor
            WHERE doctor_id=%s
            """, (doctor_id,))

class Drug(IdentityAttrMixIn):
    idattr = 'drug_id'
    def __init__(self, dbrec):
        self.drug_id = dbrec['drug_id']
        self.ndc_number = dbrec['ndc_number']
        self.name = dbrec['name']

class DrugFactory(CursorGetFactoryMixIn):
    _object_class = Drug
    def _populate_cursor_with(self, cursor, drug_id):
        cursor.execute("""
            SELECT *
            FROM drug
            WHERE drug_id=%s
            """, (drug_id,))

class Patient(IdentityAttrMixIn):
    idattr = 'patient_id'
    def __init__(self, dbrec):
        self.patient_id = dbrec['patient_id']
        self.dob = dbrec['dob']
        self.first_name = dbrec['first_name']
        self.last_name = dbrec['last_name']
        self.ssn = dbrec['ssn']
        self.address_1 = dbrec['address_1']
        self.address_2 = dbrec['address_2']
        self.city = dbrec['city']
        self.state = dbrec['state']
        self.zip_code = dbrec['zip_code']
        self.sex = dbrec['sex']

    @property
    def dob_yyyymmdd(self):
        return self.dob.strftime("%Y%m%d")

class PatientFactory(CursorGetFactoryMixIn):
    _object_class = Patient
    def _populate_cursor_with(self, cursor, patient_id):
        cursor.execute("""
            SELECT *
            FROM patient
            WHERE patient_id=%s
            """, (patient_id,))

class History(IdentityAttrMixIn):
    idattr = 'history_id'
    def __init__(self, dbrec):
        self.history_id = dbrec['history_id']
        self.group_number = dbrec['group_number']
        self.days_supply = dbrec['days_supply']
        self.doctor_dea_number = dbrec['doctor_dea_number']
        self.doctor_npi_number = dbrec['doctor_npi_number']
        self.quantity = int(dbrec['quantity'])
        self.patient_id = dbrec['patient_id']
        self.doctor_id = dbrec['doctor_id']
        self.drug_id = dbrec['drug_id']
        self.pharmacy_id = dbrec['pharmacy_id']
        self.claim_id = dbrec['claim_id']
        self.rx_date = dbrec['rx_date']
        self.rx_number = dbrec['rx_number']
        self.daw = dbrec['daw']
        self.temp_sr_ndc_override = dbrec['temp_sr_ndc_override']

    @property
    def _rx_date_yyyymmdd(self):
        return self.rx_date.strftime("%Y%m%d")

class HistoryFactory(CursorGetFactoryMixIn):
    _object_class = History
    def _populate_cursor_with(self, cursor, history_id):
        cursor.execute("""
            SELECT *
            FROM history
            WHERE history_id=%s
            """, (history_id,))

class Employer(IdentityAttrMixIn):
    idattr = 'tin'
    def __init__(self, dbrec):
        self.name = dbrec['name']
        self.tin = dbrec['tin']
        self.address_1 = dbrec['address_1']
        self.address_2 = dbrec['address_2']
        self.city = dbrec['city']
        self.state = dbrec['state']
        self.zip_code = dbrec['zip_code']
        self.policy_number = dbrec['policy_number']
        self.phone = dbrec['phone']

class NullEmployer(object):
    name = None
    tin = None
    address_1 = None
    address_2 = None
    city = None
    state = None
    zip_code = None
    policy_number = None
    phone = None

class CCMSIEmployer(object):
    def __init__(self, client):
        self.name = client.client_name
        self.tin = client.tin
        self.address_1 = '5930 Grand Ave'
        self.address_2 = None
        self.city = 'West Des Moines'
        self.state = 'IA'
        self.zip_code = '50266'
        self.policy_number = None
        self.phone = None

class EmployerFactory(CursorGetFactoryMixIn):
    _object_class = Employer
    _null_object_class = NullEmployer
    _ccmsi_groups = [] 

    def get(self, client):
        """If it's a CCMSI group we want to use the employer tin
        and name but use CCMSI address info """

        if self._ccmsi_groups == []:
            self._ccmsi_groups = self._get_ccmsi_groups()

        if client.group_number in self._ccmsi_groups: 
            return CCMSIEmployer(client)

        return CursorGetFactoryMixIn.get(self, client.tin)

    def _get_ccmsi_groups(self):
        cursor = self._db.cursor()
        cursor.execute("""
            SELECT group_number
            FROM client
            WHERE report_code = 'CCMSI';
            """)
        return ["%s" % group for group in cursor.fetchall()] 

    def _populate_cursor_with(self, cursor, tin):
        cursor.execute("""
            SELECT *
            FROM employer
            WHERE tin = %s
            """, (tin,))
    
class Claim(IdentityAttrMixIn):
    idattr = 'claim_id'
    def __init__(self, dbrec):
        self.claim_id = dbrec['claim_id']
        self.claim_number = dbrec['claim_number']
        self.doi = dbrec['doi']
        self.employer_tin = dbrec['employer_tin']

    @property
    def doi_yyyymmdd(self):
        return self.doi.strftime("%Y%m%d")

class ClaimFactory(CursorGetFactoryMixIn):
    _object_class = Claim

    def _populate_cursor_with(self, cursor, claim_id):
        cursor.execute("""
            SELECT *
            FROM claim
            WHERE claim_id=%s
            """, (claim_id,))

class Pharmacy(IdentityAttrMixIn):
    idattr = 'pharmacy_id'
    def __init__(self, dbrec):
        self.pharmacy_id = dbrec['pharmacy_id']
        self.nabp = dbrec['nabp']
        self.name = dbrec['name']
        self.tax_id = dbrec['tax_id']
        self.city = dbrec['city']
        self.state= dbrec['state']
        self.zip_code = dbrec['zip_code']
        self.npi = dbrec['npi']
        self.address_1 = dbrec['address_1']
        self.address_2 = dbrec['address_2']


class PharmacyFactory(CursorGetFactoryMixIn):
    _object_class = Pharmacy
    def _populate_cursor_with(self, cursor, pharmacy_id):
        cursor.execute("""
            SELECT *
            FROM pharmacy
            WHERE pharmacy_id=%s
            """, (pharmacy_id,))

class StateReportEntry(IdentityAttrMixIn):
    idattr = 'entry_id'
    def __init__(self, dbrec):
        self._dbrec = dbrec
        self.entry_id = dbrec['entry_id']
        self.file_id = dbrec['file_id']
        self.trans_id = dbrec['trans_id']
        self.control_number = dbrec['control_number']
        self.ack_code = dbrec['ack_code']
        self.create_date = dbrec['create_date']
        self.bill_date = dbrec['bill_date']
        self.paid_date = dbrec['paid_date']
        self.response_text = dbrec['response_text']
        self.cancel_file_id = dbrec['cancel_file_id']
        self.pending_cancel = dbrec['pending_cancel']

class StateReportEntryFactory(CursorGetFactoryMixIn):
    _object_class = StateReportEntry
    def entries_pending_report(self, reportzone):
        cursor = self._db.dict_cursor()
        cursor.execute("""
            SELECT *
            FROM state_report_entry
            WHERE 
                NOT EXISTS (SELECT trans_id 
                FROM work_queue
                WHERE state_report_entry.trans_id = work_queue.trans_id) AND
                (reportzone = %s AND
                  file_id IS NULL OR
                ( pending_cancel = TRUE AND
                  cancel_file_id IS NULL ))
        """, (reportzone,))
        return map(StateReportEntry, cursor)

    def _populate_cursor_with(self, cursor, entry_id):
        cursor.execute("""
            SELECT *
            FROM state_report_entry
            WHERE entry_id=%s
        """, (entry_id,)) 

class MockStateReportEntryFactory(object):
    """ Give a list of trans_ids and will produce fake state report
    entry objects for each of those trans ids
    """
    def __init__(self, trans_ids):
        self._trans_ids = trans_ids

    def unreported(self):
        import datetime
        recs = []
        for i, trans_id in enumerate(self._trans_ids):
            recs.append({
             'entry_id': i,
             'file_id': None,
             'trans_id': trans_id,
             'control_number': None,
             'ack_code': None,
             'create_date': datetime.date(2012, 1, 1),
             'bill_date': None,
             'paid_date': None,
             'response_text': None,
             'pending_cancel': False,
             'cancel_file_id': None})
        return map(StateReportEntry, recs)

class StateReportItemFactory(object):
    def __init__(self, transes, histories, drugs, claims, patients, invoices, pharmacys,
                 doctors, employers, clients):
        self.transes = transes
        self.histories = histories
        self.drugs = drugs
        self.claims = claims
        self.invoices = invoices
        self.patients = patients
        self.pharmacys = pharmacys
        self.doctors = doctors
        self.employers = employers
        self.clients = clients

    def for_entries(self, entries):
        return StateReportItemSet(self.for_entry(e) for e in entries)

    def for_entry(self, entry):
        trans = self.transes.get(entry.trans_id)
        history = self.histories.get(trans.history_id)
        invoice = self.invoices.get(trans.invoice_id)
        claim = self.claims.get(history.claim_id)
        patient = self.patients.get(history.patient_id)
        pharmacy = self.pharmacys.get(history.pharmacy_id)
        doctor = self.doctors.get(history.doctor_id)
        client = self.clients.get(history.group_number)
        drug = self.drugs.get(history.drug_id)
        if history.temp_sr_ndc_override != None:
            drug.ndc_number = history.temp_sr_ndc_override        
        if client.tin == None:
            client.tin = claim.employer_tin

## todo pass in whole client
        employer = self.employers.get(client)
        return StateReportItem(entry, trans, history, drug, claim, patient,
                               invoice, pharmacy, doctor, employer, client)

class StateReportItem(object):
    def __init__(self, entry, trans, history, drug, claim, patient, invoice,
                 pharmacy, doctor, employer, client):
        self.entry = entry
        self.trans = trans
        self.history = history
        self.drug = drug
        self.claim = claim
        self.invoice = invoice
        self.patient = patient
        self.pharmacy = pharmacy
        self.doctor = doctor
        self.employer = employer
        self.client = client

class StateReportItemSet(list):
    def grouped_by(self, attr):
        func = lambda x: getattr(x, attr)
        for grouped, subset in itertools.groupby(self, func):
            yield grouped, StateReportItemSet(subset)

    def unique(self, attr, size_check=None):
        data = set(getattr(i, attr) for i in self)
        if size_check and len(data) != size_check:
            raise DataError("size check for %s fails with %s"
                % (attr, size_check))
        return data

class StateReportFile(IdentityAttrMixIn):
    idattr = 'file_id'
    def __init__(self, dbrec):
        self.file_id = dbrec['file_id']
        self.file_name = dbrec['file_name']
        self.create_date = dbrec['create_date']
        self.send_date = dbrec['send_date']

class StateReportFileFactory(CursorGetFactoryMixIn):
    _object_class = StateReportFile
    def _populate_cursor_with(self, cursor, file_id):
        cursor.execute("""
            SELECT *
            FROM state_report_file
            WHERE file_id=%s
            """, (file_id,))

    def new(self, file_name, file_type, reportzone):
        """ Create a new state report file factory """
        sql = insert_sql("state_report_file", {
            'reportzone': reportzone,
            'file_type': file_type,
            'file_name': file_name
        }, ["file_id"])
        cursor = self._db.cursor()
        cursor.execute(sql)
        file_id = cursor.fetchone()[0]
        return self.get(file_id)

class DataError(Exception):
    pass

def test():
    # All transactions 
    from cpsar.runtime import db
    db.setup()

    trans_factory = TransFactory(db)
    history_factory = HistoryFactory(db)
    drug_factory = DrugFactory(db)
    claim_factory = ClaimFactory(db)
    patient_factory = PatientFactory(db)
    pharmacy_factory = PharmacyFactory(db)
    doctor_factory = DoctorFactory(db)
    employer_factory = EmployerFactory(db)

    # run through all the client factories, last man wins
    client_factory = ClientFactory(db, reportzone)

    invoice_factory = InvoiceFactory(db)
    sr_factory = StateReportEntryFactory(db)

    entry = sr_factory.get(262)
    pending_entries = sr_factory.entries_pending_report('TX')
    return

    item_factory = StateReportItemFactory(
        trans_factory,
        history_factory,
        drug_factory,
        claim_factory,
        patient_factory,
        invoice_factory,
        pharmacy_factory,
        doctor_factory,
        employer_factory,
        client_factory)

    items = StateReportItemSet()
    for entry in sr_factory.entries_pending_report('TX'):
        item = item_factory.for_entry(entry)
        items.append(item)

    for client, client_items in items.grouped_by('client'):
        print(client, len(client_items))
        for employer, employer_items in client_items.grouped_by('employer'):
            print('\t', employer, len(employer_items))
            for doctor, doctor_items in employer_items.grouped_by('doctor'):
                print('\t\t', doctor, len(doctor_items))
                for pharmacy, pharmacy_items in doctor_items.grouped_by('pharmacy'):
                    print('\t\t\t', pharmacy, len(pharmacy_items))

if __name__ == '__main__':
    test()

