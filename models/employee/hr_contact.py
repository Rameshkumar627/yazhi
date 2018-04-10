# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Contacts

class HRContact(surya.Sarpam):
    _name = "hr.contact"

    name = fields.Char(string="Name")
    relation = fields.Char(string="Relation")
    no = fields.Char(string="Door/Flat No")
    building_name = fields.Char(string="Building Name")
    street_name = fields.Char(string="Street Name")
    locality = fields.Char(string="Locality")
    city_id = fields.Many2one(comodel_name="res.city", string="State")
    landmark = fields.Char(string="Landmark")
    zip_code = fields.Char(string="Zip Code")
    state_id = fields.Many2one(comodel_name="res.state", string="State")
    country_id = fields.Many2one(comodel_name="res.country", string='Country')
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
