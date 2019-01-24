# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.model
    def _get_available_filters(self):
        res = super(StockInventory, self)._get_available_filters()
        res.append(("brand", _("By Brand")))
        return res

    filter = fields.Selection(
        selection=_get_available_filters
    )

    product_brand_ids = fields.Many2many(
        comodel_name="product.brand",
        relation="invetory_brand_rel",
        column1="inventory_id",
        column2="brand_id",
        string="Selected Brands")

    @api.model
    def _get_inventory_lines(self, inventory):
        if inventory.filter == "brand":
            location_obj = self.env["stock.location"]
            product_obj = self.env["product.product"]
            location_ids = location_obj.search([
                ("id", "child_of", [inventory.location_id.id])
            ])
            domain = " location_id in %s"
            args = (tuple(location_ids.ids),)
            domain += " and C.product_brand_id in %s"
            args += (tuple(inventory.product_brand_ids.ids),)

            self.env.cr.execute('''
            SELECT product_id, sum(qty) as product_qty,
            location_id, lot_id as prod_lot_id,
            package_id, owner_id as partner_id
            FROM stock_quant AS A
            JOIN product_product AS B ON A.product_id=B.id
            JOIN product_template AS C ON B.product_tmpl_id=C.id
            WHERE''' + domain + '''
            GROUP BY product_id, location_id, lot_id, package_id, partner_id
            ''', args)

            vals = []
            for product_line in self.env.cr.dictfetchall():
                for key, value in product_line.items():
                    if not value:
                        product_line[key] = False
                product_line["inventory_id"] = inventory.id
                product_line["theoretical_qty"] = product_line["product_qty"]
                if product_line["product_id"]:
                    product = product_obj.browse(product_line["product_id"])
                    product_line["product_uom_id"] = product.uom_id.id
                vals.append(product_line)
        else:
            return super(StockInventory, self)._get_inventory_lines(inventory)
        return vals
