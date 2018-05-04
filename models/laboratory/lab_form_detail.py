# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("completed", "Completed")]

STATUS_INFO = [("draft", "Draft"), ("completed", "Completed")]


class LabTestFormDetail(surya.Sarpam):
    _name = "lab.form.detail"

    test_id = fields.Many2one(comodel_name="lab.test", string="Test", required=True)
    status = fields.Selection(selection=STATUS_INFO, string="Status", default="draft")
    lab_form_id = fields.Many2one(comodel_name="lab.form", string="Lab Form")
    lab_form_test_detail = fields.One2many(comodel_name="lab.form.test.detail",
                                           inverse_name="detail_id",
                                           string="Lab Form Test Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="lab_form_id.progress")
    template = fields.Html(string="Template")
    report = fields.Html(string="Report")

    @api.multi
    def trigger_completed(self):
        self.write({"status": "completed"})

    def default_vals_creation(self, vals):
        test_id = self.env["lab.test"].search([("id", "=", vals["test_id"])])
        recs = test_id.test_detail

        test_detail = []
        for rec in recs:
            test_detail.append((0, 0, {"name": rec.name}))

        vals["lab_form_test_detail"] = test_detail
        return vals


class LabTestFormTestDetail(surya.Sarpam):
    _name = "lab.form.test.detail"

    name = fields.Char(string="Name", readonly=True)
    value = fields.Char(string="Value")
    detail_id = fields.Many2one(comodel_name="lab.form.detail", string="Test Detail")
