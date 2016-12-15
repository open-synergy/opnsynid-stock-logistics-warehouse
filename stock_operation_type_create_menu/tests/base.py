# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestBaseTypeCreateMenu(TransactionCase):
    def setUp(self):
        super(TestBaseTypeCreateMenu, self).setUp()
        # Object
        self.wiz =\
            self.env['stock.operation_type_create_menu']
        self.obj_picking_type =\
            self.env['stock.picking.type']

        # Data
        self.picking_type =\
            self.env.ref('stock.picking_type_in')
