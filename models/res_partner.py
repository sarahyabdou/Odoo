
from odoo import models,fields,api
from odoo.exceptions import ValidationError
from odoo.tools import email_normalize

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    vat=fields.Char(required=True)
    email = fields.Char(string='Email', required=True, unique=True)
     
    # # New field to link with HmsPatient
    related_patient_id = fields.Many2one('hms_patient', string='Related Patient')
    @api.constrains("email")
    def checkValidEmail(self):
        for rec in self:
            if rec.email:
                emailIsFound = rec.env["hms_patient"].search(
                    [("email", "=", rec.email)], limit=1
                )
                if emailIsFound:
                    raise ValidationError(
                        "This email is already assigned to a different customer."
                    )
    @api.constrains("related_patient_id ")
    def validEmail(self):
        for rec in self:
            if rec.related_patient_id :
                emailIsFound = rec.env["res.partner"].search(
                    [("related_patient_id.email", "=", rec.related_patient_id.email),("id","!=",rec.id)], limit=1
                )
                if emailIsFound:
                    raise ValidationError(
                        "This email is already assigned to a different customer."
                    )                
                    