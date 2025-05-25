from odoo import models, fields

class SchoolTimetable(models.Model):
    _name = 'school.timetable'
    _description = 'Timetable'

    class_id = fields.Many2one('school.class', required=True)
    subject_id = fields.Many2one('school.subject', required=True)
    teacher_id = fields.Many2one('school.teacher', required=True)
    day_of_week = fields.Selection([
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday')
    ], required=True)
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="End Time")
