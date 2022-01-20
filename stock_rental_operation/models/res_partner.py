# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_rental_location_id = fields.Many2one(
        string="Customer Rental Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
    supplier_rental_location_id = fields.Many2one(
        string="Supplier Rental Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
