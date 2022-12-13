{
    'name': 'Clinic_and_patient',
    'sequence': -100,
    'version': '1.0.0',

    'depends': ['base', 'account', 'mail'],
    'description': """
    """,
    'data': [
        'security/clinic_security.xml',
        'security/ir.model.access.csv',
        'data/doctor_number_seq.xml',
        'data/opd_id_seq.xml',
        'data/patient_number_seq.xml',
        'wizard/wiz_action_views.xml',
        'views/clinic_menu.xml',
        'views/doctor.xml',
        'views/department_views.xml',
        'views/patient.xml',
        'views/opd.xml',
        'views/medicine.xml',
        'report/report_Clinic.xml',
        'report/report.xml',

    ],
    'demo': [
        'data/patient_demo.xml',
        'data/department_demo.xml',
        'data/medicine_demo.xml',
        'data/opd_demo.xml',

    ],
    'application': True,
    'license': 'LGPL-3',
}
