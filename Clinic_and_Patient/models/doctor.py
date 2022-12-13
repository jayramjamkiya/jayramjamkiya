from odoo import api, fields, models, _
from datetime import date, timedelta


class Doctor(models.Model):
    _name = 'doctor.doctor'
    _description = 'doctor'
    _rec_name = "doc_name"

    doctor_num = fields.Char(string="Doctor Number", default=lambda self: _('New'), readonly=True)
    doc_name = fields.Char(string="Name", translate=True)
    address = fields.Char(string="Address")
    dob = fields.Date(string="Date of birth")
    age = fields.Integer(compute="_age_calculations", readonly="1", store=True, string='Age')
    department_id = fields.Many2one("department.department", string="Department")
    opd_count = fields.Integer(compute="_opd_count_doc", string="Patient OPD")
    # record-->
    user_id = fields.Many2one('res.users', 'User ID')
    email_id = fields.Char('email_id')

    @api.depends('dob')
    def _age_calculations(self):
        for rec in self:
            rec.age = rec.dob and date.today().year - rec.dob.year or 0

    @api.model
    def create(self, vals):
        vals['doctor_num'] = self.env['ir.sequence'].next_by_code('doctor.doctor') or _('New')
        return super(Doctor, self).create(vals)

    def action_doctor_opd(self):
        return {
            'name': _('Doctor OPD'),
            'res_model': 'opd.opd',
            'view_mode': 'list,form',
            'context': {},
            'domain': [('doc_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    def _opd_count_doc(self):
        for rec in self:
            total_opd = self.env['opd.opd'].search_count([('doc_id', '=', rec.id)])
            rec.opd_count = total_opd

    def action_create_doctor(self):
        for rec in self:
            res_user = self.env['res.users'].create({
                'name': rec.doc_name,
                'login': rec.email_id,
                'sel_groups_1_9_10': 1,
                'in_group_47': True,
            })
            rec.user_id = res_user.id
