# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    show_procure_method = fields.Boolean(
        string="Show Procure Method",
        default=True,
    )
    default_procure_method = fields.Selection(
        string="Default Procure Method",
        selection=[
            ("make_to_stock", "Default: Take From Stock"),
            ("make_to_order", "Advanced: Apply Procurement Rules"),
        ],
        default="make_to_stock",
        required=True,
    )
