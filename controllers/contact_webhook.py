from odoo import http
from odoo.http import request
import logging
import json
_logger = logging.getLogger(__name__)



class PropertyController(http.Controller):

    @http.route('/contact/update_or_create', type='json', auth='public', methods=['POST'], website=True)
    def update_or_create_property(self, **args):
        # auth_header = request.httprequest.headers.get('Authorization')
        # if not auth_header or auth_header != 'Bearer ':
        #     return {'status': 'error', 'message': 'Unauthorized'}, 401
        raw_data = request.httprequest.data

        try:
            data_str = raw_data.decode('utf-8')
        except UnicodeDecodeError as e:
            _logger.error(f"Unicode decoding error: {e}")
            return {"status": '400 Bad Request', "error": "Invalid byte data"}


        data = json.loads(data_str)["data"]


        # البحث عن سجل بوجود خاصية معينة، على سبيل المثال، باستخدام الاسم
        contact_obj = request.env['res.partner'].sudo()
        existing_contact = contact_obj.search([('contact_id', '=', data.get("contact", {}).get("id"))], limit=1)

        # الوصول إلى قائمة البريد الإلكتروني من الكائن contact
        emails = data.get("contact", {}).get("emails", [])

        # التحقق من أن القائمة غير فارغة قبل الوصول إلى العنصر الأول
        contact_email = emails[0].get("email") if emails else None

        # return {"result": data.get("contact", {}).get("emails", [])[0]}

        if existing_contact:
            # تحديث السجل الموجود
            existing_contact.write({
                'name': data.get("contact", {}).get("first_name"),
                'email': contact_email,
                'contact_id': data.get("contact", {}).get("id")
            })
            return {
                data.get("contact", {}).get("first_name")
            }

        else:
            # إنشاء سجل جديد
            contact_obj.create({
                'name': data.get("contact", {}).get("first_name"),
                'email': contact_email,
                'contact_id': data.get("contact", {}).get("id")
            })
            return {'status': '200 OK', 'message': 'Property created successfully'}
