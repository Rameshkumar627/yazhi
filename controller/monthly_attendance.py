# -*- coding: utf-8 -*-

from odoo.http import Controller, route, request


class MonthlyAttendance(Controller):
    @route('/yazhi/monthly_attendance', type="http", auth='user')
    def report(self):
        print request.env.context
        return "ramesh"
