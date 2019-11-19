# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "picking_type_id",
    )
    def _compute_allowed_product(self):
        obj_product = self.env["product.product"]
        for document in self:
            if document.picking_type_id.limit_product_selection:
                document.allowed_product_ids = \
                    document.picking_type_id.allowed_product_ids.ids
                document.allowed_product_categ_ids = \
                    document.picking_type_id.allowed_product_categ_ids.ids
            else:
                document.allowed_product_ids = \
                    obj_product.search([("type", "!=", "service")])

    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        compute="_compute_allowed_product",
        store=False,
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        compute="_compute_allowed_product",
        store=False,
    )
