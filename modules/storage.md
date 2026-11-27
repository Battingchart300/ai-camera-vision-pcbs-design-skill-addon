# Storage (SD / eMMC / SSD) — high

Where the clips live, and for how long.

## Choosing

- **microSD:** cheap, removable. Pick endurance-rated cards for
  continuous recording; a consumer card dies early on 24/7 writes.
  Check write speed against the encoder bitrate.
- **eMMC:** soldered, more reliable outdoors (no slot to corrode,
  no card to steal). The industrial default for a fixed camera.
- **NVMe SSD:** for industrial cameras and Vision PCs (needs PCIe).
- **No local storage:** stream-only is not a design — a network
  outage must not lose the event. Buffer locally, then upload.

## Sizing

- Days of storage = card GB / GB per day at the recording duty
  cycle. `benchmarks/benchmark.py` estimates it (ESTIMATE — the
  encoder bitrate is a placeholder until measured).
- Retention in the spec (`privacy.retention_days`) must fit the
  card: a 30-day retention on a card that holds 7 days is a lie.
- Overwrite oldest first (ring buffer), and keep an event's clip
  from being overwritten until it is uploaded or reviewed.

## Checks

No script checks storage size against retention yet (v0.0.1 gap —
noted in the README of this module as a known limitation). Check it
by hand: retention days × GB/day <= capacity.
