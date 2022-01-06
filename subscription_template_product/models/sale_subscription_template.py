# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleSubscriptionTemplate(models.Model):
    _inherit = "sale.subscription.template"

    template_line_ids = fields.One2many(
        string="Invoice Lines",
        comodel_name="sale.subscription.template_line",
        inverse_name="template_id",
        copy=True,
    )
