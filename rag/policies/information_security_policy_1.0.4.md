# Enterprise Information Security Policy (EISP)
**Document ID:** SEC-POL-2026-001  
**Version:** 1.0.4  
**Classification:** RESTRICTED  
**Owner:** Global Information Security Office (GISO)

---

## 1. Executive Summary and Authorization
This Enterprise Information Security Policy (EISP) defines the high-level goals, strategy, and requirements for protecting the organization's information assets. This document is authorized by the Board of Directors and the Chief Information Security Officer (CISO).

### 1.1 Statement of Management Intent
Management is committed to ensuring that information security is an integral part of business operations. Our goal is to maintain a security posture that minimizes risk while enabling innovation and digital transformation.

---

## 2. Policy Framework and Governance
The organization utilizes the NIST Cybersecurity Framework (CSF) and ISO/IEC 27001:2022 as the underlying structures for this policy.

### 2.1 Information Security Organization
* **CISO:** Responsible for the design, implementation, and management of the security program.
* **Security Steering Committee (SSC):** A cross-functional group that meets monthly to align security with business goals.
* **Incident Response Team (IRT):** A specialized unit tasked with managing and neutralizing active threats.

### 2.2 Regulatory Compliance Matrix
The organization must adhere to the following regulatory requirements:
1. **GDPR:** For data subjects within the EU/EEA.
2. **CCPA/CPRA:** For residents of California.
3. **PCI-DSS:** For all systems processing credit card information.
4. **SOX:** For financial reporting integrity.

---

## 3. Risk Management and Assessment
Risk management is the cornerstone of our security strategy. No system is 100% secure; therefore, we manage risk to an "Acceptable Level of Risk" (ALR).

### 3.1 Risk Identification (Asset-Based)
All departments must perform an annual Business Impact Analysis (BIA) to identify critical assets, including:
* **Intellectual Property (IP):** Source code, proprietary algorithms, and trade secrets.
* **PII/PHI:** Personally Identifiable Information and Protected Health Information.
* **Infrastructure:** Servers, cloud tenants (AWS/Azure/GCP), and networking gear.

### 3.2 Quantitative vs. Qualitative Analysis
We utilize the FAIR (Factor Analysis of Information Risk) methodology for quantitative analysis where $Loss Event Frequency \times Loss Magnitude = Risk$.

---

## 4. Logical Access Control
Access to organizational resources is governed by the principles of **Least Privilege** and **Need-to-Know**.

### 4.1 Identity and Access Management (IAM)
* **Provisioning:** Access must be requested via a formal ticket and approved by the Data Owner.
* **Deprovisioning:** Access must be revoked within 24 hours of employee termination.
* **Periodic Review:** Privileged accounts (Admins) must be reviewed every 30 days; standard users every 90 days.

### 4.2 Authentication Standards
1.  **Passwords:** Must be at least 16 characters if used without MFA (not recommended).
2.  **MFA:** Mandatory for all entry points. FIDO2/WebAuthn hardware keys are the preferred method.
3.  **Conditional Access:** Access is granted based on device health, location, and user behavior analytics.

---

## 5. Network Security and Cryptography
### 5.1 Network Segmentation
The internal network is divided into trust zones:
* **Zone 0 (Management):** Highly restricted access for infrastructure admins.
* **Zone 1 (Production):** Live application environments.
* **Zone 2 (Corporate):** Employee workstations and internal services.
* **Zone 3 (Guest):** Isolated internet access for visitors.

### 5.2 Encryption Standards
* **Data in Transit:** Must use TLS 1.3 or higher. Deprecated protocols like SSLv3 and TLS 1.0 are strictly forbidden.
* **Data at Rest:** All sensitive data in databases or file storage must be encrypted using AES-256.
* **Key Management:** Cryptographic keys must be stored in a Hardware Security Module (HSM) or a managed Key Management Service (KMS).

---

## 6. Physical and Environmental Security
### 6.1 Data Center Access
* Access to the server room is restricted to authorized IT personnel.
* All entries and exits must be logged via biometric scanners.
* CCTV footage must be retained for 90 days.

### 6.2 Clean Desk and Clear Screen Policy
* Employees must lock their workstations (Win+L / Cmd+Ctrl+Q) when leaving their desks.
* Sensitive documents must be shredded or stored in locked cabinets at the end of the workday.

---

## 7. Incident Response and Business Continuity
### 7.1 Incident Classification
* **Low:** Localized malware, no data exfiltration.
* **Medium:** Potential unauthorized access, single department impacted.
* **High:** Confirmed data breach, ransomware, or widespread outage.

### 7.2 The 6-Step IR Process
1.  **Preparation:** Hardening systems and training the team.
2.  **Identification:** Monitoring logs (SIEM) for anomalies.
3.  **Containment:** Isolating affected systems to prevent spread.
4.  **Eradication:** Removing the root cause (malware, compromised account).
5.  **Recovery:** Restoring services from clean backups.
6.  **Lessons Learned:** Documenting the event to prevent recurrence.

---

## 8. Software Development Security (DevSecOps)
All software developed in-house must follow the Secure Software Development Life Cycle (S-SDLC).

### 8.1 Code Review and Scanning
* **SAST:** Static Application Security Testing must be performed on every pull request.
* **DAST:** Dynamic testing must be performed in the staging environment.
* **SCA:** Software Composition Analysis must be used to track open-source vulnerabilities.

---

## 9. Security Awareness and Training
Technical controls are insufficient if the human element is not addressed.

* **Initial Training:** All new hires must complete security onboarding within 5 days.
* **Phishing Simulations:** Monthly simulated attacks will be conducted. Users who fail 3 times in a year must undergo remedial training.

---

## 10. Enforcement and Penalties
Any employee found to have violated this policy may be subject to disciplinary action, including:
* Verbal or written warnings.
* Suspension of network privileges.
* Termination of employment.
* Legal action in the event of criminal intent.

---
**End of Policy Document**