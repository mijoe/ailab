# Policy: Remote Work and Endpoint Security (RWES)
**ID:** SEC-RW-2026 | **Classification:** Internal | **Version:** 2.2

## 1. Scope and Applicability
This policy applies to all "Teleworkers"—defined as any employee or contractor accessing corporate resources from a non-corporate network (Home, Public Wi-Fi, or Cellular).

## 2. Secure Connectivity Standards
### 2.1 Transition from Legacy VPN to ZTNA
The organization has officially deprecated "Full-Tunnel" VPNs in favor of **Zero Trust Network Access (ZTNA)**.
* **Identity-Aware Proxy (IAP):** Access to internal applications is now brokered via an IAP. Users are authenticated based on identity + device posture + geolocation.
* **No Network Exposure:** Unlike a VPN, ZTNA does not provide an IP address on the internal network. It provides a point-to-point encrypted stream to a specific application port.
* **Split-Tunneling Prohibited:** On managed devices, all web traffic must pass through the Cloud Access Security Broker (CASB) for Data Loss Prevention (DLP) inspection. Local network "break-outs" are disabled.

## 3. Managed Device Requirements
All remote work must be conducted on a corporate-issued "Managed Endpoint."
* **Disk Encryption:** FileVault 2 (macOS) or BitLocker (Windows) must be active with keys escrowed in the corporate MDM.
* **Endpoint Detection and Response (EDR):** The EDR agent must be "Green" (active and updated). If the agent is disabled, ZTNA access will be automatically revoked.
* **Peripheral Control:** USB mass storage devices are disabled on all remote endpoints. Only HID-class devices (mice/keyboards) are permitted.

## 4. Remote Vendor Collaboration
When collaborating with third-party vendors via tools like Slack, Teams, or Zoom, employees must:
* Use "Guest Channels" for external communication.
* Ensure "Screen Share" does not expose sensitive windows or background documents.