# Interfaces

## MIPI CSI-2 (sensor to processor)

- Default for a sensor on the same board. 1–4 data lanes + clock.
- Data rate = width × height × fps × bits-per-pixel (Gbps).
  The link must carry it: lanes × lane_rate >= stream rate.
- D-PHY caps (MIPI Alliance): v1.1 = 1.5, v1.2 = 2.5,
  v2.0/v2.1 = 4.5 Gbps/lane. C-PHY: up to 5.7 Gsps per trio.
- 4-lane D-PHY v1.2 = 10 Gbps (4K30); v2.0 4-lane = 18 Gbps.
- Control (CCI) runs over I2C: 100 kHz / 400 kHz / 1 MHz (I3C
  optional on newer sensors). Never over the data lanes.
- Routing: 85 Ω differential, short traces, unbroken GND plane,
  length-matched within a pair (base skill §7). Long flex needs a
  re-driver or a slower lane rate.

## USB (camera to host)

- USB 2.0 = 0.48, USB 3.0 = 5, USB 3.1 = 10, USB 3.2 = 20 Gbps.
- UVC (USB Video Class) for plug-and-play; check the SoC driver.
- A stream over the link capacity FAILs `interface_check.py`.

## Ethernet / network

- 100M / 1GbE / 2.5GbE / 10GbE. RTSP for streaming, ONVIF for
  discovery and control, MQTT for events/alerts.
- PoE carries power + data on one cable (see components.md).
- Never expose RTSP without authentication; never expose an admin
  page over plain HTTP.

## Storage interfaces

- microSD: SDIO / SDR104 (Pi 5: SDR104, ~2× faster than older Pis).
- eMMC 5.1: soldered, 8-bit bus.
- NVMe: PCIe (needs a PCIe interface on the SoC — see §9).
- SATA III: 6 Gbps, for 2.5" SSDs on a workstation/server.
