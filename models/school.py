# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class SchoolGrade(models.Model):
    _name = 'school.grade'
    _description = 'School Grades'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The grade name must be unique!'),
        ('code_unique', 'UNIQUE(code)', 'The grade code must be unique!'),
    ]

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    teacher_id = fields.Many2one('school.teacher', string="Grade Teacher")
    section_ids = fields.One2many(
        'school.section', 'grade_id', string="Sections")
    description = fields.Text(string="Description")

class SchoolSection(models.Model):
    _name = "school.section"
    _description = "School Sections"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The section name must be unique!'),
        ('code_unique', 'UNIQUE(code)', 'The section code must be unique!'),
    ]

    name = fields.Char(string="Section Name", required=True)
    code = fields.Char(string="Section Code", required=True)
    grade_id = fields.Many2one('school.grade', string="Grade", required=True)
    teacher_id = fields.Many2one('school.teacher', string="Section Teacher")
    classroom_ids = fields.One2many(
        'school.classroom', 'section_id', string="Classrooms")
    description = fields.Text(string="Description")
    capacity = fields.Integer(string="Capacity")

class ClassRoom(models.Model):
    _name = "school.classroom"
    _description = "School Classrooms"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The classroom name must be unique!'),
        ('code_unique', 'UNIQUE(code)', 'The classroom code must be unique!'),
    ]

    name = fields.Char(string="Classroom Name", required=True)
    code = fields.Char(string="Classroom Code", required=True)
    section_id = fields.Many2one('school.section', string="Section", required=True)
    grade_id = fields.Many2one(
        'school.grade', related='section_id.grade_id', string="Grade", readonly=True)
    capacity = fields.Integer(related='section_id.capacity', string="Section Capacity", readonly=True)
    teacher_id = fields.Many2one('school.teacher', string="Classroom Teacher")
    description = fields.Text(string="Description")
    student_ids = fields.Many2many('school.student',string="Students")
    active = fields.Boolean(default=True)
    timetable_ids = fields.One2many(
        'school.timetable', 'classroom_id', string="Timetable Entries")
    
    
    @api.constrains('capacity', 'student_ids')
    def _check_capacity(self):
        for record in self:
            if len(record.student_ids) > record.capacity:
                raise ValidationError(
                    _("The number of students in the classroom exceeds its capacity!"))
    

    