# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class SchoolGrade(models.Model):
    _name = 'school.grade'
    _description = 'School Grades'

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

    name = fields.Char(string="Classroom Name", required=True)
    code = fields.Char(string="Classroom Code", required=True)
    section_id = fields.Many2one('school.section', string="Section", required=True)
    grade_id = fields.Many2one(
        'school.grade', related='section_id.grade_id', string="Grade", readonly=True)
    capacity = fields.Integer(related='section_id.capacity', string="Section Capacity", readonly=True)
    teacher_id = fields.Many2one('school.teacher', string="Classroom Teacher")
    description = fields.Text(string="Description")
    student_ids = fields.One2many(
        'school.student', 'classroom_id', string="Students")
    active = fields.Boolean(default=True)

    