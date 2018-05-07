# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

# Partner
PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("approved", "Approved"),
                 ("cancelled", "Cancelled")]


class HospitalPartner(surya.Sarpam):
    _name = "hospital.partner"
    _inherit = "mail.thread"

    name = fields.Char(string="Name")
    partner_uid = fields.Char(string="Partner UID")
    is_company = fields.Boolean(string="Is Company")
    is_user = fields.Boolean(string="Is User")
    is_employee = fields.Boolean(string="Is Employee")
    is_supplier = fields.Boolean(string="Is Supplier")
    is_patient = fields.Boolean(string="Is Patient")
    is_service = fields.Boolean(string="Is Service")

    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient")
    user_id = fields.Many2one(comodel_name="hospital.user", string="User")

    door_no = fields.Char(string="Door No")
    street = fields.Char(string="Street")
    street_2 = fields.Char(string="Street 2")
    city = fields.Char(string="City")
    zip_code = fields.Char(string="Zip")
    district = fields.Char(string="District")
    state_id = fields.Char(string="State")
    country_id = fields.Char(string="Country")

    gst_no = fields.Char(string="GST No")
    license_no = fields.Char(string="License No")
    tin_no = fields.Char(string="TIN No")
    pan_no = fields.Char(string="PAN No")



