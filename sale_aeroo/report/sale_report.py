# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#    Copyright (C) 2004 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.total = 0
        self.localcontext.update({
            'get_data': self.get_data,
            'get_lines': self.get_lines,
            'get_total': self.get_total,
        })

    def get_data(self, form):
        lst = []
        for order in self.pool.get('sale.order').browse(self.cr, self.uid, form['order_ids']):
            vals = {
                'number': order.name,
                'customer': order.partner_id.name,
                'order_date': order.date_order,
                'order_id': order.id,
            }
            lst.append(vals)
        return lst

    def get_lines(self, order_id):
        lst = []
        order = self.pool.get('sale.order').browse(self.cr, self.uid, order_id)
        for line in order.order_line:
            self.total += line.price_subtotal
            price_subtotal = line.price_subtotal
            vals = {
                'product': line.product_id and line.product_id.name,
                'desc': line.name,
                'qty': line.product_uom_qty,
                'price': line.price_unit,
                'sub_total': price_subtotal,
            }
            lst.append(vals)
        return lst

    def get_total(self):
        return self.total

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: