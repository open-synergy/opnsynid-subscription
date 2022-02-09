# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SaleSubscriptionTemplate(models.Model):
    _name = "sale.subscription.template"
    _inherit = "sale.subscription.template"

    @api.multi
    def _auto_create_invoice(self):
        self.ensure_one()
        obj_schedule = self.env["sale.subscription.payment_schedule"]
        date_today = fields.Date.today()
        criteria = [
            ("subscription_id.template_id", "=", self.id),
            ("subscription_id.auto_create_invoice", "=", True),
            ("date_invoice", "=", date_today),
            ("state", "=", "uninvoiced"),
        ]
        schedules = obj_schedule.search(criteria)
        schedules.action_create_invoice()
