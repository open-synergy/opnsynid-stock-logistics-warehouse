# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class BaseOtherDeliveryOperation(TransactionCase):
    def setUp(self):
        super(BaseOtherDeliveryOperation, self).setUp()
        self.obj_wh = self.env["stock.warehouse"]

    def create_wh(self, values):
        wh = self.obj_wh.create(values)
        self.assertIsNotNone(wh.other_delivery_type_id)
        self._check_type_other_delivery(wh)
        self.assertIsNotNone(wh.other_delivery_route_id)
        self._check_wh_routes(wh)
        return wh

    def edit_wh(self, wh, values):
        wh.write(values)
        self._check_type_other_delivery(wh)
        self._check_wh_routes(wh)
        return wh

    def _check_wh_routes(self, wh):
        self.assertIn(wh.other_delivery_route_id.id, wh.route_ids.ids)

    def _check_type_other_delivery(self, wh):
        cust_loc = self.env["ir.property"].get("property_stock_customer", "res.partner")
        if wh.delivery_steps in ["ship_only", "ship_transit"]:
            src1 = wh.other_delivery_type_id.default_location_src_id
            src2 = wh.lot_stock_id
            self.assertEqual(src1, src2)
        else:
            self.assertEqual(
                wh.other_delivery_type_id.default_location_src_id,
                wh.wh_output_stock_loc_id,
            )
        if wh.delivery_steps in ["ship_only", "pick_ship", "pick_pack_ship"]:
            self.assertEqual(
                wh.other_delivery_type_id.default_location_dest_id, cust_loc
            )
        else:
            self.assertEqual(
                wh.other_delivery_type_id.default_location_dest_id,
                wh.wh_transit_out_loc_id,
            )
