# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def get_domain(self):
        domain = [("type", "!=", "service")]
        context = self._context
        picking_type_id = context.get("default_picking_type_id", False)

        if picking_type_id:
            obj_picking_type = self.env["stock.picking.type"]
            criteria = [
                ("id", "=", picking_type_id)
            ]
            picking_type = obj_picking_type.search(criteria)

            if picking_type:
                if picking_type.limit_product_selection:
                    product_ids = []
                    product_categ_ids = []
                    if picking_type.allowed_product_ids:
                        product_ids = \
                            picking_type.allowed_product_ids.ids
                    if picking_type.allowed_product_categ_ids:
                        product_categ_ids = \
                            picking_type.allowed_product_categ_ids.ids
                    if product_ids and product_categ_ids:
                        domain = [
                            "|",
                            ("id", "in", product_ids),
                            ("categ_id", "in", product_categ_ids),
                        ]
                    elif product_ids and not product_categ_ids:
                        domain = [
                            ("id", "in", product_ids),
                        ]
                    elif not product_ids and product_categ_ids:
                        domain = [
                            ("categ_id", "in", product_categ_ids),
                        ]
                    else:
                        domain = domain
        return domain

    product_id = fields.Many2one(
        domain=lambda self: self.get_domain(),
    )
