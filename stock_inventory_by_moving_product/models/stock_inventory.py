# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api
from openerp.tools.translate import _


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.model
    def _get_available_filters(self):
        res = super(StockInventory, self)._get_available_filters()
        res.append(("moving_product", _("By Moving Products")))
        return res

    filter = fields.Selection(
        selection=_get_available_filters
    )

    @api.model
    def _get_inventory_lines(self, inventory):
        if inventory.filter == "moving_product":
            obj_product = self.env["product.product"]

            location = inventory.location_id
            product_ids = []
            # TODO: timezone adjustment
            dt_date_start = datetime.strptime(
                inventory.date, "%Y-%m-%d %H:%M:%S"
            )
            dt_date_start += relativedelta(hour=0, minute=0, second=0)
            date_start = dt_date_start.strftime("%Y-%m-%d %H:%M:%S")
            date_end = inventory.date

            sql1 = """
            SELECT DISTINCT product_id
            FROM stock_move AS a
            WHERE   (
                (a.location_id = %s and a.location_dest_id <> %s) OR
                (a.location_dest_id = %s and a.location_id <> %s)
                ) AND
                a.date > '%s' AND
                a.date <= '%s' AND
                a.state = 'done'
            """ % (location.id, location.id,
                   location.id, location.id, date_start, date_end)

            self.env.cr.execute(sql1)

            for result in self.env.cr.dictfetchall():
                product_ids.append(result["product_id"])

            if len(product_ids) == 0:
                product_ids = "()"
            elif len(product_ids) == 1:
                product_ids = "(%s)" % product_ids[0]
            else:
                product_ids = tuple(product_ids)

            sql2 = """
            SELECT  product_id,
                    sum(qty) AS product_qty,
                    location_id,
                    lot_id as prod_lot_id,
                    package_id,
                    owner_id AS partner_id
            FROM    stock_quant AS a
            WHERE   location_id = %s AND
                    product_id in %s
            GROUP BY    product_id,
                        location_id,
                        lot_id,
                        package_id,
                        partner_id
            """ % (location.id, product_ids)

            self.env.cr.execute(sql2)
            vals = []
            for product_line in self.env.cr.dictfetchall():
                for key, value in product_line.items():
                    if not value:
                        product_line[key] = False
                product_line["inventory_id"] = inventory.id
                product_line["theoretical_qty"] = product_line["product_qty"]
                if product_line["product_id"]:
                    product = obj_product.browse(product_line["product_id"])
                    product_line["product_uom_id"] = product.uom_id.id
                vals.append(product_line)
        else:
            return super(StockInventory, self)._get_inventory_lines(inventory)
        return vals
