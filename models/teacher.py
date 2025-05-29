# -*- coding: utf-8 -*-
from odoo import models, fields

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The teacher name must be unique!'),
    ]

    name = fields.Char(required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    res_grade_ids = fields.One2many('school.grade', 'teacher_id',string="Grade Teacher")
    res_section_ids = fields.One2many('school.section', 'teacher_id', string='Sections')
    res_classroom_ids = fields.One2many('school.classroom','teacher_id', string="Classroom Teacher")
    res_subject_ids = fields.One2many('school.subject', 'teacher_id',string="Subject Teacher")
    
    # Personal Information
    birth_date = fields.Date(string="Birth Date")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    address = fields.Text(string="Address")
    description = fields.Text(string="Description")
    photo = fields.Binary(string="Image")
    # Many2many fields to link teachers with subjects, grades, and classrooms
    subject_ids = fields.Many2many('school.subject', string="Assigned Subjects")
    grade_ids = fields.Many2many('school.grade', string="Assigned Grades")
    classroom_ids = fields.Many2many('school.classroom', string="Classrooms")
    active = fields.Boolean(default=True, string="Active")
