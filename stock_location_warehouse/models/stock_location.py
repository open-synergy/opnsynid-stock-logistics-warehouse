# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockLocation(models.Model):
    _inherit = "stock.location"

    @api.multi
    @api.depends(
        "parent_left",
    )
    def _compute_warehouse_id(self):
        obj_stock_warehouse =\
            self.env["stock.warehouse"]
        for document in self:
            document.warehouse_id = False
            criteria = [
                ("view_location_id.parent_left", "<=", document.parent_left),
                ("view_location_id.parent_right", ">=", document.parent_left),
            ]
            warehouse_id =\
                obj_stock_warehouse.search(criteria)
            if warehouse_id:
                document.warehouse_id = warehouse_id.id

    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        compute="_compute_warehouse_id"
    )
