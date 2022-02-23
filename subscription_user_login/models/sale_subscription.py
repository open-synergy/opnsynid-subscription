# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = "sale.subscription"

    login_ids = fields.One2many(
        string="Logins",
        comodel_name="sale.subscription.login",
        inverse_name="subscription_id",
    )
