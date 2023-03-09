{
    'name': "Upload CSF",
    'summary': """Upload CSF""",
    'version': '16.0.1.0.3',
    'description': """Upload CSF""",
    'category': '',
    'author': '',
    'company': '',
    'website': "",
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/create_csf.xml',
        'views/upload_csf.xml',
        'views/res_partner.xml',
    ],
    'assets': {
        'web.assets_backend': [
           '/custom_csf/static/src/xml/list_controller.xml',
           '/custom_csf/static/src/js/list_controler.js',
           '/custom_csf/static/src/js/list_view.js',
        ],
    },
    'external_dependencies': {
        "python": ["pdfminer.six"]
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
