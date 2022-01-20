# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _get_accounting_data_for_valuation(self, move):
        journal_id, acc_src, acc_dest, acc_valuation = super(
            StockQuant, self
        )._get_accounting_data_for_valuation(move)

        # raise UserError("a")

        if not move.picking_type_id:
            return journal_id, acc_src, acc_dest, acc_valuation

        # raise UserError("b")

        pick_type = move.picking_type_id

        if pick_type.acc_valuation != "default":
            acc_valuation = pick_type.acc_valuation_id._get_account(move)

            if not acc_valuation:
                err_msg = _("No valuation account configured")
                raise UserError(err_msg)

        if pick_type.acc_source != "default":
            acc_src = pick_type.acc_source_id._get_account(move)

            if not acc_src:
                err_msg = _("No source account configured")
                raise UserError(err_msg)

        if pick_type.acc_destination != "default":
            acc_dest = pick_type.acc_destination_id._get_account(move)

            if not acc_dest:
                err_msg = _("No destination account configured")
                raise UserError(err_msg)

        return journal_id, acc_src, acc_dest, acc_valuation
