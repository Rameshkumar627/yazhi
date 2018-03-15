# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Department

class HRDepartment(surya.Sarpam):
    _name = "hr.department"

    name = fields.Char(string="Department", required=True)
    head = fields.Many2many(comodel_name="hr.employee", string="Department Head")
    members = fields.Many2many(comodel_name="hr.employee", string="Department Members")
