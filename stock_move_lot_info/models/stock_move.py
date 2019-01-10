# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    lot_info_ids = fields.One2many(
        string="Lot Info",
        comodel_name="stock.move_lot_info",
        inverse_name="move_id",
    )
