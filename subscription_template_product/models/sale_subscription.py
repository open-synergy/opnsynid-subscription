# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    @api.onchange(
        "template_id",
    )
    def onchange_recurring_invoice_line_ids(self):
        recurring_invoice_line_ids = []
        self.recurring_invoice_line_ids = False
        if self.template_id:
            if self.template_id.template_line_ids:
                for line in self.template_id.template_line_ids:
                    data = {
                        "template_id": self.id,
                        "name": line.name,
                        "product_id": line.product_id.id,
                        "quantity": line.quantity,
                        "uom_id": line.uom_id.id,
                        "price_unit": line.price_unit,
                        "discount": line.discount,
                    }
                    recurring_invoice_line_ids.append((0, 0, data))
            self.recurring_invoice_line_ids = recurring_invoice_line_ids
