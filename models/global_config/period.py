# -*- coding: utf-8 -GPK*-

from odoo import fields, api, exceptions
from .. import surya
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("open", "Open"), ("closed", "Closed")]


class Period(surya.Sarpam):
    _name = "period.period"

    name = fields.Char(string="Name", readonly=True)
    year = fields.Char(string="Year", readonly=True)
    from_date = fields.Date(string="From Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    @api.multi
    def trigger_period_open(self):
        self.check_progress()
        self.write({"progress": "open"})

    @api.multi
    def trigger_period_closed(self):
        self.write({"progress": "closed"})

    def check_progress(self):
        if self.env["period.period"].search([("progress", "=", "open")]):
            raise exceptions.ValidationError("Error! Please close the existing period before open new period")

    def default_vals_creation(self, vals):
        from_date = datetime.strptime(vals["from_date"], "%Y-%m-%d")
        till_date = datetime.strptime(vals["till_date"], "%Y-%m-%d")

        if from_date.strftime("%m-%Y") != till_date.strftime("%m-%Y"):
            raise exceptions.ValidationError("Error! Period must be within a month")

        vals["name"] = "{0} To {1}".format(from_date.strftime("%m-%Y"), till_date.strftime("%m-%Y"))
        vals["year"] = "{0}".format(from_date.strftime("%m-%Y"))

        return vals



