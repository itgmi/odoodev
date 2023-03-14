{
    'name': 'MercadoLibre',
    'version': '16.0.1.5.7',
    'summary': """MercadoLibre""",
    'description': 'MercadoLibre',
    'category': '',
    'author': '',
    'company': '',
    'website': "",
    'depends': ['base', 'product', 'stock', 'delivery', 'custom_product',
                'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/config.xml',
        'data/refresh_action.xml',
        'views/cron.xml',
        'views/product.xml',
        'views/available_stock.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
