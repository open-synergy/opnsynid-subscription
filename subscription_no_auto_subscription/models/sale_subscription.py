# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = "sale.subscription"

    @api.model
    def create(self, values):
        _super = super(SaleSubscription, self)
        result = _super.create(values)
        result.message_unsubscribe(partner_ids=result.partner_id.ids)
        return result
