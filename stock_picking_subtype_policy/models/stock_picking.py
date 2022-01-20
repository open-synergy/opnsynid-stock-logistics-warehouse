# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    show_partner_on_picking_form = fields.Boolean(
        string="Show Partner on Form",
        related="picking_type_id.subtype_id.show_partner_on_picking_form",
        store=False,
    )
    show_min_date_on_picking_form = fields.Boolean(
        string="Show Scheduled Date on Stock Picking Form",
        related="picking_type_id.subtype_id.show_min_date_on_picking_form",
        store=False,
    )
    show_max_date_on_picking_form = fields.Boolean(
        string="Show Max. Expected Date on Stock Picking Form",
        related="picking_type_id.subtype_id.show_max_date_on_picking_form",
        store=False,
    )
    show_date_done_on_picking_form = fields.Boolean(
        string="Show Date Done on Stock Picking Form",
        related="picking_type_id.subtype_id.show_date_done_on_picking_form",
        store=False,
    )
    show_move_type_on_picking_form = fields.Boolean(
        string="Show Delivery Method on Stock Picking Form",
        related="picking_type_id.subtype_id.show_move_type_on_picking_form",
        store=False,
    )

    @api.onchange(
        "picking_type_id",
    )
    def onchange_move_type(self):
        result = False
        if self.picking_type_id and self.picking_type_id.subtype_id:
            result = self.picking_type_id.subtype_id.default_move_type
        self.move_type = result
