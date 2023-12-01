# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, fields, _
from odoo.http import request
from odoo.osv.expression import AND
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import json
from operator import itemgetter
from odoo.tools import groupby as groupbyelem
from datetime import datetime, timedelta


class VisitorCustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):

        values = super(VisitorCustomerPortal,
                       self)._prepare_portal_layout_values()
        visitor_obj = request.env['sh.visitor.details']
        visitors = visitor_obj.sudo().search(
            [('user_id', '=', request.env.user.id)])
        visitor_count = visitor_obj.sudo().search_count(
            [('user_id', '=', request.env.user.id)])
        values['visitor_count'] = visitor_count
        values['visitors'] = visitors
        return values

    @http.route(['/my/visitor', '/my/visitor/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_visitors(self, page=1, filterby=None, sortby=None, groupby='none', **kw):
        visitor_sudo = request.env['sh.visitor.details'].sudo()
        values = self._prepare_portal_layout_values()
        domain = [('user_id', '=', request.env.user.id)]
        visitor_count = visitor_sudo.search_count(domain)
        searchbar_sortings = {
            'name': {'label': _('Newest'), 'order': 'name desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'visit_type': {'input': 'visit_type', 'label': _('Visit Type')},
            'visit_category': {'input': 'visit_category', 'label': _('Visit Category')},
        }
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        domain = AND([domain, [('user_id', '=', request.env.user.id)]])
        # pager
        pager = portal_pager(
            url="/my/visitor",
            total=visitor_count,
            page=page,
            step=self._items_per_page,
            url_args={'sortby': sortby, 'filterby': filterby},
        )
        if groupby == 'visit_type':
            order = "visit_type_id, %s" % order
        elif groupby == 'visit_category':
            order = "visit_categ_id, %s" % order

        visitors = visitor_sudo.search(
            domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        if groupby == 'visit_type':
            grouped_visitors = [visitor_sudo.concat(
                *g) for k, g in groupbyelem(visitors, itemgetter('visit_type_id'))]
        elif groupby == 'visit_category':
            grouped_visitors = [visitor_sudo.concat(
                *g) for k, g in groupbyelem(visitors, itemgetter('visit_categ_id'))]
        else:
            grouped_visitors = [visitors]
        values.update({
            'visitors': visitors,
            'grouped_visitors': grouped_visitors,
            'page_name': 'visitor',
            'default_url': '/my/visitor',
            'picking_count': visitor_count,
            'pager': pager,
            'groupby': groupby,
            'searchbar_groupby': searchbar_groupby,
            'filterby': filterby,
        })
        return request.render("sh_visitor_management_portal.visitor_my_visitor", values)

    @http.route(['/my/visitor/<int:visitor_id>'], type='http', auth="public", website=True)
    def portal_my_visitor_form(self, visitor_id, report_type=None, message=False, download=False, **kw):
        visitor_sudo = request.env['sh.visitor.details'].sudo().search(
            [('id', '=', visitor_id)], limit=1)
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=visitor_sudo, report_type=report_type, report_ref='sh_visitor_management.visitor_report', download=download)
        values = {
            'visitor': visitor_sudo,
            'message': message,
            'bootstrap_formatting': True,
            'user_id': visitor_sudo.user_id,
            'report_type': 'html',
        }
        return request.render('sh_visitor_management_portal.portal_visitor_form_template', values)

    @http.route(['/create-visit'], type='http', auth="public", method="post", website=True, csrf=False)
    def create_visit(self, **post):
        dic = {}
        visit_obj = request.env['sh.visitor.details']
        visit_vals = {}
        if post.get('check_in') != '':
            check_in = post.get('check_in')
            check_in_date_time_obj = datetime.strptime(
                check_in, '%m/%d/%Y %I:%M %p')
            check_in_datetime = check_in_date_time_obj - \
                timedelta(hours=5, minutes=30)
            check_in_str = check_in_date_time_obj.strftime('%m/%d/%Y %I:%M %p')

            visit_vals.update({
                'check_in': check_in_datetime,
                'check_in_str': check_in_str,
            })
        if post.get('check_out') != '':
            check_out = post.get('check_out')
            check_out_date_time_obj = datetime.strptime(
                check_out, '%m/%d/%Y %I:%M %p')
            check_out_datetime = check_out_date_time_obj - \
                timedelta(hours=5, minutes=30)
            check_out_str = check_out_date_time_obj.strftime(
                '%m/%d/%Y %I:%M %p')
            visit_vals.update({
                'check_out': check_out_datetime,
                'check_out_str': check_out_str,
            })
        if post.get('check_in') != '' and post.get('check_out') != '':
            check_in = post.get('check_in')
            check_in_date_time_obj = datetime.strptime(
                check_in, '%m/%d/%Y %I:%M %p')
            check_in_datetime = check_in_date_time_obj - \
                timedelta(hours=5, minutes=30)
            check_out = post.get('check_out')
            check_out_date_time_obj = datetime.strptime(
                check_out, '%m/%d/%Y %I:%M %p')
            check_out_datetime = check_out_date_time_obj - \
                timedelta(hours=5, minutes=30)
            diff_time = check_out_datetime - check_in_datetime
            duration = float(diff_time.days) * 24 + \
                (float(diff_time.seconds) / 3600)
            visit_vals.update({
                'duration': round(duration, 2),
            })

        if post.get('visitor_name'):
            visit_vals.update({
                'visitor_name': post.get('visitor_name'),
            })
        if post.get('partner_id', False):
            visit_vals.update({
                'partner_id': int(post.get('partner_id', False)),
            })
        if post.get('company', False):
            visit_vals.update({
                'company': post.get('company', False),
            })
        if post.get('phone', False):
            visit_vals.update({
                'phone': post.get('phone', False)
            })
        if post.get('mobile', False):
            visit_vals.update({
                'mobile': post.get('mobile', False)
            })
        if post.get('mail', False):
            visit_vals.update({
                'mail': post.get('mail', False)
            })
        if post.get('destination_id', False):
            visit_vals.update({
                'destination_id': int(post.get('destination_id', False)),
            })
        if post.get('visit_type_id', False):
            visit_vals.update({
                'visit_type_id': int(post.get('visit_type_id', False)),
            })
        if post.get('visit_categ_id', False):
            visit_vals.update({
                'visit_categ_id': int(post.get('visit_categ_id', False)),
            })
        if post.get('reference', False):
            visit_vals.update({
                'reference': post.get('reference', False),
            })
        if post.get('employee_id', False):
            visit_vals.update({
                'employee_id': int(post.get('employee_id', False)),
            })
        if post.get('department', False):
            visit_vals.update({
                'department': int(post.get('department', False)),
            })
        if post.get('purpose', False):
            visit_vals.update({
                'purpose': post.get('purpose', False),
            })
        if visit_vals.get('check_in') and visit_vals.get('visitor_name'):
            visitor_id = visit_obj.sudo().create(visit_vals)
            dic.update({
                'url': '/my/visitor/'+str(visitor_id.id)
            })
        else:
            dic.update({
                'error': 'Please fill Visitor name and Check In date.'
            })
        return json.dumps(dic)

    @http.route(['/get-duration'], type='http', auth="public", method="post", website=True, csrf=False)
    def get_duration(self, **post):
        dic = {}
        if post.get('check_in') != '' and post.get('check_out') != '':
            check_in_datetime = None
            check_out_datetime = None
            check_in = post.get('check_in')
            check_out = post.get('check_out')

            if check_in and 'AM' in check_in or 'PM' in check_in:
                check_in_date_time_obj = datetime.strptime(
                    check_in, '%m/%d/%Y %I:%M %p')
                check_in_datetime = check_in_date_time_obj - \
                    timedelta(hours=5, minutes=30)
            elif check_in and not 'AM' in check_in or not 'PM' in check_in:
                check_in_date_time_obj = datetime.strptime(
                    check_in, '%Y-%m-%d %H:%M:%S')
                check_in_datetime = check_in_date_time_obj - \
                    timedelta(hours=5, minutes=30)

            if check_out and 'AM' in check_out or 'PM' in check_out:
                check_out_date_time_obj = datetime.strptime(
                    check_out, '%m/%d/%Y %I:%M %p')
                check_out_datetime = check_out_date_time_obj - \
                    timedelta(hours=5, minutes=30)
            elif check_out and not 'AM' in check_out or not 'PM' in check_out:
                check_out_date_time_obj = datetime.strptime(
                    check_out, '%Y-%m-%d %H:%M:%S')
                check_out_datetime = check_out_date_time_obj - \
                    timedelta(hours=5, minutes=30)

            if check_in_datetime and check_out_datetime:
                diff_time = check_out_datetime - check_in_datetime
                duration = float(diff_time.days) * 24 + \
                    (float(diff_time.seconds) / 3600)
                dic.update({
                    'duration': round(duration, 2),
                })
                if duration < 0.0:
                    dic.update({
                        'error': 'Check Out Time should be greater from Check In Time'
                    })
        return json.dumps(dic)

    @http.route(['/get-partner-details'], type='http', auth="public", method="post", website=True, csrf=False)
    def get_partner_details(self, **post):
        dic = {}
        if post.get('partner_id', False):
            partner_id = request.env['res.partner'].sudo().browse(
                int(post.get('partner_id', False)))
            if partner_id.phone:
                dic.update({
                    'phone': partner_id.phone,
                })
            if partner_id.email:
                dic.update({
                    'email': partner_id.email,
                })
            if partner_id.mobile:
                dic.update({
                    'mobile': partner_id.mobile,
                })
            if partner_id.parent_id:
                dic.update({
                    'visitor_name': partner_id.name,
                    'company': partner_id.parent_id.name
                })
            else:
                company_name = ''
                if partner_id.company_id:
                    company_name = partner_id.company_id.name
                dic.update({
                    'visitor_name': partner_id.name,
                    'company': company_name
                })
        return json.dumps(dic)

    @http.route(['/get-employee-details'], type='http', auth="public", method="post", website=True, csrf=False)
    def get_employee_details(self, **post):
        dic = {}
        if post.get('employee_id', False):
            employee_id = request.env['hr.employee'].sudo().browse(
                int(post.get('employee_id', False)))
            if employee_id.department_id:
                dic.update({
                    'department_id': employee_id.department_id.id,
                })

        return json.dumps(dic)

    @http.route(['/default-checkout'], type='http', auth="public", method="post", website=True, csrf=False)
    def default_checkout(self, **post):
        dic = {}
        visitor_id = request.env['sh.visitor.details'].sudo().browse(
            int(post.get('visitor_id')))
        check_out = fields.Datetime.now()
        check_out_date_time_str = datetime.strftime(
            check_out, '%m/%d/%Y %I:%M %p')
        check_out_date_time_obj = datetime.strptime(
            check_out_date_time_str, '%m/%d/%Y %I:%M %p')
        check_out_datetime = check_out_date_time_obj + \
            timedelta(hours=5, minutes=30)
        check_out_str = check_out_datetime.strftime('%m/%d/%Y %I:%M %p')

        if visitor_id:
            visitor_id.sudo().write({
                'check_out': check_out,
                'check_out_str': check_out_str,
            })
            dic.update({
                'success': 1,
            })
        else:
            dic.update({
                'success': 0,
            })
        return json.dumps(dic)

    @http.route(['/update-visitor-details'], type='http', auth="public", method="post", website=True, csrf=False)
    def update_visitor_details(self, **post):
        dic = {}
        visitor_id = request.env['sh.visitor.details'].sudo().browse(
            int(post.get('visitor_id')))
        if visitor_id:
            if post.get('check_in') != '':
                check_in = post.get('check_in')
                check_in_date_time_obj = datetime.strptime(
                    check_in, '%m/%d/%Y %I:%M %p')
                check_in_datetime = check_in_date_time_obj - \
                    timedelta(hours=5, minutes=30)
                check_in_str = check_in_date_time_obj.strftime(
                    '%m/%d/%Y %I:%M %p')
                visitor_id.sudo().write({
                    'check_in': check_in_datetime,
                    'check_in_str': check_in_str,
                })
            if post.get('check_out') != '':
                check_out = post.get('check_out')
                check_out_date_time_obj = datetime.strptime(
                    check_out, '%m/%d/%Y %I:%M %p')
                check_out_datetime = check_out_date_time_obj - \
                    timedelta(hours=5, minutes=30)
                check_out_str = check_out_date_time_obj.strftime(
                    '%m/%d/%Y %I:%M %p')
                visitor_id.sudo().write({
                    'check_out': check_out_datetime,
                    'check_out_str': check_out_str,
                })
            if post.get('check_in') != '' and post.get('check_out') != '':
                check_in = post.get('check_in')
                check_in_date_time_obj = datetime.strptime(
                    check_in, '%m/%d/%Y %I:%M %p')
                check_in_datetime = check_in_date_time_obj - \
                    timedelta(hours=5, minutes=30)
                check_out = post.get('check_out')
                check_out_date_time_obj = datetime.strptime(
                    check_out, '%m/%d/%Y %I:%M %p')
                check_out_datetime = check_out_date_time_obj - \
                    timedelta(hours=5, minutes=30)
                diff_time = check_out_datetime - check_in_datetime
                duration = float(diff_time.days) * 24 + \
                    (float(diff_time.seconds) / 3600)
                visitor_id.sudo().write({
                    'duration': round(duration, 2),
                })
            visitor_id.sudo().write({
                'visitor_name': post.get('visitor_name'),
                'company': post.get('comapny'),
                'phone': post.get('phone'),
                'mobile': post.get('mobile'),
                'mail': post.get('mail'),
                'reference': post.get('reference'),
                'partner_id': int(post.get('partner_id')),
                'destination_id': int(post.get('destination_id')),
                'employee_id': int(post.get('employee_id')),
                'purpose': post.get('purpose'),
            })
            if post.get('visit_type_id'):
                visitor_id.sudo().write({
                    'visit_type_id': int(post.get('visit_type_id'))
                })
            else:
                visitor_id.sudo().write({
                    'visit_type_id': False
                })
            if post.get('visit_categ_id'):
                visitor_id.sudo().write({
                    'visit_categ_id': int(post.get('visit_categ_id'))
                })
            else:
                visitor_id.sudo().write({
                    'visit_categ_id': False
                })
            dic.update({
                'success': 1,
            })
        return json.dumps(dic)
