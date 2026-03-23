# Cloud-Native Security Policy (CNSP)
**Document ID:** SEC-POL-2026-002  
**Version:** 2.0.0-Alpha  
**Status:** DRAFT (Testing Only)  
**Effective Date:** September 01, 2026  

---

## 3.5 Third-Party Cloud Integration (External Access)
Third-party access is now managed exclusively via **Cross-Account IAM Roles** and **External IDs**. 
* **Standard:** Vendors must not be issued IAM Users or long-lived Access Keys.
* **OIDC Federation:** Preference is given to vendors supporting OIDC federation to eliminate credential storage.
* **Permissions:** All third-party roles must include a `Condition` key in the Trust Policy restricting access to the organization's CIDR ranges.

## 5.2 Vendor Data Sovereignty
Third-party vendors processing "High" sensitivity data must agree to storage within the EU-West-1 region to maintain GDPR compliance.