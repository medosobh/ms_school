# -*- coding: utf-8 -*-
from odoo import models, fields

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The subject name must be unique!'),
        ('code_unique', 'UNIQUE(code)', 'The subject code must be unique!'),
    ]

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    description = fields.Text()
    teacher_id = fields.Many2one('school.teacher', string="Subject Supervisor")
    grade_id = fields.Many2one('school.grade', string="Grade")
    section_id = fields.Many2one('school.section', string="Section")
    active = fields.Boolean(default=True, string="Active")
    # Many2many fields to link subjects with teachers, grades, and classrooms
    teacher_ids = fields.Many2many('school.teacher', string="Assigned Teachers")
    grade_ids = fields.Many2many('school.grade', string="Assigned Grades")
    classroom_ids = fields.Many2many('school.classroom', string="Assigned Classrooms")

class SchoolBook(models.Model):
    _name = 'school.book'
    _description = 'Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The book name must be unique!'),
        ('code_unique', 'UNIQUE(code)', 'The book code must be unique!'),
    ]

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    description = fields.Text()
    subject_id = fields.Many2one('school.subject', string="Subject")
    grade_id = fields.Many2one('school.grade', string="Grade")
    section_id = fields.Many2one('school.section', string="Section")
    author = fields.Char(string="Author")
    publisher = fields.Char(string="Publisher")
    publication_date = fields.Date(string="Publication Date")
    active = fields.Boolean(default=True, string="Active")
    
   