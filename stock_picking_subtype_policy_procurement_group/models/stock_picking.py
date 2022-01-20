# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    show_create_procurement_group_on_picking_form = fields.Boolean(
        string="Show Create Procurement Group on Stock Picking Form",
        related="picking_type_id.subtype_id.show_create_procurement_group_on_picking_form",
        store=False,
    )

    @api.onchange(
        "picking_type_id",
    )
    def onchange_procure_method(self):
        result = False
        if self.picking_type_id and self.picking_type_id.subtype_id:
            result = self.picking_type_id.subtype_id.default_create_procurement_group
        self.create_procurement_group = result
