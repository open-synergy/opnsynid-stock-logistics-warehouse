# 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields
from openerp.tools.safe_eval import safe_eval as eval


class StockMoveAccountSource(models.Model):
    _name = "stock.move_account_source"
    _description = "Stock Move Account Source"

    name = fields.Char(
        string="Source Name",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    python_code = fields.Text(
        string="Python Code for Account Source",
        required=True,
        default="result = False",
    )

    def _get_localdict(self, move):
        self.ensure_one()
        return {
            "env": self.env,
            "move": move,
        }

    @api.multi
    def _get_account(self, move):
        self.ensure_one()
        localdict = self._get_localdict(move)
        try:
            eval(self.python_code,
                 localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except:  # noqa: E722
            result = False
        return result
