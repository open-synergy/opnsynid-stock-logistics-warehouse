# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp.tools import drop_view_if_exists


class StockMoveLotOut(models.Model):
    _name = "stock.stock_move_lot_out"
    _description = "Stock Move Lot Out"
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
    product_cost = fields.Float(
        string="Cost",
    )
    product_uom_id = fields.Many2one(
        string="Product UoM",
        comodel_name="product.uom",
    )

    def init(self, cr):
        drop_view_if_exists(cr, "stock_stock_move_lot_out")
        strSQL = """
                    CREATE OR REPLACE VIEW stock_stock_move_lot_out AS (
                        SELECT
                                row_number() OVER() as id,
                                a.id AS move_id,
                                a.date AS date,
                                a.name AS name,
                                a.company_id AS company_id,
                                a.product_id AS product_id,
                                e.lot_id AS lot_id,
                                a.location_dest_id AS location_id,
                                a.picking_id AS picking_id,
                                a.picking_type_id AS picking_type_id,
                                d.uom_id AS product_uom_id,
                                (-1.0 * e.quantity) AS product_qty,
                                e.cost AS cost
                        FROM    stock_move AS a
                        LEFT JOIN   stock_picking AS b ON a.picking_id = b.id
                        JOIN product_product AS c ON a.product_id = c.id
                        JOIN product_template AS d ON c.product_tmpl_id = d.id
                        JOIN stock_move_lot_info AS e ON a.id = e.move_id
                        JOIN stock_location AS f ON a.location_id = f.id
                        JOIN stock_location AS g ON a.location_dest_id = g.id
                        JOIN stock_production_lot AS h ON e.lot_id = h.id
                        WHERE   a.state = 'done' AND
                                g.usage <> 'internal' AND
                                f.usage = 'internal'
                    )
                    """
        cr.execute(strSQL)
