# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = [
        "sale.subscription",
        "mixin.multiple_approval",
    ]
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"

    state = fields.Selection(
        selection=[
            ("draft", "New"),
            ("confirm", "Confirm"),
            ("open", "In Progress"),
            ("pending", "To Renew"),
            ("close", "Closed"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ]
    )

    def action_confirm(self):
        for document in self:
            document.write({"state": "confirm"})
            document.action_request_approval()

    def action_restart(self):
        for document in self:
            document.write({"state": "draft"})

    def action_approve_approval(self):
        _super = super(SaleSubscription, self)
        _super.action_approve_approval()
        for document in self:
            if document.approved:
                document.set_open()
