# Networking

Network architecture for cameras: how they connect, what they say,
and what they never say.

## Topology

- **One camera, local only:** no network at all, or Wi-Fi to the
  house. The most private option.
- **Several cameras, one site:** Ethernet/PoE to a local switch +
  a Vision PC/server on-site. Nothing leaves the site except
  anonymized results.
- **Remote trap:** LTE, alerts + thumbnails only. Video stays on
  the card until collected.

## Protocols

- RTSP for streaming, ONVIF for discovery/control, MQTT for
  events/alerts. Standard protocols — no custom one.
- TLS where supported; authentication everywhere. No anonymous
  RTSP, no plain HTTP admin.

## Rules

- Bandwidth: a camera that streams 24/7 to the cloud wastes the
  link and the privacy budget. Send results (§8).
- A camera that does not need the internet does not get the
  internet (VLAN / firewall it off).
- Time sync (NTP) matters: clips without a correct timestamp are
  useless as evidence and confusing as data.
