# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    interwarehouse_in_type_id = fields.Many2one(
        string="Inter-Warehouse In Type",
        comodel_name="stock.picking.type"
    )
    interwarehouse_out_type_id = fields.Many2one(
        string="Inter-Warehouse Out Type",
        comodel_name="stock.picking.type"
    )
    transit_pull_loc_id = fields.Many2one(
        string="Transit Pull Location",
        comodel_name="stock.location"
    )
    transit_push_loc_id = fields.Many2one(
        string="Transit Push Location",
        comodel_name="stock.location"
    )
    inter_warehouse_pull_route_id = fields.Many2one(
        string="Inter-Warehouse Pull Route",
        comodel_name="stock.location.route"
    )
    inter_warehouse_push_route_id = fields.Many2one(
        string="Inter-Warehouse Push Route",
        comodel_name="stock.location.route"
    )
