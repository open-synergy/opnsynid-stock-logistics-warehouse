# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.addons.stock_inventory_revaluation.models.\
    stock_inventory_revaluation import StockInventoryRevaluation


@api.multi
def post(self):
    for revaluation in self:
        if revaluation.product_template_id.cost_method == "real":
            for reval_quant in revaluation.reval_quant_ids:
                reval_quant.write_new_cost()
        else:
            # revaluation._check_negative()
            revaluation._check_qty_available()
            revaluation._update_price()

        if revaluation.product_template_id.valuation == "real_time":
            revaluation._generate_accounting_entry()

        revaluation.write(revaluation._prepare_post_data())


class StockInventoryRevaluationMonkeypatch(models.TransientModel):
    _name = "stock.inventory.revaluation.monkeypatch"
    _description = "Inventory Revaluation Monkeypatch"

    def _register_hook(self, cr):
        StockInventoryRevaluation.post = post
        _super = super(StockInventoryRevaluationMonkeypatch, self)
        return _super._register_hook(cr)
