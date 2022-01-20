# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree
from openerp import api, models
from openerp.osv.orm import setup_modifiers


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def fields_view_get(
        self, view_id=None, view_type=False, toolbar=False, submenu=False
    ):
        res = super(StockPicking, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

        doc = etree.XML(res["arch"])

        picking_type_id = self.env.context.get("default_picking_type_id", False)

        if view_type == "tree":
            view_element = doc.xpath("/tree")[0]
        elif view_type == "form":
            view_element = doc.xpath("/form")[0]

        if not picking_type_id:
            if view_type in ["tree", "form"]:
                view_element.attrib["create"] = "false"
                view_element.attrib["edit"] = "false"
                view_element.attrib["delete"] = "false"
        else:
            pick_type = self.env["stock.picking.type"].browse(picking_type_id)[0]
            if view_type in ["tree", "form"]:
                view_element.attrib["create"] = (
                    pick_type.create_ok and "true" or "false"
                )
                view_element.attrib["edit"] = pick_type.edit_ok and "true" or "false"
                view_element.attrib["delete"] = (
                    pick_type.unlink_ok and "true" or "false"
                )
            if view_type == "tree":
                obj_field = self.env["ir.model.fields"]
                criteria = [
                    ("model", "=", "stock.picking.type"),
                    ("name", "ilike", "tree_show_"),
                ]
                for field in obj_field.search(criteria):
                    field_name = field.name[10:]
                    path = "//field[@name='%s']" % (field_name)
                    el = doc.xpath(path)[0]
                    if not getattr(pick_type, field.name):
                        el.set("invisible", "1")
                    else:
                        el.set("invisible", "0")
                    setup_modifiers(el, res["fields"][field_name], in_tree_view=True)
            elif view_type == "form":
                obj_field = self.env["ir.model.fields"]
                criteria = [
                    ("model", "=", "stock.picking.type"),
                    ("name", "ilike", "form_show_"),
                ]
                for field in obj_field.search(criteria):
                    field_name = field.name[10:]
                    path = "//field[@name='%s']" % (field_name)
                    el = doc.xpath(path)[0]
                    if not getattr(pick_type, field.name):
                        el.set("invisible", "1")
                    else:
                        el.set("invisible", "0")
                    setup_modifiers(el, res["fields"][field_name])
                criteria = [
                    ("model", "=", "stock.picking.type"),
                    ("name", "ilike", "form_required_"),
                ]
                for field in obj_field.search(criteria):
                    field_name = field.name[14:]
                    path = "//field[@name='%s']" % (field_name)
                    el = doc.xpath(path)[0]
                    if getattr(pick_type, field.name):
                        el.set("required", "1")
                    else:
                        el.set("required", "0")
                    setup_modifiers(el, res["fields"][field_name])

        res["arch"] = etree.tostring(doc)

        return res
