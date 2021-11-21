# -*- coding: utf-8 -*-
# Copyright 2021 PT. Simetri Sinergi Indonesia
# Copyright 2021 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools.translate import _


class StockWarehouse(models.Model):
    _name = "stock.warehouse"
    _inherit = "stock.warehouse"

    employee_in_type_id = fields.Many2one(
        string="Employee Equipment In Type",
        comodel_name="stock.picking.type"
    )

    employee_out_type_id = fields.Many2one(
        string="Employee Equipment Out Type",
        comodel_name="stock.picking.type"
    )

    employee_in_route_id = fields.Many2one(
        string="Employee Equipment In Route",
        comodel_name="stock.location.route"
    )

    employee_out_route_id = fields.Many2one(
        string="Employee Equipment Out Route",
        comodel_name="stock.location.route"
    )

    @api.multi
    def _prepare_employee_in_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Employee Equipment In",
            "prefix":  "EMI-" + self.code + "/",
            "padding": 6
        }
        return data

    @api.multi
    def _prepare_employee_out_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Employee Equipment Out",
            "prefix":  "EMO-" + self.code + "/",
            "padding": 6
        }
        return data

    @api.multi
    def _get_employee_in_src_location(self):
        self.ensure_one()
        employee_loc = self.env["ir.property"].get(
            "property_stock_employee_id",
            "res.partner")
        return {
            "one_step": employee_loc,
            "two_steps": employee_loc,
            "three_steps": employee_loc,
            "transit_one_step": self.wh_transit_in_loc_id,
            "transit_two_steps": self.wh_transit_in_loc_id,
            "transit_three_steps": self.wh_transit_in_loc_id,
        }

    @api.multi
    def _get_employee_in_dest_location(self):
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
    def _get_employee_out_src_location(self):
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
    def _get_employee_out_dest_location(self):
        self.ensure_one()
        employee_loc = self.env["ir.property"].get(
            "property_stock_employee_id",
            "res.partner")
        return {
            "ship_only": employee_loc,
            "pick_ship": employee_loc,
            "pick_pack_ship": employee_loc,
            "ship_transit": self.wh_transit_out_loc_id,
            "pick_ship_transit": self.wh_transit_out_loc_id,
            "pick_pack_ship_transit": self.wh_transit_out_loc_id,
        }

    @api.multi
    def _prepare_employee_in_type(self):
        self.ensure_one()
        obj_sequence = self.env['ir.sequence']
        if self.reception_steps in [
                "one_step", "two_steps", "three_steps"]:
            src_loc = self.env["ir.property"].get(
                "property_stock_employee_id",
                "res.partner")
        else:
            src_loc = self.wh_transit_in_loc_id
        if self.reception_steps in [
                "one_step", "transit_one_step"]:
            dest_loc = self.lot_stock_id
        else:
            dest_loc = self.wh_input_stock_loc_id

        sequence = obj_sequence.create(
            self._prepare_employee_in_sequence())

        subtype_id = \
            self.env.ref(
                "stock_employee_equipment_operation.employee_in_subtype")

        data = {
            "name": _("Employee Equipment In"),
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
    def _prepare_employee_out_type(self):
        self.ensure_one()
        obj_sequence = self.env['ir.sequence']
        if self.delivery_steps in [
                "ship_only", "ship_transit"]:
            src_loc = self.lot_stock_id
        else:
            src_loc = self.wh_output_stock_loc_id
        if self.delivery_steps in [
                "ship_only", "pick_ship", "pick_pack_ship"]:
            dest_loc = self.env["ir.property"].get(
                "property_stock_employee_id",
                "res.partner")
        else:
            dest_loc = self.wh_transit_out_loc_id

        sequence = obj_sequence.create(
            self._prepare_employee_out_sequence())

        subtype_id = \
            self.env.ref(
                "stock_employee_equipment_operation.employee_out_subtype")

        data = {
            "name": _("Employee Equipment Out"),
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
    def _create_employee_in_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(
            self._prepare_employee_in_type())
        return pick_type

    @api.multi
    def _create_employee_out_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(
            self._prepare_employee_out_type())
        return pick_type

    @api.multi
    def button_create_employee_in_type(self):
        for wh in self:
            pick_type = wh._create_employee_in_type()
            wh.employee_in_type_id = pick_type.id

    @api.multi
    def button_create_employee_out_type(self):
        for wh in self:
            pick_type = wh._create_employee_out_type()
            wh.employee_out_type_id = pick_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        employee_in_type = new_wh._create_employee_in_type()
        employee_out_type = new_wh._create_employee_out_type()
        new_wh.write({
            "employee_in_type_id": employee_in_type.id,
            "employee_out_type_id": employee_out_type.id,
        })
        employee_in_route =\
            new_wh._create_route_employee_in()
        employee_out_route =\
            new_wh._create_route_employee_out()
        new_wh.write({
            "employee_in_route_id": employee_in_route.id,
            "employee_out_route_id": employee_out_route.id,
            "route_ids": [
                (4, employee_in_route.id),
                (4, employee_out_route.id)
            ],
        })
        return new_wh

    @api.multi
    def change_route(
            self, warehouse, new_reception_step=False,
            new_delivery_step=False):
        super(StockWarehouse, self).change_route(
            warehouse, new_reception_step=new_reception_step,
            new_delivery_step=new_delivery_step)
        if new_reception_step:
            src_loc = self._get_employee_in_src_location()[
                new_reception_step]
            dest_loc = self._get_employee_in_dest_location()[
                new_reception_step]
            res_supp = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.employee_in_type_id.write(res_supp)
            warehouse.employee_in_route_id.pull_ids.unlink()
            warehouse.employee_in_route_id.write({
                "pull_ids": warehouse._prepare_employee_in_pull_rule(
                    new_reception_step)})
        if new_delivery_step:
            src_loc = self._get_employee_out_src_location()[
                new_delivery_step]
            dest_loc = self._get_employee_out_dest_location()[
                new_delivery_step]
            res_cust = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.employee_out_type_id.write(res_cust)
            warehouse.employee_out_route_id.push_ids.unlink()
            warehouse.employee_out_route_id.write({
                "push_ids": warehouse._prepare_employee_out_push_rule(
                    new_delivery_step)})
        return True

    @api.multi
    def _prepare_employee_in_pull_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.reception_steps

        if step in [
                "one_step", "two_steps", "three_steps"]:
            return result
        else:
            src_loc = self.wh_transit_in_loc_id
            dest_loc = self.env["ir.property"].get(
                "property_stock_employee_id",
                "res.partner")
            pick_type1 = self.employee_in_type_id
            pick_type2 = self.transit_in_type_id
            result.append((0, 0, {
                "name": self.code + ":  Employee Equipment In",
                "location_id": src_loc.id,
                "warehouse_id": self.id,
                "action": "move",
                "location_src_id": dest_loc.id,
                "picking_type_id": pick_type1.id,
                "procure_method": "make_to_stock",
                "picking_type_ids": [(6, 0, [pick_type2.id])],
            }))
        return result

    @api.multi
    def _prepare_employee_out_push_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.delivery_steps

        if step in [
                "ship_only", "pick_ship", "pick_pack_ship"]:
            return result
        else:
            src_loc = self.wh_transit_out_loc_id
            dest_loc = self.env["ir.property"].get(
                "property_stock_employee_id",
                "res.partner")
            pick_type1 = self.employee_out_type_id
            pick_type2 = self.transit_out_type_id
            result.append((0, 0, {
                "name": self.code + ":  Employee Equipment Out",  # TODO
                "location_from_id": src_loc.id,
                "location_dest_id": dest_loc.id,
                "picking_type_id": pick_type2.id,
                "auto": "manual",
                "picking_type_ids": [(6, 0, [pick_type1.id])],
            }))
        return result

    @api.multi
    def _prepare_route_employee_in(self):
        self.ensure_one()
        return {
            "name": self.name + ": Employee Equipment In",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "pull_ids": self._prepare_employee_in_pull_rule(),
        }

    @api.multi
    def _prepare_route_employee_out(self):
        self.ensure_one()
        return {
            "name": self.name + ": Employee Equipment Out",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "push_ids": self._prepare_employee_out_push_rule(),
        }

    @api.multi
    def _create_route_employee_in(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(
            self._prepare_route_employee_in())

    @api.multi
    def _create_route_employee_out(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(
            self._prepare_route_employee_out())

    @api.multi
    def button_create_employee_in_route(self):
        for wh in self:
            route = self._create_route_employee_in()
            wh.write({
                "employee_in_route_id": route.id,
            })

    @api.multi
    def button_create_employee_out_route(self):
        for wh in self:
            route = self._create_route_employee_out()
            wh.write({
                "employee_out_route_id": route.id,
            })
