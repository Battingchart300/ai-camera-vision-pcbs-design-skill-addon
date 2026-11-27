# Camera Interface (MIPI CSI-2 / USB / Ethernet) — critical

Moves the pixels from the sensor to the processor.

## MIPI CSI-2 (default)

- 1–4 data lanes + clock, D-PHY: v1.1 = 1.5, v1.2 = 2.5,
  v2.0/v2.1 = 4.5 Gbps/lane. C-PHY up to 5.7 Gsps per trio.
- Stream rate = width × height × fps × bits-per-pixel. The link
  must carry it — `interface_check.py` does the math and FAILs a
  link that is too narrow.
- Routing: 85 Ω differential, short, over unbroken GND
  (references/design-rules.md).

## USB

- UVC cameras: USB 2.0 = 0.48, USB 3.0 = 5 Gbps. Fine for a
  camera that is a module, not a sensor on your board.

## Ethernet

- For a camera that is a network node: 1GbE / 2.5GbE, RTSP/ONVIF.
  PoE carries power too (see power.md).

## Checks

`scripts/interface_check.py`: interface matches the sensor, lane
rate within the D-PHY cap, lanes within the processor's count,
stream fits the link.
