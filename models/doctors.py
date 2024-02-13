from odoo import models,fields
class Doctors(models.Model):
    _name='doctors'
    # _rec_name='firstname'
    firstname=fields.Char(required=True)
    lastname=fields.Char(required=True)
    
    image=fields.Image()
    
    
    doctors_id=fields.Many2many('hms_patient')