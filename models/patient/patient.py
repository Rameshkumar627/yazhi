# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


PROGRESS_INFO = [('draft', 'Draft')]
BLOOD_GROUP = [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'),
               ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-')]
GENDER = [('male', 'Male'), ('female', 'Female')]
MARITAL_STATUS = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


class Patient(surya.Sarpam):
    _name = "patient.patient"

    name = fields.Char(string="Name", required=True)
    patient_id = fields.Char(string="Patient ID")
    image = fields.Binary(string="Image")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')
    work_email = fields.Char(string="Work Email")
    work_mobile = fields.Char(string="Work Mobile", required=True)
    doj = fields.Date(string="Date of Joining", required=False)
    attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
