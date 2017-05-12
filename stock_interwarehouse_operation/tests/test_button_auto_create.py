# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import BaseInterwarehouseOperation


class TestButtonAutoCreate(BaseInterwarehouseOperation):

    def test_button_auto_create(self):
        # Case 1 : Check Create Transit Pull
        self.create_transit_pull()
        self.assertIsNotNone(
            self.warehouse.transit_pull_loc_id)

        # Case 2 : Check Create Transit Push
        self.create_transit_push()
        self.assertIsNotNone(
            self.warehouse.transit_push_loc_id)

        # Case 3 : Check Create Inter-Warehouse Out Type
        self.create_type_interwarehouse_out()
        self.assertIsNotNone(
            self.warehouse.interwarehouse_out_type_id)

        # Case 4 : Check Create Inter-Warehouse In Type
        self.create_type_interwarehouse_in()
        self.assertIsNotNone(
            self.warehouse.interwarehouse_in_type_id)

        # Case 5 : Check Create Route Inter-Warehouse Pull
        self.create_route_interwarehouse_pull()
        self.assertIsNotNone(
            self.warehouse.interwarehouse_out_type_id)

        # Case 6 : Check Create Route Inter-Warehouse Push
        self.create_route_interwarehouse_push()
        self.assertIsNotNone(
            self.warehouse.interwarehouse_in_type_id)
