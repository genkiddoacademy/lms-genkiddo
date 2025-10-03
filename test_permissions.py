#!/usr/bin/env python3
"""
Test script untuk validasi hak akses LMS berdasarkan role.
Jalankan dengan: python3 test_permissions.py
"""

import json
from typing import Dict, List

class PermissionTest:
    """Test class untuk validasi permission matrix"""

    def __init__(self):
        self.test_accounts = {
            "Administrator": {"email": "Administrator", "roles": ["Administrator", "System Manager"]},
            "Moderator": {"email": "moderator@test.com", "roles": ["Moderator"]},
            "Course Creator": {"email": "instructor@test.com", "roles": ["Course Creator"]},
            "Batch Evaluator": {"email": "evaluator@test.com", "roles": ["Batch Evaluator"]},
            "LMS Student": {"email": "student@test.com", "roles": ["LMS Student"]}
        }

        self.routes = {
            "/courses": {"required_roles": ["all"]},
            "/batches": {"required_roles": ["all"]},
            "/programming-exercises": {"required_roles": ["all"]},
            "/certified-participants": {"required_roles": ["all"]},
            "/statistics": {"required_roles": ["Administrator", "Moderator"]},
            "/job-openings": {"required_roles": ["Administrator", "Moderator"]},
            "/notifications": {"required_roles": ["all"]},
            "/settings": {"required_roles": ["Administrator"]},
        }

        self.sidebar_items = {
            "Courses": {"roles": ["all"]},
            "Batches": {"roles": ["all"]},
            "Programming Exercises": {"roles": ["all"]},
            "Certified Members": {"roles": ["all"]},
            "Statistics": {"roles": ["Administrator", "Moderator"]},
            "Jobs": {"roles": ["Administrator", "Moderator"]},
            "Notifications": {"roles": ["all"]},
            "Settings": {"roles": ["Administrator"]},
        }

    def test_route_access(self, user_roles: List[str], route: str) -> bool:
        """Test apakah user dengan roles tertentu bisa access route"""
        if route not in self.routes:
            return False

        required_roles = self.routes[route]["required_roles"]

        if "all" in required_roles:
            return True

        return any(role in user_roles for role in required_roles)

    def test_sidebar_visibility(self, user_roles: List[str], item: str) -> bool:
        """Test apakah sidebar item visible untuk user dengan roles tertentu"""
        if item not in self.sidebar_items:
            return False

        required_roles = self.sidebar_items[item]["roles"]

        if "all" in required_roles:
            return True

        return any(role in user_roles for role in required_roles)

    def run_tests(self):
        """Jalankan semua test permission"""
        print("🧪 Testing LMS Permission Matrix")
        print("=" * 50)

        for account_type, account_info in self.test_accounts.items():
            print(f"\n👤 Testing {account_type} ({account_info['email']})")
            user_roles = account_info['roles']

            print("   📱 Route Access:")
            for route in self.routes:
                can_access = self.test_route_access(user_roles, route)
                status = "✅" if can_access else "❌"
                print(f"      {status} {route}")

            print("   📋 Sidebar Visibility:")
            for item in self.sidebar_items:
                is_visible = self.test_sidebar_visibility(user_roles, item)
                status = "✅" if is_visible else "❌"
                print(f"      {status} {item}")

    def generate_permission_matrix(self):
        """Generate permission matrix dalam format tabel"""
        print("\n📊 Permission Matrix Table")
        print("=" * 80)

        # Header
        print(f"{'Route/Feature':<25}", end="")
        for account_type in self.test_accounts:
            print(f"{account_type:<15}", end="")
        print()

        print("-" * 80)

        # Routes
        for route in self.routes:
            print(f"{route:<25}", end="")
            for account_type, account_info in self.test_accounts.items():
                can_access = self.test_route_access(account_info['roles'], route)
                status = "✅" if can_access else "❌"
                print(f"{status:<15}", end="")
            print()

if __name__ == "__main__":
    tester = PermissionTest()
    tester.run_tests()
    tester.generate_permission_matrix()

    print("\n🔍 Test Results Summary:")
    print("✅ = Access Granted")
    print("❌ = Access Denied")
    print("\n⚠️  Remember to test these permissions in actual application!")
