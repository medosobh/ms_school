from odoo import models, fields

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    description = fields.Text()
