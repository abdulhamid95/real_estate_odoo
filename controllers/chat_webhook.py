from odoo import http
from odoo.http import request
import logging
import json
_logger = logging.getLogger(__name__)

class ChatWebhookController(http.Controller):

    @http.route('/chat/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def chat_webhook(self, **args):
        # auth_header = request.httprequest.headers.get('Authorization')
        # if not auth_header or auth_header != 'Bearer ':
        #     return {'status': 'error', 'message': 'Unauthorized'}, 401
        raw_data = request.httprequest.data

        try:
            data_str = raw_data.decode('utf-8')
        except UnicodeDecodeError as e:
            _logger.error(f"Unicode decoding error: {e}")
            return {"status": '400 Bad Request', "error": "Invalid byte data"}


        data = json.loads(data_str)["data"]["conversation"]

        # التعامل مع البيانات هنا
        # على سبيل المثال، إنشاء سجل رسالة جديدة في أودو
        contact = data["contacts"][0]

        request.env['conversation.management.conversation'].sudo().create({
            'title': data["title"],
            'user_name': contact.get('first_name'),
            'external_id': data["id"],
            'conversation_status': data["conversation_status"].get("name"),
            'user_id': contact.get('id'),
            'user_email': contact.get('emails')[0].get("email")
        })

        return {"status": data}