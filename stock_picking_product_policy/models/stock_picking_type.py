# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    @api.depends(
        "allowed_product_categ_ids",
        "allowed_product_ids",
    )
    def _compute_all_allowed_product_ids(self):
        obj_product = self.env["product.product"]
        for picking_type in self:
            products = picking_type.allowed_product_ids
            category_ids = picking_type.allowed_product_categ_ids.ids
            criteria = [
                ("categ_id", "in", category_ids),
            ]
            products += obj_product.search(criteria)
            picking_type.all_allowed_product_ids = products

    limit_product_selection = fields.Boolean(
        string="Limit Product Selection",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="product_category_stock_picking_type_rel",
        column1="stock_picking_type_id",
        column2="product_category_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Product",
        comodel_name="product.product",
        relation="rel_picking_type_2_product",
        column1="stock_picking_type_id",
        column2="product_product_id",
    )
    all_allowed_product_ids = fields.Many2many(
        string="All Allowed Product",
        comodel_name="product.product",
        compute="_compute_all_allowed_product_ids",
        store=True,
        relation="rel_picking_type_2_all_product",
        column1="stock_picking_type_id",
        column2="product_product_id",
    )
