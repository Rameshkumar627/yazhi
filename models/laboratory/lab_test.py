# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"),
                 ("on_processing", "On Processing"),
                 ("cancelled", "Cancelled"),
                 ("completed", "Completed")]

STATUS_INFO = [("draft", "Draft"), ("completed", "Completed")]
DELIVERY_INFO = [("not_sent", "Not Sent"), ("sent", "Sent")]
DELIVERY_REQUEST = [("mail", "Mail"), ("post", "Post"), ("in_person", "In Person")]
BILL_INFO = [("draft", "Draft"), ("partially_paid", "Partially Paid"), ("fully_paid", "Fully Paid")]


# Lab Test
class LabTest(surya.Sarpam):
    _name = "lab.test"

    date = fields.Date(string="Date")
    patient_id = fields.Many2one(comodel_name="res.patient", string="Patient")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    delivery_request = fields.Selection(selection=DELIVERY_REQUEST, string="Delivery Request")
    delivery_status = fields.Selection(selection=DELIVERY_INFO, string="Delivery Status")
    bill_status = fields.Selection(selection=BILL_INFO, string="Bill Status")

    test_detail = fields.One2many(comodel_name="lab.test.detial",
                                  inverse_name="lab_test_id",
                                  string="Lab Test Detail")

    @api.multi
    def generate_bill(self):
        recs = self.test_detail

        detail = []
        for rec in recs:
            detail.append((0, 0, {"description": rec.test_id}))

    @api.multi
    def trigger_cancel(self):
        self.write({"progress": "cancelled"})

    @api.multi
    def trigger_completed(self):
        self.write({"progress": "completed"})

    @api.multi
    def trigger_on_processing(self):
        self.write({"progress": "on_processing"})


class LabTestDetail(surya.Sarpam):
    _name = "lab.test.detail"

    test_id = fields.Many2one(comodel_name="test.test", string="Test")
    status = fields.Selection(selection=STATUS_INFO, string="Status")
    lab_test_id = fields.Many2one(comodel_name="lab.test", string="Lab Test")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="lab_test_id.progress")
