# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("cancelled", "Cancelled"),
                 ("completed", "Completed")]

STATUS_INFO = [("draft", "Draft"), ("completed", "Completed")]
DELIVERY_INFO = [("not_sent", "Not Sent"), ("sent", "Sent")]
DELIVERY_REQUEST = [("mail", "Mail"), ("post", "Post"), ("in_person", "In Person")]
BILL_INFO = [("not_paid", "Not Paid"), ("partially_paid", "Partially Paid"), ("fully_paid", "Fully Paid")]


# Lab Test
class LabForm(surya.Sarpam):
    _name = "lab.form"

    date = fields.Date(string="Date")
    sequence = fields.Char(string="Sequence", readonly=True)
    patient_id = fields.Many2one(comodel_name="res.patient", string="Patient")
    delivery_request = fields.Selection(selection=DELIVERY_REQUEST, string="Delivery Request")
    delivery_status = fields.Selection(selection=DELIVERY_INFO, string="Delivery Status", default="not_sent")
    bill_status = fields.Selection(selection=BILL_INFO, string="Bill Status", default="not_paid", readonly=True)
    lab_form_detail = fields.One2many(comodel_name="lab.form.detail",
                                      inverse_name="lab_form_id",
                                      string="Lab Form Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    template = fields.Html(string="Template")
    report = fields.Html(string="Report")

    @api.multi
    def generate_bill(self):
        pass

    @api.multi
    def revert_bill(self):
        pass

    @api.multi
    def trigger_bill_preview(self):
        pass

    @api.multi
    def trigger_confirmed(self):
        self.generate_bill()
        self.write({"progress": "confirmed"})

    @api.multi
    def trigger_cancelled(self):
        self.revert_bill()
        self.write({"progress": "cancelled"})

    @api.multi
    def trigger_completed(self):
        self.write({"progress": "completed"})
