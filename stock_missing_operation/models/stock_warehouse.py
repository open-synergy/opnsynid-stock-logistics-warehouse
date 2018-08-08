# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    missing_type_id = fields.Many2one(
        string="Missing Type",
        comodel_name="stock.picking.type"
    )
    missing_loc_id = fields.Many2one(
        string="Missing Location",
        comodel_name="stock.location"
    )

    @api.multi
    def _prepare_missing_location(self):
        self.ensure_one()
        parent_location = self.view_location_id
        data = {
            "name": _("Missing"),
            "location_id": parent_location.id,
            "usage": "inventory",
            "active": True

        }
        return data

    @api.multi
    def _prepare_missing_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Missing",
            "prefix": self.code + "/MISS/",
            "padding": 6
        }
        return data

    @api.multi
    def _prepare_missing_type(self):
        self.ensure_one()
        obj_sequence = self.env['ir.sequence']
        location = self.lot_stock_id
        missing_loc = self._get_missing_location()

        sequence = obj_sequence.create(
            self._prepare_missing_sequence())

        data = {
            "name": _("Missing"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": location.id,
            "allowed_location_ids": [(6, 0, [location.id])],
            "default_location_dest_id": missing_loc.id,
            "allowed_dest_location_ids": [(6, 0, [missing_loc.id])],
        }
        return data

    @api.multi
    def _get_missing_location(self):
        self.ensure_one()
        if not self.missing_loc_id:
            raise UserError(_("No missing location"))
        return self.missing_loc_id

    @api.multi
    def _create_missing_loc(self):
        self.ensure_one()
        obj_loc = self.env["stock.location"]
        missing_loc = obj_loc.create(
            self._prepare_missing_location())
        return missing_loc

    @api.multi
    def _create_missing_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        missing_type = obj_type.create(
            self._prepare_missing_type())
        return missing_type

    @api.multi
    def button_create_missing_loc(self):
        for wh in self:
            missing_loc = wh._create_missing_loc()
            self.missing_loc_id = missing_loc.id

    @api.multi
    def button_create_missing_type(self):
        for wh in self:
            missing_type = wh._create_missing_type()
            self.missing_type_id = missing_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        missing_loc = new_wh._create_missing_loc()
        new_wh.missing_loc_id = missing_loc.id
        missing_type = new_wh._create_missing_type()
        new_wh.missing_type_id = missing_type.id
        return new_wh
