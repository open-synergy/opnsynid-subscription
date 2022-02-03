# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Subscription State Change Constrains",
    "version": "11.0.1.0.0",
    "license": "LGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "sale_subscription",
        "ssi_state_change_constrain_mixin",
    ],
    "data": [
        "views/sale_subscription_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
