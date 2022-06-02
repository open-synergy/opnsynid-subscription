# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = "sale.subscription"

    date_end = fields.Date(
        string="Date End of Subscription",
        readonly=True,
    )

    @api.multi
    def set_close(self):
        return self.write(
            {"state": "close", "date_end": fields.Date.from_string(fields.Date.today())}
        )
