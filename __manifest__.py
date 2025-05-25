{
    'name': 'School Management',
    'version': '17.0.0.1',
    'summary': 'Manage students, classes, and more',
    'category': "Services",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/student_views.xml',
        'views/class_views.xml',
        
        'views/teacher_views.xml',
        'views/subject_views.xml',
        'views/exam_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'author': "Mohamed Sobh",
    'website': "https://egypt.odoo-express.com",
    'sequence': '33',
    'description': """
        School Management System
        =========================
        This module allows you to manage students, classes, teachers, subjects, and exams.
    """,
    }
