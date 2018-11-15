# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.model
    def _get_locations_open_inventories(self):
        _super = super(StockInventory, self)
        result = _super._get_locations_open_inventories()
        if len(result) == 0:
            result = self.env["stock.location"]
        inventories = self.search([
            ("state", "=", "pending"),
        ])
        if not inventories:
            # Early exit if no match found
            return result
        location_ids = inventories.mapped("location_id")

        # Extend to the children Locations
        return self.env["stock.location"].search(
            [("location_id", "child_of", location_ids.ids),
             ("usage", "in", ["internal", "transit"])]) + result
