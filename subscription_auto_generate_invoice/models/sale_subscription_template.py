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
        cron_name = "Generate Auto Invoice: %s" % (self.name)
        return {
            "name": cron_name,
            "user_id": self.env.user.id,
            "active": True,
            "interval_number": 5,
            "interval_type": "minutes",
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
        template = self.search([("id", "=", subscription_id)])[0]
        template._auto_create_invoice()

    @api.multi
    def _auto_create_invoice(self):
        self.ensure_one()
        obj_sale_subscription = self.env["sale.subscription"]
        date_today = fields.Date.today()
        criteria = [
            ("template_id", "=", self.id),
            ("auto_create_invoice", "=", True),
            ("recurring_next_date", "=", date_today),
        ]
        auto_generate = obj_sale_subscription.search(criteria)
        if auto_generate:
            for data_sale_subscription in auto_generate:
                if data_sale_subscription.auto_create_invoice:
                    data_sale_subscription.recurring_invoice()
