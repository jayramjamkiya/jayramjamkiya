from odoo import api, models, fields


class medi(models.Model):
    _name = 'medi.medi'
    _description = 'medicine detals'
    _rec_name = 'medicine_id_new'

    medi_name = fields.Many2one("opd.opd")
    medicine_id_new = fields.Many2one("medicine.medicine")
    qty = fields.Integer("Qty", default="1")
    price = fields.Integer('Price', related="medicine_id_new.Unit_Price")
    subtotal = fields.Integer("Subtotal", compute="_get_subtotal", store=True)
    dep_id = fields.Many2one("department.department", string="Madicine use")
    tax_id = fields.Many2many('account.tax', string='Taxes')
    tax_price = fields.Float('Tax Price', compute="compute_tax")
    discount_id = fields.Float(string='Discount (%)')
    # discount_price = fields.Float(string="discount_price", compute="disc_amount")

    # discount method -->
    @api.depends('qty', 'medicine_id_new', 'discount_id')
    def _get_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.price
            record_id = self.env['medicine.medicine'].search([('id', '=', rec.medicine_id_new.id)])
            if rec.medicine_id_new:
                dics = (rec.subtotal * rec.discount_id) / 100
                print(">>>>>>>>>>>>>>>>>>dics", dics)
                rec.subtotal = (record_id.Unit_Price * rec.qty) - dics
                print(">>>>>>>>>>>>>>>>>>>rec.subtotal", rec.subtotal)
                # rec.price = record_id.Unit_Price
            # else:
            #     rec.subtotal = 0

    # long method and take higher time to execute the code

    # @api.depends('qty', 'medicine_id_new')
    # def _get_price(self):
    #     for rec in self:
    #         record_id = self.env['medicine.medicine'].search([('id', '=', rec.medicine_id_new.id)])
    #         if rec.medicine_id_new:
    #             rec.price = record_id.Unit_Price
    #         else:
    #             rec.price = 0

    # tax process
    @api.depends("price", "qty")
    def compute_tax(self):
        for rec in self:
            print(">>>>", rec)
            total = 0
            if rec.tax_id:
                for line in rec.tax_id:
                    total = total + ((rec.subtotal * line.amount) / 100)
            rec.tax_price = total
