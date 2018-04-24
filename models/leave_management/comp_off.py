# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Leave

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('approved', 'Approved')]


class CompOff(surya.Sarpam):
    _name = "compoff.application"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    reason = fields.Text(string="Reason")
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
