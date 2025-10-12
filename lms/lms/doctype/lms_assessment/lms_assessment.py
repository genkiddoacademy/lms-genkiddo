# Copyright (c) 2023, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class LMSAssessment(Document):
	def validate(self):
		self.validate_assessment_exists()

	def validate_assessment_exists(self):
		"""Validate that the referenced assessment document exists"""
		if self.assessment_type and self.assessment_name:
			if not frappe.db.exists(self.assessment_type, self.assessment_name):
				assessment_title = self.assessment_name
				try:
					# Try to get title if document exists
					if frappe.db.exists(self.assessment_type, self.assessment_name):
						assessment_title = frappe.db.get_value(self.assessment_type, self.assessment_name, "title") or self.assessment_name
				except:
					pass

				frappe.throw(
					_("The {0} '{1}' does not exist. Please create it first or select a different assessment.").format(
						self.assessment_type,
						assessment_title
					)
				)
