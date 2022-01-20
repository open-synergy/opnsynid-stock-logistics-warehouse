# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    window_action_id = fields.Many2one(
        string="Window Action", comodel_name="ir.actions.act_window"
    )

    menu_id = fields.Many2one(string="Menu", comodel_name="ir.ui.menu")

    @api.multi
    def button_reset_menu(self):
        obj_act_window = self.env["ir.actions.act_window"]
        obj_ir_menu = self.env["ir.ui.menu"]

        if self.window_action_id:
            window_action_id = self.window_action_id.id
            self.window_action_id = False
            criteria = [("id", "=", window_action_id)]
            obj_act_window.search(criteria).unlink()
        if self.menu_id:
            menu_id = self.menu_id.id
            self.menu_id = False
            criteria = [("id", "=", menu_id)]
            obj_ir_menu.search(criteria).unlink()
