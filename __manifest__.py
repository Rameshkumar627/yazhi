# -*- coding: utf-8 -GPK*-

{
    'name': 'Hospital',
    'version': '1.0',
    "author": 'Yazhi Technologies',
    "website": 'http://www.yalitechnologies.com/',
    'category': 'Hospital Management System',
    'sequence': 1,
    'summary': 'Hospital Management System',
    'description': 'Hospital Management System',
    'depends': ['base', 'mail'],
    'data': [
        'data/recruitment.xml',
        'data/time_management.xml',
        'menu/menu.xml',
        'views/global_config/year.xml',
        'views/global_config/period.xml',
        'menu/global_config.xml',
        'views/employee/hr_employee.xml',
        'views/employee/hr_attachment.xml',
        'views/employee/hr_category.xml',
        'views/employee/hr_contact.xml',
        'views/employee/hr_department.xml',
        'views/employee/hr_designation.xml',
        'views/employee/hr_experience.xml',
        'views/employee/hr_leave.xml',
        'views/employee/hr_qualification.xml',
        'views/time_management/shift.xml',
        'views/time_management/week_schedule.xml',
        'views/time_management/attendance.xml',
        'views/time_management/monthly_attendance.xml',
        'views/time_management/time_sheet.xml',
        'views/time_management/time_sheet_application.xml',
        'views/time_management/shift_change.xml',
        'views/time_management/time_configuration.xml',
        'views/payroll_management/salary_rule.xml',
        'views/payroll_management/salary_structure.xml',
        'views/payroll_management/hr_pay.xml',
        'views/payroll_management/payslip.xml',
        'views/leave_management/leave.xml',
        'views/leave_management/permission.xml',
        'views/leave_management/compoff.xml',
        'views/recruitment/resume_bank.xml',
        'views/recruitment/interview_schedule.xml',
        'views/recruitment/appointment_order.xml',
        'views/recruitment/vacancy_position.xml',
        'menu/employee.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
