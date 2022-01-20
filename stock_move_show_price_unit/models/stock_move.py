# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("picking_type_id")
    @api.multi
    def _compute_show_price_unit(self):
        for move in self:
            move.show_price_unit = False
            if move.picking_type_id and move.picking_type_id.show_price_unit:
                move.show_price_unit = True

    show_price_unit = fields.Boolean(
        string="Show Price Unit",
        compute="_compute_show_price_unit",
        store=False,
    )
