# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from openerp.tools.translate import _

ACC_SELECTION = [
    ("default", _("Default")),
    ("product_categ_valuation", _("Valuation Account on Product Category")),
    ("product_categ_input", _("Input Account on Product Category")),
    ("product_categ_output", _("Output Account on Product Category")),
    ("product_categ_income", _("Income Account on Product Category")),
    ("product_categ_expense", _("Expense Account on Product Category")),
    ("product_input", _("Input Account on Product")),
    ("product_output", _("Output Account on Product")),
    ("product_income", _("Income Account on Product")),
    ("product_expense", _("Expense Account on Product")),
    ("src_loc_input", _("Input Account on Source Location")),
    ("src_loc_output", _("Output Account on Source Location")),
    ("dest_loc_input", _("Input Account on Destination Location")),
    ("dest_loc_output", _("Output Account on Destination Location")),
]


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    acc_valuation = fields.Selection(
        string="Valuation Account",
        selection=ACC_SELECTION,
        required=True,
    )

    acc_source = fields.Selection(
        string="Source Account",
        selection=ACC_SELECTION,
        required=True,
    )

    acc_destination = fields.Selection(
        string="Destination Account",
        selection=ACC_SELECTION,
        required=True,
    )
