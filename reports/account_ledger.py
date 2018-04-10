# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

# Profit Loss
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Ledger(surya.Sarpam):
    _name = "account.ledger"


