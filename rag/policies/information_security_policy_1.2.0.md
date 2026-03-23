# Enterprise Information Security Policy (EISP)
**Document ID:** SEC-POL-2026-001  
**Version:** 1.2.0  
**Status:** RELEASED  
**Effective Date:** June 15, 2026  
**Owner:** GISO

---

## 4.3 Policy on Third-Party Vendor Access: Zero Trust Mandate
As of June 2026, all third-party vendor access must transition from VPN-based entry to a **Zero Trust Network Access (ZTNA)** architecture.
* **Micro-segmentation:** Vendors are no longer permitted "network-level" access. Access is granted only to specific application ports.
* **Hardware Attestation:** Third-party devices must pass a health check (Managed/Compliant status) via our MDM before a session is established.
* **Session Termination:** All third-party sessions will be forcibly terminated after 4 hours of inactivity.

## 7.3 Policy on Third-Party Vendor Access: Audit Logs
In addition to session recording, all API calls made by third-party service accounts must be logged to a write-once-read-many (WORM) storage bucket for forensic permanence.