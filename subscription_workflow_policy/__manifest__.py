# Copyright 2021 PT. Simetri Sinergi Indonesia.
# Copyright 2021 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Subscription Workflow Policy",
    "version": "11.0.1.0.0",
    "license": "LGPL-3",
    "category": "Sales",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "subscription_multiple_approval",
        "ssi_policy_mixin",
    ],
    "data": [
        "views/sale_subscription_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
