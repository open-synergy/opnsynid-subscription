# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class SaleSubscriptionTemplate(models.Model):
    _name = "sale.subscription.template"
    _inherit = "sale.subscription.template"

    backdate_auto_create_invoice_offset = fields.Integer(
        string="Backdate Offset for Auto Create Invoice",
        default=0,
    )
    forwarddate_auto_create_invoice_offset = fields.Integer(
        string="Forward Offset for Auto Create Invoice",
        default=0,
    )

    @api.multi
    def _auto_create_invoice(self):
        self.ensure_one()
        obj_schedule = self.env["sale.subscription.payment_schedule"]
        date_today = fields.Date.from_string(fields.Date.today())
        date_min = date_today + relativedelta(
            days=-self.backdate_auto_create_invoice_offset
        )
        date_max = date_today + relativedelta(
            days=self.forwarddate_auto_create_invoice_offset
        )
        criteria = [
            ("subscription_id.template_id", "=", self.id),
            ("subscription_id.auto_create_invoice", "=", True),
            ("date_invoice", ">=", date_min),
            ("date_invoice", "<=", date_max),
            ("state", "=", "uninvoiced"),
        ]
        schedules = obj_schedule.search(criteria)
        schedules.action_create_invoice()
