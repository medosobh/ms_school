from odoo import models, fields

class SchoolGrade(models.Model):
    _name = 'school.grade'
    _description = 'grade'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    teacher_id = fields.Many2one('school.teacher', string="Grade Teacher")
    student_ids = fields.One2many('school.student', 'grade_id', string="Students")
