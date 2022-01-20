# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingSubtype(models.Model):
    _name = "stock.picking_subtype"
    _inherit = "stock.picking_subtype"

    show_consignee_on_picking_form = fields.Boolean(
        string="Show Consignee on Stock Picking Form",
        default=True,
    )
    show_delivery_address_on_picking_form = fields.Boolean(
        string="Show Delivery Address on Stock Picking Form",
        default=True,
    )
    show_origin_address_on_picking_form = fields.Boolean(
        string="Show Origin Address on Stock Picking Form",
        default=True,
    )
