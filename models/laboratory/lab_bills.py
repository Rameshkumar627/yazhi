# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _, models
from datetime import datetime, timedelta
from .. import surya
import json


PROGRESS_INFO = [('draft', 'Draft'), ('approved', 'approved'), ('cancelled', 'Cancelled')]


# Bills
class LabBills(surya.Sarpam):
    _name = "lab.bill"

    date = fields.Date(srring="Date")
    patient_id = fields.Many2one(comodel_name="res.patient", string="Patient")
    bill_detail = fields.One2many(comodel_name="lab.bill.detail",
                                  inverse_name="bill_id", string="Bill detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    cgst = fields.Float(string="CGST")
    sgst = fields.Float(string="SGST")
    igst = fields.Float(string="IGST")
    tax_value = fields.Float(string="Tax value")
    untaxed_value = fields.Float(string="Untaxed Value")
    taxed_value = fields.Float(string="Taxed value")
    total_amount = fields.Float(string="Total Amount")
    round_off_amount = fields.Float(string="Round-Off")
    gross_amount = fields.Float(stringt="Gross Amount")

    @api.multi
    def total_calculation(self):
        recs = self.bill_detail

        for rec in recs:
            rec.detail_calculation()

    @api.multi
    def trigger_approved(self):
        self.total_calculation()
        self.write({"progress": "approved"})

    @api.multi
    def trigger_cancel(self):
        self.write({"progress": "cancelled"})


class LabBillsDetail(surya.Sarpam):
    _name = "lab.bill.detail"

    test_id = fields.Many2one(comodel_name="test.test", string="Test")
    price = fields.Float(string="Amount")
    tax = fields.Many2one(comodel_name="res.tax", string="Tax")
    discount = fields.Float(string="Discount")
    discounted_amount = fields.Float(string="Discounted Amount")
    cgst = fields.Float(string="CGST")
    sgst = fields.Float(string="SGST")
    igst = fields.Float(string="IGST")
    tax_value = fields.Float(string="Tax value")
    untaxed_value = fields.Float(string="Untaxed Value")
    taxed_value = fields.Float(string="Taxed value")
    total_amount = fields.Float(string="Total Amount")

    @api.multi
    def detail_calculation(self):
        price = self.price
        discount = self.discount
        tax = self.tax.value
        tax_state = self.tax.state

        discounted_amount = (price - (price * (discount/100))) or 0
        tax_value = (discounted_amount * (tax/100)) or 0
        taxed_value = (discounted_amount + tax_value) or 0
        untaxed_value = 0
        total_amount = taxed_value + untaxed_value

        cgst = sgst = igst = 0
        if tax_state == 'in':
            sgst = tax_value
        elif tax_state == 'out':
            cgst = igst = tax_value / 2

        self.write({"cgst": cgst,
                    "sgst": sgst,
                    "igst": igst,
                    "discounted_amount": discounted_amount,
                    "tax_value": tax_value,
                    "taxed_value": taxed_value,
                    "untaxed_value": untaxed_value,
                    "total_amount": total_amount})
