# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleSubscriptionTemplate(models.Model):
    _name = "sale.subscription.template"
    _inherit = "sale.subscription.template"

    auto_create_invoice = fields.Boolean(
        string="Auto Create Invoice",
        default=False,
    )
    cron_id = fields.Many2one(
        string="Cron",
        comodel_name="ir.cron",
        readonly=True,
    )

    @api.multi
    def action_create_cron(self):
        for document in self:
            document._create_cron()

    @api.multi
    def action_delete_cron(self):
        for document in self:
            document._delete_cron()

    @api.multi
    def _create_cron(self):
        self.ensure_one()
        data = self._prepare_cron_data()
        obj_cron = self.env["ir.cron"]
        cron = obj_cron.create(data)
        self.write({"cron_id": cron.id})

    @api.multi
    def _prepare_cron_data(self):
        self.ensure_one()
        int_type = ""
        int_number = 1
        if self.recurring_rule_type == "daily":
            int_type = "days"
            int_number = self.recurring_interval
        elif self.recurring_rule_type == "weekly":
            int_type = "weeks"
            int_number = self.recurring_interval
        elif self.recurring_rule_type == "monthly":
            int_type = "months"
            int_number = self.recurring_interval
        elif self.recurring_rule_type == "yearly":
            int_type = "months"
            int_number = self.recurring_interval * 12
        else:
            int_type = "days"
            int_number = 1
        cron_name = "Generate Auto Invoice: %s" % (self.name)
        return {
            "name": cron_name,
            "user_id": self.env.user.id,
            "active": True,
            "interval_number": int_number,
            "interval_type": int_type,
            "numbercall": -1,
            "doall": False,
            "model_id": self.env.ref(
                "sale_subscription.model_sale_subscription_template"
            ).id,
            "code": "model.cron_auto_create_invoice(%s)" % (self.id),
            "state": "code",
        }

    @api.multi
    def _delete_cron(self):
        for document in self:
            document.cron_id.unlink()

    @api.model
    def cron_auto_create_invoice(self, subscription_id):
        subscription_id = self.search([("id", "=", subscription_id)])[0]
        subscription_id._auto_create_invoice()

    @api.multi
    def _auto_create_invoice(self):
        self.ensure_one()
        obj_sale_subscription = self.env["sale.subscription"]
        criteria = [
            ("template_id", "=", self.id.id),
        ]
        auto_generate = obj_sale_subscription.search(criteria)
        if auto_generate:
            for data_sale_subscription in auto_generate:
                if data_sale_subscription.auto_create_invoice:
                    data_sale_subscription.recurring_invoice()
