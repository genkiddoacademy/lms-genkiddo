"""Permission decorators for LMS API endpoints."""

import frappe
from functools import wraps


def require_roles(*required_roles):
	"""Decorator to check if user has any of the required roles."""
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if frappe.session.user == "Administrator":
				return func(*args, **kwargs)

			user_roles = frappe.get_roles()
			if not any(role in user_roles for role in required_roles):
				frappe.throw(
					f"You need one of these roles to access this resource: {', '.join(required_roles)}",
					frappe.PermissionError
				)

			return func(*args, **kwargs)
		return wrapper
	return decorator


def require_system_manager(func):
	"""Decorator to restrict access to System Manager only."""
	@wraps(func)
	def wrapper(*args, **kwargs):
		if frappe.session.user != "Administrator" and "System Manager" not in frappe.get_roles():
			frappe.throw("Only System Manager can access this resource", frappe.PermissionError)
		return func(*args, **kwargs)
	return wrapper


def require_moderator_or_admin(func):
	"""Decorator to restrict access to Moderator or Admin only."""
	@wraps(func)
	def wrapper(*args, **kwargs):
		user_roles = frappe.get_roles()
		if (frappe.session.user != "Administrator" and
			"System Manager" not in user_roles and
			"Moderator" not in user_roles):
			frappe.throw("Only Moderator or Administrator can access this resource", frappe.PermissionError)
		return func(*args, **kwargs)
	return wrapper


def require_instructor_or_above(func):
	"""Decorator to restrict access to Course Creator or above."""
	@wraps(func)
	def wrapper(*args, **kwargs):
		user_roles = frappe.get_roles()
		allowed_roles = ["Administrator", "System Manager", "Moderator", "Course Creator"]
		if not any(role in user_roles for role in allowed_roles):
			frappe.throw("You need Course Creator role or above to access this resource", frappe.PermissionError)
		return func(*args, **kwargs)
	return wrapper
