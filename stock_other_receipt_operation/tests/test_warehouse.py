# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import itertools

from .base import BaseOtherReceiptOperation


class TestWarehouse(BaseOtherReceiptOperation):
    def test_warehouse_create(self):
        reception_steps = [
            "one_step",
            "two_steps",
            "three_steps",
            "transit_one_step",
            "transit_two_steps",
            "transit_three_steps",
        ]
        delivery_steps = [
            "ship_only",
            "pick_ship",
            "pick_pack_ship",
            "ship_transit",
            "pick_ship_transit",
            "pick_pack_ship_transit",
        ]
        num = 1
        for combination in itertools.product(reception_steps, delivery_steps):
            self.create_wh(
                {
                    "name": "X WH %s" % str(num),
                    "code": "X%s" % str(num),
                    "reception_steps": combination[0],
                    "delivery_steps": combination[1],
                }
            )
            num += 1

    def test_warehouse_edit(self):
        reception_steps = [
            "one_step",
            "two_steps",
            "three_steps",
            "transit_one_step",
            "transit_two_steps",
            "transit_three_steps",
        ]
        delivery_steps = [
            "ship_only",
            "pick_ship",
            "pick_pack_ship",
            "ship_transit",
            "pick_ship_transit",
            "pick_pack_ship_transit",
        ]
        num = 1
        for combination in itertools.product(reception_steps, delivery_steps):
            if num == 1:
                wh = self.create_wh(
                    {
                        "name": "X WH %s" % str(num),
                        "code": "X%s" % str(num),
                        "reception_steps": combination[0],
                        "delivery_steps": combination[1],
                    }
                )
            else:
                self.edit_wh(
                    wh,
                    {
                        "reception_steps": combination[0],
                        "delivery_steps": combination[1],
                    },
                )
            num += 1
