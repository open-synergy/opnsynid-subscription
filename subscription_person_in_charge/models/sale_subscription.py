# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class SaleSubscription(models.Model):
    _name = "sale.subscription"
    _inherit = "sale.subscription"

    @api.depends(
        "partner_id",
    )
    def _compute_allowed_pic_ids(self):
        obj_partner = self.env["res.partner"]
        for record in self:
            result = []
            if record.partner_id:
                criteria = [
                    (
                        "commercial_partner_id",
                        "=",
                        record.partner_id.commercial_partner_id.id,
                    ),
                    ("is_company", "=", False),
                ]
                result = obj_partner.search(criteria).ids
            record.allowed_pic_ids = result

    allowed_pic_ids = fields.Many2many(
        string="Allowed Invoice To",
        comodel_name="res.partner",
        compute="_compute_allowed_pic_ids",
    )

    pic_id = fields.Many2one(
        string="Person in Charge",
        comodel_name="res.partner",
    )
    finance_pic_id = fields.Many2one(
        string="Finance PIC",
        comodel_name="res.partner",
    )
    tax_pic_id = fields.Many2one(
        string="Tax PIC",
        comodel_name="res.partner",
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_pic_id(self):
        self.pic_id = False
