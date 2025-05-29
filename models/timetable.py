# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class SchoolTimetableConfig(models.Model):
    _name = 'school.timetable.config'
    _description = 'Timetable Configuration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'base_date desc'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The timetable name must be unique!'),
        ('base_date_future', 'CHECK(base_date >= CURRENT_DATE)',
         'The base date must be today or in the future!'),
    ]
    _rec_name = 'name'

    name = fields.Char(string='Year Timetable Name', required=True)
    base_date = fields.Date(string='Start Date', required=True)  # e.g., 2024-09-15
    number_of_weeks = fields.Integer(string='Number of Weeks', default=40)
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)
    active = fields.Boolean(default=True)
    
    def _compute_end_date(self):
        for record in self:
            if record.base_date:
                record.end_date = record.base_date + timedelta(weeks=record.number_of_weeks) - timedelta(days=1)
            else:
                record.end_date = False

class SchoolTimetable(models.Model):
    _name = 'school.timetable'
    _description = 'Timetable'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'timetable_config_id desc, day_of_week asc, start_time asc'
    _sql_constraints = [
        ('unique_timetable', 'UNIQUE(timetable_config_id, classroom_id, subject_id, teacher_id, day_of_week, start_time)',
         'The timetable entry must be unique for the combination of year timetable, classroom, subject, teacher, day of week, and start time!'),
    ]
    _rec_name = 'name'

    name = fields.Char(string='Timetable Entry Name', compute='_compute_name', store=True)
    @api.depends('timetable_config_id', 'classroom_id', 'subject_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.timetable_config_id.name} - {record.classroom_id.name} - {record.subject_id.name}"
    
    
    timetable_config_id = fields.Many2one('school.timetable.config', string="Year Timetable", required=True)
    classroom_id = fields.Many2one('school.classroom', required=True)
    subject_id = fields.Many2one('school.subject', required=True)
    teacher_id = fields.Many2one('school.teacher', required=True)
    day_of_week = fields.Selection([
        ('sun', 'Sunday'),
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),

    ], required=True)
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="End Time")

    calendar_date = fields.Datetime(
        string="Calendar Start", compute="_compute_calendar_dates", store=True)
    calendar_end = fields.Datetime(
        string="Calendar End", compute="_compute_calendar_dates", store=True)

    @api.depends('day_of_week', 'start_time', 'end_time', 'timetable_config_id.base_date')
    def _compute_calendar_dates(self):
        weekdays = {
            'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3,
            'thu': 4, 'fri': 5, 'sat': 6
        }
        for rec in self:
            if rec.day_of_week and rec.timetable_config_id:
                base_date = fields.Date.from_string(rec.timetable_config_id.base_date)
                target_date = base_date + \
                    timedelta(days=weekdays[rec.day_of_week])
                rec.calendar_date = datetime.combine(
                    target_date, datetime.min.time()) + timedelta(hours=rec.start_time)
                rec.calendar_end = datetime.combine(
                    target_date, datetime.min.time()) + timedelta(hours=rec.end_time)
