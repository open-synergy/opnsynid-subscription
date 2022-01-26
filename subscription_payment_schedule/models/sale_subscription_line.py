# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.exceptions import UserError

from odoo import _, api, models


class SaleSubscriptionLine(models.Model):
    _name = "sale.subscription.line"
    _inherit = "sale.subscription.line"

    @api.multi
    def _get_account(self):
        self.ensure_one()
        subscription = self.analytic_account_id
        error_msg = _("No account defined")
        result = False
        asset_category = False

        if subscription.asset_category_id:
            if self.product_id.product_tmpl_id.deferred_revenue_category_id:
                asset_category = (
                    self.product_id.product_tmpl_id.deferred_revenue_category_id
                )

            if not asset_category:
                asset_category = subscription.asset_category_id

            result = asset_category.account_asset_id

        if not result:
            result = self.product_id.property_account_income_id

        if not result:
            result = self.product_id.categ_id.property_account_income_categ_id

        if not result:
            raise UserError(error_msg)

        return result

    @api.multi
    def _create_invoice_line(self, invoice):
        self.ensure_one()
        obj_account_invoice_line = self.env["account.invoice.line"]
        obj_account_invoice_line.create(self._prepare_invoice_line(invoice))

    @api.multi
    def _prepare_invoice_line(self, invoice):
        self.ensure_one()
        account = self._get_account()
        return {
            "invoice_id": invoice.id,
            "name": self.name,
            "account_id": account.id,
            "price_unit": self.price_unit,
            "product_id": self.product_id.id,
            "uom_id": self.uom_id.id,
            "quantity": self.quantity,
        }
