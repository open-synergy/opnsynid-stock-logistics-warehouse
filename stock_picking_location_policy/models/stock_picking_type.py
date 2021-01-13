# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    allowed_location_ids = fields.Many2many(
        string="Allowed Source Location",
        comodel_name="stock.location",
        relation="picking_type_location_rel",
        column1="picking_type_id",
        column2="location_id")

    allowed_dest_location_ids = fields.Many2many(
        string="Allowed Destination Location",
        comodel_name="stock.location",
        relation="picking_type_dest_location_rel",
        column1="picking_type_id",
        column2="location_id")
