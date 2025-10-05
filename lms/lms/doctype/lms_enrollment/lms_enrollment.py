# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import ceil


class LMSEnrollment(Document):
	def validate(self):
		self.validate_membership_in_same_batch()
		self.validate_membership_in_different_batch_same_course()

	def on_update(self):
		self.update_program_progress()

	def validate_membership_in_same_batch(self):
		filters = {"member": self.member, "course": self.course, "name": ["!=", self.name]}
		if self.batch_old:
			filters["batch_old"] = self.batch_old
		previous_membership = frappe.db.get_value(
			"LMS Enrollment", filters, fieldname=["member_type", "member"], as_dict=1
		)

		if previous_membership:
			member_name = frappe.db.get_value("User", self.member, "full_name")
			course_title = frappe.db.get_value("LMS Course", self.course, "title")
			frappe.throw(
				_("{0} is already a {1} of the course {2}").format(
					member_name, previous_membership.member_type, course_title
				)
			)

	def validate_membership_in_different_batch_same_course(self):
		"""Ensures that a studnet is only part of one batch."""
		# nothing to worry if the member is not a student
		if self.member_type != "Student":
			return

		course = frappe.db.get_value("LMS Batch Old", self.batch_old, "course")
		memberships = frappe.get_all(
			"LMS Enrollment",
			filters={
				"member": self.member,
				"name": ["!=", self.name],
				"member_type": "Student",
				"course": self.course,
			},
			fields=["batch_old", "member_type", "name"],
		)

		if memberships:
			membership = memberships[0]
			member_name = frappe.db.get_value("User", self.member, "full_name")
			frappe.throw(
				_("{0} is already a Student of {1} course through {2} batch").format(
					member_name, course, membership.batch_old
				)
			)

	def update_program_progress(self):
		programs = frappe.get_all(
			"LMS Program Member", {"member": self.member}, ["parent", "name"]
		)

		for program in programs:
			total_progress = 0
			courses = frappe.get_all(
				"LMS Program Course", {"parent": program.parent}, pluck="course"
			)
			for course in courses:
				progress = frappe.db.get_value(
					"LMS Enrollment", {"course": course, "member": self.member}, "progress"
				)
				progress = progress or 0
				total_progress += progress

			average_progress = ceil(total_progress / len(courses))
			frappe.db.set_value("LMS Program Member", program.name, "progress", average_progress)


@frappe.whitelist()
def create_membership(
	course, batch=None, member=None, member_type="Student", role="Member"
):
	if frappe.db.get_value("LMS Course", course, "disable_self_learning"):
		return False

	enrollment = frappe.new_doc("LMS Enrollment")
	enrollment.update(
		{
			"doctype": "LMS Enrollment",
			"batch_old": batch,
			"course": course,
			"role": role,
			"member_type": member_type,
			"member": member or frappe.session.user,
		}
	)
	enrollment.insert()
	return enrollment


@frappe.whitelist()
def update_current_membership(batch, course, member):
	all_memberships = frappe.get_all(
		"LMS Enrollment", {"member": member, "course": course}
	)
	for membership in all_memberships:
		frappe.db.set_value("LMS Enrollment", membership.name, "is_current", 0)

	current_membership = frappe.get_all(
		"LMS Enrollment", {"batch_old": batch, "member": member}
	)
	if len(current_membership):
		frappe.db.set_value("LMS Enrollment", current_membership[0].name, "is_current", 1)


def update_course_enrollment_count(doc, method=None):
	"""Update enrollment count for a course when enrollment is created or deleted"""
	try:
		if doc.course:
			from lms.lms.utils import get_lesson_count

			# Count only Student enrollments
			enrollments = frappe.db.count(
				"LMS Enrollment",
				{"course": doc.course, "member_type": "Student"}
			)

			# Update the course
			frappe.db.set_value(
				"LMS Course",
				doc.course,
				"enrollments",
				enrollments,
				update_modified=False
			)
			frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error updating enrollment count: {str(e)}", "Update Enrollment Count")


def sync_all_courses():
	"""
	Manual sync function to update statistics for all courses.
	Run this ONCE after adding hooks to sync existing data.

	Usage:
		bench --site [your-site] execute lms.lms.doctype.lms_enrollment.lms_enrollment.sync_all_courses
	"""
	from lms.lms.utils import get_lesson_count, get_average_rating
	from frappe.utils import flt

	print("=" * 60)
	print("SYNCING ALL COURSE STATISTICS")
	print("=" * 60)

	# Get all courses
	courses = frappe.get_all("LMS Course", fields=["name", "title"])
	total = len(courses)

	print(f"\nFound {total} courses to update\n")

	updated_count = 0
	for idx, course in enumerate(courses, 1):
		try:
			# Get lesson count
			lesson_count = get_lesson_count(course.name)

			# Get enrollment count (only students)
			enrollments = frappe.db.count(
				"LMS Enrollment",
				{"course": course.name, "member_type": "Student"}
			)

			# Get average rating
			avg_rating = get_average_rating(course.name) or 0
			avg_rating = flt(avg_rating, 3)

			# Update the course
			frappe.db.set_value(
				"LMS Course",
				course.name,
				{
					"lesson_count": lesson_count,
					"enrollments": enrollments,
					"rating": avg_rating
				},
				update_modified=False
			)

			print(f"[{idx}/{total}] Updated: {course.title}")
			print(f"          Lessons: {lesson_count} | Enrollments: {enrollments} | Rating: {avg_rating}")

			updated_count += 1

		except Exception as e:
			print(f"[{idx}/{total}] ERROR: {course.title} - {str(e)}")
			frappe.log_error(f"Error syncing course {course.name}: {str(e)}", "Sync Course Stats")

	# Commit all changes
	frappe.db.commit()

	print("\n" + "=" * 60)
	print(f"SYNC COMPLETED: {updated_count}/{total} courses updated")
	print("=" * 60)

	return {
		"success": True,
		"total": total,
		"updated": updated_count
	}
