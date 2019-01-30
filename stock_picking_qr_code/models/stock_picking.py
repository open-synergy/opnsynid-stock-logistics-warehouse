# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "base.qr_document"]
