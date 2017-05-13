# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.api import Environment


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    create_scrap_loc_for_existing_warehouse(env)
    create_scrap_type_for_existing_warehouse(env)


def create_scrap_loc_for_existing_warehouse(env):
    criteria = [
        ("scrap_loc_id", "=", False),
    ]
    obj_wh = env["stock.warehouse"]
    for wh in obj_wh.search(criteria):
        scrap_loc = wh._create_scrap_loc()
        wh.write({
            "scrap_loc_id": scrap_loc.id
        })


def create_scrap_type_for_existing_warehouse(env):
    criteria = [
        ("scrap_type_id", "=", False),
    ]
    obj_wh = env["stock.warehouse"]
    for wh in obj_wh.search(criteria):
        scrap_type = wh._create_scrap_type()
        wh.write({
            "scrap_type_id": scrap_type.id
        })
