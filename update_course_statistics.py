#!/usr/bin/env python3
"""
Script to manually update all course statistics (enrollments, ratings, lessons)
Run this once to sync existing data, then the hooks will keep it updated.
"""

import frappe
from frappe.utils import flt
from lms.lms.utils import get_lesson_count, get_average_rating


def update_all_course_statistics():
	"""Update statistics for all courses"""
	print("Starting course statistics update...")

	courses = frappe.get_all("LMS Course", fields=["name", "title"])

	updated_count = 0
	for course in courses:
		try:
			# Get lesson count
			lessons = get_lesson_count(course.name)

			# Get enrollment count (only Students)
			enrollments = frappe.db.count(
				"LMS Enrollment",
				{"course": course.name, "member_type": "Student"}
			)

			# Get average rating
			avg_rating = get_average_rating(course.name) or 0
			avg_rating = flt(avg_rating, frappe.get_system_settings("float_precision") or 3)

			# Update the course
			frappe.db.set_value(
				"LMS Course",
				course.name,
				{
					"lessons": lessons,
					"enrollments": enrollments,
					"rating": avg_rating
				},
				update_modified=False
			)

			print(f"✓ Updated {course.title}: {lessons} lessons, {enrollments} enrolled, {avg_rating} rating")
			updated_count += 1

		except Exception as e:
			print(f"✗ Error updating {course.name}: {str(e)}")

	frappe.db.commit()
	print(f"\n✓ Successfully updated {updated_count} out of {len(courses)} courses")


if __name__ == "__main__":
	# Initialize Frappe
	frappe.init(site="lms-genkiddo")
	frappe.connect()

	# Run the update
	update_all_course_statistics()

	print("\n✓ Done! All course statistics have been updated.")
	print("Note: Future enrollments and reviews will be updated automatically via hooks.")
