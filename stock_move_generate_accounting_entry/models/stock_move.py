# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def action_generate_account_entry(self):
        move_ids = self.ids
        obj_move = self.env["stock.move"]
        # TODO: Refactor
        for move in obj_move.search(
                [("id", "in", move_ids)],
                order="date asc, id asc",
        ):
            if move.account_move_line_ids:
                move.account_move_line_ids[0].move_id.unlink()
            move._generate_account_entry()
            move.product_price_update_before_done()

    @api.multi
    def _generate_account_entry(self):
        self.ensure_one()
        obj_location = self.env["stock.location"]
        obj_quant = self.env["stock.quant"]
        location_from = self.location_id
        location_to = self.location_dest_id
        company_from = obj_location._location_owner(location_from)
        company_to = obj_location._location_owner(location_to)

        if self.product_id.valuation != 'real_time':
            return False
        quants = obj_quant
        for q in self.quant_ids:
            if q.owner_id:
                continue
            if q.qty <= 0:
                continue
            quants += q

        if not quants:
            return False

        # Create Journal Entry for products arriving in the company
        if company_to and \
                (self.location_id.usage not in ('internal', 'transit') and
                 self.location_dest_id.usage == 'internal' or
                 company_from != company_to):
            ctx = {"force_company": company_to.id}
            journal_id, acc_src, acc_dest, acc_valuation = obj_quant.\
                with_context(ctx)._get_accounting_data_for_valuation(self)
            if location_from and location_from.usage == 'customer':
                # goods returned from customer
                self.with_context(ctx).\
                    _create_account_move_line(
                        quants, acc_dest, acc_valuation, journal_id)
            else:
                self.with_context(ctx).\
                    _create_account_move_line(
                        quants, acc_src, acc_valuation, journal_id)

        # Create Journal Entry for products leaving the company
        if company_from and \
                (self.location_id.usage == 'internal' and
                 self.location_dest_id.usage not in ('internal', 'transit') or
                 company_from != company_to):
            ctx = {"force_company": company_from.id}
            journal_id, acc_src, acc_dest, acc_valuation = obj_quant.\
                with_context(ctx)._get_accounting_data_for_valuation(self)
            if location_to and location_to.usage == 'supplier':
                # goods returned to supplier
                self.with_context(ctx).\
                    _create_account_move_line(
                        quants, acc_valuation, acc_src, journal_id)
            else:
                self.with_context(ctx).\
                    _create_account_move_line(
                        quants, acc_valuation, acc_dest, journal_id)

    def _create_account_move_line(self, quants, credit_account_id,
                                  debit_account_id, journal_id):

        obj_quant = self.env["stock.quant"]
        obj_move = self.env["account.move"]
        # group quants by cost
        quant_cost_qty = {}
        for quant in quants:
            if quant_cost_qty.get(quant.cost):
                quant_cost_qty[quant.cost] += quant.qty
            else:
                quant_cost_qty[quant.cost] = quant.qty
        for cost, qty in quant_cost_qty.items():
            move_lines = obj_quant._prepare_account_move_line(
                self, qty, cost, credit_account_id,
                debit_account_id)
            period_id = self.env.\
                context.get('force_period', self.env["account.period"].
                            find()[0].id)
            obj_move.create({
                'journal_id': journal_id,
                'line_id': move_lines,
                'period_id': period_id,
                'date': self.date,
                'ref': self.picking_id.name,
            })
