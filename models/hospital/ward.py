# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


# Ward
class Ward(surya.Sarpam):
    _name = "hospital.ward"

    name = fields.Char(string="Ward")
