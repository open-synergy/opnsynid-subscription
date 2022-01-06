# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

from odoo.addons import decimal_precision as dp


class SaleSubscriptionTemplateLine(models.Model):
    _name = "sale.subscription.template_line"

    template_id = fields.Many2one(
        string="# Template",
        comodel_name="sale.subscription.template",
        required=True,
    )
    name = fields.Text(
        string="Description",
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        domain="[('recurring_invoice', '=',True)]",
        required=True,
    )
    quantity = fields.Float(
        string="Quantity",
        help="Quantity that will be invoiced.",
        default=1.0,
    )
    uom_id = fields.Many2one(
        string="Unit of Measure",
        comodel_name="product.uom",
        required=True,
    )
    price_unit = fields.Float(
        string="Unit Price",
        required=True,
        digits=dp.get_precision("Product Price"),
    )
    discount = fields.Float(
        string="Discount (%)",
        digits=dp.get_precision("Discount"),
    )
