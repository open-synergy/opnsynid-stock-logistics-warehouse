# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    interwarehouse_in_type_id = fields.Many2one(
        string="Inter-Warehouse In Type", comodel_name="stock.picking.type"
    )
    interwarehouse_out_type_id = fields.Many2one(
        string="Inter-Warehouse Out Type", comodel_name="stock.picking.type"
    )
    transit_pull_loc_id = fields.Many2one(
        string="Transit Pull Location", comodel_name="stock.location"
    )
    transit_push_loc_id = fields.Many2one(
        string="Transit Push Location", comodel_name="stock.location"
    )
    inter_warehouse_pull_route_id = fields.Many2one(
        string="Inter-Warehouse Pull Route", comodel_name="stock.location.route"
    )
    inter_warehouse_push_route_id = fields.Many2one(
        string="Inter-Warehouse Push Route", comodel_name="stock.location.route"
    )

    @api.multi
    def _prepare_location_pull(self):
        self.ensure_one()
        parent_location = self.view_location_id
        return {
            "name": "Transit Pull",
            "location_id": parent_location.id,
            "usage": "transit",
            "active": True,
        }

    @api.multi
    def _create_location_pull(self):
        self.ensure_one()
        obj_stock_location = self.env["stock.location"]
        location = obj_stock_location.create(self._prepare_location_pull())
        return location

    @api.multi
    def _prepare_location_push(self):
        self.ensure_one()
        parent_location = self.view_location_id
        return {
            "name": "Transit Push",
            "location_id": parent_location.id,
            "usage": "transit",
            "active": True,
        }

    @api.multi
    def _create_location_push(self):
        self.ensure_one()
        obj_stock_location = self.env["stock.location"]
        location = obj_stock_location.create(self._prepare_location_push())
        return location

    @api.multi
    def _prepare_interwarehouse_in_sequence(self):
        self.ensure_one()
        return {
            "name": self.code + " Inter-Warehouse In",
            "prefix": self.code + "/IWI/",
            "padding": 6,
        }

    @api.multi
    def _create_interwarehouse_in_sequence(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        sequence = obj_sequence.create(self._prepare_interwarehouse_in_sequence())
        return sequence

    @api.multi
    def _prepare_interwarehouse_out_sequence(self):
        self.ensure_one()
        return {
            "name": self.code + " Inter-Warehouse Out",
            "prefix": self.code + "/IWO/",
            "padding": 6,
        }

    @api.multi
    def _create_interwarehouse_out_sequence(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        sequence = obj_sequence.create(self._prepare_interwarehouse_out_sequence())
        return sequence

    @api.multi
    def _prepare_interwarehouse_in_type(self):
        self.ensure_one()
        location_dest = self._get_push_route_dest_location()[self.reception_steps]
        sequence = self._create_interwarehouse_in_sequence()
        return {
            "name": "Inter-Warehouse In",
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "reception",
            "default_location_dest_id": location_dest.id,
            "allowed_dest_location_ids": [(6, 0, [location_dest.id])],
        }

    @api.multi
    def _create_type_interwarehouse_in(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        picking_type = obj_type.create(self._prepare_interwarehouse_in_type())
        return picking_type

    @api.multi
    def _prepare_interwarehouse_out_type(self):
        self.ensure_one()
        location_src = self._get_pull_route_src_location()[self.delivery_steps]
        sequence = self._create_interwarehouse_out_sequence()
        return {
            "name": "Inter-Warehouse Out",
            "warehouse_id": self.id,
            "sequence_id": sequence.id,
            "code": "outgoing",
            "default_location_src_id": location_src.id,
            "allowed_location_ids": [(6, 0, [location_src.id])],
        }

    @api.multi
    def _create_type_interwarehouse_out(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        picking_type = obj_type.create(self._prepare_interwarehouse_out_type())
        return picking_type

    @api.multi
    def _get_push_route_dest_location(self):
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
    def _prepare_push_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.reception_steps
        location = self._get_push_route_dest_location().get(step, False)
        if not location:
            raise UserError(_("No location"))
        transit_loc = (
            self.transit_push_loc_id
            and self.transit_push_loc_id
            or self._create_location_pull()
        )
        in_type = (
            self.interwarehouse_in_type_id
            and self.interwarehouse_in_type_id
            or self._create_type_interwarehouse_in()
        )
        result.append(
            (
                0,
                0,
                {
                    "name": self.code + ": Transit Push > " + self.code + ": Stock",
                    "location_from_id": transit_loc.id,
                    "location_dest_id": location.id,
                    "picking_type_id": in_type.id,
                    "auto": "manual",
                },
            )
        )
        return result

    @api.multi
    def _prepare_route_interwarehouse_push(self):
        self.ensure_one()
        return {
            "name": self.name + ": Inter-Warehouse Push",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "push_ids": self._prepare_push_rule(),
        }

    @api.multi
    def _create_route_interwarehouse_push(self):
        self.ensure_one()
        obj_stock_location_route = self.env["stock.location.route"]
        route = obj_stock_location_route.create(
            self._prepare_route_interwarehouse_push()
        )
        return route

    @api.multi
    def _get_pull_route_src_location(self):
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
    def _prepare_pull_rule(self, step=False):
        self.ensure_one()
        if not step:
            step = self.delivery_steps
        location = self._get_pull_route_src_location().get(step, False)
        result = []
        if not location:
            raise UserError(_("No location"))
        transit_loc = (
            self.transit_pull_loc_id
            and self.transit_pull_loc_id
            or self._create_location_pull()
        )
        out_type = (
            self.interwarehouse_out_type_id
            and self.interwarehouse_out_type_id
            or self._create_type_interwarehouse_out()
        )
        result.append(
            (
                0,
                0,
                {
                    "name": self.code + ": Transit Pull < " + self.code + ": Stock",
                    "location_id": transit_loc.id,
                    "action": "move",
                    "picking_type_id": out_type.id,
                    "location_src_id": location.id,
                },
            )
        )
        return result

    @api.multi
    def _prepare_route_interwarehouse_pull(self):
        self.ensure_one()
        return {
            "name": self.name + ": Inter-Warehouse Pull",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "pull_ids": self._prepare_pull_rule(),
        }

    @api.multi
    def _create_route_interwarehouse_pull(self):
        self.ensure_one()
        obj_stock_location_route = self.env["stock.location.route"]
        route = obj_stock_location_route.create(
            self._prepare_route_interwarehouse_pull()
        )
        return route

    @api.multi
    def button_auto_create(self):
        self.ensure_one()
        button_type = self._context.get("button_type", False)

        if button_type == "transit_pull":
            if not self.transit_pull_loc_id:
                location = self._create_location_pull()
                self.transit_pull_loc_id = location.id

        if button_type == "transit_push":
            if not self.transit_push_loc_id:
                location = self._create_location_push()
                self.transit_push_loc_id = location.id

        if button_type == "type_interwarehouse_in":
            if not self.interwarehouse_in_type_id:
                picking_type = self._create_type_interwarehouse_in()
                self.interwarehouse_in_type_id = picking_type.id

        if button_type == "type_interwarehouse_out":
            if not self.interwarehouse_out_type_id:
                picking_type = self._create_type_interwarehouse_out()
                self.interwarehouse_out_type_id = picking_type.id

        if button_type == "route_interwarehouse_pull":
            if not self.inter_warehouse_pull_route_id:
                route = self._create_route_interwarehouse_pull()
                if route:
                    self.inter_warehouse_pull_route_id = route.id

        if button_type == "route_interwarehouse_push":
            if not self.inter_warehouse_push_route_id:
                route = self._create_route_interwarehouse_push()
                if route:
                    self.inter_warehouse_push_route_id = route.id
        return True

    @api.model
    def _create_resupply_routes(
        self, warehouse, supplier_warehouses, default_resupply_wh
    ):
        super(StockWarehouse, self)._create_resupply_routes(
            warehouse, supplier_warehouses, default_resupply_wh
        )

        for wh in supplier_warehouses:
            if not wh.transit_pull_loc_id.id or not warehouse.interwarehouse_in_type_id:
                continue

            obj_rule = self.env["procurement.rule"]
            criteria = [
                ("route_id", "in", warehouse.resupply_route_ids.ids),
                ("warehouse_id", "=", wh.id),
            ]
            rules = obj_rule.search(criteria)
            if len(rules) > 0:
                rules.unlink()
            criteria = [
                ("route_id", "in", warehouse.resupply_route_ids.ids),
                ("warehouse_id", "=", warehouse.id),
            ]
            rules = obj_rule.search(criteria)
            if len(rules) > 0:
                rules.write(
                    {
                        "picking_type_id": warehouse.interwarehouse_in_type_id.id,
                        "location_src_id": wh.transit_pull_loc_id.id,
                    }
                )

    @api.model
    def create_sequences_and_picking_types(self, warehouse):
        super(StockWarehouse, self).create_sequences_and_picking_types(warehouse)
        transit_pull_loc = warehouse._create_location_pull()
        transit_push_loc = warehouse._create_location_push()
        warehouse.write(
            {
                "transit_pull_loc_id": transit_pull_loc.id,
                "transit_push_loc_id": transit_push_loc.id,
            }
        )
        transit_in_type = warehouse._create_type_interwarehouse_in()
        transit_out_type = warehouse._create_type_interwarehouse_out()
        warehouse.write(
            {
                "interwarehouse_in_type_id": transit_in_type.id,
                "interwarehouse_out_type_id": transit_out_type.id,
            }
        )

    @api.multi
    def create_routes(self, warehouse):
        result = super(StockWarehouse, self).create_routes(warehouse)
        pull_route = warehouse._create_route_interwarehouse_pull()
        push_route = warehouse._create_route_interwarehouse_push()
        result.update(
            {
                "inter_warehouse_pull_route_id": pull_route.id,
                "inter_warehouse_push_route_id": push_route.id,
            }
        )
        return result

    @api.multi
    def change_route(
        self, warehouse, new_reception_step=False, new_delivery_step=False
    ):
        super(StockWarehouse, self).change_route(
            warehouse,
            new_reception_step=new_reception_step,
            new_delivery_step=new_delivery_step,
        )
        warehouse.inter_warehouse_pull_route_id.pull_ids.unlink()
        warehouse.inter_warehouse_pull_route_id.write(
            {
                "pull_ids": self._prepare_pull_rule(new_delivery_step),
            }
        )
        warehouse.inter_warehouse_push_route_id.push_ids.unlink()
        warehouse.inter_warehouse_push_route_id.write(
            {
                "push_ids": self._prepare_push_rule(new_reception_step),
            }
        )
        if new_reception_step:
            location_dest = self._get_push_route_dest_location()[new_reception_step]
            res_in = {
                "default_location_dest_id": location_dest.id,
                "allowed_dest_location_ids": [(6, 0, [location_dest.id])],
            }
            warehouse.interwarehouse_in_type_id.write(res_in)
        if new_delivery_step:
            location_src = self._get_pull_route_src_location()[new_delivery_step]
            res_out = {
                "default_location_src_id": location_src.id,
                "allowed_location_ids": [(6, 0, [location_src.id])],
            }
            warehouse.interwarehouse_out_type_id.write(res_out)
        return True

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        obj_wh = self.env["stock.warehouse"]
        new_wh_push_route = new_wh.inter_warehouse_push_route_id
        if not values.get("resupply_wh_ids", False):
            return new_wh

        for cmd in values.get("resupply_wh_ids"):
            if cmd[0] != 6:
                continue

            new_ids = set(cmd[2])
            for add_wh in obj_wh.browse(new_ids):
                add_wh_pull_route = add_wh.inter_warehouse_pull_route_id
                add_wh.interwarehouse_out_type_id.write(
                    {
                        "allowed_dest_location_ids": [
                            (4, new_wh.transit_push_loc_id.id)
                        ],
                    }
                )
                new_wh.interwarehouse_in_type_id.write(
                    {
                        "allowed_location_ids": [(4, add_wh.transit_pull_loc_id.id)],
                    }
                )
                new_wh.write(
                    {
                        "route_ids": [(4, add_wh_pull_route.id)],
                    }
                )
                add_wh.write(
                    {
                        "route_ids": [(4, new_wh_push_route.id)],
                    }
                )
        return new_wh

    @api.multi
    def write(self, values):
        obj_wh = self.env["stock.warehouse"]
        for warehouse in self:
            wh_push_route = warehouse.inter_warehouse_push_route_id
            if not values.get("resupply_wh_ids", False):
                continue

            for cmd in values.get("resupply_wh_ids"):
                if cmd[0] != 6:
                    continue

                new_ids = set(cmd[2])
                old_ids = set(warehouse.resupply_wh_ids.ids)
                to_remove_ids = old_ids - new_ids
                to_add_ids = new_ids - old_ids
                allowed_loc_ids = []
                wh_tpush_loc = warehouse.transit_push_loc_id
                for add_wh in obj_wh.browse(to_add_ids):
                    add_wh_pull_route = add_wh.inter_warehouse_pull_route_id
                    allowed_loc_ids.append(add_wh.transit_pull_loc_id.id)
                    add_wh.interwarehouse_out_type_id.write(
                        {
                            "allowed_dest_location_ids": [(4, wh_tpush_loc.id)],
                        }
                    )
                    warehouse.interwarehouse_in_type_id.write(
                        {
                            "allowed_location_ids": [
                                (4, add_wh.transit_pull_loc_id.id)
                            ],
                        }
                    )
                    warehouse.write(
                        {
                            "route_ids": [(4, add_wh_pull_route.id)],
                        }
                    )
                    add_wh.write(
                        {
                            "route_ids": [(4, wh_push_route.id)],
                        }
                    )
                for old_wh in obj_wh.browse(to_remove_ids):
                    old_wh_pull_route = old_wh.inter_warehouse_pull_route_id
                    if old_wh.interwarehouse_out_type_id:
                        old_wh.interwarehouse_out_type_id.write(
                            {
                                "allowed_dest_location_ids": [(3, wh_tpush_loc.id)],
                            }
                        )
                        warehouse.interwarehouse_in_type_id.write(
                            {
                                "allowed_location_ids": [
                                    (3, old_wh.transit_pull_loc_id.id)
                                ],
                            }
                        )
                    warehouse.write(
                        {
                            "route_ids": [(3, old_wh_pull_route.id)],
                        }
                    )
                    old_wh.write(
                        {
                            "route_ids": [(3, wh_push_route.id)],
                        }
                    )
        return super(StockWarehouse, self).write(values)
