# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


# Appointment Order
class AppointmentOrder(surya.Sarpam):
    _name = "appointment.order"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")
    candidate_uid = fields.Char(string="Candidate ID")
    aadhar_card = fields.Char(string="Aadhar Card")
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    very_small_image = fields.Binary(string="Image")
    email = fields.Char(string="Work Email")
    mobile = fields.Char(string="Work Mobile", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position")
    qualification_ids = fields.One2many(comodel_name="hr.qualification",
                                        inverse_name="employee_id",
                                        string="Qualification")
    experience_ids = fields.One2many(comodel_name="hr.experience",
                                     inverse_name="employee_id",
                                     string="Experience")
    attachment_ids = fields.One2many(comodel_name="hr.attachment",
                                     inverse_name="employee_id",
                                     string="Attachment")

