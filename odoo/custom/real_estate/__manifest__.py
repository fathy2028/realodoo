{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'summary': 'Manage real estate properties',
    'description': 'Track real estate properties, their characteristics, and lifecycle from listing to sale.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/estate_property_type_data.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
