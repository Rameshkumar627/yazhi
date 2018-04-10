# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json
from purchase_calculation import PurchaseCalculation as PC


# Purchase Order
PROGRESS_INFO = [('draft', 'Draft'),
                 ('approved', 'Approved'),
                 ('cancelled', 'Cancelled')]


class PurchaseOrder(surya.Sarpam):
    _name = "purchase.order"
    _rec_name = "sequence"

    sequence = fields.Char(string="Sequence", readonly=True)
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent", readonly=True)
    date = fields.Date(string="Date", readonly=True)
    vendor_id = fields.Many2one(comodel_name="res.partner", string="Vendor", readonly=True)
    vs_id = fields.Many2one(comodel_name='vendor.selection', string='Vendor Selection', readonly=True)
    quotation_id = fields.Many2one(comodel_name='purchase.quotation', string='Quotation', readonly=True)

    processed_by = fields.Many2one(comodel_name='hr.employee', string='Processed By', readonly=True)
    processed_on = fields.Date(string='Processed On', readonly=True)
    po_detail = fields.One2many(comodel_name='po.detail', inverse_name='po_id',
                                string='Purchase Order Detail', readonly=True)
    progress = fields.Selection(PROGRESS_INFO, default='draft', string='Progress')
    comment = fields.Text(string='Comment')

    total = fields.Float(string='Total', readonly=True)
    freight_amount = fields.Float(string="Freight Amount", readonly=True)
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

    @api.multi
    def trigger_update(self):
        recs = self.po_detail

        total = freight_amount = 0
        discount_amount = discounted_amount = 0
        tax_amount = taxed_amount = un_taxed_amount = 0
        cgst = sgst = igst = 0
        gross_amount = round_off = net_amount = 0

        for rec in recs:
            rec.calculate_total()

            total = total + rec.total
            discount_amount = discount_amount + rec.discount_amount
            discounted_amount = discounted_amount + rec.discounted_amount
            tax_amount = tax_amount + rec.tax_amount
            taxed_amount = taxed_amount + rec.taxed_amount
            un_taxed_amount = un_taxed_amount + rec.un_taxed_amount
            cgst = cgst + rec.cgst
            sgst = sgst + rec.sgst
            igst = igst + rec.igst

        freight_amount = self.freight_amount
        un_taxed_amount = un_taxed_amount + self.freight_amount
        gross_amount = total + freight_amount
        net_amount = round(gross_amount)
        round_off = net_amount - gross_amount

        data = {"total": total,
                "freight_amount": freight_amount,
                "discount_amount": discount_amount,
                "discounted_amount": discounted_amount,
                "tax_amount": tax_amount,
                "taxed_amount": taxed_amount,
                "un_taxed_amount": un_taxed_amount,
                "sgst": sgst,
                "cgst": cgst,
                "igst": igst,
                "gross_amount": gross_amount,
                "round_off": round_off,
                "net_amount": net_amount}

        self.write(data)

    @api.multi
    def trigger_approved(self):
        recs = self.po_detail

        mr_detail = []
        for rec in recs:
            mr_detail.append((0, 0, {"product_id": rec.product_id.id,
                                     "uom_id": rec.uom_id.id,
                                     "unit_price": rec.unit_price,
                                     "discount": rec.discount,
                                     "tax_id": rec.tax_id.id}))

        data = {"vendor_id": self.vendor_id.id,
                "indent_id": self.indent_id.id,
                "vs_id": self.vs_id.id,
                "po_id": self.id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "mr_detail": mr_detail}

        self.env["material.receipt"].create(data)

        self.write({"progress": "approved"})

    @api.multi
    def trigger_cancelled(self):
        mr = self.env["material.receipt"].search([("po_id", "=", self.id)])
        if mr:
            raise exceptions.ValidationError("Error! You cannot cancel PO since material receipt is in progress")
        self.write({"progress": "cancelled"})


class PurchaseOrderDetail(surya.Sarpam):
    _name = "po.detail"

    product_id = fields.Many2one(comodel_name="product.product", string="Product", readonly=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", readonly=True)
    quantity = fields.Float(string="Quantity", readonly=True)
    po_id = fields.Many2one(comodel_name="purchase.order", string="Purchase Order")
    unit_price = fields.Float(string='Unit Price', default=0, readonly=True)
    discount = fields.Float(string='Discount', default=0, readonly=True)
    discount_amount = fields.Float(string='Discount Amount', default=0, readonly=True)
    discounted_amount = fields.Float(string='Discounted Amount', default=0, readonly=True)
    tax_id = fields.Many2one(comodel_name='product.tax', string='Tax', readonly=True)
    igst = fields.Float(string='IGST', default=0, readonly=True)
    cgst = fields.Float(string='CGST', default=0, readonly=True)
    sgst = fields.Float(string='SGST', default=0, readonly=True)
    tax_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    taxed_amount = fields.Float(string='Taxed Amount', default=0, readonly=True)
    un_taxed_amount = fields.Float(string='Tax Amount', default=0, readonly=True)
    total = fields.Float(string='Total', default=0, readonly=True)
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='po_id.progress')

    @api.multi
    def calculate_total(self):
        price = self.quantity * self.unit_price

        pc_obj = PC()
        discount_amount = pc_obj.calculate_percentage(price, self.discount)

        discounted_amount = price - discount_amount
        igst, cgst, sgst = pc_obj.calculate_tax(discounted_amount, self.tax_id.value, self.tax_id.name)
        tax_amount = igst + cgst + sgst
        total = discounted_amount + tax_amount

        data = {'discount_amount': discount_amount,
                'discounted_amount': discounted_amount,
                'igst': igst,
                'cgst': cgst,
                'sgst': sgst,
                'tax_amount': tax_amount,
                'taxed_amount': total,
                'un_taxed_amount': 0,
                'total': total
                }

        self.write(data)
