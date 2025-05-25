from odoo import models, fields

class SchoolExam(models.Model):
    _name = 'school.exam'
    _description = 'Exam'

    name = fields.Char(required=True)
    subject_id = fields.Many2one('school.subject', required=True)
    grade_id = fields.Many2one('school.grade', required=True)
    exam_date = fields.Date(required=True)
    total_marks = fields.Integer()
