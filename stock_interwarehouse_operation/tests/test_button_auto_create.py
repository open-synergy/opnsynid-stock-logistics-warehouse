# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import BaseInterwarehouseOperation


class TestButtonAutoCreate(BaseInterwarehouseOperation):

    def test_button_auto_create(self):
        # Case 1 : Check Error Route Inter-Warehouse Pull 1
        self.create_route_interwarehouse_pull_error_1()

        # Case 2 : Check Error Route Inter-Warehouse Push 1
        self.create_route_interwarehouse_push_error_1()

        # Case 3 : Check Create Transit Pull
        self.create_transit_pull()
        self.assertIsNotNone(
            self.warehouse.transit_pull_loc_id)

        # Case 4 : Check Create Transit Push
        self.create_transit_push()
        self.assertIsNotNone(
            self.warehouse.transit_push_loc_id)

        # Case 5 : Check Error Route Inter-Warehouse Pull 2
        self.create_route_interwarehouse_pull_error_2()

        # Case 6 : Check Error Route Inter-Warehouse Push 2
        self.create_route_interwarehouse_push_error_2()

        # Case 7 : Check Create Inter-Warehouse Out Type
        self.create_type_interwarehouse_out()
        self.assertIsNotNone(
            self.warehouse.interwarehouse_out_type_id)

        # Case 8 : Check Create Inter-Warehouse In Type
        self.create_type_interwarehouse_in()
        self.assertIsNotNone(
            self.warehouse.interwarehouse_in_type_id)

        # Case 9 : Check Create Route Inter-Warehouse Pull
        self.create_route_interwarehouse_pull()
        self.assertIsNotNone(
            self.warehouse.interwarehouse_out_type_id)

        # Case 10 : Check Create Route Inter-Warehouse Push
        self.create_route_interwarehouse_push()
        self.assertIsNotNone(
            self.warehouse.interwarehouse_in_type_id)
