from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    teacher_id = fields.Many2one('school.teacher', string="Class Teacher")
    student_ids = fields.One2many('school.student', 'class_id', string="Students")
