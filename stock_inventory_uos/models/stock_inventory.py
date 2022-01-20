# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    @api.depends(
        "product_id",
        "product_uom_id",
        "product_qty",
        "theoretical_qty",
    )
    @api.multi
    def _compute_uos(self):
        for line in self:
            line.product_uos_qty = line.product_uos_theoretical_qty = 0.0
            line_uom = line.product_uom_id
            product_uom = line.product_id.uom_id
            product_qty = self.env["product.uom"]._compute_qty(
                line_uom.id, line.product_qty, product_uom.id
            )
            product_theoretical_qty = self.env["product.uom"]._compute_qty(
                line_uom.id, line.theoretical_qty, product_uom.id
            )
            if line.product_id.uos_id:
                line.product_uos_id = line.product_id.uos_id.id
                line.product_uos_qty = product_qty * line.product_id.uos_coeff
                line.product_uos_theoretical_qty = (
                    product_theoretical_qty * line.product_id.uos_coeff
                )

    product_uos_id = fields.Many2one(
        string="UoS",
        comodel_name="product.uom",
        store=True,
        compute="_compute_uos",
    )
    product_uos_qty = fields.Float(
        string="UoS Qty.",
        store=True,
        compute="_compute_uos",
    )
    product_uos_theoretical_qty = fields.Float(
        string="UoS Theoretical Qty.",
        store=True,
        compute="_compute_uos",
    )

    @api.model
    def _resolve_inventory_line(self, inventory_line):
        move_id = super(StockInventoryLine, self)._resolve_inventory_line(
            inventory_line
        )
        if inventory_line.product_uos_id:
            move = self.env["stock.move"].browse([move_id])[0]
            move.write(
                {
                    "product_uos": inventory_line.product_uos_id.id,
                    "product_uos_qty": inventory_line.product_uos_qty,
                }
            )
        return move_id
