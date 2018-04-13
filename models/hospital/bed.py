# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
import json


# Bed
class Bed(surya.Sarpam):
    _name = "ward.bed"

    name = fields.Char(string="Bed")
    ward_id = fields.Many2one(comodel_name="hospital.ward", string="Ward")
