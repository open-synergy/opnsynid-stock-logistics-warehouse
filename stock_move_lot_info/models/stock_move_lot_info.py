# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, tools


class StockMoveLotInfo(models.Model):
    _name = "stock.move_lot_info"
    _description = "Move's Lot Information"
    _auto = False

    move_id = fields.Many2one(
        string="Stock Move",
        comodel_name="stock.move",
    )
    lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
    )
    quantity = fields.Float(
        string="Qty."
    )
    cost = fields.Float(
        string="Lot Value",
    )

    def _select(self):
        select_str = """
             SELECT row_number() OVER() as id,
                    a.id AS move_id,
                    b.lot_id AS lot_id,
                    b.quantity AS quantity,
                    b.cost AS cost
        """
        return select_str

    def _from(self):
        from_str = """
                stock_move AS a
        """
        return from_str

    def _where(self):
        where_str = """
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN (
            SELECT  b1.id AS move_id,
                    b3.lot_id AS lot_id,
                    SUM(b3.qty) AS quantity,
                    SUM(b3.qty * b3.cost) AS cost
            FROM stock_move AS b1
            JOIN stock_quant_move_rel AS b2 ON b1.id = b2.move_id
            JOIN stock_quant AS b3 ON b2.quant_id = b3.id
            GROUP BY    b1.id,
                        b3.lot_id
        ) AS b ON a.id = b.move_id
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
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where()
        ))
