# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

RESULT_INFO = [('pass', 'Pass'), ('fail', 'Fail'), ('discontinued', 'Discontinued')]

# Qualification


class HRQualification(surya.Sarpam):
    _name = "hr.qualification"
    _inherit = "qualification.qualification"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")

