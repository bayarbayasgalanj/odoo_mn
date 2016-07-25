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

{
    'name' : 'Sale order schedule',
    'version' : '0.1',
    'author' : 'Altan joloo LLC',
    'website' : 'http://www.altanjoloo.mn/',
    'category' : 'Sale',
    'description': 'Altan joloo',
    'depends' : ['base','sale'],
    'data'   :  [
        'security/sale_order_schedule_security.xml',
        'security/ir.model.access.csv',
        'sale_order_schedule_view.xml',
        'views/sale_order_schedule.xml',
        'menu_view.xml'
    ],
    'init_xml' : [ ],
    'demo_xml' : [ ],
    'update_xml' : [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': ["static/src/xml/order_schedule.xml","static/src/xml/order_route.xml"],
}