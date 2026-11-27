# Standards

Standards the skill references. The skill does not reprint them —
buy or fetch the official text when you need the exact wording.

| Standard | What it covers |
|---|---|
| MIPI CSI-2 (v1.3 / v2.0 / v2.1) | Camera serial interface, D-PHY / C-PHY |
| MIPI D-PHY (v1.1 / v1.2 / v2.0 / v2.1) | Physical layer, lane rates 1.5 / 2.5 / 4.5 Gbps |
| IEC 60529 | IP ratings (IP54 / IP66 / IP67) |
| IEEE 802.3af / at / bt | PoE (15.4 W / 30 W / 60–90 W at the source) |
| IEEE 802.11 (Wi-Fi) | Wireless link |
| ONVIF | IP camera discovery, control, streaming profiles |
| RTSP (RFC 2326) | Video streaming |
| H.264 / H.265 (HEVC) | Video encoding |
| USB UVC | USB Video Class |
| CE / RoHS | EU conformity, hazardous substances |
| GDPR (EU) 2016/679 | Personal data — recording people needs a legal basis |

Notes:

- PoE wattages in this skill are the **powered-device** budgets
  (12.95 / 25.5 / 51 W), not the source figures — the source always
  quotes more, the cable and the standard eat the rest.
- ONVIF and RTSP are protocols, not security: always use them with
  authentication and TLS where supported.
- GDPR is law, not a design rule. The skill enforces data
  minimization in the design (§8); the human checks the legal basis
  before installing a camera that records people.
