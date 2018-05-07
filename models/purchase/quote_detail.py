# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


PROGRESS_INFO = [('draft', 'Draft'),
                 ('qa', 'Quotation Approved'),
                 ('cancel', 'Cancel')]


class VSQuoteDetail(surya.Sarpam):
    _name = 'vs.quote.detail'
    _description = 'Vendor Selection Quote Detail'

    vendor_id = fields.Many2one(comodel_name='hospital.partner', string='Vendor', readonly=True)
    product_id = fields.Many2one(comodel_name='product.product', string='Product', related='vs_quote_id.product_id')
    uom_id = fields.Many2one(comodel_name='product.uom', string='UOM', related='vs_quote_id.uom_id')
    requested_quantity = fields.Float(string='Requested Quantity', default=0, readonly=True)
    accepted_quantity = fields.Float(string='Accepted Quantity', default=0)
    unit_price = fields.Float(string='Unit Price', default=0)

    discount = fields.Float(string='Discount', default=0)
    discount_amount = fields.Float(string='Discount Amount', default=0, readonly=True)
    discounted_amount = fields.Float(string='Discounted Amount', readonly=True, help='Amount after discount')
    tax_id = fields.Many2one(comodel_name='res.tax', string='Tax')
    igst = fields.Float(string='IGST', default=0, readonly=True)
    cgst = fields.Float(string='CGST', default=0, readonly=True)
    sgst = fields.Float(string='SGST', default=0, readonly=True)
    tax_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    taxed_amount = fields.Float(string='Taxed Amount', default=0, readonly=True)
    untaxed_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    total_amount = fields.Float(string='Total', default=0, readonly=True)
    vs_quote_id = fields.Many2one(comodel_name='vs.detail', string='Vendor Selection')
    quotation_id = fields.Many2one(comodel_name='purchase.quotation', string='Quotation')
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='quotation_id.progress')

    @api.multi
    def detail_calculation(self):
        price = 0
        if (self.unit_price > 0) and (self.accepted_quantity > 0):
            price = self.unit_price * self.accepted_quantity

        discount = self.discount if self.discount else 0
        tax = int(self.tax_id.value) if self.tax_id.value else 0
        tax_state = self.tax_id.state

        discounted_amount = (price - (price * (float(discount) / 100))) or 0

        tax_amount = (discounted_amount * (float(tax) / 100)) or 0

        print tax_amount

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

