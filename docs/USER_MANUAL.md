# MSU Qualification Verification System: User Manual

This manual describes the application at source commit `0faeb043c8c2c602008b1c7e1d45eb29efdcd098`, reviewed on 10 September 2026. Use the URL supplied by your team for its demonstration. For a local installation, open `http://127.0.0.1:8000/`.

## 1. Verify a certificate

1. Open the homepage or `/verify/`.
2. Enter a certificate number, verification code, student number or national ID. A name can also be searched, but a partial name may match more than one person.
3. Submit the verification form.
4. Check the displayed identity and qualification against the intended person. Use an exact identifier whenever possible.

The application returns the first matching certificate. A name result is not a list of all matching graduates, and finding an active record does not independently validate the document presented by an applicant.

| Result | Meaning |
| --- | --- |
| `VERIFIED` | A matching certificate has stored status `ACTIVE`. |
| `REVOKED` | A matching certificate has stored status `REVOKED`. Refer the matter to the registry. |
| `INVALID` | No matching certificate was found. Recheck the identifier before drawing a conclusion. |
| `PENDING` | The API uses this result for a suspended certificate. The current web page incorrectly displays its generic invalid/not-found panel for this case. Ask an administrator to check the registry status. |

For a seeded demonstration, `MSU-2024-BSC-CS-0001` is an active example and `MSU-2023-BCOM-ACC-0099` is revoked. These are sample data, not evidence of a live university award.

The result page labels a SHA-256 value as a digital signature and can label an active result's risk score as “Safe”. Those labels are not a cryptographic authenticity check or a guarantee that the request is safe.

## 2. Download a verification report

On a verified result, click **Download Verification PDF Report**. Employers can also use the PDF links in their screening history.

The PDF contains the recorded verification outcome and details read from the current certificate/student record. If a record is edited later, downloading an old log's PDF may show the old outcome alongside updated record details. It is not an immutable historical copy or a digitally signed document.

**View Printable Certificate** opens a page that requires login. That page offers **Print Certificate**, which uses your browser's print function. The verification PDF and the printable certificate page are different outputs.

## 3. QR codes and the camera page

1. Open **QR Scanner** at `/verify/scan/`.
2. **Start Camera** opens a preview if the browser permits camera access. **Stop** closes the camera stream.
3. The current page does not decode QR codes or offer an implemented photo-upload scanner.
4. Use **Manual Code Entry** to enter the verification code, certificate number or another supported identifier, then click **Verify Code**.

Enter the identifier itself, not a full URL, into the manual field. If you obtain a trusted verification link using your phone's own scanner, open that link in the browser instead.

The QR images displayed on certificate/result pages currently point to the application's fixed Vercel address. They may therefore open a different database from your local demonstration. For a local check, use the certificate number or verification code in your local verification form.

## 4. Register or sign in

Public registration at `/auth/register/` offers **Employer / Recruiter** and **Public / Academic Verifier** accounts. Privileged and graduate accounts must be provisioned by an authorised administrator.

Use a password accepted by the application and enter the same value in the confirmation field. Public registration does not grant administrator/registrar access or automatically approve a company.

Sign in at `/auth/login/` with your username or email and password. Demo credentials are listed in the [Installation Guide](INSTALLATION_GUIDE.md#demonstration-data). Signing out of the website does not revoke API tokens.

If a protected page redirects you to a missing `/accounts/login/` page, open `/auth/login/` directly and then return to the page. This is a current login-redirect configuration gap.

## 5. Employer screening

1. Sign in as an employer before performing a check so the activity is associated with your account.
2. Open your **Dashboard**, which redirects employers to `/employers/portal/`.
3. Review your own recorded checks and their results.
4. Click **Download Screening History CSV** to export your checks.

Anonymous checks are not later assigned to an employer account. Review the CSV as data; query text is supplied by users and should be imported into spreadsheets as text.

## 6. Graduate access

An administrator must create the graduate account and link its student record. The graduate dashboard shows that linked student's certificate and QR image when a certificate exists.

If your record or certificate is missing, contact the team's registry administrator. Registering a public account does not create or link a graduate record automatically.

## 7. Getting help

Report the page, the operation attempted, the displayed message and an appropriate test identifier to the team. Do not share your password or API token. Use the team's confirmed support contact: email addresses displayed in the prototype have not been verified as monitored help channels.
