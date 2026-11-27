# Benchmarks — estimates only, never measured results

`benchmark.py` computes **theoretical estimates** from a camera spec:
sensor data rate, link utilization, NPU utilization, storage days at a
given recording duty cycle, and solar autonomy. Every number it prints
is labeled `ESTIMATE`.

It never claims a measurement. A measured benchmark needs the real
board, a real sensor and a real workload — this script is for sizing
the design before that exists.

Usage:

```bash
python benchmarks/benchmark.py examples/solar_camera_trap.json
python benchmarks/benchmark.py examples/industrial_mipi_camera.json
```

Reference numbers used (all from the verified tables in
`validators/known_parts.py`):

| Quantity | Rule |
| --- | --- |
| Sensor stream | width * height * fps * bits-per-pixel |
| Link utilization | stream / (lanes * lane rate) |
| NPU utilization | model TOPS required / processor TOPS |
| Storage days | card GB / (GB per day at the recording duty cycle) |
| Solar autonomy | battery Wh / daily Wh |

Storage math assumes H.265 at ~10 Mbps for 1080p30 motion clips
(UNVERIFIED placeholder — measure the real encoder bitrate on the
board and replace it).
