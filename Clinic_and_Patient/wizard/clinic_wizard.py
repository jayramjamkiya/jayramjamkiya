from odoo import api, fields, models, _


class OPDform(models.TransientModel):
    _name = "class.wiz.action"
    _description = 'opd_from'

    # @api.onchange('dep_id')
    # def onchange_dep_id(self):
    #     for rec in self:
    #         return {'domain': {'doc_id': [('department_id.id', '=', rec.dep_id.id)]}}

    # @api.onchange('name_id')
    # def onchange_Name(self):
    #     if self.name_id:
    #         if self.name_id.address:
    #             self.address = self.name_id.address
    #         if self.name_id.dob:
    #             self.dob = self.name_id.dob
    #
    #     else:
    #         self.address = ''
    #         self.dob = ''

    patient_name = fields.Many2one("patient.patient", string="Patient Name")
    address = fields.Char(string="Address")
    dob = fields.Date(string="Date of birth")
    department_id = fields.Many2one("department.department", string="Department")
    doctor_id = fields.Many2one("doctor.doctor", string="Doctor")

    def create_opd_form(self):

        for rec in self:
            dic = {
                'name_id': rec.patient_name.id,
                'address': rec.address,
                'dob': rec.dob,
                'dep_id': rec.department_id.id,
                'doc_id': rec.doctor_id.id,
            }

            self.env['opd.opd'].create(dic)

# def action_lost_reason_apply(self):
#     for rec in self:
#         dic = {
