# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class SchoolExam(models.Model):
    _name = 'school.exam'
    _description = 'Exam'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'exam_date desc, start_time desc'  

    name = fields.Char(required=True)
    timetable_config_id = fields.Many2one('school.timetable.config', string="Timetable", required=True)
    subject_id = fields.Many2one('school.subject', required=True)
    grade_id = fields.Many2one('school.grade', required=True)
    section_id = fields.Many2one('school.section', required=True)
    teacher_id = fields.Many2one('school.teacher', string="Teacher", required=True)
    classroom_ids = fields.Many2many('school.classroom', string="Classrooms")
    exam_date = fields.Date(string="Date",required=True)
    exam_type = fields.Selection([
        ('written', 'Written'),
        ('oral', 'Oral'),
        ('practical', 'Practical'),
        ('online', 'Online')
    ], default='written', string="Exam Type")
    exam_format = fields.Selection([
        ('mcq', 'Multiple Choice Questions'),
        ('descriptive', 'Descriptive'),
        ('both', 'Both')
    ], default='mcq', string="Exam Format")
    start_time = fields.Datetime(string="Start",required=True)
    end_time = fields.Datetime(string="End",required=True)
    duration = fields.Float(string="Duration", compute='_compute_duration', store=True, help="Duration in hours")

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                record.duration = (record.end_time - record.start_time).total_seconds() / 3600
            else:
                record.duration = 0
                
    max_marks = fields.Float(string="Maximum Marks", required=True)
    min_marks = fields.Float(string="Minimum Marks", required=True)
    passing_marks = fields.Float(string="Passing Marks", required=True)
    exam_location = fields.Char(string="Location", help="Location of the exam")
    exam_instructions = fields.Text(string="Instructions", help="Instructions for the exam")
    exam_materials = fields.Text(string="Materials", help="Materials required for the exam")
    exam_link = fields.Char(string="Exam Link", help="Link for online exams")
    description = fields.Text(string="Description")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft', string="Status")
    exam_student_ids = fields.One2many('school.exam.student', 'exam_id', string="Students", help="Students enrolled in the exam")
    active = fields.Boolean(default=True, string="Active")
    
    def action_load_student(self):
        # Logic to load students for the exam
        for classroom in self.classroom_ids:
            student_ids = self.env['school.student'].search([
            ('classroom_id', '=', classroom.id)
            ])
            students_to_create = []
            for student in student_ids:
                # Check if the student is already enrolled in the exam
                existing_enrollment = self.env['school.exam.student'].search([
                    ('exam_id', '=', self.id),
                    ('student_id', '=', student.id)
                ])
                if not existing_enrollment:
                    students_to_create.append({
                        'exam_id': self.id,
                        'student_id': student.id,
                    })
            if students_to_create:
                self.env['school.exam.student'].create(students_to_create)


    def action_schedule_exam(self):
        # Logic to schedule the exam
        self.write({'state': 'scheduled'})

    def action_complete_exam(self):
        # Logic to complete the exam
        self.write({'state': 'completed'})

    def action_cancel_exam(self):
        # Logic to cancel the exam
        self.write({'state': 'cancelled'})

    def action_print_exam(self):
        # Logic to print exam details
        pass

    def action_send_exam_link(self):
        # Logic to send exam link
        pass

    def action_send_exam_materials(self):
        # Logic to send exam materials
        pass

    def action_archive_exam(self):
        # Logic to archive the exam
        self.write({'active': False})

    def action_unarchive_exam(self):
        # Logic to unarchive the exam
        self.write({'active': True})

    def action_reset_exam(self):
        # Logic to reset the exam
        self.write({'state': 'draft'})

    def action_delete_exam(self):
        # Logic to delete the exam
        pass

    def action_duplicate_exam(self):
        # Logic to duplicate the exam
        pass

    def action_view_exam_results(self):
        # Logic to view exam results
        pass

    def action_view_exam_attendance(self):
        # Logic to view exam attendance
        pass
    
    
class SchoolExamStudent(models.Model):
    _name = 'school.exam.student'
    _description = 'Exam Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'exam_id, student_id'
    _sql_constraints = [
        ('unique_exam_student', 'UNIQUE(exam_id, student_id)', 'Each student can only be associated with one exam.')
    ]
    
    exam_id = fields.Many2one('school.exam', required=True, string="Exam")
    student_id = fields.Many2one('school.student', required=True, string="Student")
    result = fields.Float(string="Result")
    marks = fields.Float(string="Marks")
    status = fields.Selection([
        ('not_attempted', 'Not Attempted'),
        ('attempted', 'Attempted'),
        ('passed', 'Passed'),
        ('failed', 'Failed')
    ], default='not_attempted', string="Status")
    attendance_status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ], default='present', string="Attendance Status")
    notes = fields.Text(string="Notes")
    active = fields.Boolean(default=True, string="Active")
    
    