# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.translate import _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    rental_customer_in_type_id = fields.Many2one(
        string="Rental Customer In Type", comodel_name="stock.picking.type"
    )

    rental_customer_out_type_id = fields.Many2one(
        string="Rental Customer Out Type", comodel_name="stock.picking.type"
    )

    rental_supplier_in_type_id = fields.Many2one(
        string="Rental Supplier In Type", comodel_name="stock.picking.type"
    )

    rental_supplier_out_type_id = fields.Many2one(
        string="Rental Supplier Out Type", comodel_name="stock.picking.type"
    )

    rental_customer_in_route_id = fields.Many2one(
        string="Rental Customer In Route", comodel_name="stock.location.route"
    )

    rental_customer_out_route_id = fields.Many2one(
        string="Rental Customer Out Route", comodel_name="stock.location.route"
    )

    rental_supplier_in_route_id = fields.Many2one(
        string="Rental Supplier In Route", comodel_name="stock.location.route"
    )

    rental_supplier_out_route_id = fields.Many2one(
        string="Rental Supplier Out Route", comodel_name="stock.location.route"
    )

    @api.multi
    def _prepare_rental_customer_in_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Rental Customer In",
            "prefix": self.code + "/LCI/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_rental_customer_out_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Rental Customer Out",
            "prefix": self.code + "/LCO/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_rental_supplier_in_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Rental Supplier In",
            "prefix": self.code + "/LSI/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_rental_supplier_out_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Rental Supplier Out",
            "prefix": self.code + "/LSO/",
            "padding": 6,
        }
        return data

    @api.multi
    def _get_rental_in_src_location(self):
        self.ensure_one()
        donation_in_loc = self.env["ir.property"].get(
            "supplier_rental_location_id", "res.partner"
        )
        return {
            "one_step": donation_in_loc,
            "two_steps": donation_in_loc,
            "three_steps": donation_in_loc,
            "transit_one_step": self.wh_transit_in_loc_id,
            "transit_two_steps": self.wh_transit_in_loc_id,
            "transit_three_steps": self.wh_transit_in_loc_id,
        }

    @api.multi
    def _get_rental_in_dest_location(self):
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
    def _get_rental_out_src_location(self):
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
    def _get_rental_out_dest_location(self):
        self.ensure_one()
        donation_in_loc = self.env["ir.property"].get(
            "customer_rental_location_id", "res.partner"
        )
        return {
            "ship_only": donation_in_loc,
            "pick_ship": donation_in_loc,
            "pick_pack_ship": donation_in_loc,
            "ship_transit": self.wh_transit_out_loc_id,
            "pick_ship_transit": self.wh_transit_out_loc_id,
            "pick_pack_ship_transit": self.wh_transit_out_loc_id,
        }

    @api.multi
    def _prepare_rental_customer_in_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.reception_steps in ["one_step", "two_steps", "three_steps"]:
            src_loc = self.env["ir.property"].get(
                "customer_rental_location_id", "res.partner"
            )
        else:
            src_loc = self.wh_transit_in_loc_id
        if self.reception_steps in ["one_step", "transit_one_step"]:
            dest_loc = self.lot_stock_id
        else:
            dest_loc = self.wh_input_stock_loc_id

        sequence = obj_sequence.create(self._prepare_rental_customer_in_sequence())

        subtype_id = self.env.ref("stock_rental_operation.customer_in_rental_subtype")

        data = {
            "name": _("Rental Customer In"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "incoming",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            "subtype_id": subtype_id.id,
        }
        return data

    @api.multi
    def _prepare_rental_customer_out_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.delivery_steps in ["ship_only", "ship_transit"]:
            src_loc = self.lot_stock_id
        else:
            src_loc = self.wh_output_stock_loc_id
        if self.delivery_steps in ["ship_only", "pick_ship", "pick_pack_ship"]:
            dest_loc = self.env["ir.property"].get(
                "customer_rental_location_id", "res.partner"
            )
        else:
            dest_loc = self.wh_transit_out_loc_id

        sequence = obj_sequence.create(self._prepare_rental_customer_out_sequence())

        subtype_id = self.env.ref("stock_rental_operation.customer_out_rental_subtype")

        data = {
            "name": _("Rental Customer Out"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            "subtype_id": subtype_id.id,
        }
        return data

    @api.multi
    def _prepare_rental_supplier_in_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.reception_steps in ["one_step", "two_steps", "three_steps"]:
            src_loc = self.env["ir.property"].get(
                "supplier_rental_location_id", "res.partner"
            )
        else:
            src_loc = self.wh_transit_in_loc_id
        if self.reception_steps in ["one_step", "transit_one_step"]:
            dest_loc = self.lot_stock_id
        else:
            dest_loc = self.wh_input_stock_loc_id

        sequence = obj_sequence.create(self._prepare_rental_supplier_in_sequence())

        subtype_id = self.env.ref("stock_rental_operation.supplier_in_rental_subtype")

        data = {
            "name": _("Rental Supplier In"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "incoming",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            "subtype_id": subtype_id.id,
        }
        return data

    @api.multi
    def _prepare_rental_supplier_out_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.delivery_steps in ["ship_only", "ship_transit"]:
            src_loc = self.lot_stock_id
        else:
            src_loc = self.wh_output_stock_loc_id
        if self.delivery_steps in ["ship_only", "pick_ship", "pick_pack_ship"]:
            dest_loc = self.env["ir.property"].get(
                "supplier_rental_location_id", "res.partner"
            )
        else:
            dest_loc = self.wh_transit_out_loc_id

        sequence = obj_sequence.create(self._prepare_rental_supplier_out_sequence())

        subtype_id = self.env.ref("stock_rental_operation.supplier_out_rental_subtype")

        data = {
            "name": _("Rental Supplier Out"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            "subtype_id": subtype_id.id,
        }
        return data

    @api.multi
    def _create_rental_customer_in_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_rental_customer_in_type())
        return pick_type

    @api.multi
    def _create_rental_customer_out_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_rental_customer_out_type())
        return pick_type

    @api.multi
    def _create_rental_supplier_in_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_rental_supplier_in_type())
        return pick_type

    @api.multi
    def _create_rental_supplier_out_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_rental_supplier_out_type())
        return pick_type

    @api.multi
    def button_create_customer_in_rental_type(self):
        for wh in self:
            pick_type = wh._create_rental_customer_in_type()
            wh.rental_customer_in_type_id = pick_type.id

    @api.multi
    def button_create_customer_out_rental_type(self):
        for wh in self:
            pick_type = wh._create_rental_customer_out_type()
            wh.rental_customer_out_type_id = pick_type.id

    @api.multi
    def button_create_supplier_in_rental_type(self):
        for wh in self:
            pick_type = wh._create_rental_supplier_in_type()
            wh.rental_supplier_in_type_id = pick_type.id

    @api.multi
    def button_create_supplier_out_rental_type(self):
        for wh in self:
            pick_type = wh._create_rental_supplier_out_type()
            wh.rental_supplier_out_type_id = pick_type.id

    @api.model
    def create(self, values):
        _super = super(StockWarehouse, self)
        new_wh = _super.create(values)

        rental_cust_in_type = new_wh._create_rental_customer_in_type()
        rental_cust_out_type = new_wh._create_rental_customer_out_type()
        rental_supp_in_type = new_wh._create_rental_supplier_in_type()
        rental_supp_out_type = new_wh._create_rental_supplier_out_type()

        new_wh.write(
            {
                "rental_customer_in_type_id": rental_cust_in_type.id,
                "rental_customer_out_type_id": rental_cust_out_type.id,
                "rental_supplier_in_type_id": rental_supp_in_type.id,
                "rental_supplier_out_type_id": rental_supp_out_type.id,
            }
        )

        rental_cust_in_route = new_wh._create_rental_customer_in_route_id()
        rental_cust_out_route = new_wh._create_rental_customer_out_route_id()
        rental_supp_in_route = new_wh._create_rental_supplier_in_route_id()
        rental_supp_out_route = new_wh._create_rental_supplier_out_route_id()

        new_wh.write(
            {
                "rental_customer_in_route_id": rental_cust_in_route.id,
                "rental_customer_out_route_id": rental_cust_out_route.id,
                "rental_supplier_in_route_id": rental_supp_in_route.id,
                "rental_supplier_out_route_id": rental_supp_out_route.id,
                "route_ids": [
                    (4, rental_cust_in_route.id),
                    (4, rental_cust_out_route.id),
                    (4, rental_supp_in_route.id),
                    (4, rental_supp_out_route.id),
                ],
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
            src_loc = self._get_rental_in_src_location()[new_reception_step]
            dest_loc = self._get_rental_in_dest_location()[new_reception_step]
            res_supp = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.rental_customer_in_type_id.write(res_supp)
            warehouse.rental_customer_in_route_id.pull_ids.unlink()
            warehouse.rental_customer_in_route_id.write(
                {
                    "pull_ids": warehouse._prepare_rental_customer_in_pull_rule(
                        new_reception_step
                    )
                }
            )
            warehouse.rental_supplier_in_type_id.write(res_supp)
            warehouse.rental_supplier_in_route_id.pull_ids.unlink()
            warehouse.rental_supplier_in_route_id.write(
                {
                    "pull_ids": warehouse._prepare_rental_supplier_in_pull_rule(
                        new_reception_step
                    )
                }
            )
        if new_delivery_step:
            src_loc = self._get_rental_out_src_location()[new_delivery_step]
            dest_loc = self._get_rental_out_dest_location()[new_delivery_step]
            res_cust = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.rental_customer_out_type_id.write(res_cust)
            warehouse.rental_customer_out_route_id.push_ids.unlink()
            warehouse.rental_customer_out_route_id.write(
                {
                    "push_ids": warehouse._prepare_rental_customer_out_push_rule(
                        new_delivery_step
                    )
                }
            )
            warehouse.rental_supplier_out_type_id.write(res_cust)
            warehouse.rental_supplier_out_route_id.push_ids.unlink()
            warehouse.rental_supplier_out_route_id.write(
                {
                    "push_ids": warehouse._prepare_rental_supplier_out_push_rule(
                        new_delivery_step
                    )
                }
            )
        return True

    @api.multi
    def _prepare_rental_customer_in_pull_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.reception_steps

        if step in ["one_step", "two_steps", "three_steps"]:
            return result
        else:
            src_loc = self.wh_transit_in_loc_id
            dest_loc = self.env["ir.property"].get(
                "customer_rental_location_id", "res.partner"
            )
            pick_type1 = self.rental_customer_in_type_id
            pick_type2 = self.transit_in_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ": Rental Customer In",
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
    def _prepare_rental_customer_out_push_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.delivery_steps

        if step in ["ship_only", "pick_ship", "pick_pack_ship"]:
            return result
        else:
            src_loc = self.wh_transit_out_loc_id
            dest_loc = self.env["ir.property"].get(
                "customer_rental_location_id", "res.partner"
            )
            pick_type1 = self.rental_customer_out_type_id
            pick_type2 = self.transit_out_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ": Rental Customer Out",
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
    def _prepare_rental_supplier_in_pull_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.reception_steps

        if step in ["one_step", "two_steps", "three_steps"]:
            return result
        else:
            src_loc = self.wh_transit_in_loc_id
            dest_loc = self.env["ir.property"].get(
                "supplier_rental_location_id", "res.partner"
            )
            pick_type1 = self.rental_supplier_in_type_id
            pick_type2 = self.transit_in_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ": Rental Supplier In",
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
    def _prepare_rental_supplier_out_push_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.delivery_steps

        if step in ["ship_only", "pick_ship", "pick_pack_ship"]:
            return result
        else:
            src_loc = self.wh_transit_out_loc_id
            dest_loc = self.env["ir.property"].get(
                "supplier_rental_location_id", "res.partner"
            )
            pick_type1 = self.rental_supplier_out_type_id
            pick_type2 = self.transit_out_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ": Rental Supplier Out",
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
    def _prepare_rental_customer_in_route_id(self):
        self.ensure_one()
        return {
            "name": self.name + ": Rental Customer In",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "pull_ids": self._prepare_rental_customer_in_pull_rule(),
        }

    @api.multi
    def _prepare_rental_customer_out_route_id(self):
        self.ensure_one()
        return {
            "name": self.name + ": Rental Customer Out",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "push_ids": self._prepare_rental_customer_out_push_rule(),
        }

    @api.multi
    def _prepare_rental_supplier_in_route_id(self):
        self.ensure_one()
        return {
            "name": self.name + ": Rental Supplier In",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "pull_ids": self._prepare_rental_supplier_in_pull_rule(),
        }

    @api.multi
    def _prepare_rental_supplier_out_route_id(self):
        self.ensure_one()
        return {
            "name": self.name + ": Rental Supplier Out",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "push_ids": self._prepare_rental_supplier_out_push_rule(),
        }

    @api.multi
    def _create_rental_customer_in_route_id(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_rental_customer_in_route_id())

    @api.multi
    def _create_rental_customer_out_route_id(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_rental_customer_out_route_id())

    @api.multi
    def _create_rental_supplier_in_route_id(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_rental_supplier_in_route_id())

    @api.multi
    def _create_rental_supplier_out_route_id(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_rental_supplier_out_route_id())

    @api.multi
    def button_create_rental_customer_in_route(self):
        for wh in self:
            route = self._create_rental_customer_in_route_id()
            wh.write(
                {
                    "rental_customer_in_route_id": route.id,
                }
            )

    @api.multi
    def button_create_rental_customer_out_route(self):
        for wh in self:
            route = self._create_rental_customer_out_route_id()
            wh.write(
                {
                    "rental_customer_out_route_id": route.id,
                }
            )

    @api.multi
    def button_create_rental_supplier_in_route(self):
        for wh in self:
            route = self._create_rental_supplier_in_route_id()
            wh.write(
                {
                    "rental_supplier_in_route_id": route.id,
                }
            )

    @api.multi
    def button_create_rental_supplier_out_route(self):
        for wh in self:
            route = self._create_rental_supplier_out_route_id()
            wh.write(
                {
                    "rental_supplier_out_route_id": route.id,
                }
            )
