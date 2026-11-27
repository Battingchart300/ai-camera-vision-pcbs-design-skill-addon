# Custom Vision Server

Centralized processing of **allowed** image data — a server that
sees what the cameras are allowed to send, and nothing else.

## What it does

- Receives anonymized results from cameras (counts, alerts,
  blurred clips, metadata).
- Runs heavier models than an edge device can (multi-camera
  tracking, long-term statistics).
- Stores results with retention limits (§8).

## What it does NOT do

- It does **not** receive raw footage of people. Raw footage stays
  on the camera. A server that stores raw footage without
  anonymization FAILs `privacy_check.py` and `vision_pc_check.py`.
- It is not a mass-surveillance backend. Anonymous statistics
  (traffic counts, flow) are the use case — not identifying people.

## Build rules (see also SKILL.md §9)

- Category `server`: ECC RAM mandatory, redundant PSU mandatory,
  both enforced by `vision_pc_check.py`.
- PSU >= peak × 1.25; cooling capacity >= peak power.
- OS: Linux (server distro). Updates and backups are part of the
  design, not an afterthought.
- The motherboard / GPU / FPGA side is designed with the PC
  component addon — this addon does not duplicate it.
