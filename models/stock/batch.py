# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Stock Location
class StockBatch(surya.Sarpam):
    _name = "stock.batch"

    name = fields.Char(string="Name")


