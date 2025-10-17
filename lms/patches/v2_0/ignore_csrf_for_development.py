import frappe


def execute():
	"""
	Patch to ignore CSRF validation for development environment.
	This helps resolve CSRF token errors when using Vite dev server.
	"""
	# Set ignore_csrf in site config for development
	if frappe.conf.get("developer_mode") or frappe.conf.get("ignore_csrf"):
		frappe.local.conf.ignore_csrf = 1
		
	# Also set it in the current session
	frappe.flags.ignore_csrf = True