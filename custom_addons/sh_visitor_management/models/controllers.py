from odoo import http
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.http import request
from datetime import datetime,timedelta

class AxVisitorMail(http.Controller):

	@http.route(['/visitor/confirmation/<int:case_id>'], type='http', website=True, auth='public')
	def visitor_accept(self, case_id, email=None, res_id=None, token=None, **post):
		visitor_id = request.env['sh.visitor.details'].sudo().search([('id','=',case_id)],limit=1)
		if visitor_id:
			visitor_id.action_visitor()
			return request.render("sh_visitor_management.visitor_accept")

	@http.route(['/invitation/confirmation/<int:case_id>'], type='http', website=True, auth='public')
	def invite_accept(self, case_id, email=None, res_id=None, token=None, **post):
		call_id = request.env['meeting.call'].sudo().search([('id','=',case_id)],limit=1)
		if call_id:
			call_id.action_invite()
			return request.render("sh_visitor_management.invite_accept")