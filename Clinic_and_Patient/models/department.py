from odoo import api, fields, models, _


class Department(models.Model):
    _name = "department.department"
    _description = "department"
    _rec_name = "department"

    department = fields.Char(string="Department Name")
    doctor_ids = fields.One2many("doctor.doctor", "department_id", string="Doctor")
#     new object ma leva mate many2many no used karel 6 ....
#     facility_ids = fields.Many2many("department.facility", string='facility')
#
# many2many leva mate apde bijo class lidhel 6 >>>>>>>>>>>>>>>>>>
# class DepartmentFacility(models.Model):
#     _name = "department.facility"
#     _rec_name = "facility"
#     _description = "facility"
#
#     facility = fields.Char("Facilities")
