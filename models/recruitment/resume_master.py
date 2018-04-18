# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Contacts
class ResumeContact(surya.Sarpam):
    _name = "resume.contact"
    _inherit = "contact.contact"

    resume_id = fields.Many2one(comodel_name="resume.bank", string="Resume Bank")


# Experience

class ResumeExperience(surya.Sarpam):
    _name = "resume.experience"
    _inherit = "experience.experience"

    resume_id = fields.Many2one(comodel_name="resume.bank", string="Resume Bank")


# Qualification
RESULT_INFO = [('pass', 'Pass'), ('fail', 'Fail'), ('discontinued', 'Discontinued')]


class ResumeQualification(surya.Sarpam):
    _name = "resume.qualification"
    _inherit = "qualification.qualification"

    resume_id = fields.Many2one(comodel_name="resume.bank", string="Resume Bank")
