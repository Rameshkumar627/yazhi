# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


# Lab Test
class Test(surya.Sarpam):
    _name = "test.test"

    name = fields.Char(string="Name")
    value = fields.Float(string="Value")
