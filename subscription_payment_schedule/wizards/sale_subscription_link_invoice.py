# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class SaleSubscriptionLinkInvoice(models.TransientModel):
    _name = "sale.subscription.link_invoice"
    _description = "Link Subscription Payment Schedule to Invoice"

    @api.model
    def _default_schedule_id(self):
        schedule_id = self.env.context.get("active_id", False)
        obj_schedule = self.env["sale.subscription.payment_schedule"]
        return obj_schedule.browse(schedule_id)[0]

    schedule_id = fields.Many2one(
        string="Payment Schedule",
        comodel_name="sale.subscription.payment_schedule",
        default=lambda r: r._default_schedule_id(),
        required=True,
    )

    @api.depends(
        "schedule_id",
    )
    def _compute_allowed_invoice_ids(self):
        obj_invoice = self.env["account.invoice"]
        for record in self:
            subscription = record.schedule_id.subscription_id
            criteria = [
                (
                    "partner_id.commercial_partner_id.id",
                    "=",
                    subscription.partner_id.commercial_partner_id.id,
                ),
                ("state", "in", ["open", "paid"]),
                ("type", "=", "out_invoice"),
            ]
            record.allowed_invoice_ids = obj_invoice.search(criteria).ids

    allowed_invoice_ids = fields.Many2many(
        string="Allowed Invoices",
        comodel_name="account.invoice",
        compute="_compute_allowed_invoice_ids",
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
        required=True,
    )

    @api.multi
    def action_link_invoice(self):
        for record in self:
            record._link_invoice()

    @api.multi
    def _link_invoice(self):
        self.ensure_one()
        self.schedule_id.write(
            {
                "invoice_id": self.invoice_id.id,
            }
        )
