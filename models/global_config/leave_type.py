# -*- coding: utf-8 -*-

from odoo import fields
from .. import surya


# Leave Type

class LeaveType(surya.Sarpam):
    _name = "leave.type"

    name = fields.Char(string="Type", required=True)
