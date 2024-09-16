# -*- coding: utf-8 -*-


from odoo import api, SUPERUSER_ID

from . import controllers
from . import models
from . import tools

def post_init_hook(cr, registry):
    from odoo.api import Environment
    env = Environment(cr, SUPERUSER_ID, {})
    env['automated.action'].create_action()