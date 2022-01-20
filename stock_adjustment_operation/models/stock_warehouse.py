# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    adjustment_in_type_id = fields.Many2one(
        string="Adjustment In Type", comodel_name="stock.picking.type"
    )
    adjustment_out_type_id = fields.Many2one(
        string="Adjustment Out Type", comodel_name="stock.picking.type"
    )
    adjustment_loc_id = fields.Many2one(
        string="Adjustment Location", comodel_name="stock.location"
    )

    @api.multi
    def _prepare_adjustment_location(self):
        self.ensure_one()
        parent_location = self.view_location_id
        data = {
            "name": _("Adjustment"),
            "location_id": parent_location.id,
            "usage": "inventory",
            "active": True,
        }
        return data

    @api.multi
    def _prepare_adjustment_in_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Adjustment In",
            "prefix": self.code + "/ADJ-IN/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_adjustment_out_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Adjustment Out",
            "prefix": self.code + "/ADJ-OUT/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_adjustment_in_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        location = self.lot_stock_id
        adjustment_loc = self._get_adjustment_location()

        sequence = obj_sequence.create(self._prepare_adjustment_in_sequence())

        data = {
            "name": _("Adjustment In"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_dest_id": location.id,
            "allowed_dest_location_ids": [(6, 0, [location.id])],
            "default_location_src_id": adjustment_loc.id,
            "allowed_location_ids": [(6, 0, [adjustment_loc.id])],
        }
        return data

    @api.multi
    def _prepare_adjustment_out_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        location = self.lot_stock_id
        adjustment_loc = self._get_adjustment_location()

        sequence = obj_sequence.create(self._prepare_adjustment_out_sequence())

        data = {
            "name": _("Adjustment Out"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_dest_id": adjustment_loc.id,
            "allowed_dest_location_ids": [(6, 0, [adjustment_loc.id])],
            "default_location_src_id": location.id,
            "allowed_location_ids": [(6, 0, [location.id])],
        }
        return data

    @api.multi
    def _get_adjustment_location(self):
        self.ensure_one()
        if not self.adjustment_loc_id:
            raise UserError(_("No adjustment location location"))
        return self.adjustment_loc_id

    @api.multi
    def _create_adjustment_loc(self):
        self.ensure_one()
        obj_loc = self.env["stock.location"]
        adjustment_loc = obj_loc.create(self._prepare_adjustment_location())
        return adjustment_loc

    @api.multi
    def _create_adjustment_in_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        adjustment_in_type = obj_type.create(self._prepare_adjustment_in_type())
        return adjustment_in_type

    @api.multi
    def _create_adjustment_out_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        adjustment_out_type = obj_type.create(self._prepare_adjustment_out_type())
        return adjustment_out_type

    @api.multi
    def button_create_adjustment_loc(self):
        for wh in self:
            adjustment_loc = wh._create_adjustment_loc()
            self.adjustment_loc_id = adjustment_loc.id

    @api.multi
    def button_create_adjustment_in_type(self):
        for wh in self:
            adjustment_in_type = wh._create_adjustment_in_type()
            self.adjustment_in_type_id = adjustment_in_type.id

    @api.multi
    def button_create_adjustment_out_type(self):
        for wh in self:
            adjustment_out_type = wh._create_adjustment_out_type()
            self.adjustment_out_type_id = adjustment_out_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        adjustment_loc = new_wh._create_adjustment_loc()
        new_wh.adjustment_loc_id = adjustment_loc.id
        adjustment_in_type = new_wh._create_adjustment_in_type()
        new_wh.adjustment_in_type_id = adjustment_in_type.id
        adjustment_out_type = new_wh._create_adjustment_out_type()
        new_wh.adjustment_out_type_id = adjustment_out_type.id
        return new_wh
