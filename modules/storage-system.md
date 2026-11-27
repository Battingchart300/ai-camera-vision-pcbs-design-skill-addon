# Storage System

Local + central storage, designed as one system — not two
afterthoughts.

## Local (on the camera)

- microSD / eMMC / NVMe — see `modules/storage.md`. Ring buffer:
  overwrite oldest first, protect event clips until uploaded.
- The card must hold the retention period: retention days × GB/day
  <= capacity. Check it by hand (v0.0.1 gap — no script checks
  this yet).

## Central (Vision PC / server)

- Only anonymized data is stored centrally (§8): counts, alerts,
  blurred clips, metadata. Raw footage stays on the camera.
- Redundancy: a server stores on RAID / mirrored disks, not a
  single drive. Backups exist and are tested.
- Retention on the server follows the same minimization rule as
  the camera (<= 30 days, prefer <= 14).

## Rules

- A network outage must not lose the event: buffer locally, upload
  when the link returns.
- Storage is sized from the encoder bitrate — measure it on the
  real board (`benchmarks/benchmark.py` uses a placeholder).
