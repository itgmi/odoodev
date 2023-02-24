{
    'name': 'S D I N',
    'version': '16.0.1.0.1',
    'summary': """Siemens Digital Inventory Network""",
    'description': 'Siemens Digital Inventory Network',
    'category': '',
    'author': '',
    'company': '',
    'website': "",
    'depends': ['base', 'product', 'website_sale'],
    'data': [
        'views/settings.xml',
        'data/shedule_action.xml',
        'views/cron.xml',
    ],
    "external_dependencies": {
        "python": ["pycryptodome"]
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
