# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class BaseInterwarehouseOperation(TransactionCase):
    def setUp(self):
        super(BaseInterwarehouseOperation, self).setUp()
        self.obj_wh = self.env["stock.warehouse"]

    def create_wh(self, values):
        wh = self.obj_wh.create(values)
        self.assertIsNotNone(wh.customer_promotion_type_id)
        self._check_type_customer(wh)
        self.assertIsNotNone(wh.supplier_promotion_type_id)
        self._check_type_supplier(wh)
        self.assertIsNotNone(wh.supplier_promotion_route_id)
        self.assertIsNotNone(wh.customer_promotion_route_id)
        self._check_wh_routes(wh)
        return wh

    def edit_wh(self, wh, values):
        wh.write(values)
        self._check_type_customer(wh)
        self._check_type_supplier(wh)
        self._check_wh_routes(wh)
        return wh

    def _check_wh_routes(self, wh):
        self.assertIn(wh.customer_promotion_route_id.id, wh.route_ids.ids)
        self.assertIn(wh.supplier_promotion_route_id.id, wh.route_ids.ids)

    def _check_type_supplier(self, wh):
        supp_promotion_loc = self.env["ir.property"].get(
            "property_stock_supplier_promotion_id", "res.partner"
        )
        if wh.reception_steps in ["one_step", "two_steps", "three_steps"]:
            self.assertEqual(
                wh.supplier_promotion_type_id.default_location_src_id,
                supp_promotion_loc,
            )
        else:
            self.assertEqual(
                wh.supplier_promotion_type_id.default_location_src_id,
                wh.wh_transit_in_loc_id,
            )
        if wh.reception_steps in ["one_step", "transit_one_step"]:
            self.assertEqual(
                wh.supplier_promotion_type_id.default_location_dest_id, wh.lot_stock_id
            )
        else:
            self.assertEqual(
                wh.supplier_promotion_type_id.default_location_dest_id,
                wh.wh_input_stock_loc_id,
            )

    def _check_type_customer(self, wh):
        cust_promotion_loc = self.env["ir.property"].get(
            "property_stock_customer_promotion_id", "res.partner"
        )
        if wh.delivery_steps in ["ship_only", "ship_transit"]:
            src1 = wh.customer_promotion_type_id.default_location_src_id
            src2 = wh.lot_stock_id
            self.assertEqual(src1, src2)
        else:
            self.assertEqual(
                wh.customer_promotion_type_id.default_location_src_id,
                wh.wh_output_stock_loc_id,
            )
        if wh.delivery_steps in ["ship_only", "pick_ship", "pick_pack_ship"]:
            self.assertEqual(
                wh.customer_promotion_type_id.default_location_dest_id,
                cust_promotion_loc,
            )
        else:
            self.assertEqual(
                wh.customer_promotion_type_id.default_location_dest_id,
                wh.wh_transit_out_loc_id,
            )
