# Copyright 2021 PT. Simetri Sinergi Indonesia.
# Copyright 2021 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = [
        "sale.subscription",
        "mixin.policy",
    ]

    def _compute_policy(self):
        _super = super(SaleSubscription, self)
        _super._compute_policy()

    open_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
    )
    quotation_ok = fields.Boolean(
        string="Can Renewal Quotation",
        compute="_compute_policy",
        store=False,
    )
    upsell_ok = fields.Boolean(
        string="Can Upsell Subscription",
        compute="_compute_policy",
        store=False,
    )
    close_ok = fields.Boolean(
        string="Can Close",
        compute="_compute_policy",
        store=False,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
    restart_ok = fields.Boolean(
        string="Can Set To Draft",
        compute="_compute_policy",
        store=False,
    )
    pending_ok = fields.Boolean(
        string="Can Renew",
        compute="_compute_policy",
        store=False,
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
        store=False,
    )
    reject_ok = fields.Boolean(
        string="Can Reject",
        compute="_compute_policy",
        store=False,
    )

    @api.onchange(
        "template_id",
    )
    def onchange_policy_template_id(self):
        policy_template_id = self._get_template_policy()
        for document in self:
            document.policy_template_id = policy_template_id
