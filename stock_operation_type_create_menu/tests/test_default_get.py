# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBaseTypeCreateMenu


class TestDefaultGet(TestBaseTypeCreateMenu):
    def test_default_get(self):
        default = self.wiz.with_context(
            active_model="stock.picking.type",
            active_ids=[self.picking_type.id]
        ).default_get({})

        # Check Default Menu Name
        self.assertEqual(
            default['menu_name'],
            self.picking_type.name
        )

        # Check Default Sequence
        self.assertEqual(
            default['sequence'],
            1
        )
