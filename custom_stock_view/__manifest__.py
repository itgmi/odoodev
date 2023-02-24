{
    'name': 'Custom Stock View',
    'version': '16.0.1.0.0',
    'summary': """Custom Stock View""",
    'description': 'Custom Stock View',
    'category': '',
    'author': '',
    'company': '',
    'website': "",
    'depends': ['base', 'website', 'website_sale',
                'portal', 'product', 'web', 'stock',
                'custom_product'],
    'data': [
        'views/stock_menu.xml',
        'views/stock_page.xml',
        'views/portal.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/custom_stock_view/static/src/js/stock.js',
            ]
    },
    'demo': [],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
