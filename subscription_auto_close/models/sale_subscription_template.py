# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SaleSubscriptionTemplate(models.Model):
    _name = "sale.subscription.template"
    _inherit = "sale.subscription.template"

    auto_close_cron_id = fields.Many2one(
        string="Auto Close Cron",
        comodel_name="ir.cron",
        readonly=True,
    )
    close_reason_id = fields.Many2one(
        string="Close Reason",
        comodel_name="sale.subscription.close.reason",
    )

    @api.multi
    def action_create_auto_close_cron(self):
        for document in self:
            document._create_auto_close_cron()

    @api.multi
    def action_delete_auto_close_cron(self):
        for document in self:
            document._delete_auto_close_cron()

    @api.multi
    def _create_auto_close_cron(self):
        self.ensure_one()
        data = self._prepare_auto_close_cron_data()
        obj_cron = self.env["ir.cron"]
        cron = obj_cron.create(data)
        self.write({"auto_close_cron_id": cron.id})

    @api.multi
    def _prepare_auto_close_cron_data(self):
        self.ensure_one()
        cron_name = "Auto Close Subscription: %s" % (self.name)
        return {
            "name": cron_name,
            "user_id": self.env.user.id,
            "active": True,
            "interval_number": 1,
            "interval_type": "days",
            "numbercall": -1,
            "doall": False,
            "model_id": self.env.ref(
                "sale_subscription.model_sale_subscription_template"
            ).id,
            "code": "model.cron_auto_close(%s)" % (self.id),
            "state": "code",
        }

    @api.multi
    def _delete_auto_close_cron(self):
        for document in self:
            document.auto_close_cron_id.unlink()

    @api.model
    def cron_auto_close(self, template_id):
        template = self.search([("id", "=", template_id)])[0]
        template._auto_close_subscription()

    @api.multi
    def _auto_close_subscription(self):
        self.ensure_one()
        obj_sale_subscription = self.env["sale.subscription"]
        criteria = [
            ("template_id", "=", self.id),
            ("state", "in", ["open"]),
            ("date", "=", fields.Date.today()),
        ]
        obj_sale_subscription.search(criteria).write(
            {
                "date_end": fields.Date.today(),
                "state": "close",
                "close_reason_id": self.close_reason_id
                and self.close_reason_id.id
                or False,
            }
        )
