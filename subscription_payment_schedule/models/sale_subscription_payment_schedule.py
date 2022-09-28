# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class SaleSubscriptionPaymentSchedule(models.Model):
    _name = "sale.subscription.payment_schedule"
    _description = "Subscription Payment Schedule"

    subscription_id = fields.Many2one(
        string="# Subscription",
        comodel_name="sale.subscription",
        required=True,
        ondelete="cascade",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    date_invoice = fields.Date(
        string="Date Invoice",
        required=True,
    )
    date_due = fields.Date(
        string="Date Due",
        required=True,
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
        readonly=True,
        ondelete="restrict",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="invoice_id.currency_id",
        store=True,
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed",
        related="invoice_id.amount_untaxed",
        store=True,
    )
    amount_tax = fields.Monetary(
        string="Tax",
        related="invoice_id.amount_tax",
        store=True,
    )
    amount_total = fields.Monetary(
        string="Total ",
        related="invoice_id.amount_total",
        store=True,
    )
    residual = fields.Monetary(
        string="Total ",
        related="invoice_id.residual",
        store=True,
    )
    no_invoice = fields.Boolean(
        string="No Invoice",
        readonly=True,
    )
    manual = fields.Boolean(
        string="Manually Controlled",
        readonly=True,
    )

    @api.depends(
        "invoice_id",
        "subscription_id.state",
        "no_invoice",
        "manual",
    )
    def _compute_state(self):
        for record in self:
            if record.subscription_id.state in ["draft", "confirm", "reject", "cancel"]:
                state = "draft"
            elif record.subscription_id.state in ["open", "close"]:
                if record.invoice_id:
                    state = "invoiced"
                elif record.no_invoice:
                    state = "free"
                elif record.manual:
                    state = "manual"
                elif record.subscription_id.state == "close" and not record.invoice_id:
                    state = "noinvoice"
                else:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("noinvoice", "No Invoice"),
            ("invoiced", "Invoiced"),
            ("cancelled", "Cancelled"),
            ("free", "Free"),
            ("manual", "Manually Controlled"),
        ],
        compute="_compute_state",
        store=True,
    )

    @api.multi
    def action_create_invoice(self):
        for record in self:
            record._create_invoice()

    @api.multi
    def action_delete_invoice(self):
        for record in self:
            record._delete_invoice()

    @api.multi
    def action_disconnect_invoice(self):
        for record in self:
            record._disconnect_invoice()

    @api.multi
    def action_mark_as_free(self):
        for record in self:
            record._mark_as_free()

    @api.multi
    def action_mark_as_must_pay(self):
        for record in self:
            record._mark_as_must_pay()

    @api.multi
    def action_manually_controlled(self):
        for record in self:
            record._manually_controlled()

    @api.multi
    def action_no_manual(self):
        for record in self:
            record._no_manual()

    @api.multi
    def _mark_as_free(self):
        self.ensure_one()
        self.write(
            {
                "no_invoice": True,
            }
        )

    @api.multi
    def _mark_as_must_pay(self):
        self.ensure_one()
        self.write(
            {
                "no_invoice": False,
            }
        )

    @api.multi
    def _manually_controlled(self):
        self.ensure_one()
        self.write(
            {
                "manual": True,
            }
        )

    @api.multi
    def _no_manual(self):
        self.ensure_one()
        self.write(
            {
                "manual": False,
            }
        )

    @api.multi
    def _disconnect_invoice(self):
        self.ensure_one()
        self.invoice_id.write(
            {
                "source_document_res_id": 0,
                "source_document_model_id": False,
            }
        )
        self.write(
            {
                "invoice_id": False,
            }
        )

    @api.multi
    def _create_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            error_msg = _("There is already an invoice")
            raise UserError(error_msg)
        subscription = self.subscription_id
        obj_account_invoice = self.env["account.invoice"]
        invoice = obj_account_invoice.create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )
        for detail in subscription.recurring_invoice_line_ids:
            detail._create_invoice_line(invoice, self.date_start, self.date_end)
        invoice.compute_taxes()
        return True

    @api.multi
    def _prepare_invoice_data(self):
        self.ensure_one()
        subscription = self.subscription_id
        partner = subscription.partner_id
        journal = self._get_receivable_journal()
        account = self._get_receivable_account()
        partner = self._get_partner()
        name = "{} {} - {}".format(
            subscription.display_name,
            subscription.date_start,
            subscription.date,
        )
        return {
            "partner_id": partner.id,
            "date_invoice": self.date_invoice,
            "date_due": self.date_due,
            "journal_id": journal.id,
            "account_id": account.id,
            "currency_id": subscription.pricelist_id.currency_id.id,
            "origin": subscription.name,
            "type_id": "out_invoice",
            "payment_term_id": subscription.payment_term_id.id,
            "name": name,
            "user_id": subscription.user_id.id,
            "team_id": subscription.user_id.team_id
            and subscription.user_id.team_id.id
            or False,
            "source_document_model_id": self.env.ref(
                "sale_subscription.model_sale_subscription"
            ).id,
            "source_document_res_id": subscription.id,
        }

    @api.multi
    def _get_partner(self):
        self.ensure_one()
        result = self.subscription_id.contact_invoice_id

        if not result:
            result = self.subscription_id.partner_id

        return result

    @api.multi
    def _get_receivable_journal(self):
        self.ensure_one()
        error_msg = _("No receivable journal defined")
        if not self.subscription_id.template_id.journal_id:
            raise UserError(error_msg)

        return self.subscription_id.template_id.journal_id

    @api.multi
    def _get_receivable_account(self):
        self.ensure_one()
        error_msg = _("No receivable account defined")
        if not self.subscription_id.partner_id.property_account_receivable_id:
            raise UserError(error_msg)
        return self.subscription_id.partner_id.property_account_receivable_id

    @api.multi
    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        if invoice.state == "draft":
            self.write({"invoice_id": False})
            invoice.unlink()
        else:
            msg_err = _("Only invoice with draft state can be deleted")
            raise UserError(msg_err)
        return True
