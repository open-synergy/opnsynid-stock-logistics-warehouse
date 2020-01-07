# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def post_init_hook(cr, pool):
    sql1 = """
    UPDATE  stock_inventory_line AS target
    SET
            manual_qty =  a.product_qty,
            initial_theoretical_qty = a.theoretical_qty
    FROM    stock_inventory_line AS a
    WHERE   target.id = a.id
    """
    cr.execute(sql1)
