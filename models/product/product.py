# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
PRODUCT_TYPE = [("service", "Service"), ("medicine", "Medicine")]


class Product(surya.Sarpam):
    _name = "product.product"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", required=True)
    product_type = fields.Selection(selection=PROGRESS_INFO, string="Product Type", required=True)
    comment = fields.Text(string="Comment")

    @api.multi
    def smart_stock_location(self):
        pass

    @api.multi
    def smart_batch(self):
        pass

