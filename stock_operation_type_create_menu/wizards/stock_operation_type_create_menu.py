# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockOperationTypeCreateMenu(models.TransientModel):
    _name = 'stock.operation_type_create_menu'
    _description = 'Stock Operation Type Create Menu'

    menu_name = fields.Char(
        string="Menu Name",
        required=True
    )

    sequence = fields.Integer(
        string="Sequence"
    )

    view_ids = fields.One2many(
        string="Views",
        comodel_name="ir.actions.act_window.view",
        inverse_name="act_window_id"
    )

    @api.model
    def default_get(self, fields):
        res = super(StockOperationTypeCreateMenu, self).default_get(
            fields)
        obj_picking_type = self.env['stock.picking.type']
        picking_type_ids = self.env.context['active_ids']

        picking_type = obj_picking_type.browse(picking_type_ids)
        res['menu_name'] = picking_type.name
        res['sequence'] = 1
        return res

    @api.model
    def _create_window_action(self, picking_type):
        obj_act_window = self.env['ir.actions.act_window']
        view_ids = []

        if not picking_type.window_action_id:
            warehouse_name = picking_type.warehouse_id.name

            if self.view_ids:
                for view in self.view_ids:
                    view_ids.append(view.id)

            res = {
                "name": warehouse_name + ': ' + picking_type.name,
                "type": "ir.actions.act_window",
                "domain": [('picking_type_id', '=', picking_type.id)],
                "context": {
                    'default_picking_type_id': picking_type.id,
                    'search_default_draft': 1,
                    'search_default_confirmed': 1,
                    'search_default_waiting': 1,
                    'search_default_available': 1
                },
                "view_ids": [(6, 0, view_ids)],
                "res_model": 'stock.picking',
                "view_type": 'form',
                "view_mode": 'tree,form',
            }

            window_action_id = obj_act_window.create(res)
            picking_type.window_action_id = window_action_id.id

            return window_action_id
        return False

    @api.model
    def _create_warehouse_menu(self, picking_type):
        obj_ir_ui_menu = self.env['ir.ui.menu']
        parent_menu_id = self.env.ref('stock.menu_stock_warehouse_mgmt')

        warehouse_name = picking_type.warehouse_id.name

        criteria = [
            ('parent_id', '=', parent_menu_id.id),
            ('name', '=', warehouse_name)
        ]

        menu = obj_ir_ui_menu.search(criteria)

        if not menu:
            res = {
                'name': warehouse_name,
                'sequence': 100,
                'parent_id': parent_menu_id.id
            }

            warehouse_menu_id = obj_ir_ui_menu.create(res)
        else:
            warehouse_menu_id = menu
        return warehouse_menu_id

    @api.model
    def _create_menu(self, picking_type, window_action):
        obj_ir_ui_menu = self.env['ir.ui.menu']

        if not picking_type.menu_id:
            warehouse_menu_id = self._create_warehouse_menu(
                picking_type)

            res = {
                'name': self.menu_name,
                'sequence': self.sequence,
                'parent_id': warehouse_menu_id.id,
                'action': 'ir.actions.act_window,%s' % window_action.id
            }

            menu_id = obj_ir_ui_menu.create(res)
            picking_type.menu_id = menu_id.id

            return menu_id
        return False

    @api.multi
    def button_create_menu(self):
        self.ensure_one()

        obj_picking_type = self.env['stock.picking.type']
        picking_type_ids = self.env.context['active_ids']

        picking_type = obj_picking_type.browse(picking_type_ids)

        window_action_id =\
            self._create_window_action(picking_type)

        self._create_menu(
            picking_type, window_action_id)
