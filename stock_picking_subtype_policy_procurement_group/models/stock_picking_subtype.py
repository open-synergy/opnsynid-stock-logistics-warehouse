# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingSubtype(models.Model):
    _name = "stock.picking_subtype"
    _inherit = "stock.picking_subtype"

    default_create_procurement_group = fields.Boolean(
        string="Default Create Procurement Group",
        default=False,
    )
    show_create_procurement_group_on_picking_form = fields.Boolean(
        string="Show Create Procurement Group on Stock Picking Form",
        default=True,
    )
