# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Attachment
class HRAttachment(surya.Sarpam):
    _name = 'hr.attachment'

    name = fields.Char(string="Name", required=True)
    attachment = fields.Binary(string="Attachment", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")

