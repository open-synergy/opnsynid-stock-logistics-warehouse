# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockInventory(models.Model):
    _name = "stock.inventory"
    _inherit = "stock.inventory"

    @api.model
    def _selection_filter(self):
        res = super(StockInventory, self)._selection_filter()
        res.append(("diff", _("By Diff Before Validate")))
        return res

    filter = fields.Selection(
        selection=_selection_filter
    )

    @api.multi
    def _get_product_diff(self):
        self.ensure_one()
        product_ids = []
        obj_line = self.env["stock.inventory.line"]
        obj_inventory = self.env["stock.inventory"]
        latest_inventory = False

        criteria1 = [
            ("filter", "=", "diff"),
            ("date", "<", self.date),
            ("state", "=", "done"),
            ("location_id", "=", self.location_id.id),
        ]

        latest_inventories = obj_inventory.search(criteria1, order="date desc")
        if len(latest_inventories) > 0:
            latest_inventory = latest_inventories[0]

        criteria2 = []

        if latest_inventory:
            criteria2 += [
                ("inventory_id.date", ">", latest_inventory.date),
            ]

        criteria2 += [
            ("inventory_id.location_id", "=", self.location_id.id),
            ("inventory_id.filter", "!=", "diff"),
            ("inventory_id.state", "=", "done"),
            ("diff_product_qty", "!=", 0.0),
        ]

        for line in obj_line.search(criteria2):
            product_ids.append(line.product_id.id)

        product_ids = list(set(product_ids))

        criteria3 = []

        if latest_inventory:
            criteria3 += [
                ("date", ">", latest_inventory.date),
            ]
        criteria3 = [
            ("location_id", "=", self.location_id.id),
            ("filter", "!=", "diff"),
            ("state", "=", "done"),
        ]
        for product_id in product_ids:
            for inventory in obj_inventory.search(criteria3, order="date"):
                mark = False
                criteria4 = [
                    ("inventory_id", "=", inventory.id),
                    ("product_id", "=", product_id),
                    ("diff_product_qty", "=", 0.0),
                ]
                if obj_line.search_count(criteria4) > 0:
                    mark = True
            if mark:
                product_ids.remove(product_id)

        if not product_ids:
            warning_msg = _("No product need adjustment")
            raise UserError(warning_msg)

        return product_ids

    @api.multi
    def _get_inventory_lines_values(self):
        self.ensure_one()
        obj_product = self.env["product.product"]
        if self.filter == "diff":
            product_ids = self._get_product_diff()

            products_to_filter = obj_product.browse(product_ids)
            quant_products = self.env['product.product']

            if len(product_ids) == 1:
                product_ids = "(%s)" % product_ids[0]
            else:
                product_ids = tuple(product_ids)

            sql1 = """
            SELECT  product_id,
                    sum(quantity) AS product_qty,
                    location_id,
                    lot_id as prod_lot_id,
                    package_id,
                    owner_id AS partner_id
            FROM    stock_quant AS a
            JOIN    product_product AS b ON a.product_id = b.id
            WHERE   a.location_id = %s AND
                    a.product_id in %s
            GROUP BY    product_id,
                        location_id,
                        lot_id,
                        package_id,
                        partner_id
            """ % (self.location_id.id, product_ids)

            self.env.cr.execute(sql1)
            vals = []
            for product_line in self.env.cr.dictfetchall():
                for key, value in product_line.items():
                    if not value:
                        product_line[key] = False
                product_line["inventory_id"] = self.id
                product_line["theoretical_qty"] = product_line["product_qty"]
                product_line["initial_theoretical_qty"] = \
                    product_line["product_qty"]
                product_line["manual_qty"] = product_line["product_qty"]
                product_line["qty_diff_method"] = self.qty_diff_method
                if product_line["product_id"]:
                    product = obj_product.browse(product_line["product_id"])
                    product_line["product_uom_id"] = product.uom_id.id
                    quant_products |= obj_product.browse(
                        product_line['product_id'])
                vals.append(product_line)

            if self.exhausted:
                exhausted_vals = self._get_exhausted_inventory_line(
                    products_to_filter, quant_products)
                vals.extend(exhausted_vals)
        else:
            return super(StockInventory, self)._get_inventory_lines_values()
        return vals
