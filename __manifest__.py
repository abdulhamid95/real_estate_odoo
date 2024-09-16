# -*- coding: utf-8 -*-
{
    'name': "real_state",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'leaflet_map', 'contacts', 'web'],
    'post_init_hook': 'post_init_hook',
    # always loaded
    'assets': {
        'web.assets_backend': [
            # تضمين مكتبة Leaflet من CDN
            'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js',
            'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css',
            # تضمين ملف JavaScript الخاص بك
            'real_state/static/src/js/property_map_view.js',
            'real_state/static/src/js/map_view.js',
        ]
    },
    'data': [
        'security/ir.model.access.csv',
        # 'views/property_map_template.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/filters_views.xml',
        'views/property_menu.xml',
        'views/res_partner_views.xml',
        'views/chat_views.xml',
        'views/report.xml',
        'views/qweb_views.xml'
        # 'views/webclient_template.xml'
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'real_state/static/src/js/notification_button.js',
    #     ],
    # },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],



    # 'assets': {
    #     'web.assets_backend': [
    #             'real_state/static/src/js/real_state_fetch.js',
    #     ],
    # }
}

