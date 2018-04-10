# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

# Purchase Indent
PROGRESS_INFO = [('draft', 'Draft'),
                 ('po_generated', 'PO Generated'),
                 ('cancelled', 'Cancelled')]


class Quotation(surya.Sarpam):
    _name = "purchase.quotation"
    _rec_name = "sequence"

    sequence = fields.Char(string='Sequence', readonly=True)
    date = fields.Date(string="Date")
    vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor")
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent")
    vs_id = fields.Many2one(comodel_name='vendor.selection', string='Vendor Selection', readonly=True)
    vendor_ref = fields.Char(string='Vendor Ref')
    processed_by = fields.Many2one(comodel_name='hr.employee', string='Processed By', readonly=True)
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
    un_taxed_amount = fields.Float(string='Untaxed Amount', readonly=True)
    sgst = fields.Float(string='SGST', readonly=True)
    cgst = fields.Float(string='CGST', readonly=True)
    igst = fields.Float(string='IGST', readonly=True)
    gross_amount = fields.Float(string='Gross Amount', readonly=True)
    round_off = fields.Float(string='Round-Off', readonly=True)
    net_amount = fields.Float(string='Net Amount', readonly=True)
