import requests
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class Property(models.Model):
    _name = 'property.management.property'
    _description = 'Property'

    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('office', 'Office'),
        ('shop', 'Shop'),
    ], string='Property Type', required=True)
    property_status = fields.Selection([
        ('for_rent', 'For Rent'),
        ('for_sale', 'For Sale')
    ])
    latitude = fields.Float(digits=(10, 7))
    longitude = fields.Float(digits=(10, 7))
    area = fields.Float(string='Area (sqm)')
    number_of_rooms = fields.Integer(string='Number of Rooms')
    number_of_bathrooms = fields.Integer(string='Number of Bathrooms')
    floor_number = fields.Integer(string='Floor Number')
    total_floors = fields.Integer(string='Total Floors')
    status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('sold', 'Sold'),
    ], string='Status', default='available')
    amenities = fields.Char(string='Amenities')
    furnishing = fields.Selection([
        ('furnished', 'Furnished'),
        ('unfurnished', 'Unfurnished'),
        ('partly_furnished', 'Partly Furnished'),
    ], string='Furnishing')
    price = fields.Float(string='Price')
    currency_id = fields.Many2one('res.currency', string='Currency')
    image = fields.Binary(string='Image', attachment=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    rented_from = fields.Date(string='Rented From')
    rented_to = fields.Date(string='Rented To')
    owner_id = fields.Many2one('res.partner', string='Owner', domain=[('is_company', '=', True)])
    tenant_id = fields.Many2one('res.partner', string='Tenant')
    #     tenant_ids = fields.One2many('contact.converstion', 'tenant_id')
    tenant_user_id = fields.Char(related='tenant_id.contact_id', string="Tenant User ID")
    conversation_ids = fields.One2many(
        'conversation.management.conversation',
        'property_ids',
        string="Conversations",
        compute='_compute_conversations'
    )
    stage_id = fields.Many2one('property.stage', string="Stage")
    country = fields.Char(string='Country')
    address = fields.Char(string='Address')

    @api.model
    def _get_default_stage(self):
        return self.env['property.stage'].search([], limit=1)

    @api.depends('tenant_user_id')
    def _compute_conversations(self):
        for record in self:
            print("Computing conversations for record:", record.id)
            _logger.info("Computing conversations for record: %s", record.id)

            if record.tenant_user_id:
                # البحث عن المحادثات
                record.conversation_ids = self.env['conversation.management.conversation'].search(
                    [('user_id', '=', record.tenant_user_id)]
                )

                # طباعة عدد المحادثات التي تم العثور عليها
                print("Number of conversations found:", len(record.conversation_ids))
                _logger.info("Number of conversations found: %s", len(record.conversation_ids))

                # إذا كان هناك محادثات، الدخول في الحلقة
                if record.conversation_ids:
                    for conversation in record.conversation_ids:
                        print("Conversations found for record ", conversation)
                        _logger.info("Conversation user_id: %s", conversation.user_id)
                else:
                    print("No conversations found for tenant_user_id:", record.tenant_user_id)
            else:
                record.conversation_ids = False
                _logger.debug("No tenant user ID found, setting conversation_ids to False.")



    @api.onchange('latitude', 'longitude')
    def _onchange_lat_long(self):
        if self.latitude and self.longitude:
            print(self.latitude)
            country, address = self.get_location_details(self.latitude, self.longitude)
            self.country = country
            self.address = address

    def get_location_details(self, lat, long):
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={long}&zoom=18&addressdetails=1"
        headers = {
            'User-Agent': 'Hsoub/1.0 (abulhamidhamsho1@gmail.com)'  # تأكد من وضع عنوان البريد الإلكتروني أو اسم التطبيق
        }
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            country = data['address'].get('country', '')
            address = data['display_name']
            return country, address
        return '', ''





class PropertyStage(models.Model):
    _name = 'property.stage'
    _description = 'Property Stage'

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1)


class Contact(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    contact_id = fields.Char("Zaetoon User Id")
    external_url = fields.Char(string='External Profile Link', compute='_compute_external_url')
    national_id = fields.Char("National ID")
    birthday_date = fields.Date("Birthday Date")
    id_image = fields.Many2many('ir.attachment', string='ID Image')


    @api.depends('contact_id')
    def _compute_external_url(self):
        for record in self:
            record.external_url = f"https://odoo-dev-dev-dev-dev-dev-dev.zaetoon.hsoubdev.com/dashboard/contacts/{record.contact_id}"


    def action_go_to_profile(self):
        self.ensure_one()
        # استخدم معرف المستخدم أو أي بيانات أخرى لبناء الرابط
        user_id = self.contact_id
        profile_url = f"https://odoo-dev-dev-dev-dev-dev-dev.zaetoon.hsoubdev.com/dashboard/contacts/{user_id}"
        return {
            'type': 'ir.actions.act_url',
            'url': profile_url,
            'target': 'new',  # لفتح الرابط في نافذة جديدة
        }




class Notification(models.Model):
    _name = 'external.notification'
    _description = 'External Notifications'

    title = fields.Char(string="Title")
    message = fields.Text(string="Message")
    url = fields.Char(string="URL")
    received_at = fields.Datetime(string="Received At", default=fields.Datetime.now)