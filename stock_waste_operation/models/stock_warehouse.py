# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    waste_type_id = fields.Many2one(
        string="Waste Type", comodel_name="stock.picking.type"
    )
    waste_loc_id = fields.Many2one(
        string="Waste Location", comodel_name="stock.location"
    )

    @api.multi
    def _prepare_waste_location(self):
        self.ensure_one()
        parent_location = self.view_location_id
        data = {
            "name": _("Waste"),
            "location_id": parent_location.id,
            "usage": "inventory",
            "active": True,
        }
        return data

    @api.multi
    def _prepare_waste_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Waste",
            "prefix": self.code + "/WST/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_waste_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        location = self.lot_stock_id
        waste_loc = self._get_waste_location()

        sequence = obj_sequence.create(self._prepare_waste_sequence())

        data = {
            "name": _("Waste"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": location.id,
            "allowed_location_ids": [(6, 0, [location.id])],
            "default_location_dest_id": waste_loc.id,
            "allowed_dest_location_ids": [(6, 0, [waste_loc.id])],
        }
        return data

    @api.multi
    def _get_waste_location(self):
        self.ensure_one()
        if not self.waste_loc_id:
            raise UserError(_("No waste location"))
        return self.waste_loc_id

    @api.multi
    def _create_waste_loc(self):
        self.ensure_one()
        obj_loc = self.env["stock.location"]
        waste_loc = obj_loc.create(self._prepare_waste_location())
        return waste_loc

    @api.multi
    def _create_waste_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        waste_type = obj_type.create(self._prepare_waste_type())
        return waste_type

    @api.multi
    def button_create_waste_loc(self):
        for wh in self:
            waste_loc = wh._create_waste_loc()
            self.waste_loc_id = waste_loc.id

    @api.multi
    def button_create_waste_type(self):
        for wh in self:
            waste_type = wh._create_waste_type()
            self.waste_type_id = waste_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        waste_loc = new_wh._create_waste_loc()
        new_wh.waste_loc_id = waste_loc.id
        waste_type = new_wh._create_waste_type()
        new_wh.waste_type_id = waste_type.id
        return new_wh
