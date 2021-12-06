# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = "sale.subscription"

    auto_create_invoice = fields.Boolean(
        string="Auto Create Invoice",
        default=False,
    )

    @api.onchange(
        "template_id",
    )
    def onchange_auto_create_invoice(self):
        auto_create_invoice = self.template_id.auto_create_invoice
        for document in self:
            document.auto_create_invoice = auto_create_invoice
