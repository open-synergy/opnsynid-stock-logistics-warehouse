# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingSubtype(models.Model):
    _name = "stock.picking_subtype"
    _inherit = "stock.picking_subtype"

    # stock.picking visibility
    show_partner_on_picking_form = fields.Boolean(
        string="Show Partner on Stock Picking Form",
        default=True,
    )
    show_min_date_on_picking_form = fields.Boolean(
        string="Show Scheduled Date on Stock Picking Form",
        default=True,
    )
    show_max_date_on_picking_form = fields.Boolean(
        string="Show Max. Expected Date on Stock Picking Form",
        default=True,
    )
    show_date_done_on_picking_form = fields.Boolean(
        string="Show Date Done on Stock Picking Form",
        default=True,
    )
    show_move_type_on_picking_form = fields.Boolean(
        string="Show Delivery Method on Stock Picking Form",
        default=True,
    )

    # stock.picking default
    default_move_type = fields.Selection(
        string="Default Delivery Method",
        selection=[
            ("direct", "Partial"),
            ("one", "All at once"),
        ],
        default="direct",
        required=True,
    )

    # stock.move visibility
    show_procure_method_on_move_form = fields.Boolean(
        string="Show Procure Method on Stock Move Form",
        default=True,
    )
    show_location_on_move_form = fields.Boolean(
        string="Show Source Location on Stock Move Form",
        default=True,
    )
    show_location_dest_on_move_form = fields.Boolean(
        string="Show Destination Location on Stock Move Form",
        default=True,
    )
    show_price_unit_on_move_form = fields.Boolean(
        string="Show Price Unit on Stock Move Form",
        default=True,
    )

    # stock.picking default
    default_procure_method = fields.Selection(
        string="Default Procure Method",
        selection=[
            ("make_to_stock", "Default: Take From Stock"),
            ("make_to_order", "Advance: Apply Procurement Rules"),
        ],
        default="make_to_stock",
        required=True,
    )
