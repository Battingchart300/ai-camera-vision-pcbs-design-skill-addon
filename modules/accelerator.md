# AI Accelerator (NPU / GPU / TPU / FPGA) — high

On-device inference: detect, count, classify — without sending
video anywhere.

## Choosing

| Accelerator | Typical TOPS (INT8) | Fits |
|---|---|---|
| RK3588 NPU | 6 | Object detection, tracking |
| Jetson Orin Nano GPU | 20 dense / 40 sparse | Multi-model, tracking, segmentation |
| Sony IMX500 (on-chip) | UNVERIFIED | Simple on-sensor inference |
| BCM2712 / ESP32-S3 | 0 (CPU only) | Tiny models, motion detection |
| FPGA (custom) | depends on design | Custom pipelines, low latency |

## Rules

- The model's TOPS demand must fit the accelerator
  (`ai.npu_tops_required` <= processor NPU TOPS — checked).
- Prefer a model that runs on the NPU over one that needs the GPU:
  it is cooler and cheaper in power.
- Quantize to INT8 where the accuracy allows it; FP16 is the
  fallback, not the default.
- A model that does not fit is not "optimized later" — pick a
  lighter model or a stronger accelerator now.

## Checks

`sensor_check.py` (TOPS demand), `benchmarks/benchmark.py`
(NPU utilization estimate).

## Privacy link

Inference on-device is what makes §8 possible: the camera sends
counts and alerts, not faces.
