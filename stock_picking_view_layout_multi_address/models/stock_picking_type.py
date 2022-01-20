# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    tree_show_consignee_id = fields.Boolean(
        string="Show Consignee on Tree View",
        default=True,
    )
    tree_show_delivery_address_id = fields.Boolean(
        string="Show Delivery Address on Tree View",
        default=True,
    )
    tree_show_origin_address_id = fields.Boolean(
        string="Show Origin Address on Tree View",
        default=True,
    )
    form_show_consignee_id = fields.Boolean(
        string="Show Consignee on Form View",
        default=True,
    )
    form_show_delivery_address_id = fields.Boolean(
        string="Show Delivery Address on Form View",
        default=True,
    )
    form_show_origin_address_id = fields.Boolean(
        string="Show Origin Address on Form View",
        default=True,
    )
    form_required_consignee_id = fields.Boolean(
        string="Required Consignee on Form View",
        default=False,
    )
    form_required_delivery_address_id = fields.Boolean(
        string="Required Delivery Address on Form View",
        default=False,
    )
    form_required_origin_address_id = fields.Boolean(
        string="Required Origin Address on Form View",
        default=False,
    )
