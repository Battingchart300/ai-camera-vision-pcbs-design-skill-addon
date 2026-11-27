#!/usr/bin/env python3
"""vision_pc_check.py — Custom Vision PC build compatibility.

Checks a vision_pc section (Edge Vision PC / Vision Workstation /
Vision Server — see SKILL.md §9 and modules/vision-pc.md):
  * category is edge / workstation / server
  * CPU/SoC is a known part (a generic CPU is allowed with a warning)
  * RAM type matches the CPU (e.g. RK3588 takes LPDDR only — DDR5 FAILs)
  * RAM size <= the CPU's max
  * NVMe storage needs a PCIe interface
  * PSU watts >= peak power * 1.25 headroom
  * cooling capacity >= peak power
  * a server needs ECC RAM and redundant PSU (error otherwise)
  * OS is a supported Linux/embedded OS
  * central storage of raw footage needs anonymization first
    (privacy rule — see privacy_check.py too)

This validator checks the COMPUTE side only. The board itself
(motherboard, GPU, FPGA) is designed with the PC component addon
(ai-pc-component-design-skill-addon) — this addon does NOT duplicate it.

Exit codes: 0 = pass, 1 = fail, 2 = setup missing (base skill / spec).
Standard library only.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import Report, check_base_or_exit, load_spec
sys.path.insert(0, str(HERE.parent))
from validators.known_parts import VISION_CPUS
from validators.types import is_bool, is_int, is_nonempty_str, is_number, is_unverified

CATEGORIES = ("edge", "workstation", "server")
OS_LIST = ("Linux", "embedded Linux", "Yocto", "Buildroot", "Ubuntu", "Debian")
PSU_HEADROOM = 1.25


def main():
    ap = argparse.ArgumentParser(description="Check a Custom Vision PC build.")
    ap.add_argument("spec", help="Camera spec JSON (with a vision_pc section)")
    ap.add_argument("--base-skill", default=None, help="Path to ai-pcb-design-skill repo")
    args = ap.parse_args()

    check_base_or_exit(args.base_skill)
    spec, err = load_spec(args.spec)
    report = Report("vision_pc_check")
    if err:
        print(f"SETUP ERROR: {err}")
        print(f"Audit log: vision_pc_check=FAIL (setup), exit=2")
        return 2

    vpc = spec.get("vision_pc")
    if vpc is None:
        report.warning("no 'vision_pc' section — nothing to check "
                       "(this check only applies to Vision PC builds)")
        return report.finish()
    if not isinstance(vpc, dict):
        report.error("'vision_pc' must be an object")
        return report.finish()

    category = vpc.get("category")
    if category not in CATEGORIES:
        report.error(f"vision_pc.category must be one of {CATEGORIES} "
                     f"(got {category!r})")
        return report.finish()

    # --- CPU ------------------------------------------------------------------
    cpu = vpc.get("cpu")
    if not isinstance(cpu, dict):
        report.error("missing 'vision_pc.cpu' object")
        return report.finish()
    cpu_part = cpu.get("part")
    cpu_info = None
    if not is_nonempty_str(cpu_part):
        report.error("vision_pc.cpu.part must be a non-empty part name")
    elif is_unverified(cpu_part):
        report.error("vision_pc.cpu.part is UNVERIFIED — name the exact CPU/SoC")
    else:
        cpu_info = VISION_CPUS.get(cpu_part)
        if cpu_info is None:
            report.error(f"vision_pc.cpu.part '{cpu_part}' is not a known "
                         "verified CPU — invented or unlisted part")
        elif not cpu_info.get("verified", True):
            report.warning(f"vision_pc.cpu.part '{cpu_part}' is generic — "
                           "verify the exact CPU against its datasheet")

    # --- RAM -------------------------------------------------------------------
    ram_type = cpu.get("ram_type")
    ram_gb = cpu.get("ram_gb")
    if not is_nonempty_str(ram_type):
        report.error("vision_pc.cpu.ram_type must name the RAM type "
                     "(e.g. 'LPDDR4X', 'DDR5')")
    elif cpu_info is not None and ram_type not in cpu_info["ram"]:
        report.error(f"RAM mismatch: {cpu_part} takes "
                     f"{', '.join(cpu_info['ram'])}, not {ram_type}")
    if not is_int(ram_gb) or ram_gb <= 0:
        report.error(f"vision_pc.cpu.ram_gb must be a positive integer (got {ram_gb!r})")
    elif cpu_info is not None and cpu_info["max_ram_gb"] is not None \
            and ram_gb > cpu_info["max_ram_gb"]:
        report.error(f"RAM too big: {ram_gb} GB exceeds the {cpu_part} max "
                     f"of {cpu_info['max_ram_gb']} GB")

    # --- storage ---------------------------------------------------------------
    storage = vpc.get("storage")
    if isinstance(storage, dict):
        stype = storage.get("type")
        iface = storage.get("interface", "")
        if stype == "NVMe" and "PCIe" not in str(iface):
            report.error("NVMe storage needs a PCIe interface "
                         f"(got interface {iface!r})")
        if stype not in ("NVMe", "SATA", "eMMC", "microSD", "UFS"):
            report.error(f"unknown vision_pc.storage.type '{stype}'")
        if cpu_info is not None and not cpu_info["pcie"] and stype == "NVMe":
            report.error(f"NVMe storage on {cpu_part}, which has no PCIe")

    # --- accelerator -------------------------------------------------------------
    accel = vpc.get("accelerator")
    if isinstance(accel, dict):
        tops = accel.get("tops")
        if tops is not None and (not is_number(tops) or tops < 0):
            report.error(f"vision_pc.accelerator.tops must be a non-negative "
                         f"number (got {tops!r})")

    # --- power / PSU ---------------------------------------------------------------
    peak_w = vpc.get("power", {}).get("peak_w") \
        if isinstance(vpc.get("power"), dict) else None
    psu_w = vpc.get("psu", {}).get("watts") \
        if isinstance(vpc.get("psu"), dict) else None
    if peak_w is not None and (not is_number(peak_w) or peak_w <= 0):
        report.error(f"vision_pc.power.peak_w must be a positive number (got {peak_w!r})")
        peak_w = None
    if psu_w is not None and (not is_number(psu_w) or psu_w <= 0):
        report.error(f"vision_pc.psu.watts must be a positive number (got {psu_w!r})")
        psu_w = None
    if peak_w is not None and psu_w is not None:
        if psu_w < peak_w * PSU_HEADROOM:
            report.error(f"PSU too small: {psu_w} W < {peak_w} W peak * "
                         f"{PSU_HEADROOM} headroom = {peak_w * PSU_HEADROOM:.1f} W")

    # --- cooling ----------------------------------------------------------------------
    cooling = vpc.get("cooling")
    if isinstance(cooling, dict):
        cap = cooling.get("capacity_w")
        if cap is not None:
            if not is_number(cap) or cap <= 0:
                report.error(f"vision_pc.cooling.capacity_w must be a positive "
                             f"number (got {cap!r})")
            elif peak_w is not None and cap < peak_w:
                report.error(f"cooling too weak: {cap} W capacity < {peak_w} W peak")

    # --- server rules -------------------------------------------------------------------
    if category == "server":
        if vpc.get("ecc_ram") is not True:
            report.error("a Vision Server needs ECC RAM (ecc_ram: true) — "
                         "central processing of image data must not silently corrupt")
        if vpc.get("redundant_psu") is not True:
            report.error("a Vision Server needs a redundant PSU "
                         "(redundant_psu: true)")
    if category == "edge" and vpc.get("ecc_ram") is True:
        report.warning("ECC RAM on an Edge Vision PC is unusual — fine, but "
                       "check the SoC actually supports it")

    # --- OS -----------------------------------------------------------------------------
    os_name = vpc.get("os")
    if os_name is not None:
        if not is_nonempty_str(os_name):
            report.error("vision_pc.os must be a non-empty string")
        elif os_name not in OS_LIST:
            report.warning(f"vision_pc.os '{os_name}' is not a listed supported "
                           f"OS ({', '.join(OS_LIST)}) — verify driver support")

    # --- central storage privacy -----------------------------------------------------------
    if vpc.get("stores_raw_footage") is True \
            and vpc.get("anonymized_before_storage") is not True:
        report.error("vision_pc stores raw footage without anonymization — "
                     "anonymize before central storage (SKILL.md §8/§9)")

    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
