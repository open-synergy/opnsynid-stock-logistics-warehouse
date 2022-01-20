# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.translate import _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    customer_promotion_type_id = fields.Many2one(
        string="Customer Promotion Type", comodel_name="stock.picking.type"
    )

    supplier_promotion_type_id = fields.Many2one(
        string="Supplier Promotion Type", comodel_name="stock.picking.type"
    )

    customer_promotion_route_id = fields.Many2one(
        string="Customer Promotion Route", comodel_name="stock.location.route"
    )

    supplier_promotion_route_id = fields.Many2one(
        string="Supplier Promotion Route", comodel_name="stock.location.route"
    )

    @api.multi
    def _prepare_customer_promotion_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Customer Promotion",
            "prefix": self.code + "/CPR/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_supplier_promotion_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Supplier Promotion",
            "prefix": self.code + "/SPR/",
            "padding": 6,
        }
        return data

    @api.multi
    def _get_supp_promotion_src_location(self):
        self.ensure_one()
        supp_promotion_loc = self.env["ir.property"].get(
            "property_stock_supplier_promotion_id", "res.partner"
        )
        return {
            "one_step": supp_promotion_loc,
            "two_steps": supp_promotion_loc,
            "three_steps": supp_promotion_loc,
            "transit_one_step": self.wh_transit_in_loc_id,
            "transit_two_steps": self.wh_transit_in_loc_id,
            "transit_three_steps": self.wh_transit_in_loc_id,
        }

    @api.multi
    def _get_supp_promotion_dest_location(self):
        self.ensure_one()
        return {
            "one_step": self.lot_stock_id,
            "two_steps": self.wh_input_stock_loc_id,
            "three_steps": self.wh_input_stock_loc_id,
            "transit_one_step": self.lot_stock_id,
            "transit_two_steps": self.wh_input_stock_loc_id,
            "transit_three_steps": self.wh_input_stock_loc_id,
        }

    @api.multi
    def _get_cust_promotion_src_location(self):
        self.ensure_one()
        return {
            "ship_only": self.lot_stock_id,
            "pick_ship": self.wh_output_stock_loc_id,
            "pick_pack_ship": self.wh_output_stock_loc_id,
            "ship_transit": self.lot_stock_id,
            "pick_ship_transit": self.wh_output_stock_loc_id,
            "pick_pack_ship_transit": self.wh_output_stock_loc_id,
        }

    @api.multi
    def _get_cust_promotion_dest_location(self):
        self.ensure_one()
        cust_promotion_loc = self.env["ir.property"].get(
            "property_stock_customer_promotion_id", "res.partner"
        )
        return {
            "ship_only": cust_promotion_loc,
            "pick_ship": cust_promotion_loc,
            "pick_pack_ship": cust_promotion_loc,
            "ship_transit": self.wh_transit_out_loc_id,
            "pick_ship_transit": self.wh_transit_out_loc_id,
            "pick_pack_ship_transit": self.wh_transit_out_loc_id,
        }

    @api.multi
    def _prepare_customer_promotion_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.delivery_steps in ["ship_only", "ship_transit"]:
            src_loc = self.lot_stock_id
        else:
            src_loc = self.wh_output_stock_loc_id
        if self.delivery_steps in ["ship_only", "pick_ship", "pick_pack_ship"]:
            dest_loc = self.env["ir.property"].get(
                "property_stock_customer_promotion_id", "res.partner"
            )
        else:
            dest_loc = self.wh_transit_out_loc_id

        sequence = obj_sequence.create(self._prepare_customer_promotion_sequence())

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
        obj_sequence = self.env["ir.sequence"]
        if self.reception_steps in ["one_step", "two_steps", "three_steps"]:
            src_loc = self.env["ir.property"].get(
                "property_stock_supplier_promotion_id", "res.partner"
            )
        else:
            src_loc = self.wh_transit_in_loc_id
        if self.reception_steps in ["one_step", "transit_one_step"]:
            dest_loc = self.lot_stock_id
        else:
            dest_loc = self.wh_input_stock_loc_id

        sequence = obj_sequence.create(self._prepare_supplier_promotion_sequence())

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
        pick_type = obj_type.create(self._prepare_customer_promotion_type())
        return pick_type

    @api.multi
    def _create_supplier_promotion_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_supplier_promotion_type())
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
        supp_promotion_type = new_wh._create_supplier_promotion_type()
        new_wh.write(
            {
                "customer_promotion_type_id": cust_promotion_type.id,
                "supplier_promotion_type_id": supp_promotion_type.id,
            }
        )
        cust_route = new_wh._create_route_customer_promotion()
        supp_route = new_wh._create_route_supplier_promotion()
        new_wh.write(
            {
                "customer_promotion_route_id": cust_route.id,
                "supplier_promotion_route_id": supp_route.id,
                "route_ids": [(4, cust_route.id), (4, supp_route.id)],
            }
        )
        return new_wh

    @api.multi
    def change_route(
        self, warehouse, new_reception_step=False, new_delivery_step=False
    ):
        super(StockWarehouse, self).change_route(
            warehouse,
            new_reception_step=new_reception_step,
            new_delivery_step=new_delivery_step,
        )
        if new_reception_step:
            src_loc = self._get_supp_promotion_src_location()[new_reception_step]
            dest_loc = self._get_supp_promotion_dest_location()[new_reception_step]
            res_supp = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.supplier_promotion_type_id.write(res_supp)
            # Adjust Supplier Promotion Route
            warehouse.supplier_promotion_route_id.pull_ids.unlink()
            warehouse.supplier_promotion_route_id.write(
                {
                    "pull_ids": warehouse._prepare_supp_promotion_pull_rule(
                        new_reception_step
                    )
                }
            )
        if new_delivery_step:
            src_loc = self._get_cust_promotion_src_location()[new_delivery_step]
            dest_loc = self._get_cust_promotion_dest_location()[new_delivery_step]
            res_cust = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.customer_promotion_type_id.write(res_cust)
            # Adjust Customer Promotion Route
            warehouse.customer_promotion_route_id.push_ids.unlink()
            warehouse.customer_promotion_route_id.write(
                {
                    "push_ids": warehouse._prepare_cust_promotion_push_rule(
                        new_delivery_step
                    )
                }
            )
        return True

    @api.multi
    def _prepare_cust_promotion_push_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.delivery_steps

        if step in ["ship_only", "pick_ship", "pick_pack_ship"]:
            return result
        else:
            src_loc = self.wh_transit_out_loc_id
            dest_loc = self.env["ir.property"].get(
                "property_stock_customer_promotion_id", "res.partner"
            )
            pick_type1 = self.customer_promotion_type_id
            pick_type2 = self.transit_out_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ":  Customer Promotion 1",  # TODO
                        "location_from_id": src_loc.id,
                        "location_dest_id": dest_loc.id,
                        "picking_type_id": pick_type2.id,
                        "auto": "manual",
                        "picking_type_ids": [(6, 0, [pick_type1.id])],
                    },
                )
            )
        return result

    @api.multi
    def _prepare_supp_promotion_pull_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.reception_steps

        if step in ["one_step", "two_steps", "three_steps"]:
            return result
        else:
            src_loc = self.wh_transit_in_loc_id
            dest_loc = self.env["ir.property"].get(
                "property_stock_supplier_promotion_id", "res.partner"
            )
            pick_type1 = self.supplier_promotion_type_id
            pick_type2 = self.transit_in_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ":  Supplier Promotion",  # TODO
                        "location_id": src_loc.id,
                        "warehouse_id": self.id,
                        "action": "move",
                        "location_src_id": dest_loc.id,
                        "picking_type_id": pick_type1.id,
                        "procure_method": "make_to_stock",
                        "picking_type_ids": [(6, 0, [pick_type2.id])],
                    },
                )
            )
        return result

    @api.multi
    def _prepare_route_customer_promotion(self):
        self.ensure_one()
        return {
            "name": self.name + ": Customer Promotion",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "push_ids": self._prepare_cust_promotion_push_rule(),
        }

    @api.multi
    def _prepare_route_supplier_promotion(self):
        self.ensure_one()
        return {
            "name": self.name + ": Supplier Promotion",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "pull_ids": self._prepare_supp_promotion_pull_rule(),
        }

    @api.multi
    def _create_route_customer_promotion(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_route_customer_promotion())

    @api.multi
    def _create_route_supplier_promotion(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_route_supplier_promotion())

    @api.multi
    def button_create_customer_promotion(self):
        for wh in self:
            route = self._create_route_customer_promotion()
            wh.write(
                {
                    "customer_promotion_route_id": route.id,
                }
            )

    @api.multi
    def button_create_supplier_promotion(self):
        for wh in self:
            route = self._create_route_supplier_promotion()
            wh.write(
                {
                    "supplier_promotion_route_id": route.id,
                }
            )
