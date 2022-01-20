# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_stock_customer_promotion_id = fields.Many2one(
        string="Customer Promotion Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
    property_stock_supplier_promotion_id = fields.Many2one(
        string="Supplier Promotion Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
