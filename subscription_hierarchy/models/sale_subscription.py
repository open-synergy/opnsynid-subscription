# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = "sale.subscription"
    _parent_name = "parent_id"
    _parent_store = True

    type = fields.Selection(
        string="Type",
        selection=[
            ("new", "New Subscription"),
            ("renewal", "Renewal"),
            ("upgrade", "Upgrade"),
            ("downgrade", "Downgrade"),
        ],
        required=True,
        default="new",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "partner_id",
    )
    def _compute_allowed_parent_ids(self):
        obj_subscription = self.env["sale.subscription"]
        for record in self:
            result = []
            if record.partner_id:
                commercial_partner = record.partner_id.commercial_partner_id
                criteria = [
                    ("partner_id.commercial_partner_id", "=", commercial_partner.id),
                    ("state", "=", "open"),
                ]
                result = obj_subscription.search(criteria).ids
            record.allowed_parent_ids = result

    allowed_parent_ids = fields.Many2many(
        string="Allowed Parents",
        comodel_name="sale.subscription",
        compute="_compute_allowed_parent_ids",
        store=False,
    )
    parent_id = fields.Many2one(
        string="Previous Subscription",
        comodel_name="sale.subscription",
        readonly=True,
        index=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    parent_left = fields.Integer(
        string="Left Parent",
        index=True,
    )
    parent_right = fields.Integer(
        string="Right Parent",
        index=True,
    )
    child_ids = fields.One2many(
        comodel_name="sale.subscription",
        inverse_name="parent_id",
        string="Child Subscriptions",
        copy=True,
    )

    @api.depends(
        "type",
        "parent_id",
    )
    def _compute_initial_subscription(self):
        for record in self:
            result = False
            if record.type != "new" and record.parent_id:
                current_subscription = record
                try:
                    while not result:
                        if current_subscription.parent_id.type == "new":
                            result = current_subscription.parent_id
                        else:
                            result = (
                                current_subscription.parent_id.initial_subscription_id
                            )
                except RecursionError:
                    result = False
            record.initial_subscription_id = result

    initial_subscription_id = fields.Many2one(
        string="Initial Subscription",
        comodel_name="sale.subscription",
        compute="_compute_initial_subscription",
        store=True,
    )
