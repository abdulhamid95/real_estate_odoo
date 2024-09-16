import requests
import json
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class APICall(models.Model):
    _name = 'api.call'
    _description = 'API Call Model'

    @api.model
    def send_user_data(self, user_data):
        api_url = "https://odoo-dev-dev-dev-dev-dev-dev.zaetoon.hsoubdev.com/contacts/save"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '
        }
        try:
            response = requests.post(api_url, data=json.dumps(user_data), headers=headers)
            if response.status_code == 200:
                _logger.info('User data sent successfully')
            else:
                _logger.error(f'Failed to send user data: {response.status_code} - {response.text}')
        except Exception as e:
            _logger.error(f'Exception occurred while sending user data: {str(e)}')