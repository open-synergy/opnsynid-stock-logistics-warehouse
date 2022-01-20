# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    manufacture_route_id = fields.Many2one(
        string="Manufacture Route",
        comodel_name="stock.location.route",
    )

    @api.model
    def _get_manufacture_pull_rule(self, warehouse):
        result = super(StockWarehouse, self)._get_manufacture_pull_rule(warehouse)
        obj_route = self.env["stock.location.route"]
        if warehouse.manufacture_route_id:
            result["route_id"] = warehouse.manufacture_route_id.id
        else:
            route = obj_route.create(warehouse._prepare_manufacture_route())
            result["route_id"] = route.id
            warehouse.manufacture_route_id = route.id

        return result

    @api.multi
    def _prepare_manufacture_route(self):
        self.ensure_one()
        return {
            "name": "%s: Manufacture" % self.name,
            "product_categ_selectable": True,
            "product_selectable": False,
            "sequence": 10,
        }
