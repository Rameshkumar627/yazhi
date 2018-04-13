# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


PROGRESS_INFO = [('draft', 'Draft'),
                 ('scheduled', 'Scheduled'),
                 ('cancelled', 'Cancelled')]


# Appointment
class Appointment(surya.Sarpam):
    _name = "hospital.appointment"

    from_time = fields.Datetime(string="From time")
    till_time = fields.Datetime(string="Till time")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    reason = fields.Text(string="Reason")
    progress = fields.Selection(PROGRESS_INFO, string="Progress", default="draft")
