from odoo import api, fields, models, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class Opd(models.Model):
    _name = 'opd.opd'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'opd'
    _rec_name = "opd_id"

    opd_id = fields.Char(string="OPD ID", default=lambda self: _('New'))
    patient_num = fields.Char(string="Patient Number")
    name_id = fields.Many2one("patient.patient", string="Patient Name")
    address = fields.Char(string="Address")
    dob = fields.Date(string="Date of birth")
    age = fields.Integer(compute="_age_cal", string='Age')
    dep_id = fields.Many2one("department.department", string="Department")
    doc_id = fields.Many2one("doctor.doctor", string="Doctor")
    med_ids = fields.Many2many("medicine.medicine", string="Medicines")
    med_ids_test = fields.One2many("medi.medi", "medi_name")

    # ------progress bar and state in color in kanban view --------

    def _group_expand_states(self, states, domain, order):
        return [key for
                key, val in type(self).state.selection]

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], string='Status', readonly=True, copy=False, index=True, default='draft', group_expand='_group_expand_states')

    # --------singnature in print(report) in used --------
    signature = fields.Image('Signature', help='Signature received through the portal.', copy=False, attachment=True,
                             max_width=1024, max_height=1024)
    signed_by = fields.Char('Signed By', help='Name of the person that signed the SO.', copy=False)
    signed_on = fields.Datetime('Signed On', help='Date of the signature.', copy=False)

    #  currency in amount prosess
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    untax_amount = fields.Monetary(compute="_compute_total_amount", store=True)
    tax_amount = fields.Monetary(compute="_compute_total_amount", store=True)
    total_amount = fields.Monetary(compute="_compute_total_amount", store=True)

    priority = fields.Selection(AVAILABLE_PRIORITIES, string='Priority', index=True,
                                default=AVAILABLE_PRIORITIES[2][0])

    # def copy(self, default=None):
    #     print(">>>>>>-----------copy method")
    #     if default is None:
    #         default = {}
    #     if not default.get("address"):
    #         default['address'] = "copy", self.address
    #     return super(Opd, self).copy(default)

    # header in state bar >

    def action_confirm(self):
        # #  ---  odoo domain search method:---
        # for recs in self:
        #     patient = self.env['opd.opd'].search([('state', '=', 'draft')])
        #     print(">>>>>>>>>>>>>>>>>patient..................", patient)
        for rec in self:
            rec.state = "confirmed"
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Click Successfull',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
        # copy = self.env['opd.opd'].browse(1)
        # copy.copy
        # print("___________________________________copy", copy)
        for rec in self:
            rec.state = "done"

    def action_cancel(self):  # write method in ORM
        # record_update = self.env['opd.opd'].browse(2)
        # if record_update.exists():
        #     vals = {
        #         'address': 'morbi'
        #     }
        #     record_update.write(vals)

        for rec in self:
            rec.state = "cancel"

    def action_reset(self):
        for rec in self:
            rec.state = "draft"

    # def unlink(self):
    #     print(">>>>>>>>>>>>unlink method................")
    #     if self.state == "confirmed":
    #         raise ValidationError(_("you cannot delete appointment with 'confirmed' status !"))
    #     return super(Opd, self).unlink()

    # ------create to whatsapp message in ----------
    def action_share_whatsapp(self):
        if not self.name_id.phone:
            raise ValidationError(_("Missing phone number  in patient record"))

        message = 'Hi %s your OPD number is: %s and your doctor is: %s Date: *%s* thank you %s' % (
            self.name_id.patient_name, self.opd_id, self.doc_id.doc_name, self.dob,
            self.name_id.patient_name,
        )
        whatsapp_api_url = 'http://api.whatsapp.com/send?phone=%s&text=%s' % (self.name_id.phone, message)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    @api.onchange('name_id')
    def onchange_name(self):
        if self.name_id:
            if self.name_id.address:
                self.address = self.name_id.address
            if self.name_id.dob:
                self.dob = self.name_id.dob
            if self.name_id.patient_num:
                self.patient_num = self.name_id.patient_num

        else:
            self.address = ''
            self.dob = ''
            self.patient_num = ''

    #  sequence  --->

    @api.model
    def create(self, vals):
        vals['opd_id'] = self.env['ir.sequence'].next_by_code('opd.opd') or _('New')
        return super(Opd, self).create(vals)

    # dob and auto age selected -->

    @api.depends('dob')
    def _age_cal(self):
        for rec in self:
            # if rec.dob:
            #     rec.age = (date.today() - rec.dob) // timedelta(days=365.2425)
            # else:
            #     rec.age = 0
            rec.age = rec.dob and date.today().year - rec.dob.year or 0

    # ----- singnature -----

    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancel', 'sent'])
        return orders.write({
            'state': 'draft',
            'signature': False,
            'signed_by': False,
            'signed_on': False,
        })

    total_price = fields.Integer(compute='compute_price')

    @api.depends("med_ids_test")
    def compute_price(self):
        total = 0
        for rec in self:
            for line in rec.med_ids_test:
                if line.medi_name:
                    total = total + line.subtotal
            rec.total_price = total

        # email function--->

    def action_send_mail(self):
        templete_id = self.env.ref('Clinic_and_Patient.mail_template_opd_details').id
        templete = self.env['mail.template'].browse(templete_id)
        templete.send_mail(self.id, force_send=True)

    @api.depends("med_ids_test")
    def _compute_total_amount(self):
        for rec in self:
            untax_amount = tax_amount = 0
            for line in rec.med_ids_test:
                if line.medicine_id_new:
                    untax_amount = untax_amount + line.subtotal
                    tax_amount = tax_amount + line.tax_price
            rec.update({
                'untax_amount': untax_amount,
                'tax_amount': tax_amount,
                'total_amount': untax_amount + tax_amount,
            })

    #  ORM method all example in state method

    # (2) write method:-
    #     record_update = self.env['opd.opd'].browse(2)
    #     if record_update.exists():
    #         vals = {
    #             'address': 'charadva'
    #         }
    #         record_update.write(vals)

    # @api.onchange('Customer_name_id')
    # def onchange_name_id(self):
    #     if self.Customer_name_id:
    #         if self.Customer_name_id.booking_date:
    #             self.booking_date = self.Customer_name_id.booking_date
    #         if self.Customer_name_id.example:
    #             self.example = self.Customer_name_id.example
    #         else:
    #             self.booking_date = " "
    #             self.example = " "
    #
    # @api.depends('date_of_birth')
    # def _age_compute(self):
    #     for rec in self:
    #         rec.age = rec.date_of_birth and date.today().year - rec.date_of_birth.year or 0
    #
