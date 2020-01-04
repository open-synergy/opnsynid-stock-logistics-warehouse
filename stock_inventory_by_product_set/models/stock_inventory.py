# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.exceptions import UserError
from openerp.tools.translate import _


class StockInventory(models.Model):
    _name = "stock.inventory"
    _inherit = "stock.inventory"

    @api.model
    def _selection_filter(self):
        res = super(StockInventory, self)._selection_filter()
        res.append(("product_set", _("By Product Sets")))
        return res

    filter = fields.Selection(
        selection=_selection_filter
    )
    product_set_ids = fields.Many2many(
        string="Product Sets",
        comodel_name="stock.inventory_product_set",
        relation="rel_stock_inventory_2_product_set",
        column1="inventory_id",
        column2="product_set_id",
    )

    @api.multi
    def _get_product_set_data(self):
        self.ensure_one()
        product_ids = []
        categ_ids = []
        for product_set in self.product_set_ids:
            product_ids += product_set.product_ids.ids
            categ_ids += product_set.product_categ_ids.ids

        if not product_ids and not categ_ids:
            warning_msg = _("No product or product category defined")
            raise UserError(warning_msg)

        return product_ids, categ_ids

    @api.multi
    def _get_inventory_lines_values(self):
        self.ensure_one()
        obj_product = self.env["product.product"]
        if self.filter == "product_set":
            product_ids, categ_ids = self._get_product_set_data()

            if len(product_ids) == 1:
                product_ids = "(%s)" % product_ids[0]
            else:
                product_ids = tuple(product_ids)

            if len(categ_ids) == 1:
                categ_ids = "(%s)" % categ_ids[0]
            else:
                categ_ids = tuple(categ_ids)

            sql1 = """
            SELECT  product_id,
                    sum(quantity) AS product_qty,
                    location_id,
                    lot_id as prod_lot_id,
                    package_id,
                    owner_id AS partner_id
            FROM    stock_quant AS a
            JOIN    product_product AS b ON a.product_id = b.id
            JOIN    product_template AS c ON b.product_tmpl_id = c.id
            WHERE   a.location_id = %s AND
                    (a.product_id in %s OR c.categ_id in %s)
            GROUP BY    product_id,
                        location_id,
                        lot_id,
                        package_id,
                        partner_id
            """ % (self.location_id.id, product_ids, categ_ids)

            self.env.cr.execute(sql1)
            vals = []
            for product_line in self.env.cr.dictfetchall():
                for key, value in product_line.items():
                    if not value:
                        product_line[key] = False
                product_line["inventory_id"] = self.id
                product_line["theoretical_qty"] = product_line["product_qty"]
                if product_line["product_id"]:
                    product = obj_product.browse(product_line["product_id"])
                    product_line["product_uom_id"] = product.uom_id.id
                vals.append(product_line)
        else:
            return super(StockInventory, self)._get_inventory_lines_values()
        return vals
