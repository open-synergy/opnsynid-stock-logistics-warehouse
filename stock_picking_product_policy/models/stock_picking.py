# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends(
        "picking_type_id",
        "picking_type_id.all_allowed_product_ids")
    def _compute_all_allowed_product_ids(self):
        obj_product = self.env["product.product"]
        for picking in self:
            if picking.picking_type_id.limit_product_selection:
                picking.all_allowed_product_ids = \
                    picking.picking_type_id.all_allowed_product_ids
            else:
                criteria = [
                    ("type", "!=", "service"),
                ]
                picking.all_allowed_product_ids = \
                    obj_product.search(criteria)

    all_allowed_product_ids = fields.Many2many(
        string="All Allowed Product",
        comodel_name="product.product",
        compute="_compute_all_allowed_product_ids",
        store=False,
    )
