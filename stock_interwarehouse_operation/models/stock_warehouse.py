# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    interwarehouse_in_type_id = fields.Many2one(
        string="Inter-Warehouse In Type",
        comodel_name="stock.picking.type"
    )
    interwarehouse_out_type_id = fields.Many2one(
        string="Inter-Warehouse Out Type",
        comodel_name="stock.picking.type"
    )
    transit_pull_loc_id = fields.Many2one(
        string="Transit Pull Location",
        comodel_name="stock.location"
    )
    transit_push_loc_id = fields.Many2one(
        string="Transit Push Location",
        comodel_name="stock.location"
    )
    inter_warehouse_pull_route_id = fields.Many2one(
        string="Inter-Warehouse Pull Route",
        comodel_name="stock.location.route"
    )
    inter_warehouse_push_route_id = fields.Many2one(
        string="Inter-Warehouse Push Route",
        comodel_name="stock.location.route"
    )

    @api.model
    def get_parent_location(self):
        obj_stock_location = self.env['stock.location']
        physical_location =\
            self.env.ref('stock.stock_location_locations')

        criteria = [
            ('name', '=', self.code),
            ('location_id', '=', physical_location.id)
        ]

        parent_location = obj_stock_location.search(criteria)
        return parent_location

    @api.model
    def get_stock_location(self):
        obj_stock_location = self.env['stock.location']
        parent_location = self.get_parent_location()

        criteria = [
            ('name', '=', 'Stock'),
            ('location_id', '=', parent_location.id)
        ]

        stock_location = obj_stock_location.search(criteria)
        return stock_location

    @api.model
    def create_location_pull(self, company_id):
        obj_stock_location = self.env['stock.location']
        parent_location = self.get_parent_location()

        vals = {
            'name': 'Transit Pull',
            'location_id': parent_location.id,
            'company_id': company_id,
            'usage': 'transit',
            'active': True

        }
        location = obj_stock_location.create(vals)
        return location

    @api.model
    def create_location_push(self, company_id):
        obj_stock_location = self.env['stock.location']
        parent_location = self.get_parent_location()

        vals = {
            'name': 'Transit Push',
            'location_id': parent_location.id,
            'company_id': company_id,
            'usage': 'transit',
            'active': True

        }
        location = obj_stock_location.create(vals)
        return location

    @api.model
    def create_type_interwarehouse_in(self):
        obj_stock_picking_type = self.env['stock.picking.type']
        obj_ir_sequence = self.env['ir.sequence']

        sequence_id = obj_ir_sequence.create({
            'name': self.code + ' Inter-Warehouse In',
            'prefix': self.code + '/IWI/',
            'padding': 6
        })

        location_dest_id = self.get_stock_location()

        vals = {
            'name': 'Inter-Warehouse In',
            'warehouse_id': self.id,
            'sequence_id': sequence_id.id,
            'code': 'reception',
            'default_location_dest_id': location_dest_id.id,
            'allowed_dest_location_ids': [(6, 0, [location_dest_id.id])]
        }
        picking_type = obj_stock_picking_type.create(vals)
        return picking_type

    @api.model
    def create_type_interwarehouse_out(self):
        obj_stock_picking_type = self.env['stock.picking.type']
        obj_ir_sequence = self.env['ir.sequence']

        sequence_id = obj_ir_sequence.create({
            'name': self.code + ' Inter-Warehouse Out',
            'prefix': self.code + '/IWO/',
            'padding': 6
        })

        location_id = self.get_stock_location()

        vals = {
            'name': 'Inter-Warehouse Out',
            'warehouse_id': self.id,
            'sequence_id': sequence_id.id,
            'code': 'outgoing',
            'default_location_src_id': location_id.id,
            'allowed_location_ids': [(6, 0, [location_id.id])]
        }
        picking_type = obj_stock_picking_type.create(vals)
        return picking_type

    @api.model
    def create_route_interwarehouse_push(self):
        obj_stock_location_route = self.env['stock.location.route']
        location_id = self.get_stock_location()

        if self.transit_push_loc_id:
            if self.interwarehouse_in_type_id.id:
                code = self.code
                vals = {
                    'name': self.code + ':Inter-Warehouse Push',
                    'product_categ_selectable': True,
                    'product_selectable': False,
                    'warehouse_selectable': False,
                    'sale_selectable': False,
                    'push_ids': [(0, 0, {
                        'name': code + ': Transit Push > ' + code + ': Stock',
                        'location_from_id': self.transit_push_loc_id.id,
                        'location_dest_id': location_id.id,
                        'picking_type_id': self.interwarehouse_in_type_id.id,
                        'auto': 'manual',
                    })]
                }
                route = obj_stock_location_route.create(vals)
                return route
            else:
                raise UserError(
                    _('Inter-Warehouse In Picking Type Not Found'))
        else:
            raise UserError(
                _('Transit Push Location Not Found'))

    @api.model
    def create_route_interwarehouse_pull(self):
        obj_stock_location_route = self.env['stock.location.route']

        if self.transit_pull_loc_id:
            if self.interwarehouse_out_type_id.id:
                code = self.code
                vals = {
                    'name': self.code + ':Inter-Warehouse Pull',
                    'product_categ_selectable': True,
                    'product_selectable': False,
                    'warehouse_selectable': False,
                    'sale_selectable': False,
                    'pull_ids': [(0, 0, {
                        'name': code + ': Transit Pull < ' + code + ': Stock',
                        'location_id': self.transit_pull_loc_id.id,
                        'action': 'move',
                        'picking_type_id': self.interwarehouse_out_type_id.id
                    })]
                }
                route = obj_stock_location_route.create(vals)
                return route
            else:
                raise UserError(
                    _('Inter-Warehouse Out Picking Type Not Found'))
        else:
            raise UserError(
                _('Transit Pull Location Not Found'))

    @api.multi
    def button_auto_create(self):
        company_id = self._context.get(
            'company_id', self.env.user.company_id.id)
        button_type = self._context.get('button_type', False)

        if button_type == 'transit_pull':
            if not self.transit_pull_loc_id:
                location = self.create_location_pull(company_id)
                self.transit_pull_loc_id = location.id

        if button_type == 'transit_push':
            if not self.transit_push_loc_id:
                location = self.create_location_push(company_id)
                self.transit_push_loc_id = location.id

        if button_type == 'type_interwarehouse_in':
            if not self.interwarehouse_in_type_id:
                picking_type = self.create_type_interwarehouse_in()
                self.interwarehouse_in_type_id = picking_type.id

        if button_type == 'type_interwarehouse_out':
            if not self.interwarehouse_out_type_id:
                picking_type = self.create_type_interwarehouse_out()
                self.interwarehouse_out_type_id = picking_type.id

        if button_type == 'route_interwarehouse_pull':
            if not self.inter_warehouse_pull_route_id:
                route = self.create_route_interwarehouse_pull()
                if route:
                    self.inter_warehouse_pull_route_id = route.id

        if button_type == 'route_interwarehouse_push':
            if not self.inter_warehouse_push_route_id:
                route = self.create_route_interwarehouse_push()
                if route:
                    self.inter_warehouse_push_route_id = route.id
        return True

    @api.multi
    def button_reset(self):
        obj_stock_location = self.env['stock.location']
        obj_stock_picking_type = self.env['stock.picking.type']
        obj_stock_location_route = self.env['stock.location.route']
        button_type = self._context.get('button_type', False)

        if button_type == 'transit_pull':
            if self.transit_pull_loc_id:
                transit_pull_loc_id = self.transit_pull_loc_id.id
                self.transit_pull_loc_id = False
                criteria = [
                    ('id', '=', transit_pull_loc_id)
                ]
                obj_stock_location.search(criteria).unlink()

        if button_type == 'transit_push':
            if self.transit_push_loc_id:
                transit_push_loc_id = self.transit_push_loc_id.id
                self.transit_push_loc_id = False
                criteria = [
                    ('id', '=', transit_push_loc_id)
                ]
                obj_stock_location.search(criteria).unlink()

        if button_type == 'type_interwarehouse_in':
            if self.interwarehouse_in_type_id:
                interwarehouse_in_type_id = self.interwarehouse_in_type_id.id
                self.interwarehouse_in_type_id = False
                criteria = [
                    ('id', '=', interwarehouse_in_type_id)
                ]
                obj_stock_picking_type.search(criteria).unlink()

        if button_type == 'type_interwarehouse_out':
            if self.interwarehouse_out_type_id:
                interwarehouse_out_type_id = self.interwarehouse_out_type_id.id
                self.interwarehouse_out_type_id = False
                criteria = [
                    ('id', '=', interwarehouse_out_type_id)
                ]
                obj_stock_picking_type.search(criteria).unlink()

        if button_type == 'route_interwarehouse_pull':
            if self.inter_warehouse_pull_route_id:
                inter_warehouse_pull_route_id =\
                    self.inter_warehouse_pull_route_id.id
                self.inter_warehouse_pull_route_id = False
                criteria = [
                    ('id', '=', inter_warehouse_pull_route_id)
                ]
                obj_stock_location_route.search(criteria).unlink()

        if button_type == 'route_interwarehouse_push':
            if self.inter_warehouse_push_route_id:
                inter_warehouse_push_route_id =\
                    self.inter_warehouse_push_route_id.id
                self.inter_warehouse_push_route_id = False
                criteria = [
                    ('id', '=', inter_warehouse_push_route_id)
                ]
                obj_stock_location_route.search(criteria).unlink()
