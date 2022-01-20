# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import itertools

from .base import BaseInterwarehouseOperation


class TestButtonAutoCreate(BaseInterwarehouseOperation):
    def test_button_auto_create(self):
        # Case 1 : Check Create Transit Pull
        self.create_transit_pull()
        self.assertIsNotNone(self.warehouse.transit_pull_loc_id)

        # Case 2 : Check Create Transit Push
        self.create_transit_push()
        self.assertIsNotNone(self.warehouse.transit_push_loc_id)

        # Case 3 : Check Create Inter-Warehouse Out Type
        self.create_type_interwarehouse_out()
        self.assertIsNotNone(self.warehouse.interwarehouse_out_type_id)

        # Case 4 : Check Create Inter-Warehouse In Type
        self.create_type_interwarehouse_in()
        self.assertIsNotNone(self.warehouse.interwarehouse_in_type_id)

        # Case 5 : Check Create Route Inter-Warehouse Pull
        self.create_route_interwarehouse_pull()
        self.assertIsNotNone(self.warehouse.interwarehouse_out_type_id)

        # Case 6 : Check Create Route Inter-Warehouse Push
        self.create_route_interwarehouse_push()
        self.assertIsNotNone(self.warehouse.interwarehouse_in_type_id)

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

    def test_resupply(self):
        wh1 = self.create_wh(
            {
                "name": "X WH 1",
                "code": "X1",
            }
        )

        wh2 = self.create_wh(
            {
                "name": "X WH 2",
                "code": "X2",
            }
        )

        wh3 = self.create_wh(
            {
                "name": "X WH 3",
                "code": "X3",
                "resupply_wh_ids": [(6, 0, [wh1.id, wh2.id])],
            }
        )

        wh4 = self.create_wh(
            {
                "name": "X WH 4",
                "code": "X4",
            }
        )

        self.edit_wh(
            wh3,
            {
                "resupply_wh_ids": [(6, 0, [wh4.id, wh2.id])],
            },
        )
