{
    'name': "custom stock upload",
    'summary': """Custom Stock Upload""",
    'version': '16.0.1.2.4',
    'description': """Custom Stock Upload""",
    'category': '',
    'author': '',
    'company': '',
    'website': "",
    'depends': ['base', 'stock', 'stock_account', 'website_sale',
                'website', 'web', 'sale', 'delivery'],
    'data': [
        'views/stock_upload.xml',
        'views/users.xml',
        'views/product.xml',
        'views/location.xml',
        'views/transfers.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/custom_stock_upload/static/src/js/modal.js',
            ],
        'web.assets_backend': [
            '/custom_stock_upload/static/src/widgets/qty_popover.xml',
        ],
    },
    'demo': [],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
