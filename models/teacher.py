from odoo import models, fields

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'

    name = fields.Char(required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    subject_ids = fields.Many2many('school.subject', string="Subjects")
    class_ids = fields.One2many('school.class', 'teacher_id', string="Assigned Classes")
