# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    show_consignee_on_picking_form = fields.Boolean(
        string="Show Consignee on Stock Picking Form",
        related="picking_type_id.subtype_id.show_consignee_on_picking_form",
        store=False,
    )
    show_delivery_address_on_picking_form = fields.Boolean(
        string="Show Delivery Address on Stock Picking Form",
        related="picking_type_id.subtype_id.show_delivery_address_on_picking_form",
        store=False,
    )
    show_origin_address_on_picking_form = fields.Boolean(
        string="Show Origin Address on Stock Picking Form",
        related="picking_type_id.subtype_id.show_origin_address_on_picking_form",
        store=False,
    )
