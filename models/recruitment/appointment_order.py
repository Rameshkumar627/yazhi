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
    _rec_name = "sequence"

    # Resume Details
    resume_id = fields.Many2one(comodel_name="resume.bank", string="Resume", required=True)
    sequence = fields.Char(string="Sequence", readonly=True)

    date = fields.Date(string="Date", required=True)
    image = fields.Binary(string="Image", related="resume_id.image")
    name = fields.Char(string="Name", related="resume_id.name")
    candidate_uid = fields.Char(string="Candidate ID", related="resume_id.candidate_uid")

    # Contact Detail
    email = fields.Char(string="Email", related="resume_id.email")
    mobile = fields.Char(string="Mobile", related="resume_id.mobile")

    # Order Detail
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position", required=True)
    template = fields.Html(string="Template")
    order_preview = fields.Html(string="Order Preview", readonly=1)
    order = fields.Binary(string="Appointment Order", readonly=1)

    # Salary Details
    basic = fields.Float(string="Basic")
    salary_structure = fields.Many2one(comodel_name="salary.structure", string="Salary Structure")

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft", track_visibility='always')
    writter = fields.Many2one(comodel_name="res.user", string="User", track_visibility='always')

    @api.multi
    def trigger_confirmed(self):
        data = {"progress": "confirmed",
                "writter": self.env.user.id}

        self.write(data)

    @api.multi
    def view_resume_bank(self):
        view = self.env.ref('yazhi.view_resume_bank_form')

        return {
            'name': 'Issue created',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'resume.bank',
            'type': 'ir.actions.act_window',
            'res_id': self.resume_id.id,
            'context': self.env.context
        }

    def default_vals_creation(self, vals):
        vals["sequence"] = self.env['ir.sequence'].sudo().next_by_code(self._name)
        return vals




