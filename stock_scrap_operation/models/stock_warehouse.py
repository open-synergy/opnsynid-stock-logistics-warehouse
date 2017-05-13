# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    scrap_type_id = fields.Many2one(
        string="Scrap Type",
        comodel_name="stock.picking.type"
    )
    scrap_loc_id = fields.Many2one(
        string="Scrap Location",
        comodel_name="stock.location"
    )

    @api.multi
    def _prepare_scrap_location(self):
        self.ensure_one()
        parent_location = self.view_location_id
        data = {
            "name": _("Scrap"),
            "location_id": parent_location.id,
            "usage": "inventory",
            "active": True

        }
        return data

    @api.multi
    def _prepare_scrap_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Scrap",
            "prefix": self.code + "/SCR/",
            "padding": 6
        }
        return data

    @api.multi
    def _prepare_scrap_type(self):
        self.ensure_one()
        obj_sequence = self.env['ir.sequence']
        location = self.lot_stock_id
        scrap_loc = self._get_scrap_location()

        sequence = obj_sequence.create(
            self._prepare_scrap_sequence())

        data = {
            "name": _("Scrap"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": location.id,
            "allowed_location_ids": [(6, 0, [location.id])],
            "default_location_dest_id": scrap_loc.id,
            "allowed_dest_location_ids": [(6, 0, [scrap_loc.id])],
        }
        return data

    @api.multi
    def _get_scrap_location(self):
        self.ensure_one()
        if not self.scrap_loc_id:
            raise UserError(_("No scrap location"))
        return self.scrap_loc_id

    @api.multi
    def _create_scrap_loc(self):
        self.ensure_one()
        obj_loc = self.env["stock.location"]
        scrap_loc = obj_loc.create(
            self._prepare_scrap_location())
        return scrap_loc

    @api.multi
    def _create_scrap_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        scrap_type = obj_type.create(
            self._prepare_scrap_type())
        return scrap_type

    @api.multi
    def button_create_scrap_loc(self):
        for wh in self:
            scrap_loc = wh._create_scrap_loc()
            wh.scrap_loc_id = scrap_loc.id

    @api.multi
    def button_create_scrap_type(self):
        for wh in self:
            scrap_type = wh._create_scrap_type()
            wh.scrap_type_id = scrap_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        scrap_loc = new_wh._create_scrap_loc()
        self.scrap_loc_id = scrap_loc.id
        scrap_type = new_wh._create_scrap_type()
        self.scrap_type_id = scrap_type.id
        return new_wh
