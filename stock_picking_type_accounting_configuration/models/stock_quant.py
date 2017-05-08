# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _get_accounting_data_for_valuation(self, move):
        journal_id, acc_src, acc_dest, acc_valuation = \
            super(StockQuant, self)._get_accounting_data_for_valuation(move)

        if not move.picking_type_id:
            return journal_id, acc_src, acc_dest, acc_valuation

        pick_type = move.picking_type_id

        if pick_type.acc_valuation != "default":
            acc_valuation = self._get_custom_account_selection(
                move, pick_type.acc_valuation)

        if pick_type.acc_source != "default":
            acc_src = self._get_custom_account_selection(
                move, pick_type.acc_source)

        if pick_type.acc_destination != "default":
            acc_dest = self._get_custom_account_selection(
                move, pick_type.acc_destination)

        return journal_id, acc_src, acc_dest, acc_valuation

    @api.model
    def _get_custom_account_selection(self, move, selection):
        account = self._map_custom_account_selection(
            move).get(selection, False)
        if not account:
            raise UserError(_("No account"))
        return account.id

    @api.model
    def _map_custom_account_selection(self, move):
        return {
            "product_categ_valuation":
                move.product_id.categ_id.property_stock_valuation_account_id,
            "product_categ_input":
                move.product_id.categ_id.property_stock_account_input_categ,
            "product_categ_output":
                move.product_id.categ_id.property_stock_account_output_categ,
            "product_categ_income":
                move.product_id.categ_id.property_account_income_categ,
            "product_categ_expense":
                move.product_id.categ_id.property_account_expense_categ,
            "product_input":
                move.product_id.property_stock_account_input,
            "product_output":
                move.product_id.property_stock_account_output,
            "product_income":
                move.product_id.property_account_income,
            "product_expense":
                move.product_id.property_account_expense,
            "src_loc_input":
                move.location_id.valuation_in_account_id,
            "src_loc_output":
                move.location_id.valuation_out_account_id,
            "dest_loc_input":
                move.location_dest_id.valuation_in_account_id,
            "dest_loc_output":
                move.location_dest_id.valuation_out_account_id,
        }
