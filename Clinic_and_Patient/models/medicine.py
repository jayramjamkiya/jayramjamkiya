from odoo import api, fields, models, _


class Medicine(models.Model):
    _name = "medicine.medicine"
    _description = 'medicine'
    _rec_name = "medicine_name"

    medicine_name = fields.Char(string="Medicine Name")
    madicine_id = fields.Many2one("department.department", string="Madicine use")
    # Quantity = fields.Integer(string="Quantity")
    Unit_Price = fields.Integer(string="unit price")

    # Ammount = fields.Integer(string='Total', store=True)

    # @api.depends('Quantity', 'Unit_Price')
    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for rec in self:
    #         rec.Ammount = rec.Unit_Price * rec.Quantity
    #     return rec.Ammount
