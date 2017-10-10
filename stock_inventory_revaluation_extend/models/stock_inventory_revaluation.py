# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _
import time


class StockInventoryRevaluation(models.Model):
    _inherit = "stock.inventory.revaluation"

    @api.multi
    def _prepare_post_data(self):
        data = {
            "state": "posted",
            "post_date": fields.Datetime.now(),
        }
        return data

    @api.multi
    def _update_price(self):
        self.ensure_one()
        self.write(self._prepare_cost_value())
        self.product_template_id.write(self._prepare_product_standard_cost())

    @api.multi
    def _prepare_cost_value(self):
        self.ensure_one()
        data = {}
        if self.revaluation_type == "price_change":
            data.update({"old_cost": self.current_cost})
        else:
            data.update({
                "old_cost": self.current_cost,
                "old_value": self.current_value,
            })
        return data

    @api.multi
    def _prepare_product_standard_cost(self):
        self.ensure_one()
        data = {}
        if self.revaluation_type == "price_change":
            data.update({
                "standard_price": self.new_cost,
            })
        else:
            value_diff = self.current_value - \
                self.new_value
            new_cost = value_diff / self.qty_available
            data.update({
                "standard_price": new_cost,
            })
        return data

    @api.multi
    def _check_qty_available(self):
        self.ensure_one()
        check = self.env.context.get("skip_check_qty_available", False)
        if check:
            return True
        for variant in self.\
                product_template_id.product_variant_ids:
            if variant.qty_available <= 0.0:
                raise UserError(
                    _("Cannot do an inventory value change if the "
                        "quantity available for product %s "
                        "is 0 or negative" %
                        variant.name))

    @api.multi
    def _check_negative(self):
        self.ensure_one()
        check = self.env.context.get("skip_check_negative", False)
        if check:
            return True
        if self.revaluation_type == "inventory_value":
            if self.new_value < 0:
                raise UserError(
                    _("The new value for product %s cannot "
                        "be negative" %
                        self.product_template_id.name))

    @api.multi
    def _check_increase_decrease_account(self):
        self.ensure_one()
        check = self.env.context.get("skip_check_account", False)
        if self.decrease_account_id and self.increase_account_id:
            check = True
        return check

    @api.multi
    def _generate_accounting_entry(self):
        self.ensure_one()
        timenow = time.strftime('%Y-%m-%d')
        move_data = self._prepare_move_data(timenow)
        move_line_obj = self.env['account.move.line']

        if not self._check_increase_decrease_account():
            raise UserError(_("Please add an Increase Account and "
                              "a Decrease Account."))

        for prod_variant in self.product_template_id.product_variant_ids:
            amount_diff = 0.0
            if self.product_template_id.cost_method == 'real':
                amount_diff = self._get_real_amount_diff(prod_variant)
                if amount_diff == 0.0:
                    return True
            else:
                amount_diff = self._get_avg_std_amount_diff(prod_variant)

            qty = prod_variant.qty_available
            if qty:
                debit_account_id, credit_account_id = self._get_account(
                    amount_diff)
                move = self.env['account.move'].create(move_data)
                move_line_data = self._prepare_debit_move_line_data(
                    move, abs(amount_diff), debit_account_id, prod_variant.id)
                move_line_obj.create(move_line_data)
                move_line_data = self._prepare_credit_move_line_data(
                    move, abs(amount_diff), credit_account_id, prod_variant.id)
                move_line_obj.create(move_line_data)
                if move.journal_id.entry_posted:
                    move.post()

    @api.multi
    def _get_real_amount_diff(self, product_variant):
        self.ensure_one()
        amount_diff = 0.0
        for reval_quant in self.reval_quant_ids:
            if reval_quant.product_id == product_variant:
                amount_diff += reval_quant.get_total_value()
        return amount_diff

    @api.multi
    def _get_avg_std_amount_diff(self, product_variant):
        self.ensure_one()
        amount_diff = 0.0
        prec = self.env['decimal.precision'].precision_get('Account')
        if self.revaluation_type == 'price_change':
            diff = self.old_cost - self.new_cost
            amount_diff = product_variant.qty_available * diff
        else:
            proportion = product_variant.qty_available / \
                self.product_template_id.qty_available
            amount_diff = round(self.new_value * proportion, prec)
        return amount_diff

    @api.multi
    def _get_account(self, amount_diff):
        self.ensure_one()
        datas = self.env['product.template'].get_product_accounts(
            self.product_template_id.id)
        if amount_diff > 0:
            debit_account_id = self.decrease_account_id.id
            credit_account_id = \
                datas['property_stock_valuation_account_id']
        else:
            debit_account_id = \
                datas['property_stock_valuation_account_id']
            credit_account_id = self.increase_account_id.id
        return [debit_account_id, credit_account_id]
