# Enterprise Information Security Policy (EISP)
**Document ID:** SEC-POL-2026-001  
**Version:** 1.1.0  
**Status:** RELEASED  
**Classification:** RESTRICTED  
**Owner:** Global Information Security Office (GISO)
**Effective Date:** March 23, 2026

---

## 1. Executive Summary and Authorization
This Enterprise Information Security Policy (EISP) defines the high-level goals, strategy, and requirements for protecting the organization's information assets. This document is authorized by the Board of Directors and the Chief Information Security Officer (CISO). 

The digital landscape of 2026 requires a proactive, "Zero Trust" posture. This policy mandates that security is not a perimeter-based defense but a continuous verification process applied to every user, device, and network flow.

---

## 2. Policy Framework and Governance
The organization utilizes the NIST Cybersecurity Framework (CSF) 2.0 and ISO/IEC 27001:2022 as the underlying structures for this policy.

### 2.1 Information Security Organization
* **CISO:** Responsible for the design, implementation, and management of the security program.
* **Security Steering Committee (SSC):** A cross-functional group that meets monthly to align security with business goals.
* **Incident Response Team (IRT):** A specialized unit tasked with managing and neutralizing active threats.

### 2.2 Regulatory Compliance Matrix
The organization must adhere to the following regulatory requirements:
1. **GDPR:** For data subjects within the EU/EEA.
2. **CCPA/CPRA:** For residents of California.
3. **PCI-DSS v4.0:** For all systems processing credit card information.
4. **SOX:** For financial reporting integrity.

### 2.3 Policy on Third-Party Vendor Access: Risk Assessment
All third-party vendors requiring access to internal systems must undergo a **Security Supply Chain Risk Management (S-SCRM)** review before contract signing.
* **Tier 1 Vendors (Critical):** Must provide a SOC2 Type II report or ISO 27001 certification.
* **Tier 2 Vendors (Standard):** Must complete the organization's Security Assessment Questionnaire (SAQ).
* **Annual Reviews:** All third-party access rights are subject to a mandatory risk re-validation every 12 months to ensure the vendor's security posture has not degraded.

---

## 3. Risk Management and Assessment
Risk management is the cornerstone of our security strategy. No system is 100% secure; therefore, we manage risk to an "Acceptable Level of Risk" (ALR).

### 3.1 Risk Identification (Asset-Based)
All departments must perform an annual Business Impact Analysis (BIA) to identify critical assets, including:
* **Intellectual Property (IP):** Source code, proprietary algorithms, and trade secrets.
* **PII/PHI:** Personally Identifiable Information and Protected Health Information.
* **Infrastructure:** Servers, cloud tenants (AWS/Azure/GCP), and networking gear.

---

## 4. Logical Access Control
Access to organizational resources is governed by the principles of **Least Privilege** and **Need-to-Know**.

### 4.1 Identity and Access Management (IAM)
* **Provisioning:** Access must be requested via a formal ticket and approved by the Data Owner.
* **Deprovisioning:** Access must be revoked within 24 hours of employee termination.

### 4.2 Authentication Standards
1. **MFA:** Mandatory for all entry points. FIDO2/WebAuthn hardware keys are the preferred method.
2. **Conditional Access:** Access is granted based on device health, location, and user behavior analytics.

### 4.3 Policy on Third-Party Vendor Access: Provisioning
Third-party access must be strictly controlled through the following technical mandates:
* **No Permanent Access:** All vendor accounts must be disabled by default and enabled only for the duration of scheduled maintenance windows (Just-In-Time Access).
* **Identity Federation:** Where possible, vendors must authenticate via their own corporate Identity Provider (IdP) using SAML 2.0 or OIDC, subject to our MFA requirements.
* **Unique Credentials:** Shared "Vendor" accounts are strictly prohibited. Each individual consultant must have a unique, trackable credential.

---

## 5. Network Security and Cryptography
### 5.1 Network Segmentation
The internal network is divided into trust zones using micro-segmentation:
* **Zone 0 (Management):** Highly restricted access for infrastructure admins.
* **Zone 1 (Production):** Live application environments.
* **Zone 2 (Corporate):** Employee workstations and internal services.

### 5.2 Encryption Standards
* **Data in Transit:** Must use TLS 1.3. 
* **Data at Rest:** All sensitive data must be encrypted using AES-256 with keys managed in a FIPS 140-2 Level 3 HSM.

---

## 6. Physical and Environmental Security
Access to the server room is restricted to authorized IT personnel. All entries and exits must be logged via biometric scanners. CCTV footage must be retained for 90 days.

---

## 7. Operations and Incident Response
### 7.1 Incident Classification
* **Low:** Localized malware, no data exfiltration.
* **High:** Confirmed data breach or ransomware.

### 7.2 The 6-Step IR Process
1. Preparation, 2. Identification, 3. Containment, 4. Eradication, 5. Recovery, 6. Lessons Learned.

### 7.3 Policy on Third-Party Vendor Access: Monitoring & Auditing
All third-party activities within the production environment must be subjected to enhanced logging:
* **Privileged Access Management (PAM):** All vendor sessions must be brokered through a PAM solution (e.g., CyberArk, BeyondTrust) which records a video log of the session.
* **Log Aggregation:** Logs of vendor activity must be streamed in real-time to the SIEM and flagged for immediate review by the SOC if "Create," "Delete," or "Change" actions are performed on production databases.
* **Automatic Expiry:** All third-party credentials will automatically expire every 90 days unless a formal extension is requested by the internal Business Sponsor.

---

## 8. Software Development Security (DevSecOps)
All software developed in-house must follow the Secure Software Development Life Cycle (S-SDLC). 
* **SAST:** Static Application Security Testing on every pull request.
* **DAST:** Dynamic testing in staging.
* **SCA:** Software Composition Analysis for open-source vulnerabilities.

---

## 9. Security Awareness and Training
* **Initial Training:** All new hires must complete security onboarding within 5 days.
* **Phishing Simulations:** Monthly simulated attacks will be conducted. 

---

## 10. Enforcement and Penalties
Any employee found to have violated this policy may be subject to disciplinary action, including termination of employment or legal action.

---
**Document Revision History**
| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| 1.0.0 | 2026-01-10 | Initial Draft | CISO Office |
| 1.1.0 | 2026-03-23 | Added Third-Party Access Policy | GISO |