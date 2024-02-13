from odoo import models,fields
class Department(models.Model):
    _name='department'
    _rec_name='department_name'
    department_name=fields.Char()
    capacity=fields.Integer()
   
    is_opened=fields.Boolean(default=False)
    patient_id=fields.One2many('hms_patient','department_id')
    
    