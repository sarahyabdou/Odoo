from odoo import models,fields,api
from odoo.exceptions import ValidationError
from odoo.tools import email_normalize

class HmsPatient(models.Model):
    _name='hms_patient'
    _rec_name='firstname'
    firstname=fields.Char(required=True)
    lastname=fields.Char(required=True)
    birth_date=fields.Date()
    age=fields.Integer(compute='_compute_age', store=True)
    address=fields.Text()
    blood_type=fields.Selection([('A','A'),('B','B'),('O','O'),('AB','AB')])
    log_history=fields.Html()
    cr_ratio=fields.Float(required=True)
    pcr=fields.Boolean(string='PCR')
    image=fields.Binary()
    email = fields.Char(string='Email', required=True)

    
    state=fields.Selection([('undetermined','undetermined'),('fair','fair'),('good','good'),('serious','serious')])
    department_id=fields.Many2one('department')
    department_capacity=fields.Integer(related='department_id.capacity')
    doctor_id=fields.Many2many('doctors')
    log_history_ids = fields.One2many('log', 'patient_id')
    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique.')
    ]
    # @api.model
    # def create(self, vals):
    #     patient = super(HmsPatient, self).create(vals)
    #     patient._create_log_entry("patient", f"{patient.state}")
    #     return patient

    # def write(self, vals):
    #     if 'state' in vals:
    #         old_state = self.state
    #         new_state = vals['state']
    #         self._create_log_entry(self.env.user.name, f" {new_state}")
    #     return super(HmsPatient, self).write(vals)

    def _create_log_entry(self, created_by, description):
        self.ensure_one()
        self.env['log'].create({
            'patient_id': self.id,
            'created_by': created_by,
            'description': description,
        })
    def change_state(self):
        if self.state == 'undetermined':
            self.state ='fair'
        elif self.state =='fair':
            self.state ='good'
        elif self.state =='good':
            self.state ='serious'    
        else:
            self.state='undetermined'
            

    # @api.onchange('is_working')
    # def  set_loghistory(self):
        #   for rec in self :
        #       if rec.is_working and rec.summery ==False:
        #           rec.summery='this stdent is working'
        #       else:
        #           pass    
        # if self.log_history
    # @api.onchange('state')   
    # def warn_user(self):
    #     for rec in  self:
    #        return {
    
    #     'warning':{
    #          'titile':('State change warning'),
    #          'message': 'state changed to %s' %(rec.state)
    #         }
    #     }
           
    @api.onchange('state') 
    def log_state(self):
          for rec in self:
              rec.env['log'].create(
                  { 'description':'state changed %s'%rec.state,
                    'patient_id' :rec.id }
          )
    # @api.constrains('age')         
    # def check_age(self) :
    #     for rec in self:
    #         if rec.age <=0:
    #             raise ValidationError(' age can\'t be less than or equal zero ')
            
     
    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                delta = fields.Date.today().year - patient.birth_date.year
                patient.age = delta
            else:
                patient.age = 0

    @api.constrains('age')
    def _check_age(self):
        for patient in self:
           if patient.age < 30:
                 patient.pcr = True
                #  raise ValidationError('PCR field has been automatically checked for patients under 30 years old.')       
    # @api.depends('birth_date')
    # def _compute_age(self):
    #     for patient in self:
    #         if patient.birth_date:
    #             delta = fields.Date.today().year - patient.birth_date.year
    #             patient.age = delta
    #             # Automatically set PCR field based on age
    #             patient.pcr = delta < 30
    #         else:
    #             patient.age = 0
    #             patient.pcr = False

    # @api.constrains('age')
    # def _check_age(self):
    #     for patient in self:
    #         if patient.age < 0:
    #             raise ValidationError('Age cannot be negative.')
    #         elif patient.age < 30:
    #             if not patient.pcr:
    #                 patient.pcr = True
    #                 raise ValidationError('PCR field has been automatically checked for patients under 30 years old.')
    #         else:
    #             if patient.pcr:
    #                 patient.pcr = False
   
    @api.constrains('email')
    def _check_email(self):
        for patient in self:
            if patient.email and not email_normalize(patient.email):
                raise ValidationError('Invalid email address.')