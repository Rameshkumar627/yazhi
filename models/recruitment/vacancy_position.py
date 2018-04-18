# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"),
                 ("open", "Opened"),
                 ("closed", "Closed")]


# Vacancy Position
class VacancyPosition(surya.Sarpam):
    _name = "vacancy.position"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    roles = fields.Html(string="Roles & Responsibility")
    experience = fields.Html(string="Experience")
    preference = fields.Html(string="Preference")
    qualification = fields.Html(string="Qualification")
    comment = fields.Text(string="Comment")
    opened_by = fields.Many2one(comodel_name="hr.employee", string="Opended By")
    opened_date = fields.Datetime(string="Opened Date")
    closed_by = fields.Many2one(comodel_name="hr.employee", string="Closed By")
    closed_date = fields.Datetime(string="Closed Date")

    @api.multi
    def trigger_open(self):
        user_id = self.env.user.id
        employee_id = self.env["hr.employee"].search([("user_id", "=", user_id)])
        data = {"opened_by": user_id.id,
                "progress": "opened"}

    @api.multi
    def trigger_close(self):
        user_id = self.env.user.id
        employee_id = self.env["hr.employee"].search([("user_id", "=", user_id)])
        data = {"opened_by": user_id.id,
                "progress": "closed"}
