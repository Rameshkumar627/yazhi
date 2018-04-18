# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Experience

class HRExperience(surya.Sarpam):
    _name = "hr.experience"
    _inherit = "experience.experience"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
