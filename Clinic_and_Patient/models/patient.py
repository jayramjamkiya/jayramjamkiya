from odoo import api, fields, models, _
from datetime import date, timedelta


class Patient(models.Model):
    _name = 'patient.patient'
    _description = 'patient'
    _rec_name = "patient_name"

    patient_num = fields.Char(string="Patient Number", default=lambda self: _('New'))
    patient_name = fields.Char(string="Name", translate=True)
    address = fields.Char(string="Address")
    dob = fields.Date(string="Date of birth")
    age = fields.Integer(compute="_age_calculations", store=True, string='Age')
    opd_count = fields.Integer(compute="_opd_count", string="Patient OPD")
    image = fields.Image(string="Image")
    color = fields.Integer(string="color")
    # record ->
    user_id = fields.Many2one('res.users', 'user_id')
    email_id = fields.Char('email_id')
    phone = fields.Char(string="phone number")

    @api.depends('dob')
    def _age_calculations(self):
        for rec in self:
            # if rec.dob:
            #     rec.age = (date.today() - rec.dob) // timedelta(days=365.2425)
            # else:
            #     rec.age = 0
            rec.age = rec.dob and date.today().year - rec.dob.year or 0

    @api.model
    def create(self, vals):
        vals['patient_num'] = self.env['ir.sequence'].next_by_code('patient.patient') or _('New')
        return super(Patient, self).create(vals)

    def action_patient_opd(self):
        return {
            'name': _('Patient OPD'),
            'res_model': 'opd.opd',
            'view_mode': 'list,form',
            'context': {},
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',

        }

    def _opd_count(self):
        for rec in self:
            total_opd = self.env['opd.opd'].search_count([('name_id', '=', rec.id)])
            rec.opd_count = total_opd

    def action_create_patient(self):
        for rec in self:
            res_user = self.env['res.users'].create({
                'name': rec.patient_name,
                'login': rec.email_id,
                'sel_groups_1_9_10': 1,
                'in_group_46': 1,
            })
            rec.user_id = res_user.id
