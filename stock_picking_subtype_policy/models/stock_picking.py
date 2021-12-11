# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


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
