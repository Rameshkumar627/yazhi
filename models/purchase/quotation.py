# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

# Purchase Indent
PROGRESS_INFO = [('draft', 'Draft'),
                 ('invoice_generated', 'Invoice Generated'),
                 ('cancelled', 'Cancelled')]


class Quotation(surya.Sarpam):
    _name = "purchase.quotation"
    _inherit = "mail.thread"

    name = fields.Char(string='Name', readonly=True)
    date = fields.Date(string="Date", readonly=True)
    vendor_id = fields.Many2one(comodel_name="hospital.partner", string="Vendor", readonly=True)
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent", readonly=True)
    vs_id = fields.Many2one(comodel_name="purchase.vs", string="Vendor Selection", readonly=True)
    vendor_ref = fields.Char(string="Vendor Ref")
    processed_by = fields.Many2one(comodel_name="hr.employee", string="Processed By", readonly=True)
    processed_on = fields.Date(string='Processed On', readonly=True)
    quotation_detail = fields.One2many(comodel_name='vs.quote.detail', inverse_name='quotation_id', string='Quotation Detail')
    progress = fields.Selection(PROGRESS_INFO, default='draft', string='Progress')
    comment = fields.Text(string='Comment')

    total = fields.Float(string='Total', readonly=True)
    freight_amount = fields.Float(string="Freight Amount")
    discount_amount = fields.Float(string='Discount Amount', readonly=True, help='Discount value')
    discounted_amount = fields.Float(string='Discounted Amount', readonly=True, help='Amount after discount')
    tax_amount = fields.Float(string='Tax Amount', readonly=True, help='Tax value')
    taxed_amount = fields.Float(string='Taxed Amount', readonly=True, help='Tax after discounted amount')
    untaxed_amount = fields.Float(string='Untaxed Amount', readonly=True)
    sgst = fields.Float(string='SGST', readonly=True)
    cgst = fields.Float(string='CGST', readonly=True)
    igst = fields.Float(string='IGST', readonly=True)
    gross_amount = fields.Float(string='Gross Amount', readonly=True)
    round_off_amount = fields.Float(string='Round-Off', readonly=True)
    net_amount = fields.Float(string='Net Amount', readonly=True)
    writter = fields.Text(string="Writter", track_visibility='always')

    @api.multi
    def total_calculation(self):
        recs = self.quotation_detail

        if not recs:
            raise exceptions.ValidationError("Error! Bill details not found")

        for rec in recs:
            rec.detail_calculation()

    @api.multi
    def trigger_quote_approve(self):
        data = {}

        invoice_detail = []
        recs = self.quotation_detail
        for rec in recs:
            invoice_detail.append((0, 0, {"product_id": rec.product_id.id,
                                          "unit_price": rec.unit_price,
                                          "quantity": rec.accepted_quantity,
                                          "discount": rec.discount,
                                          "tax_id": rec.tax_id.id}))

        data["date"] = datetime.now().strftime("%Y-%m-%d")
        data["name"] = self.env["ir.sequence"].next_by_code("")
        data["partner_id"] = self.vendor_id.id
        data["invoice_detail"] = invoice_detail
        data["invoice_type"] = 'purchase_bill'
        data["reference"] = self.name

        self.env["hospital.invoice"].create(data)

        employee = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        writter = "Invoice generated by {0}".format(employee.name)

        self.write({"progress": "invoice_generated", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        employee = self.env["hr.employee"].search([("user_id", "=", self.env.user.id)])
        writter = "Quotation cancelled by {0}".format(employee.name)

        self.write({"progress": "cancelled", "writter": writter})

