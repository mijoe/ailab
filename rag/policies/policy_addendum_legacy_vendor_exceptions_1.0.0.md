# Policy Addendum: Legacy Vendor Exceptions
**Document ID:** SEC-ADD-2026-001  
**Version:** 1.0.0  
**Effective Date:** January 01, 2026  
**Status:** ACTIVE

---

## 1.1 Scope of Exceptions
This addendum provides temporary authorization for legacy third-party vendors who cannot comply with the MFA or Unique Credential requirements of EISP v1.1.0.

## 1.2 Policy on Third-Party Vendor Access: Legacy Protocols
* **Shared Accounts:** For legacy industrial control systems (ICS) where individual identities are not supported, shared accounts are permitted provided the password is changed every 24 hours.
* **VPN Access:** Vendors on the "Exempt List" may continue using IPsec VPNs instead of ZTNA, provided they are restricted to a single jump-host.
* **Duration:** All legacy exceptions expire on December 31, 2026. After this date, non-compliant vendors will be disconnected.