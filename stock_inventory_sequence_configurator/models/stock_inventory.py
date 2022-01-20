# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockInventory(models.Model):
    _inherit = [
        "stock.inventory",
        "base.sequence_document",
    ]
    _name = "stock.inventory"

    @api.model
    def _default_name(self):
        return "/"

    name = fields.Char(
        default=lambda self: self._default_name(),
    )

    @api.model
    def create(self, values):
        _super = super(StockInventory, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write(
            {
                "name": sequence,
            }
        )
        return result
