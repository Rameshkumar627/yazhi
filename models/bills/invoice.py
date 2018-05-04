# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _, models
from datetime import datetime, timedelta
from .. import surya
import json


PROGRESS_INFO = [('draft', 'Draft'), ('approved', 'approved'), ('cancelled', 'Cancelled')]
INVOICE_TYPE = [('lab_bill', "Lab Bill"),
                ('pharmacy_bill', 'Pharmacy Bill'),
                ('purchase_bill', 'Purchase Bill'),
                ('service_bill', 'Service Bill')]


# Bills
class HospitalInvoice(surya.Sarpam):
    _name = "hospital.invoice"
    _inherit = "mail.thread"

    date = fields.Date(srring="Date", required=True)
    name = fields.Char(string="Name", readonly=True)
    partner_id = fields.Many2one(comodel_name="hr.employee", string="Partner")
    writter = fields.Many2one(comodel_name="hr.employee", string="User", track_visibility='always')

    invoice_detail = fields.One2many(comodel_name="invoice.detail",
                                     inverse_name="invoice_id",
                                     string="Invoice detail")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    invoice_type = fields.Selection(selection=INVOICE_TYPE, string="Invoice Type")

    discount_amount = fields.Float(string="Discount Amount", readonly=True)
    discounted_amount = fields.Float(string="Discounted Amount", readonly=True)
    tax_amount = fields.Float(string="Tax Amount", readonly=True)
    untaxed_amount = fields.Float(string="Untaxed Amount", readonly=True)
    taxed_amount = fields.Float(string="Taxed Amount", readonly=True)
    cgst = fields.Float(string="CGST", readonly=True)
    sgst = fields.Float(string="SGST", readonly=True)
    igst = fields.Float(string="IGST", readonly=True)

    total = fields.Float(string="Total", readonly=True)
    freight_amount = fields.Float(string="Freight Amount", readonly=True)
    total_amount = fields.Float(string="Total Amount", readonly=True)
    round_off_amount = fields.Float(string="Round-Off", readonly=True)
    gross_amount = fields.Float(stringt="Gross Amount", readonly=True)
    net_amount = fields.Float(string="Net Amount", readonly=True)

    reference = fields.Char(string="Reference", readonly=True)
    # payment_detail = fields.One2many(comodel_name="invoice.detail",
    #                                  inverse_name="invoice_id",
    #                                  string="Invoice detail")
    # Account_detail

    def default_vals_creation(self, vals):
        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        vals['name'] = self.env['ir.sequence'].next_by_code(self._name)
        vals['writter'] = writter.id
        if vals.get('date', True):
            vals['date'] = datetime.now().strftime("%Y-%m-%d")
        return vals

    @api.multi
    def total_calculation(self):
        recs = self.invoice_detail

        if not recs:
            raise exceptions.ValidationError("Error! Bill details not found")

        for rec in recs:
            rec.detail_calculation()

    @api.multi
    def trigger_approved(self):
        self.total_calculation()
        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        self.write({"progress": "approved", "writter": writter.id})

    @api.multi
    def trigger_cancel(self):
        writter = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        self.write({"progress": "cancelled", "writter": writter.id})


class InvoiceDetail(surya.Sarpam):
    _name = "invoice.detail"

    product_id = fields.Many2one(comodel_name="product.product", string="Description", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    price = fields.Float(string="Amount", required=True)
    discount = fields.Float(string="Discount")
    tax = fields.Many2one(comodel_name="res.tax", string="Tax", required=True)
    total_amount = fields.Float(string="Total Amount", readonly=True)

    cgst = fields.Float(string="CGST", readonly=True)
    sgst = fields.Float(string="SGST", readonly=True)
    igst = fields.Float(string="IGST", readonly=True)

    tax_amount = fields.Float(string="Tax Amount", readonly=True)
    discounted_amount = fields.Float(string="Discounted Amount", readonly=True)
    untaxed_amount = fields.Float(string="Untaxed Value", readonly=True)
    taxed_amount = fields.Float(string="Taxed value", readonly=True)

    invoice_id = fields.Many2one(comodel_name="hospital.invoice", string="Hospital Invoice")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="invoice_id.progress")

    @api.multi
    def detail_calculation(self):
        price = self.price if self.price else 0
        discount = self.discount if self.discount else 0
        tax = int(self.tax.value) if self.tax.value else 0
        tax_state = self.tax.state

        discounted_amount = (price - (price * float(discount/100))) or 0

        tax_amount = (discounted_amount * float(tax/100)) or 0
        taxed_amount = (discounted_amount + tax_amount) or 0
        untaxed_amount = 0
        total_amount = taxed_amount + untaxed_amount

        cgst = sgst = igst = 0
        if tax_state == 'inter_state':
            sgst = tax_amount
        elif tax_state == 'outer_state':
            cgst = igst = tax_amount / 2

        self.write({"cgst": cgst,
                    "sgst": sgst,
                    "igst": igst,
                    "discounted_amount": discounted_amount,
                    "tax_amount": tax_amount,
                    "taxed_amount": taxed_amount,
                    "untaxed_amount": untaxed_amount,
                    "total_amount": total_amount})
