# Copyright 2021 PT. Simetri Sinergi Indonesia
# Copyright 2021 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Subscription Multiple Approval",
    "version": "11.0.1.1.0",
    "license": "LGPL-3",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "sale_subscription",
        "ssi_multiple_approval_mixin",
    ],
    "data": [
        "data/approval_template_data.xml",
        "views/sale_subscription_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "auto_install": False,
}
