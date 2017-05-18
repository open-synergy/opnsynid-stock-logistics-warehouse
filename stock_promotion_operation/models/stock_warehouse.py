# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    customer_promotion_type_id = fields.Many2one(
        string="Customer Promotion Type",
        comodel_name="stock.picking.type"
    )

    supplier_promotion_type_id = fields.Many2one(
        string="Supplier Promotion Type",
        comodel_name="stock.picking.type"
    )

    @api.multi
    def _prepare_customer_promotion_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Customer Promotion",
            "prefix": self.code + "/CPR/",
            "padding": 6
        }
        return data

    @api.multi
    def _prepare_supplier_promotion_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Supplier Promotion",
            "prefix": self.code + "/SPR/",
            "padding": 6
        }
        return data

    @api.multi
    def _get_supp_promotion_dest_location(self):
        self.ensure_one()
        return {
            "one_step": self.lot_stock_id,
            "two_steps": self.wh_input_stock_loc_id,
            "three_steps": self.wh_input_stock_loc_id,
            "transit_one_step": self.wh_transit_in_loc_id,
            "transit_two_steps": self.wh_transit_in_loc_id,
            "transit_three_steps": self.wh_transit_in_loc_id,
        }

    @api.multi
    def _get_cust_promotion_src_location(self):
        self.ensure_one()
        return {
            "ship_only": self.lot_stock_id,
            "pick_ship": self.wh_output_stock_loc_id,
            "pick_pack_ship": self.wh_output_stock_loc_id,
            "ship_transit": self.wh_transit_out_loc_id,
            "pick_ship_transit": self.wh_transit_out_loc_id,
            "pick_pack_ship_transit": self.wh_transit_out_loc_id,
        }

    @api.multi
    def _prepare_customer_promotion_type(self):
        self.ensure_one()
        obj_sequence = self.env['ir.sequence']
        src_loc = self._get_cust_promotion_src_location()[self.delivery_steps]
        dest_loc = self.env["ir.property"].get(
            "property_stock_customer_promotion_id",
            "res.partner")

        sequence = obj_sequence.create(
            self._prepare_customer_promotion_sequence())

        data = {
            "name": _("Customer Promotion"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
        }
        return data

    @api.multi
    def _prepare_supplier_promotion_type(self):
        self.ensure_one()
        obj_sequence = self.env['ir.sequence']
        src_loc = self.env["ir.property"].get(
            "property_stock_supplier_promotion_id",
            "res.partner")
        dest_loc = self._get_supp_promotion_dest_location()[
            self.reception_steps]

        sequence = obj_sequence.create(
            self._prepare_supplier_promotion_sequence())

        data = {
            "name": _("Supplier Promotion"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
        }
        return data

    @api.multi
    def _create_customer_promotion_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(
            self._prepare_customer_promotion_type())
        return pick_type

    @api.multi
    def _create_supplier_promotion_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(
            self._prepare_supplier_promotion_type())
        return pick_type

    @api.multi
    def button_create_customer_promotion_type(self):
        for wh in self:
            pick_type = wh._create_customer_promotion_type()
            wh.customer_promotion_type_id = pick_type.id

    @api.multi
    def button_create_supplier_promotion_type(self):
        for wh in self:
            pick_type = wh._create_supplier_promotion_type()
            wh.supplier_promotion_type_id = pick_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        cust_promotion_type = new_wh._create_customer_promotion_type()
        new_wh.customer_promotion_type_id = cust_promotion_type.id
        supp_promotion_type = new_wh._create_supplier_promotion_type()
        new_wh.supplier_promotion_type_id = supp_promotion_type.id
        return new_wh

    @api.multi
    def change_route(
            self, warehouse, new_reception_step=False,
            new_delivery_step=False):
        super(StockWarehouse, self).change_route(
            warehouse, new_reception_step=new_reception_step,
            new_delivery_step=new_delivery_step)
        if new_reception_step:
            location_dest = self._get_supp_promotion_dest_location()[
                new_reception_step]
            res_supp = {
                "default_location_dest_id": location_dest.id,
                "allowed_dest_location_ids": [(6, 0, [location_dest.id])],
            }
            warehouse.supplier_promotion_type_id.write(res_supp)
        if new_delivery_step:
            location_src = self._get_cust_promotion_src_location()[
                new_delivery_step]
            res_cust = {
                "default_location_src_id": location_src.id,
                "allowed_location_ids": [(6, 0, [location_src.id])],
            }
            warehouse.customer_promotion_type_id.write(res_cust)
        return True
