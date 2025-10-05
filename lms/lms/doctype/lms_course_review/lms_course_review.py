# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint


class LMSCourseReview(Document):
	def validate(self):
		self.validate_if_already_reviewed()

	def validate_if_already_reviewed(self):
		if frappe.db.exists(
			"LMS Course Review", {"course": self.course, "owner": self.owner}
		):
			frappe.throw(frappe._("You have already reviewed this course"))


@frappe.whitelist()
def submit_review(rating, review, course):
	out_of_ratings = frappe.db.get_all(
		"DocField", {"parent": "LMS Course Review", "fieldtype": "Rating"}, ["options"]
	)
	out_of_ratings = (len(out_of_ratings) and out_of_ratings[0].options) or 5
	rating = cint(rating) / out_of_ratings
	frappe.get_doc(
		{"doctype": "LMS Course Review", "rating": rating, "review": review, "course": course}
	).save(ignore_permissions=True)
	return "OK"


def update_course_rating(doc, method=None):
	"""Update average rating for a course when review is created, updated, or deleted"""
	try:
		if doc.course:
			from lms.lms.utils import get_average_rating
			from frappe.utils import flt

			# Calculate new average rating
			avg_rating = get_average_rating(doc.course) or 0
			avg_rating = flt(avg_rating, frappe.get_system_settings("float_precision") or 3)

			# Update the course
			frappe.db.set_value(
				"LMS Course",
				doc.course,
				"rating",
				avg_rating,
				update_modified=False
			)
			frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error updating course rating: {str(e)}", "Update Course Rating")
