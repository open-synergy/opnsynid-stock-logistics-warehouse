# -*- coding: utf-8 -*-
# Copyright 2021 PT. Simetri Sinergi Indonesia
# Copyright 2021 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    property_stock_employee_id = fields.Many2one(
        string="Employee Equipment Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
