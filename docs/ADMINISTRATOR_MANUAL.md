# Midlands State University QVS - Administrator Manual

## 1. System Administration & Role Access
Log in with Administrator credentials (`username: admin`, `password: AdminPass123!`).

## 2. Managing Student Records & Issuing Certificates
1. Navigate to **Students** -> **Register New Student**.
2. Fill in the Student Number, National ID, Full Name, Programme, Faculty, Level, Graduation Date, and Qualification.
3. Click **Save Student Record**.
4. The system automatically creates the digital certificate record, generates the unique Certificate Number, creates the SHA-256 digital signature hash, and builds the PNG QR code.

## 3. Revoking or Suspending Credentials
1. Open the Django Admin Panel at `/admin/` or the **Qualifications Registry** page.
2. Select the target Certificate.
3. Change status from `ACTIVE` to `REVOKED`.
4. Enter a detailed **Revocation Reason** (e.g. academic dishonesty or transcript falsification).
5. Click **Save**. Any subsequent verification queries on this certificate will immediately trigger the Red Revoked Alert and alert the AI Fraud engine.

## 4. Inspecting AI Fraud Analytics
1. Click **AI Fraud Analytics** in the top navigation bar.
2. Review the incident log table listing high anomaly score queries, suspicious burst scanning IPs, and automated bot scraping attempts.
