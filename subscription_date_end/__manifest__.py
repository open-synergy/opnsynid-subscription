# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Subscription Date End",
    "version": "11.0.1.1.0",
    "license": "LGPL-3",
    "category": "Sales",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "sale_subscription",
    ],
    "data": [
        "views/sale_subscription_views.xml",
        "wizards/sale_subscription_close_reason_wizard_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
