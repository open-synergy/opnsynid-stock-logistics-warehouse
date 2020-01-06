# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockInventory(models.Model):
    _name = "stock.inventory"
    _inherit = "stock.inventory"

    qty_diff_method = fields.Selection(
        string="Use Quantity From",
        selection=[
            ("manual", "Manual Real Quantity"),
            ("recompute", "Recomputed Theorecical Quantity"),
        ],
        required=True,
        default="manual",
    )

    @api.multi
    def action_recompute_theoretical(self):
        for document in self:
            document._recompute_theoretical()

    @api.multi
    def _recompute_theoretical(self):
        self.ensure_one()
        for line in self.line_ids:
            line._recompute_theoretical()

    @api.multi
    def _get_inventory_lines_values(self):
        self.ensure_one()
        _super = super(StockInventory, self)
        vals = _super._get_inventory_lines_values()
        for item in vals:
            manual_qty = item.get("theoretical_qty", 0.0)
            item["manual_qty"] = manual_qty
            item["qty_diff_method"] = self.qty_diff_method
        return vals

    @api.multi
    def action_reset_product_qty(self):
        _super = super(StockInventory, self)
        _super.action_reset_product_qty()
        self.mapped('line_ids').write({'manual_qty': 0})
        return True

    @api.multi
    def action_done(self):
        _super = super(StockInventory, self)
        self.action_recompute_theoretical()
        _super.action_done()
