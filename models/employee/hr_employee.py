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


class HrEmployee(surya.Sarpam):
    _name = "hr.employee"
    _inherit = ["hr.account.info", "hr.personal.info"]

    name = fields.Char(string="Name", required=True)
    employee_uid = fields.Char(string="Employee ID")
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    very_small_image = fields.Binary(string="Image")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')
    work_email = fields.Char(string="Work Email")
    work_mobile = fields.Char(string="Work Mobile", required=True)
    doj = fields.Date(string="Date of Joining", required=False)
    date_of_relieving = fields.Date(string="Date of Relieving")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    designation_id = fields.Many2one(comodel_name="hr.designation", string="Designation")
    reporting_to_id = fields.Many2one(comodel_name="hr.employee", string="Reporting To")
    employee_category_id = fields.Many2one(comodel_name="hr.category", string="Employee Category")
    qualification_ids = fields.One2many(comodel_name="hr.qualification",
                                        inverse_name="employee_id",
                                        string="Qualification")
    experience_ids = fields.One2many(comodel_name="hr.experience",
                                     inverse_name="employee_id",
                                     string="Experience")
    attachment_ids = fields.One2many(comodel_name="hr.attachment",
                                     inverse_name="employee_id",
                                     string="Attachment")
    leave_ids = fields.One2many(comodel_name="hr.leave",
                                inverse_name="employee_id",
                                string="Leave")
    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level")
    user_id = fields.Many2one(comodel_name="res.users", string="User")

    is_doctor = fields.Boolean(string="Doctor")
    is_nurse = fields.Boolean(string="Nurse")
    is_contract = fields.Boolean(string="Contract")
    is_admin_staff = fields.Boolean(string="Admin Staff")
    is_ambulance_driver = fields.Boolean(string="Ambulance Driver")
