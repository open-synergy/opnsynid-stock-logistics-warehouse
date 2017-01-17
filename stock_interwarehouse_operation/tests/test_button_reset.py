# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import BaseInterwarehouseOperation


class TestButtonAutoCreate(BaseInterwarehouseOperation):
    def test_button_auto_create(self):
        self.create_transit_pull()
        self.create_transit_push()
        self.create_type_interwarehouse_out()
        self.create_type_interwarehouse_in()
        self.create_route_interwarehouse_pull()
        self.create_route_interwarehouse_push()

        # Case 1 : Reset Transit Pull
        self.reset_button('transit_pull')
        self.assertFalse(
            self.warehouse.transit_pull_loc_id)

        # Case 2 : Reset Transit Push
        self.reset_button('transit_push')
        self.assertFalse(
            self.warehouse.transit_push_loc_id)

        # Case 3 : Reset Interwarehouse In Type
        self.reset_button('type_interwarehouse_in')
        self.assertFalse(
            self.warehouse.interwarehouse_in_type_id)

        # Case 4 : Reset Interwarehouse Out Type
        self.reset_button('type_interwarehouse_out')
        self.assertFalse(
            self.warehouse.interwarehouse_out_type_id)

        # Case 5 : Reset Route Inter-Warehouse Pull
        self.reset_button('route_interwarehouse_pull')
        self.assertFalse(
            self.warehouse.inter_warehouse_pull_route_id)

        # Case 6 : Reset Route Inter-Warehouse Push
        self.reset_button('route_interwarehouse_push')
        self.assertFalse(
            self.warehouse.inter_warehouse_push_route_id)
