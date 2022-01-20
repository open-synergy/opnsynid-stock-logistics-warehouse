# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("picking_type_id")
    @api.multi
    def _compute_show_procure_method(self):
        for move in self:
            move.show_procure_method = False
            if move.picking_type_id and move.picking_type_id.show_procure_method:
                move.show_procure_method = True

    show_procure_method = fields.Boolean(
        string="Show Procure Method",
        compute="_compute_show_procure_method",
        store=False,
    )

    @api.onchange("picking_type_id")
    def onchange_procure_method(self):
        self.procure_method = "make_to_stock"
        if self.picking_type_id:
            self.procure_method = self.picking_type_id.default_procure_method
