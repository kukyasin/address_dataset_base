{
    "name": "Address Dataset Base",
    "version": "19.0.1.0.0",
    "category": "Localization",
    "summary": "Core address dataset engine with hierarchy, partner integration and coordinate visibility controls",
    "description": """
Address Dataset Base

Core module for multi-country address dataset addons.

Includes:
- Generic address dataset model
- Country/State/City/Neighborhood/ZIP hierarchy support
- Partner auto-fill integration
- Latitude/Longitude fields and visibility settings
- Common views, menus and helper logic
    """,
    "author": "ALGORITMETIC LTD",
    "website": "https://www.algoritmetic.com",
    "license": "LGPL-3",
    "price": 0.0,
    "currency": "EUR",
    "support": "support@algoritmetic.com",
    "images": [
        "static/description/main_screen.png",
    ],
    "depends": ["base_address_extended"],
    "data": [
        "security/address_dataset_base_security.xml",
        "views/address_dataset_settings_views.xml",
        "views/res_partner_views.xml",
        "views/address_dataset_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "address_dataset_base/static/src/js/neighborhood_many2one_patch.js",
            "address_dataset_base/static/src/xml/float_field_placeholder.xml",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
