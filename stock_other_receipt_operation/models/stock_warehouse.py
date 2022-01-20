# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.translate import _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    other_receipt_type_id = fields.Many2one(
        string="Other Receipt Type", comodel_name="stock.picking.type"
    )

    other_receipt_route_id = fields.Many2one(
        string="Other Receipt Route", comodel_name="stock.location.route"
    )

    @api.multi
    def _prepare_other_receipt_sequence(self):
        self.ensure_one()
        data = {
            "name": self.code + " - Other Receipt",
            "prefix": self.code + "/OGR/",
            "padding": 6,
        }
        return data

    @api.multi
    def _get_other_receipt_src_location(self):
        self.ensure_one()
        supplier_loc = self.env["ir.property"].get(
            "property_stock_supplier", "res.partner"
        )
        return {
            "one_step": supplier_loc,
            "two_steps": supplier_loc,
            "three_steps": supplier_loc,
            "transit_one_step": self.wh_transit_in_loc_id,
            "transit_two_steps": self.wh_transit_in_loc_id,
            "transit_three_steps": self.wh_transit_in_loc_id,
        }

    @api.multi
    def _get_other_receipt_dest_location(self):
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
    def _prepare_other_receipt_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]
        if self.reception_steps in ["one_step", "two_steps", "three_steps"]:
            src_loc = self.env["ir.property"].get(
                "property_stock_supplier", "res.partner"
            )
        else:
            src_loc = self.wh_transit_in_loc_id
        if self.reception_steps in ["one_step", "transit_one_step"]:
            dest_loc = self.lot_stock_id
        else:
            dest_loc = self.wh_input_stock_loc_id

        sequence = obj_sequence.create(self._prepare_other_receipt_sequence())

        data = {
            "name": _("Other Receipt"),
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
    def _create_other_receipt_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        pick_type = obj_type.create(self._prepare_other_receipt_type())
        return pick_type

    @api.multi
    def button_create_other_receipt_type(self):
        for wh in self:
            pick_type = wh._create_other_receipt_type()
            wh.other_receipt_type_id = pick_type.id

    @api.model
    def create(self, values):
        new_wh = super(StockWarehouse, self).create(values)
        other_receipt_type = new_wh._create_other_receipt_type()
        new_wh.write(
            {
                "other_receipt_type_id": other_receipt_type.id,
            }
        )
        receipt_route = new_wh._create_route_other_receipt()
        new_wh.write(
            {
                "other_receipt_route_id": receipt_route.id,
                "route_ids": [(4, receipt_route.id)],
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
            src_loc = self._get_other_receipt_src_location()[new_reception_step]
            dest_loc = self._get_other_receipt_dest_location()[new_reception_step]
            res_supp = {
                "default_location_src_id": src_loc.id,
                "allowed_location_ids": [(6, 0, [src_loc.id])],
                "default_location_dest_id": dest_loc.id,
                "allowed_dest_location_ids": [(6, 0, [dest_loc.id])],
            }
            warehouse.other_receipt_type_id.write(res_supp)
            # Adjust Other Receipt Route
            warehouse.other_receipt_route_id.pull_ids.unlink()
            warehouse.other_receipt_route_id.write(
                {
                    "pull_ids": warehouse._prepare_other_receipt_pull_rule(
                        new_reception_step
                    )
                }
            )
        return True

    @api.multi
    def _prepare_other_receipt_pull_rule(self, step=False):
        self.ensure_one()
        result = []
        if not step:
            step = self.reception_steps

        if step in ["one_step", "two_steps", "three_steps"]:
            return result
        else:
            src_loc = self.wh_transit_in_loc_id
            dest_loc = self.env["ir.property"].get(
                "property_stock_supplier", "res.partner"
            )
            pick_type1 = self.other_receipt_type_id
            pick_type2 = self.transit_in_type_id
            result.append(
                (
                    0,
                    0,
                    {
                        "name": self.code + ":  Other Receipt",  # TODO
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
    def _prepare_route_other_receipt(self):
        self.ensure_one()
        return {
            "name": self.name + ": Other Receipt",
            "product_categ_selectable": False,
            "product_selectable": False,
            "warehouse_selectable": True,
            "sale_selectable": False,
            "pull_ids": self._prepare_other_receipt_pull_rule(),
        }

    @api.multi
    def _create_route_other_receipt(self):
        self.ensure_one()
        obj_route = self.env["stock.location.route"]
        return obj_route.create(self._prepare_route_other_receipt())

    @api.multi
    def button_create_other_receipt(self):
        for wh in self:
            route = self._create_route_other_receipt()
            wh.write(
                {
                    "other_receipt_route_id": route.id,
                }
            )
