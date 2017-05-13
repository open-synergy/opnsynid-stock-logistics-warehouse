# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.api import Environment


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    create_waste_loc_for_existing_warehouse(env)
    create_waste_type_for_existing_warehouse(env)


def create_waste_loc_for_existing_warehouse(env):
    criteria = [
        ("waste_loc_id", "=", False),
    ]
    obj_wh = env["stock.warehouse"]
    for wh in obj_wh.search(criteria):
        waste_loc = wh._create_waste_loc()
        wh.write({
            "waste_loc_id": waste_loc.id
        })


def create_waste_type_for_existing_warehouse(env):
    criteria = [
        ("waste_type_id", "=", False),
    ]
    obj_wh = env["stock.warehouse"]
    for wh in obj_wh.search(criteria):
        waste_type = wh._create_waste_type()
        wh.write({
            "waste_type_id": waste_type.id
        })
