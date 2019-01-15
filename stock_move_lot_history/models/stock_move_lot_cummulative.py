# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class StockMoveLotCummulative(models.Model):
    _name = "stock.stock_move_lot_cummulative"
    _description = "Stock Move Lot Cummulative"
    _auto = False

    lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    move_id = fields.Many2one(
        string="Stock Move",
        comodel_name="stock.move",
    )
    date = fields.Date(
        string="Date",
    )
    product_qty = fields.Float(
        string="Quantity",
    )
    cummulative_qty = fields.Float(
        string="Past Quantity",
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            a.lot_id,
            a.product_id,
            a.move_id,
            a.date,
            a.product_qty,
            COALESCE(SUM(b.product_qty),0) As cummulative_qty
        """
        return select_str

    def _from(self):
        from_str = """
                stock_stock_move_lot_history AS a
        """
        return from_str

    def _group_by(self):
        group_str = """
        GROUP BY
            a.lot_id,
            a.product_id,
            a.date,
            a.move_id,
            a.product_qty
        """
        return group_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _order_by(self):
        order_by = """
        ORDER BY
            a.lot_id,
            a.product_id,
            a.date,
            a.move_id
        """
        return order_by

    def _join(self):
        join_str = """
        LEFT JOIN (
            SELECT
                b1.*
            FROM stock_stock_move_lot_history AS b1
        ) AS b ON
            a.lot_id = b.lot_id AND
            a.product_id = b.product_id AND
            a.date >= b.date
        """
        return join_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where(),
            self._group_by(),
            self._order_by(),
        ))
