# 2017-2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    acc_valuation = fields.Selection(
        string="Valuation Account Policy",
        selection=[
            ("default", "Default"),
            ("custom", "Custom"),
        ],
        required=True,
        default="default",
    )
    acc_valuation_id = fields.Many2one(
        string="Valuation Account",
        comodel_name="stock.move_account_source",
    )
    acc_source = fields.Selection(
        string="Source Account Policy",
        selection=[
            ("default", "Default"),
            ("custom", "Custom"),
        ],
        required=True,
        default="default",
    )
    acc_source_id = fields.Many2one(
        string="Source Account",
        comodel_name="stock.move_account_source",
    )
    acc_destination = fields.Selection(
        string="Destination Account Policy",
        selection=[
            ("default", "Default"),
            ("custom", "Custom"),
        ],
        required=True,
        default="default",
    )
    acc_destination_id = fields.Many2one(
        string="Destination Account",
        comodel_name="stock.move_account_source",
    )
