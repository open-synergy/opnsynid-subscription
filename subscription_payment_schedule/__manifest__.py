# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Subscription Payment Schedule",
    "version": "11.0.1.3.0",
    "license": "LGPL-3",
    "category": "Sales",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "subscription_workflow_policy",
        "sale_subscription_asset",
        "subscription_auto_generate_invoice",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/sale_subscription_link_invoice.xml",
        "views/sale_subscription_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
