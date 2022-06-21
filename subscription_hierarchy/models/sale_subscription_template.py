# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleSubscriptionTemplate(models.Model):
    _name = "sale.subscription.template"
    _inherit = "sale.subscription.template"

    grace_period = fields.Integer(
        string="Subscription Grace Period",
        default=30,
    )
