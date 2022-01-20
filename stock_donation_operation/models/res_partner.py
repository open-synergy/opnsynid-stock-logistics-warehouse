# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_stock_donation_in_id = fields.Many2one(
        string="Donation In Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
    property_stock_donation_out_id = fields.Many2one(
        string="Donation Out Location",
        comodel_name="stock.location",
        company_dependent=True,
    )
