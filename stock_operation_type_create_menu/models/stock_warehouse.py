# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    menu_id = fields.Many2one(
        string="Menu",
        comodel_name="ir.ui.menu",
        readonly=True
    )
