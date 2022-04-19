# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta
from openerp.exceptions import UserError

from odoo import _, api, fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = "sale.subscription"

    @api.depends(
        "partner_id",
    )
    def _compute_allowed_contact_invoice_ids(self):
        obj_partner = self.env["res.partner"]
        for record in self:
            result = []
            if record.partner_id:
                criteria = [
                    (
                        "commercial_partner_id",
                        "=",
                        record.partner_id.commercial_partner_id.id,
                    ),
                ]
                result = obj_partner.search(criteria).ids
            record.allowed_contact_invoice_ids = result

    allowed_contact_invoice_ids = fields.Many2many(
        string="Allowed Invoice To",
        comodel_name="res.partner",
        compute="_compute_allowed_contact_invoice_ids",
    )

    contact_invoice_id = fields.Many2one(
        string="Invoice To",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = 0

    invoice_count = fields.Integer(compute="_compute_invoice_count")

    @api.multi
    @api.depends(
        "date_start",
        "date",
    )
    def _compute_period(self):
        for document in self:
            if document.date_start and document.date:
                start = datetime.strptime(document.date_start, "%Y-%m-%d")
                end = datetime.strptime(document.date, "%Y-%m-%d")
                delta_date = relativedelta(end, start)
                document.yearly_period = delta_date.years
                document.monthly_period = delta_date.months
                document.daily_period = delta_date.days

    yearly_period = fields.Integer(
        string="Yearly Period",
        compute="_compute_period",
        store=True,
    )
    monthly_period = fields.Integer(
        string="Monthly Period",
        compute="_compute_period",
        store=True,
    )
    daily_period = fields.Integer(
        string="Daily Period",
        compute="_compute_period",
        store=True,
    )

    @api.multi
    @api.depends(
        "template_id",
        "date_start",
        "date",
    )
    def _compute_invoice_number(self):
        for document in self:
            invoice_number = 0
            if document.template_id and document.date_start and document.date:
                payment_term_period_number = document.template_id.recurring_interval
                period_type = document.template_id.recurring_rule_type
                format = "%Y-%m-%d"

                dt_start = datetime.strptime(document.date_start, format)
                dt_end = datetime.strptime(document.date, format)
                subscription_days = (dt_end - dt_start).days
                if period_type == "yearly":
                    conv_days = subscription_days / 365
                elif period_type == "monthly":
                    r_months = relativedelta(dt_end, dt_start)
                    conv_days = r_months.months + (12 * r_months.years)
                elif period_type == "daily":
                    conv_days = subscription_days
                else:
                    conv_days = 0
                invoice_number = conv_days / payment_term_period_number
            document.invoice_number = invoice_number

    invoice_number = fields.Integer(
        string="Invoice Number",
        compute="_compute_invoice_number",
        store=True,
    )
    invoice_computation_method = fields.Selection(
        string="Invoice Computation",
        selection=[("offset", "Offset"), ("fixed", "Fixed Date")],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default="offset",
    )
    invoice_method = fields.Selection(
        string="Invoice Method",
        selection=[
            ("advance", "Advance"),
            ("arear", "Arear"),
        ],
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_invoice_offset = fields.Integer(
        string="Date Invoice Offset",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    payment_term_id = fields.Many2one(
        string="Invoice Payment Term",
        comodel_name="account.payment.term",
        required=False,
        readonly=False,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    payment_schedule_ids = fields.One2many(
        string="Payment Schedule(s)",
        comodel_name="sale.subscription.payment_schedule",
        inverse_name="subscription_id",
        copy=False,
    )

    @api.depends(
        "payment_schedule_ids",
        "payment_schedule_ids.date_invoice",
        "payment_schedule_ids.state",
        "state",
    )
    def _compute_first_invoice_date(self):
        for record in self:
            result = False
            if len(record.payment_schedule_ids) > 0:
                result = record.payment_schedule_ids[0].date_invoice
            record.first_date_invoice = result

    first_date_invoice = fields.Date(
        string="First Date Invoice",
        compute="_compute_first_invoice_date",
        store=True,
    )

    @api.depends(
        "payment_schedule_ids",
        "payment_schedule_ids.date_invoice",
        "payment_schedule_ids.state",
    )
    def _compute_first_payment_schedule_state(self):
        for record in self:
            result = False
            if len(record.payment_schedule_ids) > 0:
                result = record.payment_schedule_ids[0].state
            record.first_payment_schedule_state = result

    first_payment_schedule_state = fields.Selection(
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
        compute="_compute_first_payment_schedule_state",
        store=True,
    )

    @api.depends(
        "payment_schedule_ids",
        "payment_schedule_ids.date_invoice",
        "payment_schedule_ids.state",
    )
    def _compute_next_invoice_date(self):
        obj_schedule = self.env["sale.subscription.payment_schedule"]
        for record in self:
            result = False
            criteria = [
                ("subscription_id", "=", record.id),
                ("state", "=", "uninvoiced"),
            ]
            schedule = obj_schedule.search(criteria, limit=1)
            if len(schedule) == 1:
                result = schedule[0].date_invoice
            record.next_invoice_date = result

    next_invoice_date = fields.Date(
        string="Next Date Invoice",
        compute="_compute_next_invoice_date",
        store=True,
    )

    @api.multi
    def action_create_payment_schedule(self):
        for document in self:
            document._delete_payment_schedule()
            document._create_payment_schedule()

    @api.multi
    def _delete_payment_schedule(self):
        self.ensure_one()
        if self.payment_schedule_ids:
            for schedule in self.payment_schedule_ids:
                invoice_id = schedule.invoice_id
                schedule.write({"invoice_id": False})
                invoice_id.unlink()
            self.payment_schedule_ids.unlink()

    @api.multi
    def _create_payment_schedule(self):
        self.ensure_one()
        obj_payment_schedule = self.env["sale.subscription.payment_schedule"]
        date_start = self.date_start
        for _period_num in range(1, self.invoice_number + 1):
            date_end = self._get_payment_schedule_date_end(date_start)
            date_invoice = self._get_payment_schedule_date_invoice(date_start, date_end)
            date_due = self._get_payment_schedule_date_due(date_invoice)
            data = {
                "subscription_id": self.id,
                "date_start": date_start,
                "date_end": date_end,
                "date_invoice": date_invoice,
                "date_due": date_due,
            }
            obj_payment_schedule.create(data)
            date_start = date_end

    @api.multi
    def _get_payment_schedule_date_due(self, date_invoice):
        self.ensure_one()
        res = date_invoice
        obj_account_payment_term = self.env["account.payment.term"]
        payment_term = obj_account_payment_term.browse(self.payment_term_id.id)
        payment_term_list = payment_term.compute(value=1, date_ref=date_invoice)[0]
        if payment_term_list:
            res = max(line[0] for line in payment_term_list)
        return res

    @api.multi
    def _get_payment_schedule_date_invoice(self, date_start, date_end):
        self.ensure_one()
        if self.invoice_computation_method == "offset":
            if self.invoice_method == "advance":
                factor = relativedelta(days=(self.date_invoice_offset * -1))
                date = date_start
            else:
                factor = relativedelta(days=self.date_invoice_offset)
                date = date_end
        else:
            if self.invoice_method == "advance":
                factor = relativedelta(months=-1, day=self.date_invoice_offset)
                date = date_start
            else:
                factor = relativedelta(months=1, day=self.date_invoice_offset)
                date = date_start

        dt_date = fields.Date.from_string(date)
        date_invoice = dt_date + factor
        return fields.Date.to_string(date_invoice)

    @api.multi
    def _get_payment_schedule_date_start(self, date_end):
        self.ensure_one()

        dt_end = fields.Date.from_string(date_end)
        date_start = dt_end + relativedelta(days=1)
        return fields.Date.to_string(date_start)

    @api.multi
    def _get_payment_schedule_date_end(self, date):
        self.ensure_one()

        if self.template_id.recurring_rule_type == "daily":
            add = relativedelta(days=self.template_id.recurring_interval)
        elif self.template_id.recurring_rule_type == "monthly":
            add = relativedelta(months=self.template_id.recurring_interval)
        elif self.template_id.recurring_rule_type == "yearly":
            add = relativedelta(years=self.template_id.recurring_interval)
        dt_date = fields.Date.from_string(date)
        date_end = dt_date + add
        return fields.Date.to_string(date_end)

    @api.constrains(
        "state",
    )
    def _check_schedule_can_cancel(self):
        obj_schedule = self.env["sale.subscription.payment_schedule"]
        error_msg = _("Cancel all schedule invoice(s)")
        for record in self:
            if record.state == "cancel":
                criteria = record._prepare_check_schedule_dom()
                count_schedule = obj_schedule.search_count(criteria)
                if count_schedule > 0:
                    raise UserError(error_msg)

    @api.multi
    def _prepare_check_schedule_dom(self):
        self.ensure_one()
        return [
            ("subscription_id", "=", self.id),
            ("invoice_id", "!=", False),
        ]

    @api.onchange(
        "partner_id",
    )
    def onchange_contact_invoice_id(self):
        self.contact_invoice_id = False
