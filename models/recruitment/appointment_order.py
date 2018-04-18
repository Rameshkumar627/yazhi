# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
MARITAL_INFO = [('male', 'Male'), ('female', 'Female')]
GENDER_INFO = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


# Appointment Order
class AppointmentOrder(surya.Sarpam):
    _name = "appointment.order"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")
    candidate_uid = fields.Char(string="Candidate ID")
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
    basic = fields.Float(string="Basic")
    salary_structure = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")
    template = fields.Html(string="Template")
    order_preview = fields.Html(string="Order Preview")
    order = fields.Binary(string="Appointment Order")

    # Education Details
    qualification_ids = fields.One2many(comodel_name="appointment.qualification",
                                        inverse_name="appointment_id",
                                        string="Qualification")
    experience_ids = fields.One2many(comodel_name="appointment.experience",
                                     inverse_name="appointment_id",
                                     string="Experience")

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    confirmed_by = fields.Many2one(comodel_name="hr.employee", string="Employee")
    confirmed_on = fields.Datetime(string="Confirmed On")

    @api.multi
    def trigger_confirmed(self):
        user_id = self.env.user.id
        employee_id = self.env["hr.employee"].search([("user_id", "=", user_id.id)])

        data = {"progress": "confirmed",
                "confirmed_by": employee_id.id}

        self.write(data)
