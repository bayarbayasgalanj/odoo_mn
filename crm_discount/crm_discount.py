# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-today Altan joloo LLC (<http://www.altanjoloo.mn>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from datetime import datetime, timedelta
from openerp.tools.translate import _
from openerp.http import request

class crm_discount_sale(osv.osv):
    _name ='crm.discount.sale'
    _description = 'Sale'
    _inherit = ["mail.thread"]

    _columns = {
        'name': fields.char('Name', size=30),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'datetime': fields.datetime('Datetime', required=True),
        'sale_count': fields.float('Sale count'),
    }
    _order = 'datetime desc'
class crm_discount_car(osv.osv):
    _name ='crm.discount.car'
    _description = 'Crm discount car'
    _inherit = ["mail.thread"]

    _columns = {
        'name': fields.char('Number', size=9, required=True),
    }
class crm_discount_card(osv.osv):
    _name ='crm.discount.card'
    _description = 'Crm discount card'
    _inherit = ["mail.thread"]

    _columns = {
        'name': fields.char('Number', size=8, required=True),
    }
class res_partner(osv.osv):
    _inherit = 'res.partner'
    def _sale_count(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context):
            res[partner.id] = len(partner.sale_ids)
        return res
    _columns = {
        'car_ids': fields.many2many('crm.discount.car', 'res_partner_crm_discount_car_rel', 'partner_id','car_id', 'Car'),
        'card_ids': fields.many2many('crm.discount.card', 'res_partner_crm_discount_card_rel', 'partner_id','card_id', 'Card'),
        'is_discount': fields.boolean('Is discount', readonly=True),
        'register': fields.char('Register', size=10),
        'sale_ids': fields.one2many('crm.discount.sale', 'partner_id', 'Sales'),
        'sale_count': fields.function(_sale_count, string="Sales", type='integer'),
        
    }
    def _get_discount(self, cr, uid, context=None):
        if 'custom_view' in  context:
            if context['custom_view'] == 'is_discount':
                return True
            else:
                return False

    _defaults = {
        'is_discount': _get_discount,
    }