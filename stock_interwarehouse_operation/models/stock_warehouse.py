# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    interwarehouse_in_type_id = fields.Many2one(
        string="Inter-Warehouse In Type",
        comodel_name="stock.picking.type"
    )
    interwarehouse_out_type_id = fields.Many2one(
        string="Inter-Warehouse Out Type",
        comodel_name="stock.picking.type"
    )
    transit_pull_loc_id = fields.Many2one(
        string="Transit Pull Location",
        comodel_name="stock.location"
    )
    transit_push_loc_id = fields.Many2one(
        string="Transit Push Location",
        comodel_name="stock.location"
    )
    inter_warehouse_pull_route_id = fields.Many2one(
        string="Inter-Warehouse Pull Route",
        comodel_name="stock.location.route"
    )
    inter_warehouse_push_route_id = fields.Many2one(
        string="Inter-Warehouse Push Route",
        comodel_name="stock.location.route"
    )

    @api.multi
    def _prepare_location_pull(self):
        self.ensure_one()
        parent_location = self.view_location_id
        return {
            "name": "Transit Pull",
            "location_id": parent_location.id,
            "usage": "transit",
            "active": True
        }

    @api.multi
    def _create_location_pull(self):
        self.ensure_one()
        obj_stock_location = self.env['stock.location']
        location = obj_stock_location.create(
            self._prepare_location_pull())
        return location

    @api.multi
    def _prepare_location_push(self):
        self.ensure_one()
        parent_location = self.view_location_id
        return {
            "name": "Transit Push",
            "location_id": parent_location.id,
            "usage": "transit",
            "active": True
        }

    @api.multi
    def _create_location_push(self):
        self.ensure_one()
        obj_stock_location = self.env['stock.location']
        location = obj_stock_location.create(
            self._prepare_location_push())
        return location

    @api.multi
    def _prepare_interwarehouse_in_sequence(self):
        self.ensure_one()
        return {
            "name": self.code + " Inter-Warehouse In",
            "prefix": self.code + "/IWI/",
            "padding": 6
        }

    @api.multi
    def _create_interwarehouse_in_sequence(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        sequence = obj_sequence.create(
            self._prepare_interwarehouse_in_sequence())
        return sequence

    @api.multi
    def _prepare_interwarehouse_out_sequence(self):
        self.ensure_one()
        return {
            "name": self.code + " Inter-Warehouse Out",
            "prefix": self.code + "/IWO/",
            "padding": 6
        }

    @api.multi
    def _create_interwarehouse_out_sequence(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        sequence = obj_sequence.create(
            self._prepare_interwarehouse_out_sequence())
        return sequence

    @api.multi
    def _prepare_interwarehouse_in_type(self):
        self.ensure_one()
        location_dest = self.lot_stock_id
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
        picking_type = obj_type.create(
            self._prepare_interwarehouse_in_type())
        return picking_type

    @api.multi
    def _prepare_interwarehouse_out_type(self):
        self.ensure_one()
        location_src = self.lot_stock_id
        sequence = self._create_interwarehouse_out_sequence()
        return {
            "name": "Inter-Warehouse In",
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
        picking_type = obj_type.create(
            self._prepare_interwarehouse_in_type())
        return picking_type

    @api.multi
    def _prepare_route_interwarehouse_push(self):
        self.ensure_one()
        code = self.code
        location = self.lot_stock_id
        transit_loc = self.transit_push_loc_id and \
            self.transit_push_loc_id or \
            self._create_location_pull()
        in_type = self.interwarehouse_in_type_id and \
            self.interwarehouse_in_type_id or \
            self._create_type_interwarehouse_in()
        return {
            "name": self.code + ":Inter-Warehouse Push",
            "product_categ_selectable": True,
            "product_selectable": False,
            "warehouse_selectable": False,
            "sale_selectable": False,
            "push_ids": [(0, 0, {
                "name": code + ": Transit Push > " + code + ": Stock",
                "location_from_id": transit_loc.id,
                "location_dest_id": location.id,
                "picking_type_id": in_type.id,
                "auto": "manual",
            })]}

    @api.multi
    def _create_route_interwarehouse_push(self):
        self.ensure_one()
        obj_stock_location_route = self.env["stock.location.route"]
        route = obj_stock_location_route.create(
            self._prepare_route_interwarehouse_push())
        return route

    @api.multi
    def _prepare_route_interwarehouse_pull(self):
        self.ensure_one()
        code = self.code
        location = self.lot_stock_id
        transit_loc = self.transit_pull_loc_id and \
            self.transit_pull_loc_id or \
            self._create_location_pull()
        out_type = self.interwarehouse_out_type_id and \
            self.interwarehouse_out_type_id or \
            self._create_type_interwarehouse_out()
        return {
            "name": self.code + ":Inter-Warehouse Push",
            "product_categ_selectable": True,
            "product_selectable": False,
            "warehouse_selectable": False,
            "sale_selectable": False,
            "pull_ids": [(0, 0, {
                "name": code + ": Transit Pull < " + code + ": Stock",
                "location_id": transit_loc.id,
                "action": "move",
                "picking_type_id": out_type.id,
                "location_src_id": location.id
            })]}

    @api.multi
    def _create_route_interwarehouse_pull(self):
        self.ensure_one()
        obj_stock_location_route = self.env["stock.location.route"]
        route = obj_stock_location_route.create(
            self._prepare_route_interwarehouse_pull())
        return route

    @api.multi
    def button_auto_create(self):
        self.ensure_one()
        button_type = self._context.get('button_type', False)

        if button_type == 'transit_pull':
            if not self.transit_pull_loc_id:
                location = self._create_location_pull()
                self.transit_pull_loc_id = location.id

        if button_type == 'transit_push':
            if not self.transit_push_loc_id:
                location = self._create_location_push()
                self.transit_push_loc_id = location.id

        if button_type == 'type_interwarehouse_in':
            if not self.interwarehouse_in_type_id:
                picking_type = self._create_type_interwarehouse_in()
                self.interwarehouse_in_type_id = picking_type.id

        if button_type == 'type_interwarehouse_out':
            if not self.interwarehouse_out_type_id:
                picking_type = self._create_type_interwarehouse_out()
                self.interwarehouse_out_type_id = picking_type.id

        if button_type == 'route_interwarehouse_pull':
            if not self.inter_warehouse_pull_route_id:
                route = self._create_route_interwarehouse_pull()
                if route:
                    self.inter_warehouse_pull_route_id = route.id

        if button_type == 'route_interwarehouse_push':
            if not self.inter_warehouse_push_route_id:
                route = self._create_route_interwarehouse_push()
                if route:
                    self.inter_warehouse_push_route_id = route.id
        return True

    @api.model
    def _create_resupply_routes(
            self, warehouse, supplier_warehouses,
            default_resupply_wh):
        super(StockWarehouse, self)._create_resupply_routes(
            warehouse, supplier_warehouses, default_resupply_wh)

        for wh in supplier_warehouses:
            if not wh.transit_pull_loc_id.id \
                    or not warehouse.interwarehouse_in_type_id:
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
                rules.write({
                    "picking_type_id": warehouse.interwarehouse_in_type_id.id,
                    "location_src_id": wh.transit_pull_loc_id.id,
                })
