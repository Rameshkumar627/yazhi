# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from lxml import etree


# Resume Bank
class ResumeBank(surya.Sarpam):
    _name = "resume.bank"
    _inherit = "hr.personal.info"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")
    candidate_uid = fields.Char(string="Candidate ID")
    aadhar_card = fields.Char(string="Aadhar Card")
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    very_small_image = fields.Binary(string="Image")
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position")
    qualification_ids = fields.One2many(comodel_name="hr.qualification",
                                        inverse_name="employee_id",
                                        string="Qualification")
    experience_ids = fields.One2many(comodel_name="hr.experience",
                                     inverse_name="employee_id",
                                     string="Experience")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Resume Bank")
