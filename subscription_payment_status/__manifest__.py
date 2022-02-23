# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Subscription Payment Status",
    "version": "11.0.1.0.0",
    "license": "LGPL-3",
    "category": "Sales",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "subscription_payment_schedule",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_subscription_payment_status_views.xml",
        "views/sale_subscription_template_views.xml",
        "views/sale_subscription_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
