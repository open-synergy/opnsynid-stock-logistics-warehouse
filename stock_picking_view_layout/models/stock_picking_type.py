# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    create_ok = fields.Boolean(
        string="Create Ok",
        default=True,
    )
    edit_ok = fields.Boolean(
        string="Edit Ok",
        default=True,
    )
    unlink_ok = fields.Boolean(
        string="Unlink Ok",
        default=True,
    )
    tree_partner_ok = fields.Boolean(
        string="Show Partner",
        default=True,
    )
    tree_show_partner_id = fields.Boolean(
        string="Show Partner on Tree View",
        default=True,
    )
    tree_show_invoice_state = fields.Boolean(
        string="Show Invoice State on Tree View",
        default=True,
    )
    tree_show_date = fields.Boolean(
        string="Show Create Date on Tree View",
        default=True,
    )
    tree_show_min_date = fields.Boolean(
        string="Show Schedulled Date on Tree View",
        default=True,
    )
    form_show_partner_id = fields.Boolean(
        string="Show Partner on Form View",
        default=True,
    )
    form_show_date = fields.Boolean(
        string="Show Create Date on Form View",
        default=True,
    )
    form_show_min_date = fields.Boolean(
        string="Show Schedulled Date on Form View",
        default=True,
    )
    form_required_partner_id = fields.Boolean(
        string="Required Partner on Form View",
        default=False,
    )
