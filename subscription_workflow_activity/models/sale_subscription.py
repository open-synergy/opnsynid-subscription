# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = [
        "sale.subscription",
    ]
    confirm_activity_ids = fields.Many2many(
        string="Confirm Activities",
        comodel_name="mail.activity",
        relation="rel_subscription_2_confirm_activity",
        column1="subscription_id",
        column2="activity_id",
    )
    approve_activity_ids = fields.Many2many(
        string="Approve Activities",
        comodel_name="mail.activity",
        relation="rel_subscription_2_approve_activity",
        column1="subscription_id",
        column2="activity_id",
    )
    close_activity_ids = fields.Many2many(
        string="Close Activities",
        comodel_name="mail.activity",
        relation="rel_subscription_2_close_activity",
        column1="subscription_id",
        column2="activity_id",
    )

    @api.multi
    def _create_confirm_activity(self):
        self.ensure_one()
        obj_activity = self.env["mail.activity"]
        activity = obj_activity.create(self._prepare_confirm_activity())
        self.write({"confirm_activity_ids": [(6, 0, [activity.id])]})

    @api.multi
    def _prepare_confirm_activity(self):
        self.ensure_one()
        return {
            "res_id": self.id,
            "res_model_id": self.env.ref(
                "sale_subscription.model_sale_subscription"
            ).id,
            "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
            "summary": _("Confirm subscription"),
            "user_id": self.user_id.id,
        }

    @api.multi
    def _create_close_activity(self):
        self.ensure_one()
        obj_activity = self.env["mail.activity"]
        activity = obj_activity.create(self._prepare_close_activity())
        self.write({"close_activity_ids": [(6, 0, [activity.id])]})

    @api.multi
    def _create_approve_activity(self):
        self.ensure_one()
        obj_activity = self.env["mail.activity"]
        activity_ids = []
        self._cancel_approve_activity()
        for user in self.active_approver_user_ids:
            activity = obj_activity.create(self._prepare_approve_activity(user))
            activity_ids.append(activity.id)
        self.write({"approve_activity_ids": [(6, 0, activity_ids)]})

    @api.multi
    def _prepare_approve_activity(self, user):
        self.ensure_one()
        return {
            "res_id": self.id,
            "res_model_id": self.env.ref(
                "sale_subscription.model_sale_subscription"
            ).id,
            "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
            "summary": _("Approve subscription"),
            "user_id": user.id,
        }

    @api.multi
    def _prepare_close_activity(self):
        self.ensure_one()
        return {
            "res_id": self.id,
            "res_model_id": self.env.ref(
                "sale_subscription.model_sale_subscription"
            ).id,
            "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
            "summary": _("Close subscription"),
            "user_id": self.user_id.id,
            "date_deadline": self.date,
        }

    @api.model
    def create(self, values):
        _super = super(SaleSubscription, self)
        result = _super.create(values)
        result._create_confirm_activity()
        return result

    @api.multi
    def action_confirm(self):
        _super = super(SaleSubscription, self)
        _super.action_confirm()
        for record in self:
            record._create_approve_activity()

    @api.multi
    def action_restart(self):
        _super = super(SaleSubscription, self)
        _super.action_restart()
        for record in self:
            record._create_confirm_activity()

    @api.multi
    def set_open(self):
        _super = super(SaleSubscription, self)
        _super.set_open()
        for record in self:
            record._cancel_approve_activity()
            record._create_close_activity()

    @api.multi
    def set_cancel(self):
        _super = super(SaleSubscription, self)
        _super.set_cancel()
        for record in self:
            record._cancel_confirm_activity()
            record._cancel_close_activity()
            record._cancel_approve_activity()

    @api.multi
    def set_close(self):
        _super = super(SaleSubscription, self)
        _super.set_close()
        for record in self:
            record._cancel_close_activity()

    @api.multi
    def action_reject_approval(self):
        _super = super(SaleSubscription, self)
        _super.action_reject_approval()
        for record in self:
            record._cancel_approve_activity()

    @api.multi
    def set_active(self, approver):
        _super = super(SaleSubscription, self)
        _super.set_active(approver)
        for record in self:
            record._cancel_confirm_activity()
            record._create_approve_activity()

    @api.multi
    def _cancel_confirm_activity(self):
        self.ensure_one()
        if self.confirm_activity_ids:
            self.confirm_activity_ids.action_done()

    @api.multi
    def _cancel_close_activity(self):
        self.ensure_one()
        if self.close_activity_ids:
            self.close_activity_ids.action_done()

    @api.multi
    def _cancel_approve_activity(self):
        self.ensure_one()
        if self.approve_activity_ids:
            self.approve_activity_ids.action_done()
