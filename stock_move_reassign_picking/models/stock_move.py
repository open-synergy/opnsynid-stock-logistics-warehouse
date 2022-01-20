# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def action_reassign_picking(self):
        for move in self:
            move._picking_assign(
                move.group_id.id, move.location_id.id, move.location_dest_id.id
            )
