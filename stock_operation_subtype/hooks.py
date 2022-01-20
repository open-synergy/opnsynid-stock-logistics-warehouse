# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=E8103

from openerp import SUPERUSER_ID


def update_existing_picking_type(cr, registry):
    """
    This post-init-hook will update all existing issue assigning them the
    corresponding sequence code.
    """

    obj_data = registry["ir.model.data"]

    # Good Receipt

    subtype_id = obj_data.get_object_reference(
        cr, SUPERUSER_ID, "stock_operation_subtype", "good_receipt_subtype"
    )[1]

    sql = """
    UPDATE stock_picking_type
    SET subtype_id = %d
    WHERE id IN (SELECT in_type_id FROM stock_warehouse);
    """ % (
        subtype_id
    )

    cr.execute(sql)

    # Internal Transfer

    subtype_id = obj_data.get_object_reference(
        cr, SUPERUSER_ID, "stock_operation_subtype", "internal_transfer_subtype"
    )[1]

    sql = """
    UPDATE stock_picking_type
    SET subtype_id = %d
    WHERE id IN (SELECT int_type_id FROM stock_warehouse);
    """ % (
        subtype_id
    )

    cr.execute(sql)

    # Delivery Order

    subtype_id = obj_data.get_object_reference(
        cr, SUPERUSER_ID, "stock_operation_subtype", "delivery_order_subtype"
    )[1]

    sql = """
    UPDATE stock_picking_type
    SET subtype_id = %d
    WHERE id IN (SELECT out_type_id FROM stock_warehouse);
    """ % (
        subtype_id
    )

    cr.execute(sql)

    # Pick

    subtype_id = obj_data.get_object_reference(
        cr, SUPERUSER_ID, "stock_operation_subtype", "pick_subtype"
    )[1]

    sql = """
    UPDATE stock_picking_type
    SET subtype_id = %d
    WHERE id IN (SELECT pick_type_id FROM stock_warehouse);
    """ % (
        subtype_id
    )

    cr.execute(sql)

    # Pack

    subtype_id = obj_data.get_object_reference(
        cr, SUPERUSER_ID, "stock_operation_subtype", "pack_subtype"
    )[1]

    sql = """
    UPDATE stock_picking_type
    SET subtype_id = %d
    WHERE id IN (SELECT pack_type_id FROM stock_warehouse);
    """ % (
        subtype_id
    )

    cr.execute(sql)
