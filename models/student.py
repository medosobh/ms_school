# -*- coding: utf-8 -*-
from odoo import models, fields


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _rec_name = 'full_name'

    full_name = fields.Char(
        string="Full Name",
        compute='_compute_full_name',
        store=True
    )
    name = fields.Char(
        required=True
    )
    
    student_id = fields.Char(
        string="Student ID", required=True, copy=False
    )
    date_of_birth = fields.Date(
        string="Date of Birth", required=True
    )
    gender = fields.Selection(
        string="Gender",
        required=True,
        selection=[
            ('male', 'Male'),
            ('female', 'Female')
        ]
    )
    class_id = fields.Many2one(
        comodel_name='school.class',
        string="Class"
    )
    parent_id = fields.Many2one(
        comodel_name='res.partner', string="Guardian" # to be invoiced later
    )
    photo = fields.Binary(
        string="Photo"
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ('active', 'Active'),
            ('graduated', 'Graduated'),
            ('left', 'Left'),
        ], default='active')
    

    

    def create(self, vals):
        record = super(SchoolStudent, self).create(vals)
        record._compute_full_name()
        return record

        def _compute_full_name(self):
            for rec in self:
                if rec.parent_id:
                    rec.full_name = f"{rec.name} ({rec.parent_id.name})"
                else:
                    rec.full_name = rec.name
