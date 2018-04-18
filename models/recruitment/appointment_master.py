# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Contacts

class AppointmentContact(surya.Sarpam):
    _name = "appointment.contact"
    _inherit = "contact.contact"

    appointment_id = fields.Many2one(comodel_name="appointment.order", string="Appointment Order")

# Experience

class AppointmentExperience(surya.Sarpam):
    _name = "appointment.experience"
    _inherit = "experience.experience"

    appointment_id = fields.Many2one(comodel_name="appointment.order", string="Appointment Order")

# Qualification


RESULT_INFO = [('pass', 'Pass'), ('fail', 'Fail'), ('discontinued', 'Discontinued')]


class AppointmentQualification(surya.Sarpam):
    _name = "appointment.qualification"
    _inherit = "qualification.qualification"

    appointment_id = fields.Many2one(comodel_name="appointment.order", string="Appointment Order")

