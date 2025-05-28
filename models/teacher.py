# -*- coding: utf-8 -*-
from odoo import models, fields

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'

    name = fields.Char(required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    subject_ids = fields.Many2many('school.subject', string="Subjects")
    grade_ids = fields.One2many('school.grade', 'teacher_id', string="Assigned Grades")
    classroom_id = fields.Many2one('school.classroom', string="Classroom")
    classroom_ids = fields.One2many('school.classroom', 'teacher_id', string="Classrooms")
