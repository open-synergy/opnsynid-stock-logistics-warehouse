# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class StockQuant(models.Model):
    _name = "stock.quant"
    _inherit = [
        "stock.quant",
        "base.qr_document",
    ]
