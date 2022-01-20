# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingSubtype(models.Model):
    _name = "stock.picking_subtype"
    _inherit = "stock.picking_subtype"

    show_invoice_state_on_move_form = fields.Boolean(
        string="Show Invoice State on Stock Move Form",
        default=True,
    )
