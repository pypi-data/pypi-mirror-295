import cpsar.report
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'CPS Prescriptions'

    params = [
        ('Start Date', kcontrol.DatePicker('start_date')), 
        ('End Date',   kcontrol.DatePicker('end_date'))
    ]

    query_css = """
        #report_body {width: auto; }
        TD.data1 { text-align: right; }
        TD.data2 { text-align: center; }
        TD.data3 { text-align: center; }
        TD.data4 { text-align: left; }
        TD.data5 { text-align: left; }
        TD.data6 { text-align: right; }
        TD.data7 { text-align: right; }
        TD.data8 { text-align: right; }
        TD.data9 { text-align: right; }
        TD.data10 { text-align: right; }
        TD.data11 { text-align: right; }
        TD.data12 { text-align: right; }
    """

    sql = """
        SELECT
            trans.batch_date::date,
            trans.group_number,
            trans.rx_date,
            trans.rx_number,
            drug.name,
            trans.refill_number,
            patient.first_name,
            patient.last_name,
            trans.total,
            trans.adjustments
        FROM trans
        JOIN patient ON
            patient.patient_id = trans.patient_id AND
            trans.batch_date BETWEEN %(start_date)s AND %(end_date)s
        JOIN pharmacy ON
            pharmacy.nabp = '0123682' AND
            trans.pharmacy_id = pharmacy.pharmacy_id
        JOIN drug ON
            trans.drug_id = drug.drug_id
        ORDER BY trans.batch_date,
                 trans.rx_number,
                 trans.refill_number
        """

application = Report().wsgi()
