# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    allowed_location_ids = fields.Many2many(
        string="Allowed Source Location",
        comodel_name="stock.location",
        related="picking_type_id.allowed_location_ids",
        store=False,
    )

    allowed_dest_location_ids = fields.Many2many(
        string="Allowed Destination Location",
        comodel_name="stock.location",
        related="picking_type_id.allowed_dest_location_ids",
        store=False,
    )
