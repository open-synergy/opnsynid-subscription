# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = [
        "sale.subscription",
        "mixin.related_attachment",
    ]

    @api.onchange(
        "template_id",
    )
    def onchange_related_attachment_template_id(self):
        super(SaleSubscription, self)._onchange_related_attachment_template_id()
