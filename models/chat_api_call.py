from odoo import models, fields, api
import requests
import logging
_logger = logging.getLogger(__name__)

class Conversation(models.Model):
    _name = 'conversation.management.conversation'
    _description = 'Conversation Management'

    title = fields.Char(string='Title', required=True)
    user_name = fields.Char(string='User Name')
    conversation_link = fields.Char(string='Conversation Link')
    conversation_date = fields.Datetime(string='Conversation Date')
    external_id = fields.Char(string='External ID', unique=True)
    conversation_status = fields.Char(string="Converstion Status")
    user_id = fields.Char(string="user id")
    user_email = fields.Char(string="Email")
    property_ids = fields.Many2one("property.management.property")
    tenant_id = fields.Many2one('res.partner', string='Tenant')

    @api.model
    def fetch_conversations(self):
        # قم هنا بجلب البيانات من الـ API ومعالجتها
        url = 'https://al-munasib.zaetoon.com/api/agent/v1/conversations'
        headers = {
            'Authorization': 'Bearer '
            # استبدل YOUR_ACCESS_TOKEN برمز التحقق الخاص بك
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            conversations = response.json().get('data', [])  # افترض أن البيانات عبارة عن JSON
            for conversation in conversations:
                _logger.warning(conversation)
                # تحقق مما إذا كانت المحادثة موجودة مسبقاً
                existing_conversation = self.search([('external_id', '=', conversation.get('id'))], limit=1)
                if not existing_conversation:
                    self.create({
                        'title': conversation.get('title'),
                        'user_name': conversation.get('contacts')[0].get('first_name'),
                        'conversation_date': conversation.get('conversation_date'),
                        'external_id': conversation.get('id'),
                        'conversation_status': conversation.get('conversation_status').get('name')
                    })
        else:
            _logger.error('Failed to fetch conversations from API')


    def action_open_conversation(self):
        for record in self:
            id = record.external_id
            return {
                'type': 'ir.actions.act_url',
                'url': f'https://al-munasib.zaetoon.com/dashboard/conversations/{id}',
                'target': 'new',
            }