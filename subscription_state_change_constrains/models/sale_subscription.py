# Copyright 2021 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = [
        "sale.subscription",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    @api.onchange(
        "template_id",
    )
    def onchange_status_check_template_id(self):
        self.status_check_template_id = False
        if self.template_id:
            cek_template_id = self._get_template_status_check()
            self.status_check_template_id = cek_template_id

    @api.model
    def create(self, values):
        _super = super(SaleSubscription, self)
        result = _super.create(values)
        if not result.status_check_template_id:
            result.onchange_status_check_template_id()
            result.onchange_state_change_constrain_template_id()
        return result
