# Cybersecurity — critical

A camera is a computer on a network. An unpatched camera is an
open door.

## Rules

- **TLS** on every network service. No plain HTTP admin page.
- **RTSP only with authentication.** No anonymous stream.
- **Default passwords must be changed** (`security.default_password_changed`).
  No hard-coded credentials in firmware.
- **Secure boot** where the SoC supports it; signed firmware updates.
- **Update path:** a camera that cannot be patched will be owned.
  Keep the update path working for the whole life of the product.
- **No debug UART left open** on a shipped board. No open Telnet/SSH
  with a known password.
- **Minimize attack surface:** close every port the camera does not
  need. If it does not need the internet, do not give it the internet.

## Checks

`privacy_check.py` covers the data side. Network hardening is not
checkable by a script — verify with a port scan of the real device
before install.
