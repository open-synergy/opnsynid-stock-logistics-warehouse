# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.api import Environment


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    create_consume_loc_for_existing_warehouse(env)
    create_consume_type_for_existing_warehouse(env)


def create_consume_loc_for_existing_warehouse(env):
    criteria = [
        ("consume_loc_id", "=", False),
    ]
    obj_wh = env["stock.warehouse"]
    for wh in obj_wh.search(criteria):
        consume_loc = wh._create_consume_loc()
        wh.write({
            "consume_loc_id": consume_loc.id
        })


def create_consume_type_for_existing_warehouse(env):
    criteria = [
        ("consume_type_id", "=", False),
    ]
    obj_wh = env["stock.warehouse"]
    for wh in obj_wh.search(criteria):
        consume_type = wh._create_consume_type()
        wh.write({
            "consume_type_id": consume_type.id
        })
