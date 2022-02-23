# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = "sale.subscription"

    @api.multi
    def _get_payment_status_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    @api.multi
    def _compute_payment_status_id(self):
        for record in self:
            res = False
            localdict = record._get_payment_status_localdict()
            if record.template_id:
                template = record.template_id
                try:
                    safe_eval(
                        template.payment_status_python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    res = localdict["result"]
                except Exception:
                    res = False
            record.payment_status_id = res

    payment_status_id = fields.Many2one(
        string="Payment Status",
        comodel_name="sale.subscription.payment_status",
        compute="_compute_payment_status_id",
        store=True,
    )
