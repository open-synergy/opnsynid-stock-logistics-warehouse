# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBaseTypeCreateMenu


class TestCreateResetMenu(TestBaseTypeCreateMenu):
    def test_create_reset_menu(self):
        # Check menu_id & window_action_id
        # Condition :
            # If menu_id or window_action_id == True
            # Reset Menu
        if self.picking_type.menu_id.id or\
                self.picking_type.window_action_id:

            # Pressing Reset Button
            self.picking_type.button_reset_menu()

        # Check menu_id & window_action_id
        # Condition : menu_id or window_action_id == False
        self.assertEqual(
            False,
            self.picking_type.menu_id.id
        )
        self.assertEqual(
            False,
            self.picking_type.window_action_id.id
        )

        new = self.wiz.with_context(
            active_model="stock.picking.type",
            active_ids=[self.picking_type.id]
        ).new()

        new.menu_name = self.picking_type.name
        # Create Menu
        new.button_create_menu()

        # Check menu_id & window_action_id
        # Condition : menu_id or window_action_id == False
        result_menu_id = False
        result_window_action_id = False

        if self.picking_type.menu_id.id:
            result_menu_id = True
        self.assertEqual(
            True,
            result_menu_id
        )
        if self.picking_type.window_action_id.id:
            result_window_action_id = True
        self.assertEqual(
            True,
            result_window_action_id
        )
