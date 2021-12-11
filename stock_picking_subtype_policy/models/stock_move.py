# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    show_location_on_move_form = fields.Boolean(
        string="Show Source Location on Stock Move Form",
        related="picking_type_id.subtype_id.show_location_on_move_form",
        store=False,
    )
    show_location_dest_on_move_form = fields.Boolean(
        string="Show Destination Location on Stock Move Form",
        related="picking_type_id.subtype_id.show_location_dest_on_move_form",
        store=False,
    )
    show_procure_method_on_move_form = fields.Boolean(
        string="Show Procure Method on Stock Move Form",
        related="picking_type_id.subtype_id.show_procure_method_on_move_form",
        store=False,
    )
    show_price_unit_on_move_form = fields.Boolean(
        string="Show Price Unit on Stock Move Form",
        related="picking_type_id.subtype_id.show_price_unit_on_move_form",
        store=False,
    )
