# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class GenerateStockMoveAccountEntry(models.TransientModel):
    _name = "stock.generate_stock_move_account_entry"
    _description = "Generate Stock Move Accounting Entry"

    @api.multi
    def action_generate(self):
        self.ensure_one()
        record_ids = self.env.context['active_ids']
        obj_move = self.env["stock.move"]

        for move in obj_move.browse(record_ids):
            move.action_generate_account_entry()
