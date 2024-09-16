from odoo import api, models, SUPERUSER_ID

class AutomatedAction(models.Model):
    _name = 'automated.action'
    _description = 'Automated Action for New Users'

    @api.model
    def create_action(self):
        action = self.env['ir.actions.server'].create({
            'name': 'Send User Data to API',
            'model_id': self.env.ref('base.model_res_users').id,
            'state': 'code',
            'code': """
                user_data = {
                    'first_name': record.name,
                    'last_name': record.function,
                    'email': record.email,
                }
                
                env['api.call'].send_user_data(user_data)
            """
        })

        self.env['base.automation'].create({
            'name': 'Send User Data on User Creation',
            'model_id': self.env.ref('base.model_res_users').id,
            'trigger': 'on_create',
            'state': 'object_create',
            'server_action_ids': [(6, 0, [action.id])],
        })
