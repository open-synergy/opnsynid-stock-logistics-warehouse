# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp.tools import drop_view_if_exists


class StockMoveLotHistory(models.Model):
    _name = "stock.stock_move_lot_history"
    _description = "Stock Move Lot History"
    _auto = False

    name = fields.Char(
        string="Description",
    )
    move_id = fields.Many2one(
        string="Move",
        comodel_name="stock.move",
    )
    date = fields.Datetime(
        string="Date",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
    )
    lot_id = fields.Many2one(
        string="Serial Number",
        comodel_name="stock.production.lot",
    )
    picking_id = fields.Many2one(
        string="Picking",
        comodel_name="stock.picking",
    )
    picking_type_id = fields.Many2one(
        string="Picking Type",
        comodel_name="stock.picking.type",
    )
    product_qty = fields.Float(
        string="Product Qty",
    )
    product_uom_id = fields.Many2one(
        string="Product UoM",
        comodel_name="product.uom",
    )

    def init(self, cr):
        drop_view_if_exists(cr, "stock_stock_move_lot_history")
        strSQL = """
                    CREATE OR REPLACE VIEW stock_stock_move_lot_history AS (
                        SELECT
                                row_number() OVER() as id,
                                c.*
                        FROM
                        (
                        SELECT
                                a.move_id,
                                a.date,
                                a.name,
                                a.company_id,
                                a.product_id,
                                a.lot_id,
                                a.location_id,
                                a.picking_id,
                                a.picking_type_id,
                                a.product_qty,
                                a.product_uom_id
                        FROM    stock_stock_move_lot_in AS a
                        UNION
                        SELECT
                                b.move_id,
                                b.date,
                                b.name,
                                b.company_id,
                                b.product_id,
                                b.lot_id,
                                b.location_id,
                                b.picking_id,
                                b.picking_type_id,
                                b.product_qty,
                                b.product_uom_id
                        FROM    stock_stock_move_lot_out AS b
                        ) AS c
                    )
                    """
        cr.execute(strSQL)
