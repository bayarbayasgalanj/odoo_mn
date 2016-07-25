# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-today MNO LLC (<http://www.mno.mn>)
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
from openerp import tools
from openerp.tools.translate import _
from openerp.http import request

class sale_order_schedule(osv.osv):
    _name ='sale.order.schedule'
    _inherit = ['mail.thread']
    _description = 'Sale order schedule'

    def _set_date(self, cr, uid, ids, name, args, context=None):
        res = {}
        obj = self.browse(cr,uid,ids)[0]
        date_object = datetime.strptime(obj.date, '%Y-%m-%d')
        res[obj.id] ={ 
        'year': date_object.year,
        'month': date_object.month,
        'day': date_object.day
        }
        return res

    _columns = {
        'date': fields.date('Date', required=True),
        'year': fields.function(_set_date, type='integer', string='Year', multi='dates', readonly=True, store=True),
        'month': fields.function(_set_date, type='integer', string='Month', multi='dates', readonly=True, store=True),
        'day': fields.function(_set_date, type='integer', string='Day', multi='dates', readonly=True, store=True),
        
        'trade_agent': fields.many2one('res.users','Trade agent' ,required=True),
        
    	'schedule_line': fields.one2many('sale.order.schedule.line', 'schedule_id', string='Schedule line', required=True),    	
    }
    _defaults = {
        'date': fields.date.context_today, 
    }

class sale_order_schedule_line(osv.osv):
    _name ='sale.order.schedule.line'
    _description = 'Sale order schedule line'

    _columns = {
        'schedule_id': fields.many2one('sale.order.schedule','Schedule ID' ,required=True),
    	'partner_id': fields.many2one('res.partner','Partner' ,required=True),
    	'partner_latitude': fields.related('partner_id','partner_latitude', string='Latitude', type='float', digits=(16, 5)),
        'partner_longitude': fields.related('partner_id','partner_longitude', string='Longitude', type='float', digits=(16, 5)),
        'sequince': fields.integer('Sequince'),
    }
    _order = 'sequince asc'


class sale_order_route(osv.osv):
    _name ='sale.order.route'
    _inherit = ['mail.thread']
    _description = 'Sale order route'

    _columns = {
        'name': fields.char('Name', size=30),
        'route_line': fields.one2many('sale.order.route.line', 'route_id', string='Route line', required=True),
    }
    def import_zone(self, cr, uid, ids, context=None):
        obj = self.browse(cr,uid,ids,context)[0]
        line_ids = self.pool.get('sale.order.route.line').search(cr, uid, [('route_id','=',obj.id)])
        
        # for item in line_ids:
        #     data = { 'route_id': obj.id,}
        #     line_id = self.pool.get('sale.order.zone').write(cr, uid, item, data, context=context)
        zone_ids = []
        for item in self.pool.get('sale.order.route.line').browse(cr, uid, line_ids):
            zone_ids.append(item.zone_id.id) 
        not_zone_ids = self.pool.get('sale.order.zone').search(cr, uid, [('id','not in',zone_ids)])
        
        for item in not_zone_ids:
            data = { 'route_id': obj.id, 'zone_id': item}
            line_id = self.pool.get('sale.order.route.line').create(cr, uid, data, context=context)
        line_ids = self.pool.get('sale.order.route.line').search(cr, uid, [('route_id','=',obj.id)])
        return {
                'value': {
                'route_line':line_ids
            }
        }

class sale_order_rout_line(osv.osv):
    _name ='sale.order.route.line'
    _description = 'Sale order route line'

    _columns = {
        'route_id': fields.many2one('sale.order.route','Zone ID' ,required=True),
        'zone_id': fields.many2one('sale.order.zone','Zone' ,required=True),
        'trade_agent': fields.related('zone_id','trade_agent', string='Trade agent', type='many2one', relation='res.users', readonly=True),
        'description': fields.related('zone_id','description', string='Description', type='char', store=True),
        'is_view': fields.boolean('View'),
        'color': fields.related('zone_id','color', string='Color', type='char', store=True),
        # 'partner_longitude': fields.related('partner_id','partner_longitude', string='Longitude', type='float', digits=(16, 5)),
    }

class sale_order_zone(osv.osv):
    _name ='sale.order.zone'
    _inherit = ['mail.thread']
    _description = 'Sale order zone'

    _columns = {
        # 'route_id': fields.many2one('sale.order.route','Zone ID'),
        'name': fields.char('Name', size=30, required=True),
        'trade_agent': fields.many2one('res.users','Trade agent' ,required=True),
        'description': fields.char('Description', size=100),
        'is_view': fields.boolean('View'),
        'color': fields.char('Color', size=20, required=True),
        'partner_line': fields.one2many('sale.order.zone.partner', 'zone_id', string='Partner line', required=True),
        'lat_line': fields.one2many('sale.order.zone.lat', 'zone_id', string='Lat line', required=True),
    }
    _defaults = {'is_view': True}

class sale_order_zone_lat(osv.osv):
    _name ='sale.order.zone.lat'
    _description = 'Sale order zone lat'
    _columns = {
        'zone_id': fields.many2one('sale.order.zone','Zone ID' ,required=True),
        'latitude': fields.float('Latitude', digits=(16, 5)),
        'longitude': fields.float('Longitude', digits=(16, 5)),
    }

class sale_order_zone_partner(osv.osv):
    _name ='sale.order.zone.partner'
    _description = 'Sale order zone partner'

    _columns = {
        'zone_id': fields.many2one('sale.order.zone','Zone ID' ,required=True),
        'partner_id': fields.many2one('res.partner','Partner' ,required=True),
        'partner_latitude': fields.related('partner_id','partner_latitude', string='Latitude', type='float', digits=(16, 5)),
        'partner_longitude': fields.related('partner_id','partner_longitude', string='Longitude', type='float', digits=(16, 5)),
    }
    