# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Category

class HREmployeeCategory(surya.Sarpam):
    _name = "hr.employee.category"

    name = fields.Char(string="Category", required=True)
