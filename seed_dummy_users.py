#!/usr/bin/env python3
"""
Seeder script untuk membuat akun dummy untuk setiap role
Sederhana dan langsung tanpa perlu ubah environment dev/prod
"""

import requests
import json

# Konfigurasi akun dummy yang akan dibuat
DUMMY_ACCOUNTS = [
    {
        "email": "moderator@test.com",
        "full_name": "Moderator Test",
        "password": "Test123!@#",
        "role": "Moderator"
    },
    {
        "email": "instructor@test.com", 
        "full_name": "Instructor Test",
        "password": "Test123!@#",
        "role": "Course Creator"
    },
    {
        "email": "evaluator@test.com",
        "full_name": "Evaluator Test", 
        "password": "Test123!@#",
        "role": "Batch Evaluator"
    },
    {
        "email": "student@test.com",
        "full_name": "Student Test",
        "password": "Test123!@#",
        "role": "LMS Student"
    }
]

def create_dummy_accounts():
    base_url = "http://localhost:8080"
    session = requests.Session()

    try:
        # Login as Administrator
        print("🔐 Login sebagai Administrator...")
        login_data = {
            "usr": "Administrator", 
            "pwd": "admin"
        }

        login_response = session.post(f"{base_url}/api/method/login", json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Login gagal: {login_response.text}")
            return False

        print("✅ Login berhasil!")

        created_count = 0
        
        for account in DUMMY_ACCOUNTS:
            print(f"\n👤 Membuat akun {account['role']}: {account['email']}")
            
            # Cek apakah user sudah ada
            check_response = session.post(f"{base_url}/api/method/frappe.client.get", json={
                "doctype": "User",
                "name": account["email"]
            })
            
            if check_response.status_code == 200:
                print(f"⚠️  User {account['email']} sudah ada, skip...")
                continue
            
            # Buat user baru
            user_data = {
                "doctype": "User",
                "email": account["email"],
                "first_name": account["full_name"],
                "user_type": "Website User",
                "enabled": 1,
                "send_welcome_email": 0
            }

            create_response = session.post(f"{base_url}/api/method/frappe.client.insert", json={
                "doc": user_data
            })
            
            if create_response.status_code == 200:
                print(f"✅ User {account['email']} berhasil dibuat")
                
                # Set password setelah user dibuat
                password_response = session.post(f"{base_url}/api/method/frappe.client.set_value", json={
                    "doctype": "User",
                    "name": account["email"],
                    "fieldname": "new_password", 
                    "value": account["password"]
                })
                
                if password_response.status_code == 200:
                    print(f"✅ Password untuk {account['email']} berhasil diset")
                else:
                    print(f"❌ Gagal set password: {password_response.text}")
                
                # Assign role
                role_data = {
                    "doctype": "Has Role",
                    "parent": account["email"],
                    "role": account["role"],
                    "parenttype": "User",
                    "parentfield": "roles"
                }
                
                role_response = session.post(f"{base_url}/api/method/frappe.client.insert", json={
                    "doc": role_data
                })
                
                if role_response.status_code == 200:
                    print(f"✅ Role {account['role']} berhasil diassign")
                    created_count += 1
                else:
                    print(f"❌ Gagal assign role: {role_response.text}")
            else:
                print(f"❌ Gagal membuat user: {create_response.text}")

        print(f"\n🎉 Selesai! {created_count} akun dummy berhasil dibuat")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def print_account_info():
    print("\n" + "="*50)
    print("📋 AKUN DUMMY YANG TERSEDIA")
    print("="*50)
    print("\n🏛️  ADMIN (sudah ada):")
    print("   Username: Administrator")
    print("   Password: admin")
    
    print("\n👥 AKUN TEST:")
    for account in DUMMY_ACCOUNTS:
        print(f"\n{account['role'].upper()}:")
        print(f"   Email: {account['email']}")
        print(f"   Password: {account['password']}")
    
    print("\n💡 Cara pakai:")
    print("1. Buka http://localhost:8080/login")
    print("2. Login dengan email dan password di atas")
    print("3. Test fitur sesuai role masing-masing")
    print("\n" + "="*50)

if __name__ == "__main__":
    print("🚀 Memulai seeder akun dummy...")
    success = create_dummy_accounts()
    
    if success:
        print_account_info()
    else:
        print("❌ Seeder gagal dijalankan")