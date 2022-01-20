# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    manager_id = fields.Many2one(
        string="Manager",
        comodel_name="res.users",
    )
