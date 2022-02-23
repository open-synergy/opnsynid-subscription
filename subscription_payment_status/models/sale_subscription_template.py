# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SaleSubscriptionTemplate(models.Model):
    _name = "sale.subscription.template"
    _inherit = "sale.subscription.template"

    payment_status_python_code = fields.Text(
        string="Python Code for Payment Status",
        required=True,
        default="result = False",
    )
    payment_status_cron_id = fields.Many2one(
        string="Payment Status Cron",
        comodel_name="ir.cron",
        readonly=True,
    )

    @api.multi
    def action_create_payment_status_cron(self):
        for document in self:
            document._create_payment_status_cron()

    @api.multi
    def action_delete_payment_status_cron(self):
        for document in self:
            document._delete_payment_status_cron()

    @api.multi
    def _create_payment_status_cron(self):
        self.ensure_one()
        data = self._prepare_payment_status_cron_data()
        obj_cron = self.env["ir.cron"]
        cron = obj_cron.create(data)
        self.write({"payment_status_cron_id": cron.id})

    @api.multi
    def _prepare_payment_status_cron_data(self):
        self.ensure_one()
        cron_name = "Compute Payment Status: %s" % (self.name)
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
            "code": "model.cron_compute_payment_status(%s)" % (self.id),
            "state": "code",
        }

    @api.multi
    def _delete_payment_status_cron(self):
        for document in self:
            document.payment_status_cron_id.unlink()

    @api.model
    def cron_compute_payment_status(self, template_id):
        template = self.search([("id", "=", template_id)])[0]
        template._compute_payment_status()

    @api.multi
    def _compute_payment_status(self):
        self.ensure_one()
        obj_sale_subscription = self.env["sale.subscription"]
        criteria = [("template_id", "=", self.id), ("state", "in", ["open"])]
        obj_sale_subscription.search(criteria)._compute_payment_status_id()
