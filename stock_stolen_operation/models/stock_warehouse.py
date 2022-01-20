# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    stolen_type_id = fields.Many2one(
        string="Stolen Type", comodel_name="stock.picking.type"
    )
    stolen_loc_id = fields.Many2one(
        string="Stolen Location", comodel_name="stock.location"
    )

    @api.multi
    def _prepare_stolen_location(self):
        self.ensure_one()
        parent_location = self.view_location_id
        data = {
            "name": _("Stolen"),
            "location_id": parent_location.id,
            "usage": "inventory",
            "active": True,
        }
        return data

    @api.multi
    def _prepare_stolen_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Stolen",
            "prefix": self.code + "/STL/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_stolen_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        location = self.lot_stock_id
        stolen_loc = self._get_stolen_location()

        sequence = obj_sequence.create(self._prepare_stolen_sequence())

        subtype_id = self.env.ref("stock_stolen_operation.stolen_subtype")

        data = {
            "name": _("Stolen"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": location.id,
            "allowed_location_ids": [(6, 0, [location.id])],
            "default_location_dest_id": stolen_loc.id,
            "allowed_dest_location_ids": [(6, 0, [stolen_loc.id])],
            "subtype_id": subtype_id.id,
        }
        return data

    @api.multi
    def _get_stolen_location(self):
        self.ensure_one()
        if not self.stolen_loc_id:
            raise UserError(_("No stolen location"))
        return self.stolen_loc_id

    @api.multi
    def _create_stolen_loc(self):
        self.ensure_one()
        obj_loc = self.env["stock.location"]
        stolen_loc = obj_loc.create(self._prepare_stolen_location())
        return stolen_loc

    @api.multi
    def _create_stolen_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        stolen_type = obj_type.create(self._prepare_stolen_type())
        return stolen_type

    @api.multi
    def button_create_stolen_loc(self):
        for wh in self:
            stolen_loc = wh._create_stolen_loc()
            self.stolen_loc_id = stolen_loc.id

    @api.multi
    def button_create_stolen_type(self):
        for wh in self:
            stolen_type = wh._create_stolen_type()
            self.stolen_type_id = stolen_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        stolen_loc = new_wh._create_stolen_loc()
        new_wh.stolen_loc_id = stolen_loc.id
        stolen_type = new_wh._create_stolen_type()
        new_wh.stolen_type_id = stolen_type.id
        return new_wh
