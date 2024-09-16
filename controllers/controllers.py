# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
import json
_logger = logging.getLogger(__name__)

# class Real-state(http.Controller):
class PropertyController(http.Controller):
    @http.route(['/properties'], type='http', auth='public', website=True)
    def list_properties(self, **kw):
        # عدد العناصر في كل صفحة
        page = int(kw.get('page', 1))
        per_page = 9
        min_price = float(kw.get('min_price', 0))
        max_price = float(kw.get('max_price', float('inf')))
        property_type = kw.get('property_type', False)
        property_status = kw.get('property_status', False)
        min_area = float(kw.get('min_area', 0))
        max_area = float(kw.get('max_area', float('inf')))
        number_of_rooms = int(kw.get('number_of_rooms', 0))
        furnishing = kw.get('furnishing', False)
        floor_number = int(kw.get('floor_number', 0))

        domain = [('status', '=', 'available'), ('price', '>=', min_price), ('price', '<=', max_price)]

        if property_type:
            domain.append(('property_type', '=', property_type))
        if property_status:
            domain.append(('property_status', '=', property_status))
        if min_area > 0 or max_area < float('inf'):
            domain.append(('area', '>=', min_area))
            domain.append(('area', '<=', max_area))
        if number_of_rooms > 0:
            domain.append(('number_of_rooms', '>=', number_of_rooms))
        if furnishing:
            domain.append(('furnishing', '=', furnishing))
        if floor_number > 0:
            domain.append(('floor_number', '=', floor_number))

        # Fetching properties based on filters
        Property = request.env['property.management.property'].sudo()
        total_properties = Property.search_count(domain)
        properties = Property.search(domain, limit=per_page, offset=(page - 1) * per_page)

        # Calculating total pages
        total_pages = (total_properties // per_page) + (1 if total_properties % per_page > 0 else 0)
        return request.render('real_state.property_list_template', {
            'properties': properties,
            'page': page,
            'total_pages': total_pages,
            'min_price': min_price,
            'max_price': max_price,
            'property_type': property_type,
            'property_status': property_status,
            'min_area': min_area,
            'max_area': max_area,
            'number_of_rooms': number_of_rooms,
            'furnishing': furnishing,
            'floor_number': floor_number,
        })



    @http.route(['/property/<model("property.management.property"):property>'], type='http', auth='public',
                website=True)
    def property_info(self, property, **kw):
        return request.render('real_state.property_info_template', {
            'property': property,
            'images': property.attachment_ids  # Assuming you are storing images in attachments
        })

    @http.route('/properties/map', auth='public', cors="*", method=['GET'])
    def properties_map(self, **kw):

        # إعداد المجال
        min_price = float(kw.get('min_price', 0))
        max_price = float(kw.get('max_price', float('inf')))
        property_type = kw.get('property_type', False)
        property_status = kw.get('property_status', False)
        min_area = float(kw.get('min_area', 0))
        max_area = float(kw.get('max_area', float('inf')))
        number_of_rooms = int(kw.get('number_of_rooms', 0))
        floor_number = int(kw.get('floor_number', 0))

        domain = [('price', '>=', min_price),
                  ('price', '<=', max_price),
                  ('area', '>=', min_area),
                  ('area', '<=', max_area),
                  ('number_of_rooms', '>=', number_of_rooms)]

        if property_type:
            domain.append(('property_type', '=', property_type))
        if property_status and property_status.strip():
            domain.append(('property_status', '=', property_status))
        if floor_number:
            domain.append(('floor_number', '=', floor_number))

        # جلب العقارات
        properties = request.env['property.management.property'].sudo().search(domain)

        data = []

        for property in properties:
            data.append({
                'id': property.id,
                'name': property.name,
                'latitude': property.latitude,
                'longitude': property.longitude,
                'image': property.image
            })

        return request.make_json_response(data)

    @http.route("/check_method_get", auth='none', method=['GET'])
    def check_method_get(self, **values):
        output = {
            'results': {
                'code': 200,
                'message': 'OK'
            }
        }

        return request.make_json_response(output)
