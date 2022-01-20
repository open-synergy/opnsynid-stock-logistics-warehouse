# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.translate import _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    lease_customer_in_type_id = fields.Many2one(
        string="Lease Customer In Type", comodel_name="stock.picking.type"
    )

    lease_customer_out_type_id = fields.Many2one(
        string="Lease Customer Out Type", comodel_name="stock.picking.type"
    )

    lease_supplier_in_type_id = fields.Many2one(
        string="Lease Supplier In Type", comodel_name="stock.picking.type"
    )

    lease_supplier_out_type_id = fields.Many2one(
        string="Lease Supplier Out Type", comodel_name="stock.picking.type"
    )

    lease_customer_in_route_id = fields.Many2one(
        string="Lease Customer In Route", comodel_name="stock.location.route"
    )

    lease_customer_out_route_id = fields.Many2one(
        string="Lease Customer Out Route", comodel_name="stock.location.route"
    )

    lease_supplier_in_route_id = fields.Many2one(
        string="Lease Supplier In Route", comodel_name="stock.location.route"
    )

    lease_supplier_out_route_id = fields.Many2one(
        string="Lease Supplier Out Route", comodel_name="stock.location.route"
    )

    @api.multi
    def _prepare_lease_customer_in_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Lease Customer In",
            "prefix": self.code + "/LCI/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_lease_customer_out_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Lease Customer Out",
            "prefix": self.code + "/LCO/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_lease_supplier_in_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Lease Supplier In",
            "prefix": self.code + "/LSI/",
            "padding": 6,
        }
        return data

    @api.multi
    def _prepare_lease_supplier_out_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Lease Supplier Out",
            "prefix": self.code + "/LSO/",
            "padding": 6,
        }
        return data

    @api.multi
    def _get_lease_in_src_location(self):
        self.ensure_one()
        donation_in_loc = self.env["ir.property"].get(
            "supplier_lease_location_id", "res.partner"
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
    def _get_lease_in_dest_location(self):
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
    def _get_lease_out_src_location(self):
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
    def _get_lease_out_dest_location(self):
        self.ensure_one()
        donation_in_loc = self.env["ir.property"].get(
            "customer_lease_location_id", "res.partner"
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
    def _prepare_lease_customer_in_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.reception_steps in ["one_step", "two_steps", "three_steps"]:
            src_loc = self.env["ir.property"].get(
                "customer_lease_location_id", "res.partner"
            )
        else:
            src_loc = self.wh_transit_in_loc_id
        if self.reception_steps in ["one_step", "transit_one_step"]:
            dest_loc = self.lot_stock_id
        else:
            dest_loc = self.wh_input_stock_loc_id

        sequence = obj_sequence.create(self._prepare_lease_customer_in_sequence())

        subtype = self.env.ref("stock_lease_operation.customer_in_lease_subtype")

        data = {
            "name": _("Lease Customer In"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "incoming",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            "subtype_id": subtype.id,
        }
        return data

    @api.multi
    def _prepare_lease_customer_out_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.delivery_steps in ["ship_only", "ship_transit"]:
            src_loc = self.lot_stock_id
        else:
            src_loc = self.wh_output_stock_loc_id
        if self.delivery_steps in ["ship_only", "pick_ship", "pick_pack_ship"]:
            dest_loc = self.env["ir.property"].get(
                "customer_lease_location_id", "res.partner"
            )
        else:
            dest_loc = self.wh_transit_out_loc_id

        sequence = obj_sequence.create(self._prepare_lease_customer_out_sequence())

        subtype = self.env.ref("stock_lease_operation.customer_out_lease_subtype")

        data = {
            "name": _("Lease Customer Out"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            "subtype_id": subtype.id,
        }
        return data

    @api.multi
    def _prepare_lease_supplier_in_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.reception_steps in ["one_step", "two_steps", "three_steps"]:
            src_loc = self.env["ir.property"].get(
                "supplier_lease_location_id", "res.partner"
            )
        else:
            src_loc = self.wh_transit_in_loc_id
        if self.reception_steps in ["one_step", "transit_one_step"]:
            dest_loc = self.lot_stock_id
        else:
            dest_loc = self.wh_input_stock_loc_id

        sequence = obj_sequence.create(self._prepare_lease_supplier_in_sequence())

        subtype = self.env.ref("stock_lease_operation.supplier_in_lease_subtype")

        data = {
            "name": _("Lease Supplier In"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "incoming",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            "subtype_id": subtype.id,
        }
        return data

    @api.multi
    def _prepare_lease_supplier_out_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.delivery_steps in ["ship_only", "ship_transit"]:
            src_loc = self.lot_stock_id
        else:
            src_loc = self.wh_output_stock_loc_id
        if self.delivery_steps in ["ship_only", "pick_ship", "pick_pack_ship"]:
            dest_loc = self.env["ir.property"].get(
                "supplier_lease_location_id", "res.partner"
            )
        else:
            dest_loc = self.wh_transit_out_loc_id

        sequence = obj_sequence.create(self._prepare_lease_supplier_out_sequence())

        subtype = self.env.ref("stock_lease_operation.supplier_out_lease_subtype")

        data = {
            "name": _("Lease Supplier Out"),
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": src_loc.id,
            "allowed_location_ids": [(6, 0, [src_loc.id])],
            "default_location_dest_id": dest_loc.id,
            "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            "subtype_id": subtype.id,
        }
        return data

    @api.multi
    def _create_lease_customer_in_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_lease_customer_in_type())
        return pick_type

    @api.multi
    def _create_lease_customer_out_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_lease_customer_out_type())
        return pick_type

    @api.multi
    def _create_lease_supplier_in_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_lease_supplier_in_type())
        return pick_type

    @api.multi
    def _create_lease_supplier_out_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_lease_supplier_out_type())
        return pick_type

    @api.multi
    def button_create_customer_in_lease_type(self):
        for wh in self:
            pick_type = wh._create_lease_customer_in_type()
            wh.lease_customer_in_type_id = pick_type.id

    @api.multi
    def button_create_customer_out_lease_type(self):
        for wh in self:
            pick_type = wh._create_lease_customer_out_type()
            wh.lease_customer_out_type_id = pick_type.id

    @api.multi
    def button_create_supplier_in_lease_type(self):
        for wh in self:
            pick_type = wh._create_lease_supplier_in_type()
            wh.lease_supplier_in_type_id = pick_type.id

    @api.multi
    def button_create_supplier_out_lease_type(self):
        for wh in self:
            pick_type = wh._create_lease_supplier_out_type()
            wh.lease_supplier_out_type_id = pick_type.id

    @api.model
    def create(self, values):
        _super = super(StockWarehouse, self)
        new_wh = _super.create(values)

        lease_cust_in_type = new_wh._create_lease_customer_in_type()
        lease_cust_out_type = new_wh._create_lease_customer_out_type()
        lease_supp_in_type = new_wh._create_lease_supplier_in_type()
        lease_supp_out_type = new_wh._create_lease_supplier_out_type()

        new_wh.write(
            {
                "lease_customer_in_type_id": lease_cust_in_type.id,
                "lease_customer_out_type_id": lease_cust_out_type.id,
                "lease_supplier_in_type_id": lease_supp_in_type.id,
                "lease_supplier_out_type_id": lease_supp_out_type.id,
            }
        )

        lease_cust_in_route = new_wh._create_lease_customer_in_route_id()
        lease_cust_out_route = new_wh._create_lease_customer_out_route_id()
        lease_supp_in_route = new_wh._create_lease_supplier_in_route_id()
        lease_supp_out_route = new_wh._create_lease_supplier_out_route_id()

        new_wh.write(
            {
                "lease_customer_in_route_id": lease_cust_in_route.id,
                "lease_customer_out_route_id": lease_cust_out_route.id,
                "lease_supplier_in_route_id": lease_supp_in_route.id,
                "lease_supplier_out_route_id": lease_supp_out_route.id,
                "route_ids": [
                    (4, lease_cust_in_route.id),
                    (4, lease_cust_out_route.id),
                    (4, lease_supp_in_route.id),
                    (4, lease_supp_out_route.id),
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
            src_loc = self._get_lease_in_src_location()[new_reception_step]
            dest_loc = self._get_lease_in_dest_location()[new_reception_step]
            res_supp = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.lease_customer_in_type_id.write(res_supp)
            warehouse.lease_customer_in_route_id.pull_ids.unlink()
            warehouse.lease_customer_in_route_id.write(
                {
                    "pull_ids": warehouse._prepare_lease_customer_in_pull_rule(
                        new_reception_step
                    )
                }
            )
            warehouse.lease_supplier_in_type_id.write(res_supp)
            warehouse.lease_supplier_in_route_id.pull_ids.unlink()
            warehouse.lease_supplier_in_route_id.write(
                {
                    "pull_ids": warehouse._prepare_lease_supplier_in_pull_rule(
                        new_reception_step
                    )
                }
            )
        if new_delivery_step:
            src_loc = self._get_lease_out_src_location()[new_delivery_step]
            dest_loc = self._get_lease_out_dest_location()[new_delivery_step]
            res_cust = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.lease_customer_out_type_id.write(res_cust)
            warehouse.lease_customer_out_route_id.push_ids.unlink()
            warehouse.lease_customer_out_route_id.write(
                {
                    "push_ids": warehouse._prepare_lease_customer_out_push_rule(
                        new_delivery_step
                    )
                }
            )
            warehouse.lease_supplier_out_type_id.write(res_cust)
            warehouse.lease_supplier_out_route_id.push_ids.unlink()
            warehouse.lease_supplier_out_route_id.write(
                {
                    "push_ids": warehouse._prepare_lease_supplier_out_push_rule(
                        new_delivery_step
                    )
                }
            )
        return True

    @api.multi
    def _prepare_lease_customer_in_pull_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.reception_steps

        if step in ["one_step", "two_steps", "three_steps"]:
            return result
        else:
            src_loc = self.wh_transit_in_loc_id
            dest_loc = self.env["ir.property"].get(
                "customer_lease_location_id", "res.partner"
            )
            pick_type1 = self.lease_customer_in_type_id
            pick_type2 = self.transit_in_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ": Lease Customer In",
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
    def _prepare_lease_customer_out_push_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.delivery_steps

        if step in ["ship_only", "pick_ship", "pick_pack_ship"]:
            return result
        else:
            src_loc = self.wh_transit_out_loc_id
            dest_loc = self.env["ir.property"].get(
                "customer_lease_location_id", "res.partner"
            )
            pick_type1 = self.lease_customer_out_type_id
            pick_type2 = self.transit_out_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ": Lease Customer Out",
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
    def _prepare_lease_supplier_in_pull_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.reception_steps

        if step in ["one_step", "two_steps", "three_steps"]:
            return result
        else:
            src_loc = self.wh_transit_in_loc_id
            dest_loc = self.env["ir.property"].get(
                "supplier_lease_location_id", "res.partner"
            )
            pick_type1 = self.lease_supplier_in_type_id
            pick_type2 = self.transit_in_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ": Lease Supplier In",
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
    def _prepare_lease_supplier_out_push_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.delivery_steps

        if step in ["ship_only", "pick_ship", "pick_pack_ship"]:
            return result
        else:
            src_loc = self.wh_transit_out_loc_id
            dest_loc = self.env["ir.property"].get(
                "supplier_lease_location_id", "res.partner"
            )
            pick_type1 = self.lease_supplier_out_type_id
            pick_type2 = self.transit_out_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ": Lease Supplier Out",
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
    def _prepare_lease_customer_in_route_id(self):
        self.ensure_one()
        return {
            "name": self.name + ": Lease Customer In",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "pull_ids": self._prepare_lease_customer_in_pull_rule(),
        }

    @api.multi
    def _prepare_lease_customer_out_route_id(self):
        self.ensure_one()
        return {
            "name": self.name + ": Lease Customer Out",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "push_ids": self._prepare_lease_customer_out_push_rule(),
        }

    @api.multi
    def _prepare_lease_supplier_in_route_id(self):
        self.ensure_one()
        return {
            "name": self.name + ": Lease Supplier In",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "pull_ids": self._prepare_lease_supplier_in_pull_rule(),
        }

    @api.multi
    def _prepare_lease_supplier_out_route_id(self):
        self.ensure_one()
        return {
            "name": self.name + ": Lease Supplier Out",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "push_ids": self._prepare_lease_supplier_out_push_rule(),
        }

    @api.multi
    def _create_lease_customer_in_route_id(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_lease_customer_in_route_id())

    @api.multi
    def _create_lease_customer_out_route_id(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_lease_customer_out_route_id())

    @api.multi
    def _create_lease_supplier_in_route_id(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_lease_supplier_in_route_id())

    @api.multi
    def _create_lease_supplier_out_route_id(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_lease_supplier_out_route_id())

    @api.multi
    def button_create_lease_customer_in_route(self):
        for wh in self:
            route = self._create_lease_customer_in_route_id()
            wh.write(
                {
                    "lease_customer_in_route_id": route.id,
                }
            )

    @api.multi
    def button_create_lease_customer_out_route(self):
        for wh in self:
            route = self._create_lease_customer_out_route_id()
            wh.write(
                {
                    "lease_customer_out_route_id": route.id,
                }
            )

    @api.multi
    def button_create_lease_supplier_in_route(self):
        for wh in self:
            route = self._create_lease_supplier_in_route_id()
            wh.write(
                {
                    "lease_supplier_in_route_id": route.id,
                }
            )

    @api.multi
    def button_create_lease_supplier_out_route(self):
        for wh in self:
            route = self._create_lease_supplier_out_route_id()
            wh.write(
                {
                    "lease_supplier_out_route_id": route.id,
                }
            )
