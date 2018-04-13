# -*- coding: utf-8 -*-

from odoo.http import Controller, route, request
from odoo.addons.web.controllers.main import db_monodb, ensure_db, set_cookie_and_redirect, login_and_redirect


class MonthlyAttendance(Controller):
    @route('/yazhi/monthly_attendance', type="http", auth='none')
    def report_monthly_attendance(self):
        return "Ramesh"


