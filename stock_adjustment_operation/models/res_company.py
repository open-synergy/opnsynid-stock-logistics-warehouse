# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    adjustment_type_id = fields.Many2one(
        string="Adjustment Type",
        comodel_name="stock.picking.type"
    )

    @api.multi
    def _prepare_adjustment_sequence(self):
        self.ensure_one()
        data = {
            "name": _("Adjustment"),
            "prefix": "ADJ/%(y)s/",
            "padding": 6
        }
        return data

    @api.multi
    def _prepare_adjustment_type(self):
        self.ensure_one()
        obj_sequence = self.env["ir.sequence"]

        sequence = obj_sequence.create(
            self._prepare_adjustment_sequence())

        data = {
            "name": _("Adjustment"),
            "sequence_id": sequence.id,
            "warehouse_id": False,
            "code": "internal",
        }
        return data

    @api.multi
    def _create_adjustment_type(self):
        self.ensure_one()
        obj_type = self.env["stock.picking.type"]
        adjustment_type = obj_type.create(
            self._prepare_adjustment_type())
        return adjustment_type

    @api.multi
    def button_create_adjustment_type(self):
        for company in self:
            adj_type = company._create_adjustment_type()
            company.adjustment_type_id = adj_type.id

    @api.model
    def create(self, values):
        new_company = super(ResCompany, self).create(values)
        adj_type = new_company._create_adjustment_type()
        new_company.adjustment_type_id = adj_type.id
        return new_company
