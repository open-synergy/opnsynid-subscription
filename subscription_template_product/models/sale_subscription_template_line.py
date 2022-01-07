# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

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

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_allowed_uom_ids(self):
        obj_uom = self.env["product.uom"]
        for document in self:
            result = []
            if document.product_id:
                categ = document.product_id.uom_id.category_id
                criteria = [
                    ("category_id", "=", categ.id),
                ]
                result = obj_uom.search(criteria).ids
            document.allowed_uom_ids = result

    allowed_uom_ids = fields.Many2many(
        string="Allowed UoM",
        comodel_name="product.uom",
        compute="_compute_allowed_uom_ids",
        store=False,
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

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id:
            self.uom_id = self.product_id.uom_id

    @api.onchange(
        "product_id",
    )
    def onchange_name(self):
        self.name = False
        if self.product_id:
            self.name = self.product_id.name
