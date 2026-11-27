# Architecture

Three reference architectures. Pick the closest one, then change
only what your use case needs.

## 1. Solar camera trap (battery, off-grid)

```
Lens -> Sensor (IMX219) -> MIPI CSI-2 -> SoC (BCM2712, PiSP ISP)
  -> microSD (clips) -> Wi-Fi (upload when in range)
  Solar panel -> MPPT charger -> 18650 battery -> 5 V rail
  PIR sensor -> wake SoC on motion
```

Power is the design driver: avg under 1 W, sleep most of the time,
PIR wake, short clips. See `examples/solar_camera_trap.json`.

## 2. Industrial MIPI camera (PoE, always on)

```
Lens (CS-mount) -> Sensor (IMX477) -> MIPI CSI-2 x4 -> SoC (RK3588)
  -> ISP (48 MP) -> NPU (6 TOPS, object detection on-device)
  -> NVMe (local buffer) -> 1GbE + PoE 802.3at -> NVR / Vision Server
```

Bandwidth is the design driver: 12 MP @ 30 fps = 3.7 Gbps raw —
4 lanes at 1.5 Gbps. PoE powers it (12 W peak < 25.5 W budget).
See `examples/industrial_mipi_camera.json`.

## 3. Robotic vision (Edge Vision PC)

```
Sensor (IMX708) -> MIPI CSI-2 x2 -> SoC (RK3588) -> ISP + NPU
  -> Edge Vision PC (same board or next to it) -> decisions on-device
  -> Wi-Fi / Ethernet: only results leave the robot
```

Latency is the design driver: process where the image is made,
never stream raw video to the cloud to decide.

## Data flow rule (all three)

Sensor -> ISP -> AI (on-device) -> anonymized result -> storage/network.
Raw video never leaves the device unless a human explicitly decided
it must — and then it is the exception, logged with a reason.
