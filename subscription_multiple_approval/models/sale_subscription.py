# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
        selection_add=[
            ("confirm", "Confirm"),
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

    # def action_reject_approval(self):
    #     _super = super(AccountBankStatement, self)
    #     _super.action_reject_approval()
    #     for document in self:
    #         if document.rejected:
    #             for line in document.line_ids:
    #                 if line.journal_entry_ids:
    #                     line.button_cancel_reconciliation()
