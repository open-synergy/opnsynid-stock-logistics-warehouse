# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.onchange("picking_type_id")
    def onchange_create_procurement_group(self):
        ptype = self.picking_type_id
        self.create_procurement_group = False
        if ptype:
            self.create_procurement_group = ptype.create_procurement_group
