# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.translate import _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    other_delivery_type_id = fields.Many2one(
        string="Other Delivery Type", comodel_name="stock.picking.type"
    )

    other_delivery_route_id = fields.Many2one(
        string="Other Delivery Route", comodel_name="stock.location.route"
    )

    @api.multi
    def _prepare_other_delivery_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Other Delivery",
            "prefix": self.code + "/ODO/",
            "padding": 6,
        }
        return data

    @api.multi
    def _get_other_delivery_src_location(self):
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
    def _get_other_delivery_dest_location(self):
        self.ensure_one()
        cust_loc = self.env["ir.property"].get("property_stock_customer", "res.partner")
        return {
            "ship_only": cust_loc,
            "pick_ship": cust_loc,
            "pick_pack_ship": cust_loc,
            "ship_transit": self.wh_transit_out_loc_id,
            "pick_ship_transit": self.wh_transit_out_loc_id,
            "pick_pack_ship_transit": self.wh_transit_out_loc_id,
        }

    @api.multi
    def _prepare_other_delivery_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.delivery_steps in ["ship_only", "ship_transit"]:
            src_loc = self.lot_stock_id
        else:
            src_loc = self.wh_output_stock_loc_id
        if self.delivery_steps in ["ship_only", "pick_ship", "pick_pack_ship"]:
            dest_loc = self.env["ir.property"].get(
                "property_stock_customer", "res.partner"
            )
        else:
            dest_loc = self.wh_transit_out_loc_id

        sequence = obj_sequence.create(self._prepare_other_delivery_sequence())

        data = {
            "name": _("Other Delivery"),
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
    def _create_other_delivery_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_other_delivery_type())
        return pick_type

    @api.multi
    def button_create_other_delivery_type(self):
        for wh in self:
            pick_type = wh._create_other_delivery_type()
            wh.other_delivery_type_id = pick_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        other_delivery_type = new_wh._create_other_delivery_type()
        new_wh.write(
            {
                "other_delivery_type_id": other_delivery_type.id,
            }
        )
        cust_route = new_wh._create_route_other_delivery()
        new_wh.write(
            {
                "other_delivery_route_id": cust_route.id,
                "route_ids": [(4, cust_route.id)],
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
        if new_delivery_step:
            src_loc = self._get_other_delivery_src_location()[new_delivery_step]
            dest_loc = self._get_other_delivery_dest_location()[new_delivery_step]
            res_cust = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.other_delivery_type_id.write(res_cust)
            # Adjust Other Delivery Route
            warehouse.other_delivery_route_id.push_ids.unlink()
            warehouse.other_delivery_route_id.write(
                {
                    "push_ids": warehouse._prepare_other_delivery_push_rule(
                        new_delivery_step
                    )
                }
            )
        return True

    @api.multi
    def _prepare_other_delivery_push_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.delivery_steps

        if step in ["ship_only", "pick_ship", "pick_pack_ship"]:
            return result
        else:
            src_loc = self.wh_transit_out_loc_id
            dest_loc = self.env["ir.property"].get(
                "property_stock_customer", "res.partner"
            )
            pick_type1 = self.other_delivery_type_id
            pick_type2 = self.transit_out_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ":  Other Receipt 1",  # TODO
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
    def _prepare_route_other_delivery(self):
        self.ensure_one()
        return {
            "name": self.name + ": Other Delivery",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "push_ids": self._prepare_other_delivery_push_rule(),
        }

    @api.multi
    def _create_route_other_delivery(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_route_other_delivery())

    @api.multi
    def button_create_other_delivery(self):
        for wh in self:
            route = self._create_route_other_delivery()
            wh.write(
                {
                    "other_delivery_route_id": route.id,
                }
            )
