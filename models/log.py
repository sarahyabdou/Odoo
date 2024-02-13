from odoo import models, fields
import datetime
class PatientLog(models.Model):
    _name = 'log'
   

    patient_id = fields.Many2one('hms_patient')
    created_by = fields.Char()
    date = fields.Datetime( default=fields.Datetime.now)
    description = fields.Text()
    