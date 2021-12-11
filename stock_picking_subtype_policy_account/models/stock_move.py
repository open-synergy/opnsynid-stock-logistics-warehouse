# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    show_invoice_state_on_move_form = fields.Boolean(
        string="Show Invoice State on Stock Move Form",
        related="picking_type_id.subtype_id.show_invoice_state_on_move_form",
        store=False,
    )
