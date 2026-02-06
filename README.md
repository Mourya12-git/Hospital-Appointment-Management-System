Hospital & Appointment Management System (Django Backend)

A backend-focused Hospital & Appointment Management System built using **Django + Django REST Framework**, designed to model real-world hospital workflows including doctor scheduling, patient booking, revenue sharing, and role-based access control.

This project intentionally goes beyond basic CRUD and focuses on **data modeling, business logic, conflict handling, and backend design**.

---

## Features

### User Roles (Implicit Role-Based Access)
- **Hospital Owner**
  - Create and manage hospitals
  - View patients associated with their hospital
- **Doctor**
  - Register as a doctor
  - Associate with hospitals
  - Create availability slots
  - View personal earnings
- **Patient**
  - Book appointments
  - View appointment history

> Role access is enforced at the **endpoint level**, not UI-only.

---

## Hospital Management
- Hospitals have:
  - Name
  - Location
  - Multiple specializations
- Hospitals are owned by a user (hospital admin)

---

## Doctor Management
- Doctors:
  - Have multiple specializations
  - Can associate with multiple hospitals
  - Set consultation charges
- Doctors create **time slots** for availability

---

## Slot Management (Key Backend Logic)
- Slots use `DateTimeField` for both start and end
- **Slot collision detection implemented**
  - A doctor cannot create overlapping slots
  - Collision logic uses interval overlap detection
- Slot conflicts are checked **across all hospitals** for the same doctor

---

## Appointment Booking
- Patients book appointments using available slots
- Once booked, appointments are stored and linked correctly
- Booking automatically triggers income calculation

---

## Income & Revenue Sharing
- Each appointment generates an **income record**
- Revenue split:
  - **60% → Doctor**
  - **40% → Hospital**
- Income is:
  - Stored once (no recalculation)
  - Aggregated later for dashboards
- Supports:
  - Doctor-wise earnings
  - Hospital-wise earnings
  - Earnings grouped by hospital

---

## Dashboards (Backend-Driven)
- **Doctor Dashboard**
  - Total earnings
  - Earnings per hospital
- **Hospital Owner Dashboard**
  - Patients list
  - Hospital-related data
- **Patient Dashboard**
  - Appointment history

---

## 🔐 Authentication & Authorization
- Django session-based authentication
- Role-based authorization implemented using domain models:
  - `Doctor.objects.filter(user=request.user)`
  - `Hospital.objects.filter(user=request.user)`
- No reliance on Django `is_staff` / `is_superuser` for app logic

> JWT is intentionally not used yet to keep focus on core backend logic.

---

## 🧠 Key Backend Concepts Used
- Django ORM relationship traversal
- Aggregations (`annotate`, `Sum`)
- Transaction handling (`transaction.atomic`)
- Interval overlap detection
- Role-based endpoint protection
- Clean separation of business logic vs presentation

---

## 🛠️ Tech Stack
- **Python**
- **Django**
- **Django REST Framework**
- **SQLite** (development)
- **HTML** (templates)
- **Bootstrap** (basic UI polish)

---

## 📂 Project Structure (Simplified)

medical/
├── models.py
├── views.py
├── serializers.py
├── forms.py
├── urls.py
├── templates/
│ ├── base.html
│ ├── hospital.html
│ ├── doctor.html
│ ├── slots.html
│ ├── patient.html
│ ├── earnings.html

yaml
Copy code
