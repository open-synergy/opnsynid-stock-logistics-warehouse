# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.exceptions import Warning as UserError
from openerp.tests.common import TransactionCase


class BaseInterwarehouseOperation(TransactionCase):
    def setUp(self):
        super(BaseInterwarehouseOperation, self).setUp()
        # Data
        self.warehouse = self.env.ref("stock.warehouse0")
        self.obj_wh = self.env["stock.warehouse"]

    def create_route_interwarehouse_pull_error_1(self):
        # Check Create Route Interwarehouse Pull
        # Condition : Transit Pull == False
        # Result : Raises User Error

        msg = "Transit Pull Location Not Found"
        with self.assertRaises(UserError) as error:
            self.warehouse.with_context(
                button_type="route_interwarehouse_pull"
            ).button_auto_create()
        self.assertEqual(error.exception.message, msg)

    def create_route_interwarehouse_push_error_1(self):
        # Check Create Route Interwarehouse Push
        # Condition : Transit Push == False
        # Result : Raises User Error

        msg = "Transit Push Location Not Found"
        with self.assertRaises(UserError) as error:
            self.warehouse.with_context(
                button_type="route_interwarehouse_push"
            ).button_auto_create()
        self.assertEqual(error.exception.message, msg)

    def create_route_interwarehouse_pull_error_2(self):
        # Check Create Route Interwarehouse Pull
        # Condition : Inter-Warehouse Out Type == False
        # Result : Raises User Error

        msg = "Inter-Warehouse Out Picking Type Not Found"
        with self.assertRaises(UserError) as error:
            self.warehouse.with_context(
                button_type="route_interwarehouse_pull"
            ).button_auto_create()
        self.assertEqual(error.exception.message, msg)

    def create_route_interwarehouse_push_error_2(self):
        # Check Create Route Interwarehouse Push
        # Condition : Inter-Warehouse In Type == False
        # Result : Raises User Error

        msg = "Inter-Warehouse In Picking Type Not Found"
        with self.assertRaises(UserError) as error:
            self.warehouse.with_context(
                button_type="route_interwarehouse_push"
            ).button_auto_create()
        self.assertEqual(error.exception.message, msg)

    def create_transit_pull(self):
        transit_pull = self.warehouse.with_context(
            button_type="transit_pull"
        ).button_auto_create()

        return transit_pull

    def create_transit_push(self):
        transit_push = self.warehouse.with_context(
            button_type="transit_push"
        ).button_auto_create()

        return transit_push

    def create_type_interwarehouse_out(self):
        interwarehouse_out = self.warehouse.with_context(
            button_type="type_interwarehouse_out"
        ).button_auto_create()

        return interwarehouse_out

    def create_type_interwarehouse_in(self):
        interwarehouse_in = self.warehouse.with_context(
            button_type="type_interwarehouse_in"
        ).button_auto_create()

        return interwarehouse_in

    def create_route_interwarehouse_pull(self):
        interwarehouse_pull = self.warehouse.with_context(
            button_type="route_interwarehouse_pull"
        ).button_auto_create()

        return interwarehouse_pull

    def create_route_interwarehouse_push(self):
        interwarehouse_push = self.warehouse.with_context(
            button_type="route_interwarehouse_push"
        ).button_auto_create()

        return interwarehouse_push

    def reset_button(self, data):
        val = self.warehouse.with_context(button_type=data).button_reset()

        return val

    def create_wh(self, values):
        wh = self.obj_wh.create(values)
        self.assertIsNotNone(wh.interwarehouse_in_type_id)
        self._check_type_in(wh)
        self.assertIsNotNone(wh.interwarehouse_out_type_id)
        self._check_type_out(wh)
        self.assertIsNotNone(wh.transit_pull_loc_id)
        self.assertIsNotNone(wh.transit_push_loc_id)
        self.assertIsNotNone(wh.inter_warehouse_pull_route_id)
        self.assertIsNotNone(wh.inter_warehouse_push_route_id)
        self._check_wh_routes(wh)
        return wh

    def edit_wh(self, wh, values):
        wh.write(values)
        self._check_type_in(wh)
        self._check_type_out(wh)
        self._check_wh_routes(wh)
        return wh

    def _check_wh_routes(self, wh):
        for supply_wh in wh.resupply_wh_ids:
            self.assertIn(supply_wh.inter_warehouse_pull_route_id.id, wh.route_ids.ids)
            self.assertIn(wh.inter_warehouse_push_route_id.id, supply_wh.route_ids.ids)

    def _check_type_in(self, wh):
        if wh.reception_steps in ["one_step", "transit_one_step"]:
            self.assertEqual(
                wh.interwarehouse_in_type_id.default_location_dest_id, wh.lot_stock_id
            )
        else:
            self.assertEqual(
                wh.interwarehouse_in_type_id.default_location_dest_id,
                wh.wh_input_stock_loc_id,
            )
        for supply_wh in wh.resupply_wh_ids:
            swh_out = supply_wh.interwarehouse_out_type_id
            self.assertIn(
                supply_wh.transit_pull_loc_id.id,
                wh.interwarehouse_in_type_id.allowed_location_ids.ids,
            )
            self.assertIn(
                wh.transit_push_loc_id.id, swh_out.allowed_dest_location_ids.ids
            )

    def _check_type_out(self, wh):
        if wh.delivery_steps in ["ship_only", "ship_transit"]:
            self.assertEqual(
                wh.interwarehouse_out_type_id.default_location_src_id, wh.lot_stock_id
            )
        else:
            self.assertEqual(
                wh.interwarehouse_out_type_id.default_location_src_id,
                wh.wh_output_stock_loc_id,
            )
