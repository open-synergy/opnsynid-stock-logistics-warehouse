# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class BaseInterwarehouseOperation(TransactionCase):

    def setUp(self):
        super(BaseInterwarehouseOperation, self).setUp()
        # Data
        self.warehouse =\
            self.env.ref('stock.warehouse0')

    def create_route_interwarehouse_pull_error_1(self):
        # Check Create Route Interwarehouse Pull
        # Condition : Transit Pull == False
        # Result : Raises User Error

        msg = 'Transit Pull Location Not Found'
        with self.assertRaises(UserError) as error:
            self.warehouse.with_context(
                button_type='route_interwarehouse_pull'
            ).button_auto_create()
        self.assertEqual(error.exception.message, msg)

    def create_route_interwarehouse_push_error_1(self):
        # Check Create Route Interwarehouse Push
        # Condition : Transit Push == False
        # Result : Raises User Error

        msg = 'Transit Push Location Not Found'
        with self.assertRaises(UserError) as error:
            self.warehouse.with_context(
                button_type='route_interwarehouse_push'
            ).button_auto_create()
        self.assertEqual(error.exception.message, msg)

    def create_route_interwarehouse_pull_error_2(self):
        # Check Create Route Interwarehouse Pull
        # Condition : Inter-Warehouse Out Type == False
        # Result : Raises User Error

        msg = 'Inter-Warehouse Out Picking Type Not Found'
        with self.assertRaises(UserError) as error:
            self.warehouse.with_context(
                button_type='route_interwarehouse_pull'
            ).button_auto_create()
        self.assertEqual(error.exception.message, msg)

    def create_route_interwarehouse_push_error_2(self):
        # Check Create Route Interwarehouse Push
        # Condition : Inter-Warehouse In Type == False
        # Result : Raises User Error

        msg = 'Inter-Warehouse In Picking Type Not Found'
        with self.assertRaises(UserError) as error:
            self.warehouse.with_context(
                button_type='route_interwarehouse_push'
            ).button_auto_create()
        self.assertEqual(error.exception.message, msg)

    def create_transit_pull(self):
        transit_pull = self.warehouse.with_context(
            button_type='transit_pull'
        ).button_auto_create()

        return transit_pull

    def create_transit_push(self):
        transit_push = self.warehouse.with_context(
            button_type='transit_push'
        ).button_auto_create()

        return transit_push

    def create_type_interwarehouse_out(self):
        interwarehouse_out = self.warehouse.with_context(
            button_type='type_interwarehouse_out'
        ).button_auto_create()

        return interwarehouse_out

    def create_type_interwarehouse_in(self):
        interwarehouse_in = self.warehouse.with_context(
            button_type='type_interwarehouse_in'
        ).button_auto_create()

        return interwarehouse_in

    def create_route_interwarehouse_pull(self):
        interwarehouse_pull = self.warehouse.with_context(
            button_type='route_interwarehouse_pull'
        ).button_auto_create()

        return interwarehouse_pull

    def create_route_interwarehouse_push(self):
        interwarehouse_push = self.warehouse.with_context(
            button_type='route_interwarehouse_push'
        ).button_auto_create()

        return interwarehouse_push

    def reset_button(self, data):
        val = self.warehouse.with_context(
            button_type=data
        ).button_reset()

        return val
