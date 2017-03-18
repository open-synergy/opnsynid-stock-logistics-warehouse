# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductBrand(models.Model):
    _inherit = "product.brand"

    orderpoint_filter_ok = fields.Boolean(
        string="Filter on Orderpoint",
    )
