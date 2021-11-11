# Copyright 2020 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Subscription Multiple Approval",
    "version": "11.0.1.0.0",
    "license": "LGPL-3",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "sale_subscription",
        "ssi_multiple_approval_mixin",
    ],
    "data": [
        "views/sale_subscription_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "auto_install": False,
}
