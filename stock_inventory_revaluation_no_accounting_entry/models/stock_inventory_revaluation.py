# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockInventoryRevaluation(models.Model):
    _inherit = "stock.inventory.revaluation"

    no_accounting_entry = fields.Boolean(
        string="Do not Create Accounting Entry",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _check_generate_accounting_entry(self):
        self.ensure_one()
        _super = super(StockInventoryRevaluation, self)
        result = _super._check_generate_accounting_entry()
        if self.no_accounting_entry:
            result = False
        return result
