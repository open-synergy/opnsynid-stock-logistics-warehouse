# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_lease_location_id = fields.Many2one(
        string="Customer Lease Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
    supplier_lease_location_id = fields.Many2one(
        string="Supplier Lease Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
