# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class BaseOtherReceiptOperation(TransactionCase):
    def setUp(self):
        super(BaseOtherReceiptOperation, self).setUp()
        self.obj_wh = self.env["stock.warehouse"]

    def create_wh(self, values):
        wh = self.obj_wh.create(values)
        self.assertIsNotNone(wh.other_receipt_type_id)
        self._check_type_other_receipt(wh)
        self.assertIsNotNone(wh.other_receipt_route_id)
        self._check_wh_routes(wh)
        return wh

    def edit_wh(self, wh, values):
        wh.write(values)
        self._check_type_other_receipt(wh)
        self._check_wh_routes(wh)
        return wh

    def _check_wh_routes(self, wh):
        self.assertIn(wh.other_receipt_route_id.id, wh.route_ids.ids)

    def _check_type_other_receipt(self, wh):
        supp_loc = self.env["ir.property"].get("property_stock_supplier", "res.partner")
        if wh.reception_steps in ["one_step", "two_steps", "three_steps"]:
            self.assertEqual(wh.other_receipt_type_id.default_location_src_id, supp_loc)
        else:
            self.assertEqual(
                wh.other_receipt_type_id.default_location_src_id,
                wh.wh_transit_in_loc_id,
            )
        if wh.reception_steps in ["one_step", "transit_one_step"]:
            self.assertEqual(
                wh.other_receipt_type_id.default_location_dest_id, wh.lot_stock_id
            )
        else:
            self.assertEqual(
                wh.other_receipt_type_id.default_location_dest_id,
                wh.wh_input_stock_loc_id,
            )
