# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("completed", "Completed")]

STATUS_INFO = [("draft", "Draft"), ("completed", "Completed")]
DELIVERY_INFO = [("not_sent", "Not Sent"), ("sent", "Sent")]
DELIVERY_REQUEST = [("mail", "Mail"), ("post", "Post"), ("in_person", "In Person")]
BILL_INFO = [("not_paid", "Not Paid"), ("partially_paid", "Partially Paid"), ("fully_paid", "Fully Paid")]


# Lab Test
class LabForm(surya.Sarpam):
    _name = "lab.form"
    _inherit = "mail.thread"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="hr.employee", string="Patient")
    delivery_request = fields.Selection(selection=DELIVERY_REQUEST, string="Delivery Request", default="in_person")
    delivery_status = fields.Selection(selection=DELIVERY_INFO, string="Delivery Status", default="not_sent")
    bill_status = fields.Selection(selection=BILL_INFO, string="Bill Status", default="not_paid", readonly=True)
    lab_form_detail = fields.One2many(comodel_name="lab.form.detail",
                                      inverse_name="lab_form_id",
                                      string="Lab Form Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    template = fields.Html(string="Template")
    report = fields.Html(string="Report")
    writter = fields.Many2one(comodel_name="res.user", string="User", track_visibility='always')

    @api.multi
    def bill_generation(self):
        vals = {}
        vals['partner_id'] = self.patient_id.id
        vals['reference'] = self.name
        invoice_detail = []

        recs = self.lab_form_detail
        for rec in recs:
            tax = self.env["tax.configuration"].search([("name", "=", "Laboratory")])

            invoice_detail.append((0, 0, {"product_id": rec.test_id.product_id.id,
                                          "price": rec.test_id.amount,
                                          "tax": tax.tax_id.id}))

        vals["invoice_detail"] = invoice_detail

        invoice = self.env["hospital.invoice"].create(vals)
        invoice.total_calculation()

    @api.multi
    def trigger_bill_preview(self):
        rec = self.env["hospital.invoice"].search([("reference", "=", self.name)])

        if not rec:
            self.bill_generation()
            rec = self.env["hospital.invoice"].search([("reference", "=", self.name)])

        view = self.env.ref('yazhi.view_hospital_invoice_form')

        return {
            'name': 'Laboratory Bill',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'hospital.invoice',
            'type': 'ir.actions.act_window',
            'res_id': rec.id,
            'target': 'new',
            'context': self.env.context
        }

    @api.multi
    def trigger_confirmed(self):
        self.trigger_bill_preview()
        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        self.write({"progress": "confirmed", "writter": writter.id})

    @api.multi
    def trigger_completed(self):
        self.check_pending_test()
        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        self.write({"progress": "completed", "writter": writter.id})

    def check_pending_test(self):
        recs = self.env["lab.form.detail"].search_count([("lab_form_id", "=", self.id),
                                                         ("status", "!=", "completed")])

        if recs:
            raise exceptions.ValidationError("Error! Some Test is In-Progress")

    def default_vals_creation(self, vals):
        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        vals['name'] = self.env['ir.sequence'].next_by_code(self._name)
        vals['writter'] = writter.id
        if vals.get('date', False):
            vals['date'] = datetime.now().strftime("%Y-%m-%d")
        return vals

