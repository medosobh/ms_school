# -*- coding: utf-8 -*-
from odoo import models, fields
import random
import string


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _rec_name = 'full_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    
    state = fields.Selection(
        string="State",
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        tracking=True
    )
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
    grade_id = fields.Many2one(
        comodel_name='school.grade',
        string="Grade"
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
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Uncheck to archive the student record"
    )
    email = fields.Char(
        string="Email",
        help="Email address of the student"
    )
    phone = fields.Char(    
        string="Phone",
        help="Phone number of the student"
    )
    address = fields.Text(
        string="Address",
        help="Home address of the student"
    )    
    
    

    def create(self, vals):
        
        if not vals.get('student_id'):
            # Generate a unique student ID
            chars = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
            nums = ''.join(random.choice(string.digits) for _ in range(4))
            student_id = f"{chars}{nums}"
            
            # Ensure the generated ID is unique
            while self.search([('student_id', '=', student_id)]):
                chars = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
                nums = ''.join(random.choice(string.digits) for _ in range(4))
                student_id = f"{chars}{nums}"
                
            vals['student_id'] = student_id
            
        record = super(SchoolStudent, self).create(vals)
        return record
    
    def write(self, vals):
        res = super(SchoolStudent, self).write(vals)
        if 'name' in vals or 'parent_id' in vals:
            self._compute_full_name()
        return res

    def _compute_full_name(self):
        for rec in self:
            if rec.parent_id:
                rec.full_name = f"{rec.name} ({rec.parent_id.name})"
            else:
                rec.full_name = rec.name

    