# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('approved', 'Approved')]


class Leave(surya.Sarpam):
    _name = "leave.application"
    _inherit = "mail.thread"

    from_date = fields.Date(string="From Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", readonly=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Many2one(comodel_name="res.user", string="User", track_visibility='always')

    @api.multi
    def trigger_confirmed(self):
        data = {"progress": "confirmed",
                "writter": self.env.user.id}

        self.write(data)

    @api.multi
    def trigger_cancelled(self):
        data = {"progress": "cancelled",
                "writter": self.env.user.id}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        data = {"progress": "approved",
                "writter": self.env.user.id}

        self.write(data)

    def default_vals_creation(self, vals):
        employee_id = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        vals["employee_id"] = employee_id.id
        return vals
