# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockInventoryProductSet(models.Model):
    _name = "stock.inventory_product_set"
    _description = "Stock Inventory Product Set"

    name = fields.Char(
        string="Product Set",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    product_ids = fields.Many2many(
        string="Products",
        comodel_name="product.product",
        relation="rel_stock_inventory_product_set_2_product",
        column1="product_set_id",
        column2="product_id",
    )

    product_categ_ids = fields.Many2many(
        string="Product Categories",
        comodel_name="product.category",
        relation="rel_stock_inventory_product_set_2_product_categ",
        column1="product_set_id",
        column2="categ_id",
    )
