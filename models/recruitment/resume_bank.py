# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from lxml import etree

MARITAL_INFO = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]
GENDER_INFO = [('male', 'Male'), ('female', 'Female')]


# Resume Bank
class ResumeBank(surya.Sarpam):
    _name = "resume.bank"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")
    candidate_uid = fields.Char(string="Candidate ID", readonly=True)
    aadhar_card = fields.Char(string="Aadhar Card")
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    very_small_image = fields.Binary(string="Image")

    # Contact Detail
    email = fields.Char(string="Email", required=True)
    mobile = fields.Char(string="Mobile", required=True)
    door_no = fields.Char(string="Door No/ Flat")
    street = fields.Char(string="Street")
    locality = fields.Char(string="Locality")
    city = fields.Char(string="City")
    state_id = fields.Many2one(comodel_name="res.state", string="State")
    country_id = fields.Many2one(comodel_name="res.country", string="Country")
    zip_code = fields.Char(string="Zip Code")

    # Personal Detail
    age = fields.Integer(string="Age")
    dob = fields.Date(string="Date Of Birth")
    marital_status = fields.Selection(MARITAL_INFO, string="Marital Status")
    gender = fields.Selection(GENDER_INFO, string="Gender")

    # Order Detail
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position", required=True)

    # Education Details
    qualification_ids = fields.One2many(comodel_name="resume.qualification",
                                        inverse_name="resume_id",
                                        string="Qualification")
    experience_ids = fields.One2many(comodel_name="resume.experience",
                                     inverse_name="resume_id",
                                     string="Experience")

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Others")

    # Resume
    resume = fields.Binary(string="Resume")

    def default_vals_creation(self, vals):
        vals["date"] = datetime.now().strftime("%Y-%m-%d")
        vals["candidate_uid"] = self.env['ir.sequence'].sudo().next_by_code(self._name)
        return vals