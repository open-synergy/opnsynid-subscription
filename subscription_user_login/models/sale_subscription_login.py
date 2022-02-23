# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class SaleSubscriptionLogin(models.Model):
    _name = "sale.subscription.login"
    _description = "Sale Subscription Login"

    subscription_id = fields.Many2one(
        string="Subscription",
        comodel_name="sale.subscription",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(
        string="Name",
        required=True,
    )
    login = fields.Char(
        string="Login",
        required=True,
    )
