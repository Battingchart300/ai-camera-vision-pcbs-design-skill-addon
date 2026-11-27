# Connectivity (Wi-Fi / LTE / Ethernet / PoE) — high

How the camera talks to the world — and how little it needs to say.

## Choosing

- **Wi-Fi:** cheap, short range, needs a network nearby. Fine for
  a garden or a house camera.
- **LTE:** for a trap far from Wi-Fi. Costs power and a SIM/data
  plan — send alerts and thumbnails, not video.
- **Ethernet / PoE:** the industrial default — one cable for data
  and power, reliable, no batteries.
- **No link at all:** a trap can store locally and be collected.
  The most private option.

## Rules

- Send results, not raw video: counts, alerts, blurred clips
  (§8). A camera that streams 24/7 to the cloud is a privacy and
  a bandwidth failure.
- TLS everywhere; no plain HTTP admin; RTSP only with auth.
- ONVIF for discovery/control, RTSP for streaming, MQTT for
  events — standard protocols, not a custom one.
- LTE: check the modem's power draw in the budget — transmitting
  is the most expensive thing a trap does.

## Checks

Link bandwidth is checked in `interface_check.py` (Ethernet/USB
variants). Privacy of what is sent is checked in `privacy_check.py`.
