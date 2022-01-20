# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"
    _name = "stock.location"

    stock_inventory_sequence_id = fields.Many2one(
        string="Sequence for Stock Inventory",
        comodel_name="ir.sequence",
    )
