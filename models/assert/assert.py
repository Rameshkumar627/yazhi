# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


# Assert
class Assert(surya.Sarpam):
    _name = "hospital.assert"

    product_id = fields.Many2one(comodel_name="hospital.product", string="Product")

    # Product Info
    serial_no = ""
    

    # Vendor Info
    # Maintenance Info
    # Account Info
