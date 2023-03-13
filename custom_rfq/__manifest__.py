{
    'name': "custom RFQ",
    'summary': """Custom RFQ""",
    'version': '16.0.1.0.1',
    'description': """Custom RFQ""",
    'category': '',
    'author': '',
    'company': '',
    'website': "",
    'depends': ['base', 'website_sale', 'product', 'website'],
    'data': [
        'views/request.xml',
        'views/product.xml',
        'views/settings.xml',
    ],
    'assets': {
       'web.assets_frontend': {
           '/custom_rfq/static/src/js/request.js',
       },
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
