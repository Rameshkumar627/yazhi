# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Stock Batch
class StockBatch(surya.Sarpam):
    _name = "stock.batch"

    name = fields.Char(string="Name")
    vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor")
    price = fields.Float(string="Price")
    quantity = fields.Float(string="Quantity")
    date = fields.Date(string="Date")
    reference = fields.Char(string="Reference")
    expiry = fields.Date(string="Expiry")
    mrp = fields.Float(string="MRP")

    @api.multi
    def smart_stock_location(self):
        pass






