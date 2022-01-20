# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    consume_type_id = fields.Many2one(
        string="Consume Type", comodel_name="stock.picking.type"
    )
    consume_loc_id = fields.Many2one(
        string="Consume Location", comodel_name="stock.location"
    )

    @api.multi
    def _prepare_consume_location(self):
        self.ensure_one()
        parent_location = self.view_location_id
        data = {
            "name": _("Consume"),
            "location_id": parent_location.id,
            "usage": "inventory",
            "active": True,
        }
        return data

    @api.multi
    def _prepare_consume_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Consume",
            "prefix": self.code + "/CON/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_consume_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        location = self.lot_stock_id
        consume_loc = self._get_consume_location()

        sequence = obj_sequence.create(self._prepare_consume_sequence())

        data = {
            "name": _("Consume"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": location.id,
            "allowed_location_ids": [(6, 0, [location.id])],
            "default_location_dest_id": consume_loc.id,
            "allowed_dest_location_ids": [(6, 0, [consume_loc.id])],
        }
        return data

    @api.multi
    def _get_consume_location(self):
        self.ensure_one()
        if not self.consume_loc_id:
            raise UserError(_("No consume location"))
        return self.consume_loc_id

    @api.multi
    def _create_consume_loc(self):
        self.ensure_one()
        obj_loc = self.env["stock.location"]
        consume_loc = obj_loc.create(self._prepare_consume_location())
        return consume_loc

    @api.multi
    def _create_consume_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        consume_type = obj_type.create(self._prepare_consume_type())
        return consume_type

    @api.multi
    def button_create_consume_loc(self):
        for wh in self:
            consume_loc = wh._create_consume_loc()
            self.consume_loc_id = consume_loc.id

    @api.multi
    def button_create_consume_type(self):
        for wh in self:
            consume_type = wh._create_consume_type()
            self.consume_type_id = consume_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        consume_loc = new_wh._create_consume_loc()
        new_wh.consume_loc_id = consume_loc.id
        consume_type = new_wh._create_consume_type()
        new_wh.consume_type_id = consume_type.id
        return new_wh
