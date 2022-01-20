# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    production_rm_type_id = fields.Many2one(
        string="Raw Material Consumption Type", comodel_name="stock.picking.type"
    )
    production_rm_loc_id = fields.Many2one(
        string="Raw Material Consumption Location", comodel_name="stock.location"
    )
    production_fg_type_id = fields.Many2one(
        string="Production Result Type", comodel_name="stock.picking.type"
    )
    production_fg_loc_id = fields.Many2one(
        string="Production Result Location", comodel_name="stock.location"
    )

    @api.multi
    def _prepare_production_rm_location(self):
        self.ensure_one()
        parent_location = self.view_location_id
        data = {
            "name": _("RM Consumption"),
            "location_id": parent_location.id,
            "usage": "production",
            "active": True,
        }
        return data

    @api.multi
    def _prepare_production_fg_location(self):
        self.ensure_one()
        parent_location = self.view_location_id
        data = {
            "name": _("Production Result"),
            "location_id": parent_location.id,
            "usage": "production",
            "active": True,
        }
        return data

    @api.multi
    def _prepare_production_rm_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - RM Consumption",
            "prefix": self.code + "/RM/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_production_fg_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Production Result",
            "prefix": self.code + "/FG/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_production_rm_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        src_location = self.lot_stock_id
        dest_location = self._get_production_rm_location()

        sequence = obj_sequence.create(self._prepare_production_rm_sequence())

        data = {
            "name": _("RM Consumption"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": src_location.id,
            "allowed_location_ids": [(6, 0, [src_location.id])],
            "default_location_dest_id": dest_location.id,
            "allowed_dest_location_ids": [(6, 0, [dest_location.id])],
        }
        return data

    @api.multi
    def _prepare_production_fg_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        dest_location = self.lot_stock_id
        src_location = self._get_production_fg_location()

        sequence = obj_sequence.create(self._prepare_production_fg_sequence())

        data = {
            "name": _("Production Result"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "incoming",
            "default_location_src_id": src_location.id,
            "allowed_location_ids": [(6, 0, [src_location.id])],
            "default_location_dest_id": dest_location.id,
            "allowed_dest_location_ids": [(6, 0, [dest_location.id])],
        }
        return data

    @api.multi
    def _get_production_rm_location(self):
        self.ensure_one()
        if not self.production_rm_loc_id:
            raise UserError(_("No RM Consumption location"))
        return self.production_rm_loc_id

    @api.multi
    def _get_production_fg_location(self):
        self.ensure_one()
        if not self.production_fg_loc_id:
            raise UserError(_("No production result location"))
        return self.production_fg_loc_id

    @api.multi
    def _create_production_rm_loc(self):
        self.ensure_one()
        obj_loc = self.env["stock.location"]
        production_rm_loc = obj_loc.create(self._prepare_production_rm_location())
        return production_rm_loc

    @api.multi
    def _create_production_fg_loc(self):
        self.ensure_one()
        obj_loc = self.env["stock.location"]
        production_fg_loc = obj_loc.create(self._prepare_production_fg_location())
        return production_fg_loc

    @api.multi
    def _create_production_rm_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        production_rm_type = obj_type.create(self._prepare_production_rm_type())
        return production_rm_type

    @api.multi
    def _create_production_fg_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        production_fg_type = obj_type.create(self._prepare_production_fg_type())
        return production_fg_type

    @api.multi
    def button_create_production_rm_loc(self):
        for wh in self:
            production_rm_loc = wh._create_production_rm_loc()
            self.production_rm_loc_id = production_rm_loc.id

    @api.multi
    def button_create_production_fg_loc(self):
        for wh in self:
            production_fg_loc = wh._create_production_fg_loc()
            self.production_fg_loc_id = production_fg_loc.id

    @api.multi
    def button_create_production_rm_type(self):
        for wh in self:
            production_rm_type = wh._create_production_rm_type()
            self.production_rm_type_id = production_rm_type.id

    @api.multi
    def button_create_production_fg_type(self):
        for wh in self:
            production_fg_type = wh._create_production_fg_type()
            self.production_fg_type_id = production_fg_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        production_rm_loc = new_wh._create_production_rm_loc()
        production_fg_loc = new_wh._create_production_fg_loc()
        new_wh.production_rm_loc_id = production_rm_loc.id
        new_wh.production_fg_loc_id = production_fg_loc.id
        production_rm_type = new_wh._create_production_rm_type()
        production_fg_type = new_wh._create_production_fg_type()
        new_wh.production_rm_type_id = production_rm_type.id
        new_wh.production_fg_type_id = production_fg_type.id
        return new_wh
