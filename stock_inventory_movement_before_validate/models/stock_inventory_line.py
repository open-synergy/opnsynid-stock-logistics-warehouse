# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockInventoryLine(models.Model):
    _name = "stock.inventory.line"
    _inherit = "stock.inventory.line"

    @api.multi
    @api.depends(
        "qty_diff_method",
        "manual_qty",
        "qty_recompute",
    )
    def _compute_product_qty(self):
        for document in self:
            if document.qty_diff_method == "manual":
                result = document.manual_qty
            else:
                result = document.qty_recompute
            document.product_qty = result

    @api.multi
    @api.depends(
        "product_qty",
        "manual_qty",
    )
    def _compute_diff_product_qty(self):
        for document in self:
            document.diff_product_qty = document.product_qty - \
                document.manual_qty

    qty_diff_in = fields.Float(
        string="Incoming Quantity Diff",
        readonly=True,
    )
    qty_diff_out = fields.Float(
        string="Outgoing Quantity Diff",
        readonly=True,
    )
    qty_recompute = fields.Float(
        string="Recomputed Theoretical Qty",
        readonly=True,
    )
    initial_theoretical_qty = fields.Float(
        string="Initial Theoretical Quantity",
        readonly=True,
    )
    manual_qty = fields.Float(
        string="Manual Real Quantity"
    )
    diff_product_qty = fields.Float(
        string="Diff Real Quantity",
        compute="_compute_diff_product_qty",
        store=True,
    )
    qty_diff_method = fields.Selection(
        string="Use Quantity From",
        selection=[
            ("manual", "Manual Real Quantity"),
            ("recompute", "Recomputed Theorecical Quantity"),
        ],
        required=True,
        default="manual",
    )
    product_qty = fields.Float(
        compute="_compute_product_qty",
        store=True,
    )

    @api.multi
    def _recompute_theoretical(self):
        self.ensure_one()
        obj_ml = self.env["stock.move.line"]
        qty_incoming = qty_outgoing = qty_recompute = 0.0
        criteria = [
            ("state", "=", "done"),
            ("product_id", "=", self.product_id.id),
            ("lot_id", "=", self.prod_lot_id and self.prod_lot_id.id or False),
            ("owner_id", "=", self.partner_id and self.partner_id.id or False),
            ("date", ">=", self.inventory_id.date),
            ("date", "<=", fields.Datetime.now()),
            "|",
            ("location_id", "=", self.location_id.id),
            ("location_dest_id", "=", self.location_id.id),
        ]
        for ml in obj_ml.search(criteria):
            if ml.location_id.id == self.location_id.id:
                qty_outgoing += ml.qty_done

            if ml.location_dest_id.id == self.location_id.id:
                qty_incoming += ml.qty_done

        qty_recompute = self.initial_theoretical_qty + \
            qty_incoming - qty_outgoing

        self.write({
            "qty_diff_in": qty_incoming,
            "qty_diff_out": qty_outgoing,
            "qty_recompute": qty_recompute,
            "theoretical_qty": qty_recompute,
        })
