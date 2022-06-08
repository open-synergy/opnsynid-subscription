# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleSubscriptionCloseReasonWizard(models.TransientModel):
    _name = "sale.subscription.close.reason.wizard"
    _inherit = "sale.subscription.close.reason.wizard"

    date_end = fields.Date(
        string="Date End",
    )

    @api.model
    def _default_show_date_end(self):
        hide_date_end = self.env.context.get("cancel", False)
        if not hide_date_end:
            return True
        else:
            return False

    show_date_end = fields.Boolean(
        string="Show Date End",
        store=True,
        default=lambda self: self._default_show_date_end(),
    )

    @api.multi
    def set_close_cancel(self):
        self.ensure_one()
        subscriptions = self.env["sale.subscription"].browse(
            self.env.context.get("active_ids")
        )
        write_data = {
            "close_reason_id": self.close_reason_id.id,
        }
        if self.env.context.get("cancel"):
            subscriptions.set_cancel()
        else:
            subscriptions.set_close()
            date_end = fields.Date.today()
            if self.date_end:
                date_end = self.date_end
            write_data.update({"date_end": date_end})
        subscriptions.write(write_data)
