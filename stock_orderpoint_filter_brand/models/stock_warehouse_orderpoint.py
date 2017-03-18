# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from lxml import etree


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.model
    def fields_view_get(self, view_id=None,
                        view_type=False, toolbar=False,
                        submenu=False):
        res = super(StockWarehouseOrderpoint, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        doc = etree.XML(res["arch"])
        empty_filter = doc.xpath("//group[@name='grp_brand']")

        if view_type == "search" and empty_filter:
            obj_brand = self.env["product.brand"]
            criteria = [
                ("orderpoint_filter_ok", "=", True),
            ]
            for brand in obj_brand.search(criteria):
                filter_name = "filter_brand_%s" % (str(brand.id))
                filter_string = "%s" % (str(brand.name))
                fdomain = "[('product_id.product_brand_id.id', '=', %s)]" \
                    % (str(brand.id))
                xelement = etree.Element(
                    "filter", {"name": filter_name,
                               "string": filter_string,
                               "domain": fdomain,
                               })
                empty_filter[0].insert(0, xelement)

        res["arch"] = etree.tostring(doc)

        return res
