#!/usr/bin/env python3
"""Build the two P2 pilot notebook skeletons as nbformat 4 JSON (standard library only).

Usage, from the project root:
  python exp/P2_nb/build_notebooks.py          build, check, then write the notebooks
  python exp/P2_nb/build_notebooks.py --check  build and check in memory, compare with disk, write nothing

This script writes the notebooks and never executes them. Every check is static: ast.parse and
compile on each code cell, an undefined-name scan in cell order, a call-arity scan, a structure
check against the nbformat 4.5 cell layout, and rule checks taken from the task brief (banner
cell, licence cells, empty source addresses, no address-like text, no download code, imports,
docstrings, timing cells, last cell, size, ASCII, no stored output).

A notebook on disk is replaced only when it is an unmodified earlier build (the cell digest
stored in its metadata still matches its cells). A notebook that was edited or run is never
replaced by this script.
"""
import ast
import builtins
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
BANNER = "PILOT SKELETON - NOT RUN - synthetic data only - no result may be quoted from this notebook"
LICENCE_PENDING = "to confirm from the official page"
SIZE_LIMIT = 26000  # bytes per notebook (docs/playbook/12_methods.md 12.10: under 26 KB each)
CUE_FUNCTIONS = ["contour_box_agreement", "shadow_band_edge_stat", "saturated_region_stat",
                 "global_local_luminance_residual", "flicker_stat"]
LAST_CELL_TITLE = "What must replace the synthetic frames before any claim is made"

# Candidate datasets: labels as they appear on the owner's deck and design slides (leads, not
# confirmed facts). No licence and no source address is typed here: task LIT_X2 collects them.
DATASETS = [
    ("BDD100K (video)", "candidate; named on the deck plan and on design slide 05; not selected; not downloaded"),
    ("PVDN", "candidate; named on the deck plan; not selected; not downloaded"),
    ("ACDC", "candidate; named on the deck plan; not selected; not downloaded"),
    ("Lost and Found", "candidate; named on the deck plan; not selected; not downloaded"),
    ("low-light dataset (no name given on the deck)", "candidate; dataset not yet named; not selected; not downloaded"),
    ("CODA", "candidate; named on the deck plan; not selected; not downloaded"),
    ("LISA (label on design slide 02)", "candidate; named on design slide 02; not selected; not downloaded"),
    ("GTSRB", "candidate; named on design slide 02; not selected; not downloaded"),
]


def md(text):
    return ("markdown", text.strip("\n"))


def code(text):
    return ("code", text.strip("\n"))


# ---------------------------------------------------------------------------------------------
# Notebook 1: environment and data manifest
# ---------------------------------------------------------------------------------------------

N1_INTRO = r'''
# P2 pilot 01 - environment and data manifest

Preparation for the Paper 2 (P2) pilot. Written by an agent through `build_notebooks.py`. Never executed. Not audited.

Run in Colab, this notebook:

1. mounts Drive and sets the project folder as one variable, `PROJECT_DIR`;
2. reports Python, CPU, RAM, GPU and library versions of the runtime (it reads only and installs nothing);
3. holds the data manifest: dataset, licence, source address, status;
4. defines helpers that record sha256 and write a split manifest by recording, never by frame;
5. marks the place where a download cell would go. It contains no download code.

Rules: public data only. A licence is recorded before any download. Splits are by recording or route. Times come from the runtime clock. No file is overwritten. Every printed value is PILOT. To keep this skeleton as written, run a copy (File, Save a copy in Drive).
'''

N1_S1 = r'''
## 1. Drive mount and project path

`PROJECT_DIR` is the one variable every other path is built from. Its default was derived from the Drive for desktop path of the project folder and was not checked in Colab: if the cell prints `project folder found: False`, edit it. Third-party data goes to `DATA_DIR` on the Colab disk, not into the shared Drive folder.
'''

N1_C1 = r'''
import os
import sys

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")   # the owner approves the Drive prompt in the browser

# The one variable every other path is built from.
# ASSUMPTION: derived from the Drive for desktop path of the project folder; not checked in Colab.
PROJECT_DIR = "/content/drive/MyDrive/US/Documents/Projects/PhD_Thesis_Research_UDC_CS/Opencode_PhD_Thesis_Research_UDC_CS"

NB_DIR = os.path.join(PROJECT_DIR, "exp", "P2_nb")
OUT_DIR = os.path.join(NB_DIR, "manifests")   # small text records written by this notebook
DATA_DIR = "/content/data"                    # Colab disk, not Drive: third-party data stays out of the shared folder
SAVE_OUTPUTS = False                          # True lets later cells write new files under OUT_DIR
SEED = 20261119                               # one fixed seed for the split helper

PROJECT_OK = os.path.isfile(os.path.join(NB_DIR, "README.md"))
print("in Colab:", IN_COLAB)
print("PROJECT_DIR:", PROJECT_DIR)
print("project folder found:", PROJECT_OK)
if not PROJECT_OK:
    print("Edit PROJECT_DIR: it must be the folder that holds exp/P2_nb/README.md. Nothing is saved until it is found.")
'''

N1_S2 = r'''
## 2. Environment report

Python, CPU, RAM, GPU, free disk and library versions, read from the runtime. A library that is absent is reported as `not installed`; nothing is installed. A runtime without a GPU is reported as such: the CPU-first route does not need one.
'''

N1_C2 = r'''
import importlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone

# Reported only. None of these is installed by this notebook.
LIBRARIES = ["numpy", "opencv-python", "opencv-python-headless", "opencv-contrib-python", "scipy",
             "scikit-learn", "pandas", "torch", "torchvision", "onnxruntime"]


def utc_now(compact=False):
    """UTC time read from the runtime clock at call time (never typed by hand)."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ" if compact else "%Y-%m-%dT%H:%M:%SZ")


def new_file(path):
    """Open a new text file for writing. An existing file is never replaced: the call fails instead."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    return open(path, "x", encoding="utf-8", newline="")


def save_record(stem, record):
    """Write record as JSON to a new file OUT_DIR/<stem>_<UTC>.json. Skipped unless SAVE_OUTPUTS and PROJECT_OK."""
    if not (SAVE_OUTPUTS and PROJECT_OK):
        print("not saved (SAVE_OUTPUTS is False or the project folder was not found):", stem)
        return None
    path = os.path.join(OUT_DIR, stem + "_" + utc_now(compact=True) + ".json")
    with new_file(path) as handle:
        json.dump(record, handle, indent=1)
    print("saved:", path)
    return path


def proc_value(path, key):
    """Value of the first 'key: value' line of a /proc text file; empty text when the file or the key is absent."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if line.lower().startswith(key) and ":" in line:
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return ""


def environment_report():
    """Python, CPU, RAM, GPU, free disk and library versions of this runtime. Reads only; installs nothing."""
    report = {"read_utc": utc_now(), "in_colab": IN_COLAB, "python": sys.version.split()[0],
              "platform": platform.platform(),
              "cpu_model": proc_value("/proc/cpuinfo", "model name") or platform.processor() or "unknown",
              "cpu_logical_cores": os.cpu_count(),
              "ram_total": proc_value("/proc/meminfo", "memtotal") or "unknown",
              "ram_available": proc_value("/proc/meminfo", "memavailable") or "unknown",
              "disk_free_gib": round(shutil.disk_usage(os.getcwd()).free / 2 ** 30, 1)}
    smi = shutil.which("nvidia-smi")
    if smi is None:
        report["gpu"] = "none visible (no nvidia-smi on this runtime)"
    else:
        try:
            done = subprocess.run([smi, "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                                  capture_output=True, text=True, timeout=30)
            report["gpu"] = done.stdout.strip() or "nvidia-smi listed no GPU"
        except (OSError, subprocess.SubprocessError) as error:
            report["gpu"] = "nvidia-smi failed: " + type(error).__name__
    libraries = {}
    for name in LIBRARIES:
        try:
            libraries[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            libraries[name] = "not installed"
    for module in ("numpy", "cv2"):
        try:
            libraries["import " + module] = str(getattr(importlib.import_module(module), "__version__", "unknown"))
        except ImportError:
            libraries["import " + module] = "import failed"
    report["libraries"] = libraries
    return report


ENV = environment_report()
print("PILOT environment report (this runtime only)")
for key, value in ENV.items():
    print(f"  {key}: {value}")
save_record("env_report", ENV)
'''

N1_S3 = r'''
## 3. Data manifest

No dataset is chosen and none is downloaded. The names are the labels on the owner's deck and design slides: leads, not confirmed facts. Every licence cell reads "to confirm from the official page". Every source address cell is empty on purpose: the writer of this notebook checked no address. Task LIT_X2 collects licences and addresses (planned output: `notes/P2_LIT_X2_notes.md`). Copy from it only after it has been audited; the owner confirms each licence on the official page.

| dataset | licence | source address | status |
|---|---|---|---|
@@ROWS@@

Design slide 01 also names "APDE patch attacks". The acronym is not identified (UNVERIFIED), so it has no row.
'''

N1_C3 = r'''
LICENCE_PENDING = "to confirm from the official page"

# One row per candidate dataset. The names are labels from the owner's deck and design slides (leads).
# source_address stays empty until an audited table or the owner supplies it: never type one from memory.
DATA_MANIFEST = [
@@ROWS@@
]


def ready_for_download(row):
    """True only when the licence cell holds the confirmed licence, an address is recorded and the status starts with 'owner confirmed'."""
    return (row["licence"] != LICENCE_PENDING and row["source_address"] != ""
            and row["status"].startswith("owner confirmed"))


def print_manifest(rows):
    """Print the manifest as a plain text table."""
    columns = ["dataset", "licence", "source_address", "status"]
    widths = [max(len(c), max(len(r[c]) for r in rows)) for c in columns]
    print(" | ".join(c.ljust(w) for c, w in zip(columns, widths)))
    for r in rows:
        print(" | ".join(r[c].ljust(w) for c, w in zip(columns, widths)))


print_manifest(DATA_MANIFEST)
print("licence pending:", sum(1 for r in DATA_MANIFEST if r["licence"] == LICENCE_PENDING), "of", len(DATA_MANIFEST), "rows")
save_record("data_manifest", DATA_MANIFEST)
'''

N1_S4 = r'''
## 4. Helpers: sha256 records and a split manifest by recording

- `write_hash_manifest` pins a folder of files: one sha256 per file plus a record with the dataset name, version, source address and the UTC of hashing.
- `split_by_recording` assigns whole recordings to splits and `write_split_manifest` writes one row per recording. A frame has no row of its own: it takes the split of its recording, so neighbouring frames of one recording cannot be separated.
- The order of recordings comes from the sha256 of seed and recording id, so it does not depend on the Python version or on hash randomisation.
'''

N1_C4 = r'''
import csv
import hashlib

# Placeholder split names and fractions. An internal analysis plan fixes them before any run.
SPLIT_FRACTIONS = (("train", 0.5), ("val", 0.15), ("calib", 0.15), ("test", 0.2))


def sha256_file(path, chunk_bytes=1 << 20):
    """sha256 hex digest of one file, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(chunk_bytes), b""):
            digest.update(block)
    return digest.hexdigest()


def write_tsv(path, header, rows):
    """Write rows to a new tab-separated file (an existing file is never replaced). Returns its sha256."""
    with new_file(path) as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    return sha256_file(path)


def write_hash_manifest(root_dir, out_tsv, dataset="", version="", source_address=""):
    """Record the sha256 and size of every file under root_dir. Keep out_tsv outside root_dir.

    Writes out_tsv (relative_path, bytes, sha256; sorted) and out_tsv + ".json" with the dataset
    name, version, source address, UTC of hashing, file count, byte total and sha256 of out_tsv.
    """
    if not os.path.isdir(root_dir):
        raise FileNotFoundError(root_dir)
    if os.path.exists(out_tsv) or os.path.exists(out_tsv + ".json"):
        raise FileExistsError(out_tsv)   # checked before hashing, so no time is lost on a name that is taken
    rows = []
    for folder, _, files in os.walk(root_dir):
        for name in files:
            full = os.path.join(folder, name)
            relative = os.path.relpath(full, root_dir).replace(os.sep, "/")
            rows.append((relative, os.path.getsize(full), sha256_file(full)))
    rows.sort()
    record = {"dataset": dataset, "version": version, "source_address": source_address, "hashed_utc": utc_now(),
              "files": len(rows), "bytes": sum(row[1] for row in rows),
              "manifest_sha256": write_tsv(out_tsv, ["relative_path", "bytes", "sha256"], rows)}
    with new_file(out_tsv + ".json") as handle:
        json.dump(record, handle, indent=1)
    return record


def recording_of(relative_path, depth=1):
    """Recording id of a frame: its first `depth` folder names.

    Layout assumption (one folder per recording). Replace it with the dataset's own recording or
    route key, read from the dataset documentation, before any real split is written.
    """
    parts = [part for part in relative_path.replace("\\", "/").split("/") if part not in ("", ".")]
    if len(parts) <= depth:
        raise ValueError("frame is not inside a recording folder: " + relative_path)
    return "/".join(parts[:depth])


def split_by_recording(frame_paths, fractions=SPLIT_FRACTIONS, seed=SEED, key=recording_of):
    """Assign whole recordings to splits. The unit is the recording, never the frame.

    Recordings are ordered by sha256 of "seed:recording id" and cut at the cumulative fractions.
    Returns (split of each recording, frame count of each recording). With few recordings a
    split can stay empty; that is printed as a warning, not repaired.
    """
    if abs(sum(fraction for _, fraction in fractions) - 1.0) > 1e-9:
        raise ValueError("fractions must sum to 1")
    frames = {}
    for path in frame_paths:
        rec = key(path)
        frames[rec] = frames.get(rec, 0) + 1
    order = sorted(frames, key=lambda rec: hashlib.sha256(f"{seed}:{rec}".encode("utf-8")).hexdigest())
    split, start, cumulative = {}, 0, 0.0
    for index, (name, fraction) in enumerate(fractions):
        cumulative += fraction
        end = len(order) if index == len(fractions) - 1 else int(round(cumulative * len(order)))
        for rec in order[start:end]:
            split[rec] = name
        start = max(start, end)
    empty = [name for name, _ in fractions if name not in split.values()]
    if empty:
        print("WARNING: splits without any recording:", empty)
    return split, frames


def write_split_manifest(split, frames, out_tsv, fractions=SPLIT_FRACTIONS, seed=SEED):
    """Write one row per recording (recording_id, split, frames) and a JSON record beside it.

    The file has no frame rows. A frame takes the split of its recording, so neighbouring frames
    of one recording cannot land in different splits.
    """
    rows = [(rec, split[rec], frames[rec]) for rec in sorted(split)]
    names = [name for name, _ in fractions]
    record = {"unit": "recording", "seed": seed, "fractions": [list(pair) for pair in fractions],
              "written_utc": utc_now(),
              "recordings": {n: sum(1 for row in rows if row[1] == n) for n in names},
              "frames": {n: sum(row[2] for row in rows if row[1] == n) for n in names},
              "manifest_sha256": write_tsv(out_tsv, ["recording_id", "split", "frames"], rows)}
    with new_file(out_tsv + ".json") as handle:
        json.dump(record, handle, indent=1)
    return record


def read_split_manifest(tsv_path):
    """Read a split manifest back. Fails if a recording id occurs twice (it would sit in two splits)."""
    split = {}
    with open(tsv_path, "r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["recording_id"] in split:
                raise ValueError("recording listed twice: " + row["recording_id"])
            split[row["recording_id"]] = row["split"]
    return split


def split_of_frame(relative_path, split, key=recording_of):
    """Split of one frame, looked up through its recording only."""
    return split[key(relative_path)]
'''

N1_C5 = r'''
# DEMO on made-up file names: no data is read and nothing is written.
demo_frames = [f"rec_{r:02d}/frame_{i:04d}.png" for r in range(10) for i in range(6)]
demo_split, demo_counts = split_by_recording(demo_frames)
demo_groups = {}
for path in demo_frames:
    demo_groups.setdefault(recording_of(path), set()).add(split_of_frame(path, demo_split))
print("DEMO (made-up names, not data) recordings per split:",
      {name: sum(1 for rec in demo_split if demo_split[rec] == name) for name, _ in SPLIT_FRACTIONS})
print("DEMO every recording sits in exactly one split:", all(len(found) == 1 for found in demo_groups.values()))

# Use on real files, once a dataset is on the Colab disk and SAVE_OUTPUTS is True (not run here):
#   stamp = utc_now(compact=True)
#   write_hash_manifest(os.path.join(DATA_DIR, "<dataset>"), os.path.join(OUT_DIR, "<dataset>_sha256_" + stamp + ".tsv"),
#                       dataset="<name>", version="<version>", source_address="<from the manifest>")
#   split, frames = split_by_recording(<relative frame paths>, key=<recording or route key of that dataset>)
#   write_split_manifest(split, frames, os.path.join(OUT_DIR, "<dataset>_split_" + stamp + ".tsv"))
'''

N1_S5 = r'''
## 5. Download placeholder

**No download cell exists in this notebook.** The owner confirms the licence on the official page first. Until then the cell below only prints which manifest rows are ready, which is none.
'''

N1_C6 = r'''
# =============================================================================================
# DOWNLOAD PLACEHOLDER - INTENTIONALLY EMPTY - THIS NOTEBOOK FETCHES NOTHING
# The owner confirms the licence on the official page first. Only after that:
#   1. the owner fills licence, source_address and status ("owner confirmed ...") of that row;
#   2. a cell for that one dataset is written here, saving to DATA_DIR on the Colab disk;
#   3. write_hash_manifest(...) pins the files before any use.
# =============================================================================================
ready = [row["dataset"] for row in DATA_MANIFEST if ready_for_download(row)]
print("rows with an owner-confirmed licence and a source address:", ready if ready else "none")
print("Nothing is fetched by this notebook. The owner confirms the licence first.")
'''

N1_S6 = r'''
## 6. Status and what is not done

- PILOT SKELETON. Not run. Not audited. Written by the same agent that wrote the builder script.
- `PROJECT_DIR` was derived from the Drive for desktop path of the project folder and was not checked in Colab.
- No dataset is chosen, no licence is recorded, no source address is recorded, nothing is downloaded.
- `recording_of` (one folder per recording) is a layout assumption. Each dataset needs its own recording or route key, checked against its documentation.
- Split names and fractions are placeholders until an internal analysis plan, self-hashed before the first run, fixes them.
- The split helper has no stratification by condition (night, weather, attack type).
- Library versions are read, not pinned: no requirements file exists yet.
- `DATA_DIR` is on the Colab disk, which does not persist between runtimes. Where third-party data is kept between sessions is an owner decision.
'''

# ---------------------------------------------------------------------------------------------
# Notebook 2: cue features on synthetic frames
# ---------------------------------------------------------------------------------------------

N2_INTRO = r'''
# P2 pilot 02 - cue features on synthetic frames

Five small cue functions, one per cue family of the owner's design slides, applied to frames this notebook draws itself. numpy and OpenCV only, CPU only, fixed seed. It mounts no Drive and writes no file. Written by an agent through `build_notebooks.py`. Never executed. Not audited.

| Cue function | Design slide | Synthetic input |
|---|---|---|
| `contour_box_agreement` | 01 object appearance | sign-like polygon on a textured background |
| `shadow_band_edge_stat` | 02 shadows | dark slanted band |
| `saturated_region_stat` | 03 reflections | bright blob clipped to white |
| `global_local_luminance_residual` | 04 lighting | one gain on the whole frame |
| `flicker_stat` | 04 lighting and 05 video frames | horizontal stripes whose phase moves |

The functions return raw statistics. They set no threshold and take no decision. Not built here: viewpoint tracking, the reliability gates, the evidence accumulation of design slide 05, calibration, the explanation output and the abstain rule. The design slides state hypotheses, not a proven method. Synthetic frames can show only that the code runs and what each statistic responds to by construction.
'''

N2_C1 = r'''
import platform
import sys
import time

import cv2
import numpy as np

SEED = 20261119   # one fixed seed, reused by every cell
H, W = 240, 320   # synthetic frame size in pixels, small on purpose
REPEATS = 30      # timed calls per function
TIMINGS = {}      # function name -> timing row
NAN = float("nan")
CHECK = "PILOT synthetic check, not a result"

cv2.setNumThreads(1)              # fixed OpenCV thread count
cv2.setRNGSeed(SEED)
if hasattr(cv2, "ocl"):
    cv2.ocl.setUseOpenCL(False)   # CPU code path only

print("PILOT SKELETON - synthetic frames only - nothing printed by this notebook is a result")
print("python", sys.version.split()[0], "| numpy", np.__version__, "| opencv", cv2.__version__)
print("platform", platform.platform(), "| seed", SEED, "| frame", W, "x", H)


def to_u8(values):
    """Round, clip to 0..255 and convert to uint8."""
    return np.clip(np.rint(values), 0, 255).astype(np.uint8)


def clip_box(box, shape):
    """Clip an (x, y, w, h) box to an image shape. Returns (x0, y0, x1, y1); empty when x1 <= x0 or y1 <= y0."""
    x, y, w, h = [int(v) for v in box]
    return max(0, x), max(0, y), min(int(shape[1]), x + w), min(int(shape[0]), y + h)


def time_call(name, fn, *args):
    """Call fn(*args) once to warm up, then REPEATS times with a timer; store and print one PILOT row.

    The row describes this runtime and one small synthetic input. It is not a latency result for
    a camera pipeline: decoding, the detector, tracking and queueing are all absent.
    """
    fn(*args)
    ms = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        fn(*args)
        ms.append((time.perf_counter() - start) * 1000.0)
    TIMINGS[name] = dict(function=name, calls=REPEATS, seed=SEED, frame=f"{W}x{H}",
                         p50_ms=round(float(np.percentile(ms, 50)), 4),
                         p95_ms=round(float(np.percentile(ms, 95)), 4))
    print("PILOT timing, synthetic input, not a result:", TIMINGS[name])
    return TIMINGS[name]
'''

N2_S2 = r'''
## 2. Synthetic frames

The frames drawn below are stand-ins chosen so that each statistic has something to respond to. They are not road scenes, not attacks and not benign look-alikes.
'''

N2_C2 = r'''
def make_background(rng):
    """Textured grey background: a smooth random field plus fine noise. Not a road scene."""
    coarse = rng.normal(0.0, 1.0, (H // 8 + 1, W // 8 + 1)).astype(np.float32)
    coarse = cv2.resize(coarse, (W, H), interpolation=cv2.INTER_CUBIC)
    fine = rng.normal(0.0, 1.0, (H, W)).astype(np.float32)
    return cv2.cvtColor(to_u8(120.0 + 20.0 * coarse + 6.0 * fine), cv2.COLOR_GRAY2BGR)


def sensor_noise(frame, rng, sigma=2.0):
    """Add independent Gaussian noise per pixel and channel (a crude stand-in for sensor noise)."""
    return to_u8(frame.astype(np.float32) + rng.normal(0.0, sigma, frame.shape).astype(np.float32))


def make_scene(rng, sides=8, radius=48):
    """Clean frame with one filled sign-like polygon near the centre.

    Returns (frame, box, mask): box = (x, y, w, h) of the drawn polygon, used as a stand-in for
    a detector box; mask = boolean polygon mask of the frame size.
    """
    frame = make_background(rng)
    cx = W // 2 + int(rng.integers(-20, 21))
    cy = H // 2 + int(rng.integers(-10, 11))
    angles = np.pi / sides + 2.0 * np.pi * np.arange(sides) / sides
    points = np.stack([cx + radius * np.cos(angles), cy + radius * np.sin(angles)], axis=1)
    polygon = np.rint(points).astype(np.int32).reshape(-1, 1, 2)
    cv2.fillPoly(frame, [polygon], (40, 40, 190))
    mask = np.zeros((H, W), np.uint8)
    cv2.fillPoly(mask, [polygon], 255)
    return sensor_noise(frame, rng), cv2.boundingRect(polygon), mask > 0


def add_shadow_band(frame, angle_deg=30.0, width=36.0, strength=0.5, soft_px=2.0):
    """Darken a slanted band through the frame centre (stand-in for a cast shadow band).

    Pixels in the band are multiplied by (1 - strength); the edge is a linear ramp soft_px wide.
    A real shadow also shifts colour and follows scene geometry; this one does neither.
    """
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    theta = np.deg2rad(angle_deg)
    distance = np.abs((xx - W / 2.0) * np.cos(theta) + (yy - H / 2.0) * np.sin(theta))
    inside = np.clip((width / 2.0 - distance) / soft_px + 0.5, 0.0, 1.0)
    return to_u8(frame.astype(np.float32) * (1.0 - strength * inside)[:, :, None])


def add_specular_blob(frame, centre, sigma=7.0, peak=300.0):
    """Add a bright Gaussian blob that clips to white at its core (stand-in for a specular highlight)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    blob = np.exp(-((xx - centre[0]) ** 2 + (yy - centre[1]) ** 2) / (2.0 * sigma ** 2))
    return to_u8(frame.astype(np.float32) + peak * blob[:, :, None])


def apply_exposure_jump(frame, gain=1.3):
    """Multiply the whole frame by one gain (stand-in for an auto-exposure step). Clips at white."""
    return to_u8(frame.astype(np.float32) * gain)


def add_stripe_flicker(frame, phase, period_px=12.0, amplitude=14.0):
    """Add horizontal sinusoidal stripes at a phase given in cycles (stand-in for banding under a modulated light)."""
    rows = np.arange(H, dtype=np.float32)
    stripes = amplitude * np.sin(2.0 * np.pi * (rows / period_px + phase))
    return to_u8(frame.astype(np.float32) + stripes[:, None, None])


def make_sequence(rng, kind, n_frames=8):
    """Short frame list from one scene, with fresh noise per frame.

    kind: "static", "exposure" (one gain step halfway) or "stripes" (stripe phase moves each frame).
    Returns (frames, box, mask).
    """
    base, box, mask = make_scene(rng)
    frames = []
    for index in range(n_frames):
        frame = base
        if kind == "exposure" and index >= n_frames // 2:
            frame = apply_exposure_jump(frame)
        elif kind == "stripes":
            frame = add_stripe_flicker(frame, 0.37 * index)
        frames.append(sensor_noise(frame, rng))
    return frames, box, mask
'''

N2_S3 = r'''
## 3. Cue 1: contour-versus-box agreement (design slide 01)
'''

N2_C4 = r'''
def contour_box_agreement(frame_bgr, box, pad=8):
    """Contour-versus-box agreement (design slide 01, object appearance).

    Measures: inside the box grown by pad pixels, an Otsu threshold on HSV saturation gives a
    foreground mask, and its largest external contour is compared with the box. Returned: IoU of
    the contour's bounding rectangle with the box, contour area over box area, contour area over
    convex-hull area, and the vertex count of a polygon approximation.
    Does not show: that a patch or sticker is present, or that the detector is wrong. Low
    agreement also follows from a grey or white sign face, low light, occlusion, clutter or a
    loose box. Viewpoint is not modelled and no threshold or decision is set here.
    """
    out = dict(found=False, box_iou=NAN, fill_ratio=NAN, solidity=NAN, vertices=0)
    x, y, w, h = [int(v) for v in box]
    x0, y0, x1, y1 = clip_box((x - pad, y - pad, w + 2 * pad, h + 2 * pad), frame_bgr.shape)
    if x1 <= x0 or y1 <= y0 or w <= 0 or h <= 0:
        return out
    hsv = cv2.cvtColor(frame_bgr[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
    saturation = cv2.GaussianBlur(np.ascontiguousarray(hsv[:, :, 1]), (5, 5), 0)
    _, foreground = cv2.threshold(saturation, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours = cv2.findContours(foreground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(contours) == 0:
        return out
    contour = max(contours, key=cv2.contourArea)
    area = float(cv2.contourArea(contour))
    cx, cy, cw, ch = cv2.boundingRect(contour)
    cx, cy = cx + x0, cy + y0   # back to frame coordinates
    inter_w = max(0, min(x + w, cx + cw) - max(x, cx))
    inter_h = max(0, min(y + h, cy + ch) - max(y, cy))
    inter = float(inter_w * inter_h)
    hull_area = float(cv2.contourArea(cv2.convexHull(contour)))
    polygon = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    out.update(found=True, box_iou=inter / (w * h + cw * ch - inter), fill_ratio=area / (w * h),
               solidity=area / hull_area if hull_area > 0 else NAN, vertices=int(len(polygon)))
    return out
'''

N2_T1 = r'''
# TIMING CELL 1 of 5 - contour_box_agreement - fixed seed
rng = np.random.default_rng(SEED)
clean, box, mask = make_scene(rng)
loose_box = (box[0] - 25, box[1], box[2] + 50, box[3])
print(CHECK, "| matching box:", contour_box_agreement(clean, box))
print(CHECK, "| loose box   :", contour_box_agreement(clean, loose_box))
time_call("contour_box_agreement", contour_box_agreement, clean, box)
'''

N2_S4 = r'''
## 4. Cue 2: shadow-band edge statistic (design slide 02)
'''

N2_C5 = r'''
def shadow_band_edge_stat(frame_bgr, box, object_mask=None):
    """Shadow-band edge statistic (design slide 02, shadows).

    Measures, on the pixels of the box that lie in object_mask (the whole box if None): an Otsu
    split of luminance into a dark and a lit part; the dark fraction; the dark-to-lit luminance
    ratio; the shift in colour shares between the two parts (a cast shadow mainly scales
    intensity); and the mean luminance gradient on the dark/lit boundary over the luminance step
    (higher means a sharper edge).
    Does not show: that a shadow is present. Otsu splits any surface, also paint, dirt or plain
    noise on a uniform face, and the shape of the dark part (band or not) is not tested. It does
    not show what cast a shadow or whether it is physically plausible: one frame only, with no
    motion, sun or camera geometry.
    """
    out = dict(valid=False, dark_fraction=NAN, luminance_ratio=NAN, colour_shift=NAN, edge_sharpness=NAN)
    x0, y0, x1, y1 = clip_box(box, frame_bgr.shape)
    if x1 <= x0 or y1 <= y0:
        return out
    roi = frame_bgr[y0:y1, x0:x1]
    inside = np.ones(roi.shape[:2], bool) if object_mask is None else object_mask[y0:y1, x0:x1].astype(bool)
    if inside.shape != roi.shape[:2] or int(inside.sum()) < 16:
        return out
    luminance = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    threshold, _ = cv2.threshold(luminance[inside].reshape(-1, 1), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    dark = inside & (luminance <= threshold)
    lit = inside & (luminance > threshold)
    if not dark.any() or not lit.any():
        return out
    lum = luminance.astype(np.float32)
    mean_dark, mean_lit = float(lum[dark].mean()), float(lum[lit].mean())
    colour = roi.astype(np.float32)
    shares = colour / (colour.sum(axis=2, keepdims=True) + 1e-6)
    shift = float(np.abs(shares[dark].mean(axis=0) - shares[lit].mean(axis=0)).sum())
    gradient = cv2.magnitude(cv2.Sobel(lum, cv2.CV_32F, 1, 0, ksize=3, scale=0.25),
                             cv2.Sobel(lum, cv2.CV_32F, 0, 1, ksize=3, scale=0.25))
    boundary = (cv2.dilate(dark.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & lit
    step = mean_lit - mean_dark
    out.update(valid=True, dark_fraction=float(dark.sum()) / float(inside.sum()),
               luminance_ratio=mean_dark / max(mean_lit, 1e-6), colour_shift=shift,
               edge_sharpness=float(gradient[boundary].mean()) / step if boundary.any() and step > 0 else NAN)
    return out
'''

N2_T2 = r'''
# TIMING CELL 2 of 5 - shadow_band_edge_stat - fixed seed
rng = np.random.default_rng(SEED)
clean, box, mask = make_scene(rng)
shadowed = add_shadow_band(clean)
print(CHECK, "| no band  :", shadow_band_edge_stat(clean, box, mask))
print(CHECK, "| with band:", shadow_band_edge_stat(shadowed, box, mask))
time_call("shadow_band_edge_stat", shadow_band_edge_stat, shadowed, box, mask)
'''

N2_S5 = r'''
## 5. Cue 3: saturated-region statistic (design slide 03)
'''

N2_C6 = r'''
def saturated_region_stat(frame_bgr, box, v_min=250, s_max=40):
    """Saturated-region statistic (design slide 03, reflections).

    Measures, inside the box: the fraction of near-white pixels (HSV value >= v_min and
    saturation <= s_max), the area fraction of the largest connected near-white region, and the
    mean value contrast between that region and the rest of the box.
    Does not show: what caused the bright region. Sun glint, retroreflection, a wet surface, a
    lamp, white paint and a reflected-light attack can look alike in one RGB frame. Infrared
    light, which an IR-filtered camera may not record, is out of reach. No view, motion or
    exposure conditioning is done.
    """
    out = dict(valid=False, white_fraction=NAN, largest_region_fraction=NAN, value_contrast=NAN)
    x0, y0, x1, y1 = clip_box(box, frame_bgr.shape)
    if x1 <= x0 or y1 <= y0:
        return out
    hsv = cv2.cvtColor(frame_bgr[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
    value = hsv[:, :, 2]
    white = ((value >= v_min) & (hsv[:, :, 1] <= s_max)).astype(np.uint8)
    out.update(valid=True, white_fraction=float(white.mean()), largest_region_fraction=0.0)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(white, connectivity=8)
    if count > 1:
        largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        region = labels == largest
        out["largest_region_fraction"] = float(stats[largest, cv2.CC_STAT_AREA]) / float(white.size)
        if not region.all():
            out["value_contrast"] = float(value[region].mean()) - float(value[~region].mean())
    return out
'''

N2_T3 = r'''
# TIMING CELL 3 of 5 - saturated_region_stat - fixed seed
rng = np.random.default_rng(SEED)
clean, box, mask = make_scene(rng)
shiny = add_specular_blob(clean, (box[0] + box[2] // 2 - 12, box[1] + box[3] // 2 - 10))
print(CHECK, "| no blob  :", saturated_region_stat(clean, box))
print(CHECK, "| with blob:", saturated_region_stat(shiny, box))
time_call("saturated_region_stat", saturated_region_stat, shiny, box)
'''

N2_S6 = r'''
## 6. Cue 4: global-versus-local luminance residual (design slide 04)
'''

N2_C7 = r'''
def global_local_luminance_residual(prev_bgr, curr_bgr, box):
    """Global-versus-local luminance residual (design slide 04, lighting).

    Measures: the log ratio of mean luminance between two frames inside the box (local term) and
    over the rest of the frame (global term), and their difference (residual). One gain on the
    whole frame moves both terms together; a light change confined to the box moves the local
    term only.
    Does not show: why the local term moved. Headlights, a passing shadow, object or camera
    motion, clipping at white and a projected pattern all leave a residual. The box is assumed
    to cover the same surface in both frames: no registration, tracking or camera response model.
    """
    out = dict(valid=False, global_log_ratio=NAN, local_log_ratio=NAN, residual=NAN)
    x0, y0, x1, y1 = clip_box(box, curr_bgr.shape)
    n_box = (x1 - x0) * (y1 - y0)
    n_all = curr_bgr.shape[0] * curr_bgr.shape[1]
    if x1 <= x0 or y1 <= y0 or prev_bgr.shape != curr_bgr.shape or n_box >= n_all:
        return out
    means = []
    for frame in (prev_bgr, curr_bgr):
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        box_sum = float(grey[y0:y1, x0:x1].sum(dtype=np.float64))
        rest_sum = float(grey.sum(dtype=np.float64)) - box_sum
        means.append((max(box_sum / n_box, 1e-6), max(rest_sum / (n_all - n_box), 1e-6)))
    local_term = float(np.log(means[1][0] / means[0][0]))
    global_term = float(np.log(means[1][1] / means[0][1]))
    out.update(valid=True, global_log_ratio=global_term, local_log_ratio=local_term,
               residual=local_term - global_term)
    return out
'''

N2_T4 = r'''
# TIMING CELL 4 of 5 - global_local_luminance_residual - fixed seed
rng = np.random.default_rng(SEED)
clean, box, mask = make_scene(rng)
jump = apply_exposure_jump(clean)
local_light = add_specular_blob(clean, (box[0] + box[2] // 2, box[1] + box[3] // 2))
print(CHECK, "| gain on the whole frame:", global_local_luminance_residual(clean, jump, box))
print(CHECK, "| blob inside the box    :", global_local_luminance_residual(clean, local_light, box))
time_call("global_local_luminance_residual", global_local_luminance_residual, clean, jump, box)
'''

N2_S7 = r'''
## 7. Cue 5: frame-to-frame flicker statistic (design slides 04 and 05)
'''

N2_C8 = r'''
def flicker_stat(frames_bgr, box):
    """Frame-to-frame flicker statistic (design slides 04 and 05, lighting and video frames).

    Measures, over a short list of frames and inside the box: the log of the row-mean luminance
    profile of each frame; its frame-to-frame change with the mean removed (so one gain on the
    whole frame largely cancels); the mean absolute size of that change; and the share of its
    non-DC spectral power that falls in the strongest row frequency (horizontal stripes
    concentrate the power, broadband noise spreads it).
    Does not show: that a light is modulated or that anything is malicious. Rolling shutter, LED
    signs, PWM lamps, compression and frame-rate aliasing can hide or imitate stripes. Frames are
    not registered and the box is fixed, so motion also changes the profile. The function reads
    the list it is given: a bounded causal buffer and a decision rule are not built.
    """
    out = dict(valid=False, frames=len(frames_bgr), mean_abs_row_change=NAN, stripe_peak_share=NAN)
    if len(frames_bgr) < 2:
        return out
    x0, y0, x1, y1 = clip_box(box, frames_bgr[0].shape)
    if x1 <= x0 or y1 - y0 < 8 or any(frame.shape != frames_bgr[0].shape for frame in frames_bgr):
        return out
    profiles = []
    for frame in frames_bgr:
        grey = cv2.cvtColor(frame[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
        profiles.append(np.log(np.maximum(grey.mean(axis=1), 1e-3)))
    change = np.diff(np.stack(profiles), axis=0)
    change = change - change.mean(axis=1, keepdims=True)
    power = np.abs(np.fft.rfft(change, axis=1)[:, 1:]) ** 2
    share = power.max(axis=1) / np.maximum(power.sum(axis=1), 1e-12)
    out.update(valid=True, mean_abs_row_change=float(np.abs(change).mean()), stripe_peak_share=float(share.mean()))
    return out
'''

N2_T5 = r'''
# TIMING CELL 5 of 5 - flicker_stat - fixed seed
for kind in ("static", "exposure", "stripes"):
    frames, box, mask = make_sequence(np.random.default_rng(SEED), kind)
    print(CHECK, "|", kind.ljust(8), ":", flicker_stat(frames, box))
time_call("flicker_stat", flicker_stat, frames, box)
'''

N2_S8 = r'''
## 8. What must replace the synthetic frames before any claim is made

Nothing printed by this notebook is evidence about attacks, detectors or road scenes. Before any claim is made:

1. **Real recordings** from datasets whose licence the owner confirmed (manifest in notebook 01), pinned by sha256, replace `make_scene` and `make_sequence`.
2. **A real detector**: boxes, classes and scores of a frozen detector replace the box of the drawn polygon, and tracked boxes replace the fixed box in the two-frame and multi-frame functions.
3. **Real attack and benign material**: physical or validly simulated attack clips for each cue family (patch or sticker, crafted shadow, reflected light, projected or flickering light, object-vanishing sequences) and benign look-alikes as hard negatives (tree and cloud shadows, glare, wet roads, retroreflection, auto-exposure jumps, lamp and sign flicker) replace the drawn band, blob, gain step and stripes.
4. **Held-out recordings**: splits by recording or route from the split manifest of notebook 01, never by frame, with thresholds and calibration fitted on recordings outside the test split.
5. **An internal analysis plan, self-hashed** before the first run on evaluation data: hypotheses, decisive metric, baselines, splits, stop rules.
6. **Baselines**: detector-only, each cue alone, and the published comparators named on the design slides once the literature catalog has confirmed them.
7. **Operating points**: recall at a matched false-alarm point and false alarms per hour of ordinary driving replace the raw statistics printed here.
8. **End-to-end cost**: p50 and p95 latency per frame including decoding, detector, tracking and queueing on the target hardware, and peak memory, replace the per-function timings.
9. **Sensors and conditions**: more than one camera, frame rate and compression setting; night, rain and low visibility; rolling shutter. Nothing tuned to this noise model and frame size carries over by default.
10. **Abstention counts**: the number of cases with no usable evidence (occlusion, failed segmentation, clipped pixels), reported next to every rate.
11. **A fresh-agent audit** that traces every number to a run log before anything is called a result.
'''


def manifest_markdown():
    rows = "\n".join("| %s | %s |  | %s |" % (name, LICENCE_PENDING, status) for name, status in DATASETS)
    return N1_S3.replace("@@ROWS@@", rows)


def manifest_code():
    rows = ",\n".join('    {"dataset": %s, "licence": LICENCE_PENDING, "source_address": "", "status": %s}'
                      % (json.dumps(name), json.dumps(status)) for name, status in DATASETS)
    return N1_C3.replace("@@ROWS@@", rows + ",")


NOTEBOOKS = [
    {
        "file": "P2_pilot_01_environment_and_data_manifest.ipynb",
        "tag": "nb01",
        "imports": {"os", "sys", "csv", "hashlib", "importlib", "json", "platform", "shutil", "subprocess",
                    "datetime", "google"},
        "cells": [md(BANNER), md(N1_INTRO), md(N1_S1), code(N1_C1), md(N1_S2), code(N1_C2),
                  md(manifest_markdown()), code(manifest_code()), md(N1_S4), code(N1_C4), code(N1_C5),
                  md(N1_S5), code(N1_C6), md(N1_S6)],
    },
    {
        "file": "P2_pilot_02_cue_features_synthetic.ipynb",
        "tag": "nb02",
        "imports": {"platform", "sys", "time", "cv2", "numpy"},
        "cells": [md(BANNER), md(N2_INTRO), code(N2_C1), md(N2_S2), code(N2_C2),
                  md(N2_S3), code(N2_C4), code(N2_T1), md(N2_S4), code(N2_C5), code(N2_T2),
                  md(N2_S5), code(N2_C6), code(N2_T3), md(N2_S6), code(N2_C7), code(N2_T4),
                  md(N2_S7), code(N2_C8), code(N2_T5), md(N2_S8)],
    },
]

# ---------------------------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------------------------


def cells_digest(cells):
    packed = json.dumps(cells, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(packed.encode("ascii")).hexdigest()


def build(spec):
    """Return (notebook dict, file bytes) for one notebook spec."""
    cells = []
    for index, (kind, text) in enumerate(spec["cells"]):
        lines = text.split("\n")
        cell = {"cell_type": kind, "id": "c%02d" % index, "metadata": {},
                "source": [line + "\n" for line in lines[:-1]] + [lines[-1]]}
        if kind == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        cells.append(cell)
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
            "p2_skeleton": {"status": "PILOT SKELETON - NOT RUN", "builder": "exp/P2_nb/build_notebooks.py",
                            "cells_sha256": cells_digest(cells)},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    # indent=0 and tight separators: one item per line, no leading spaces, which keeps the file under SIZE_LIMIT.
    packed = json.dumps(notebook, indent=0, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    data = (packed + "\n").encode("ascii")
    return notebook, data


def joined(cell):
    return "".join(cell["source"])


# ---------------------------------------------------------------------------------------------
# Static checks (nothing below executes notebook code)
# ---------------------------------------------------------------------------------------------

ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")
ADDRESS = re.compile(r"(?i)\b[a-z0-9]+://|\bwww\.|\b[a-z0-9-]+\.(?:com|org|net|edu|gov|io|ai|de|ch|uk|cn|fr)\b")
FETCH = re.compile(r"(?i)\b(urllib|requests|wget|curl|gdown|kaggle|kagglehub|load_dataset|urlretrieve|urlopen"
                   r"|snapshot_download|hf_hub_download)\b")
MAGIC = re.compile(r"(?m)^\s*[!%]")


def structure_problems(notebook):
    """Compare the notebook with the nbformat 4.5 layout this script writes."""
    problems = []
    if sorted(notebook) != ["cells", "metadata", "nbformat", "nbformat_minor"]:
        problems.append("top-level keys are not exactly cells, metadata, nbformat, nbformat_minor")
    if notebook.get("nbformat") != 4 or notebook.get("nbformat_minor") != 5:
        problems.append("nbformat is not 4.5")
    kernel = notebook.get("metadata", {}).get("kernelspec", {})
    if not (isinstance(kernel.get("name"), str) and isinstance(kernel.get("display_name"), str)):
        problems.append("kernelspec lacks name or display_name")
    wanted_keys = {"markdown": ["cell_type", "id", "metadata", "source"],
                   "code": ["cell_type", "execution_count", "id", "metadata", "outputs", "source"]}
    seen = set()
    cells = notebook.get("cells", [])
    if not cells:
        problems.append("no cells")
    for index, cell in enumerate(cells):
        where = "cell %d" % index
        kind = cell.get("cell_type")
        if kind not in wanted_keys:
            problems.append(where + ": cell_type is neither markdown nor code")
            continue
        if sorted(cell) != wanted_keys[kind]:
            problems.append(where + ": unexpected or missing keys")
        cell_id = cell.get("id", "")
        if not isinstance(cell_id, str) or not ID_PATTERN.match(cell_id) or cell_id in seen:
            problems.append(where + ": bad or repeated id")
        seen.add(cell_id)
        if not isinstance(cell.get("metadata"), dict):
            problems.append(where + ": metadata is not an object")
        source = cell.get("source")
        if not (isinstance(source, list) and source and all(isinstance(line, str) for line in source)):
            problems.append(where + ": source is not a non-empty list of strings")
            continue
        if any(not line.endswith("\n") or "\n" in line[:-1] for line in source[:-1]) or "\n" in source[-1]:
            problems.append(where + ": source is not split one line per item")
        if not "".join(source).strip():
            problems.append(where + ": empty source")
        if kind == "code" and (cell.get("execution_count") is not None or cell.get("outputs") != []):
            problems.append(where + ": stored output or execution count")
    return problems


def parse_code_cells(notebook, label):
    """ast.parse, then compile, every code cell. Returns (trees, problems, counts)."""
    trees, problems = [], []
    counts = {"code": 0, "parsed": 0, "compiled": 0}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        counts["code"] += 1
        name = "%s#%s" % (label, cell["id"])
        text = joined(cell)
        if MAGIC.search(text):
            problems.append(name + ": line starts with ! or % (not plain Python)")
        try:
            tree = ast.parse(text, filename=name)
        except SyntaxError as error:
            problems.append("%s: ast.parse failed at line %s: %s" % (name, error.lineno, error.msg))
            continue
        counts["parsed"] += 1
        try:
            compile(tree, name, "exec")
        except (SyntaxError, ValueError) as error:
            problems.append("%s: compile failed: %s" % (name, error))
            continue
        counts["compiled"] += 1
        trees.append((cell["id"], tree))
    return trees, problems, counts


def scope_bindings(statements):
    """Names bound in one scope by these statements (function, lambda and comprehension bodies are other scopes)."""
    names, stack = set(), list(statements)
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
            continue
        if isinstance(node, (ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            continue
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.add(node.id)
        elif isinstance(node, ast.alias):
            names.add((node.asname or node.name).split(".")[0])
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
        stack.extend(ast.iter_child_nodes(node))
    return names


def parameters(arguments):
    names = {item.arg for item in arguments.posonlyargs + arguments.args + arguments.kwonlyargs}
    for extra in (arguments.vararg, arguments.kwarg):
        if extra is not None:
            names.add(extra.arg)
    return names


def check_loads(node, visible, cell_names, label, problems):
    """Report every name that is read where no binding makes it visible."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        outer = node.decorator_list + node.args.defaults + [d for d in node.args.kw_defaults if d is not None]
        for sub in outer:
            check_loads(sub, visible, cell_names, label, problems)
        inner = visible | cell_names | parameters(node.args) | scope_bindings(node.body)
        for statement in node.body:
            check_loads(statement, inner, cell_names, label, problems)
    elif isinstance(node, ast.Lambda):
        check_loads(node.body, visible | cell_names | parameters(node.args), cell_names, label, problems)
    elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
        targets = {n.id for gen in node.generators for n in ast.walk(gen.target) if isinstance(n, ast.Name)}
        for child in ast.iter_child_nodes(node):
            check_loads(child, visible | targets, cell_names, label, problems)
    elif isinstance(node, ast.Name):
        if isinstance(node.ctx, ast.Load) and node.id not in visible:
            problems.append("%s: name %r is read at line %d with no earlier binding" % (label, node.id, node.lineno))
    else:
        for child in ast.iter_child_nodes(node):
            check_loads(child, visible, cell_names, label, problems)


def undefined_names(trees):
    """Names read before any binding, taking the cells in notebook order. Returns (problems, names read)."""
    problems, known, reads = [], set(dir(builtins)), 0
    for label, tree in trees:
        reads += sum(1 for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load))
        cell_names = scope_bindings(tree.body)
        seen = set(known)
        for statement in tree.body:
            seen |= scope_bindings([statement])
            check_loads(statement, seen, cell_names, label, problems)
        known |= cell_names
    return problems, reads


def arity_problems(trees):
    """Check calls of functions defined in the notebook: positional count, keyword names, missing arguments.

    Calls with * or ** are skipped. time_call(name, fn, a, b) is also checked as fn(a, b).
    Returns (problems, calls checked).
    """
    defs = {}
    for _, tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defs[node.name] = node.args
    problems, checked = [], 0
    for label, tree in trees:
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in defs):
                continue
            calls = [(node.func.id, node.args, node.keywords)]
            if (node.func.id == "time_call" and len(node.args) >= 2 and isinstance(node.args[1], ast.Name)
                    and node.args[1].id in defs):
                calls.append((node.args[1].id, node.args[2:], []))
            for name, args, keywords in calls:
                if any(isinstance(a, ast.Starred) for a in args) or any(k.arg is None for k in keywords):
                    continue
                checked += 1
                spec = defs[name]
                positional = [item.arg for item in spec.posonlyargs + spec.args]
                keyword_only = [item.arg for item in spec.kwonlyargs]
                where = "%s: call of %s at line %d" % (label, name, node.lineno)
                if len(args) > len(positional) and spec.vararg is None:
                    problems.append(where + ": too many positional arguments")
                given = set(positional[:len(args)])
                for keyword in keywords:
                    if keyword.arg in given:
                        problems.append(where + ": argument %s given twice" % keyword.arg)
                    elif keyword.arg not in positional and keyword.arg not in keyword_only and spec.kwarg is None:
                        problems.append(where + ": unknown keyword %s" % keyword.arg)
                    given.add(keyword.arg)
                required = positional[:len(positional) - len(spec.defaults)]
                required += [item for item, default in zip(keyword_only, spec.kw_defaults) if default is None]
                missing = [item for item in required if item not in given]
                if missing:
                    problems.append(where + ": missing " + ", ".join(missing))
    return problems, checked


def imported_modules(trees):
    modules = set()
    for _, tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[0])
    return modules


def function_defs(trees):
    return [node for _, tree in trees for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def manifest_problems(notebook, trees):
    """Brief rule: every licence cell reads the pending text and every source address cell is empty."""
    problems, code_rows, table_rows = [], 0, 0
    pending_ok = False
    for _, tree in trees:
        for node in tree.body:
            if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
                continue
            target = node.targets[0].id
            if target == "LICENCE_PENDING":
                pending_ok = isinstance(node.value, ast.Constant) and node.value.value == LICENCE_PENDING
            if target != "DATA_MANIFEST":
                continue
            for row in node.value.elts:
                code_rows += 1
                keys = [k.value for k in row.keys]
                if keys != ["dataset", "licence", "source_address", "status"]:
                    problems.append("manifest code row %d: keys are %s" % (code_rows, keys))
                    continue
                licence, address = row.values[1], row.values[2]
                if not (isinstance(licence, ast.Name) and licence.id == "LICENCE_PENDING"):
                    problems.append("manifest code row %d: licence cell is not LICENCE_PENDING" % code_rows)
                if not (isinstance(address, ast.Constant) and address.value == ""):
                    problems.append("manifest code row %d: source address is not empty" % code_rows)
    if not pending_ok:
        problems.append("LICENCE_PENDING is not the text of the brief")
    for cell in notebook["cells"]:
        lines = joined(cell).split("\n")
        if cell["cell_type"] != "markdown" or "| dataset | licence | source address | status |" not in lines:
            continue
        start = lines.index("| dataset | licence | source address | status |") + 2
        for line in lines[start:]:
            if not line.startswith("|"):
                break
            table_rows += 1
            cells = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(cells) != 4:
                problems.append("manifest table row %d: %d cells" % (table_rows, len(cells)))
            elif cells[1] != LICENCE_PENDING:
                problems.append("manifest table row %d: licence cell differs" % table_rows)
            elif cells[2] != "":
                problems.append("manifest table row %d: source address is not empty" % table_rows)
    if code_rows != len(DATASETS) or table_rows != len(DATASETS):
        problems.append("manifest rows: code %d, table %d, expected %d" % (code_rows, table_rows, len(DATASETS)))
    return problems, code_rows, table_rows


def check_notebook(spec, notebook, data):
    """Run every static check. Returns (problems, facts) where facts feed the printed report."""
    label = spec["file"]
    problems = structure_problems(notebook)
    cells = notebook["cells"]
    facts = {"cells": len(cells),
             "markdown": sum(1 for c in cells if c["cell_type"] == "markdown"),
             "code_cells": sum(1 for c in cells if c["cell_type"] == "code"),
             "stored_outputs": sum(1 for c in cells if c["cell_type"] == "code"
                                   and (c.get("outputs") or c.get("execution_count") is not None)),
             "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    trees, parse_problems, counts = parse_code_cells(notebook, label)
    problems += parse_problems
    facts.update(counts)
    name_problems, facts["names_read"] = undefined_names(trees)
    call_problems, facts["calls_checked"] = arity_problems(trees)
    facts["undefined_names"], facts["arity_problems"] = len(name_problems), len(call_problems)
    problems += name_problems + call_problems

    first = cells[0] if cells else {}
    facts["banner"] = first.get("cell_type") == "markdown" and joined(first) == BANNER
    if not facts["banner"]:
        problems.append("first cell is not the banner markdown cell")
    text = "\n".join(joined(c) for c in cells)
    facts["non_ascii"] = sum(1 for ch in text if ord(ch) > 127)
    facts["address_like"] = len(ADDRESS.findall(text))
    facts["fetch_tokens"] = sum(len(FETCH.findall(joined(c))) for c in cells if c["cell_type"] == "code")
    for key, message in (("non_ascii", "non-ASCII characters"), ("address_like", "address-like text"),
                         ("fetch_tokens", "download code tokens")):
        if facts[key]:
            problems.append("%s: %d" % (message, facts[key]))
    if facts["bytes"] > SIZE_LIMIT:
        problems.append("size %d bytes is over the limit of %d" % (facts["bytes"], SIZE_LIMIT))
    modules = imported_modules(trees)
    facts["imports"] = sorted(modules)
    if modules - spec["imports"]:
        problems.append("imports outside the allowed set: " + ", ".join(sorted(modules - spec["imports"])))
    functions = function_defs(trees)
    facts["functions"] = len(functions)
    facts["with_docstring"] = sum(1 for f in functions if ast.get_docstring(f))
    if facts["with_docstring"] != facts["functions"]:
        problems.append("functions without a docstring: %d" % (facts["functions"] - facts["with_docstring"]))

    extra = []
    if spec["tag"] == "nb01":
        rule_problems, code_rows, table_rows = manifest_problems(notebook, trees)
        problems += rule_problems
        extra.append("manifest rows: code %d, table %d; licence cells pending and source addresses empty: %s"
                     % (code_rows, table_rows, "yes" if not rule_problems else "NO"))
        marked = sum(1 for c in cells if c["cell_type"] == "code" and "DOWNLOAD PLACEHOLDER" in joined(c))
        extra.append("download placeholder cells: %d" % marked)
        if marked != 1:
            problems.append("expected exactly one DOWNLOAD PLACEHOLDER code cell")
        if "drive.mount(" not in text or "PROJECT_DIR = " not in text:
            problems.append("Drive mount or PROJECT_DIR assignment is missing")
    else:
        by_name = {f.name: f for f in functions}
        good = [n for n in CUE_FUNCTIONS if n in by_name and "Measures" in (ast.get_docstring(by_name[n]) or "")
                and "Does not show" in (ast.get_docstring(by_name[n]) or "")]
        extra.append("cue functions with a Measures part and a Does not show part: %d of %d"
                     % (len(good), len(CUE_FUNCTIONS)))
        if len(good) != len(CUE_FUNCTIONS):
            problems.append("a cue function or one part of its docstring is missing")
        timing = [joined(c) for c in cells if c["cell_type"] == "code" and joined(c).startswith("# TIMING CELL")]
        timed = [n for n in CUE_FUNCTIONS
                 if sum(1 for t in timing if 'time_call("%s", %s,' % (n, n) in t and "SEED" in t) == 1]
        extra.append("timing cells: %d; cue functions with one seeded timing cell: %d of %d"
                     % (len(timing), len(timed), len(CUE_FUNCTIONS)))
        if len(timing) != len(CUE_FUNCTIONS) or len(timed) != len(CUE_FUNCTIONS):
            problems.append("timing cells do not match the cue functions one to one")
        last_ok = bool(cells) and cells[-1]["cell_type"] == "markdown" and LAST_CELL_TITLE in joined(cells[-1])
        extra.append("last cell is the replacement list: %s" % ("yes" if last_ok else "NO"))
        if not last_ok:
            problems.append("last cell is not the replacement list")
    facts["extra"] = extra
    return problems, facts


def disk_state(path, data):
    """Compare the file on disk with this build. Returns (state, sentence)."""
    if not path.exists():
        return "absent", "not on disk"
    old = path.read_bytes()
    if old == data:
        return "same", "on disk and identical to this build"
    try:
        notebook = json.loads(old.decode("utf-8"))
        pristine = notebook["metadata"]["p2_skeleton"]["cells_sha256"] == cells_digest(notebook["cells"])
    except (ValueError, KeyError, TypeError):
        pristine = False
    if pristine:
        return "old_build", "on disk as an unmodified earlier build that differs from this build"
    return "edited", "on disk but edited or run since it was built; this script never replaces it"


def report(spec, problems, facts, state_text):
    print("[%s]" % spec["file"])
    print("  cells: %d (markdown %d, code %d)" % (facts["cells"], facts["markdown"], facts["code_cells"]))
    print("  bytes: %d (limit %d)" % (facts["bytes"], SIZE_LIMIT))
    print("  ast.parse: %d of %d code cells; compile: %d of %d"
          % (facts["parsed"], facts["code"], facts["compiled"], facts["code"]))
    print("  undefined names: %d (of %d names read); call arity problems: %d (of %d calls checked)"
          % (facts["undefined_names"], facts["names_read"], facts["arity_problems"], facts["calls_checked"]))
    print("  functions: %d, with a docstring: %d" % (facts["functions"], facts["with_docstring"]))
    print("  imports: %s" % ", ".join(facts["imports"]))
    print("  banner first cell: %s; non-ASCII characters: %d; address-like text: %d; download code tokens: %d"
          % ("yes" if facts["banner"] else "NO", facts["non_ascii"], facts["address_like"], facts["fetch_tokens"]))
    for line in facts["extra"]:
        print("  " + line)
    print("  code cells with a stored output or an execution count: %d" % facts["stored_outputs"])
    print("  sha256 of this build: %s" % facts["sha256"])
    print("  disk: %s" % state_text)
    print("  problems: %d" % len(problems))
    for problem in problems:
        print("    - " + problem)


def checker_selftest():
    """Feed small known-good and known-bad snippets to the checkers. Parses only; runs nothing.

    Returns (cases that behaved as expected, cases). A checker that flags nothing here would make
    the zero counts in the report meaningless.
    """
    def scan(*sources):
        trees = [("selftest%d" % index, ast.parse(source)) for index, source in enumerate(sources)]
        return len(undefined_names(trees)[0]), len(arity_problems(trees)[0])

    def syntax_error(source):
        try:
            ast.parse(source)
        except SyntaxError:
            return True
        return False

    good = "import math\n\ndef area(r, scale=1.0):\n    return math.pi * r * r * scale\n\nprint(area(2.0, scale=3.0))\n"
    cases = [
        scan(good) == (0, 0),
        scan("def f(a):\n    return a + missing_name\n")[0] == 1,
        scan("print(later)\n", "later = 1\n")[0] == 1,
        scan("def f():\n    inner = 1\n    return inner\n\nprint(inner)\n")[0] == 1,
        scan("total = [q for q in range(3)]\nprint(q)\n")[0] == 1,
        scan("def g(a, b):\n    return a\n\ng(1)\n")[1] == 1,
        scan("def g(a, b):\n    return a\n\ng(1, 2, 3)\n")[1] == 1,
        scan("def g(a, b):\n    return a\n\ng(1, c=2)\n")[1] == 2,
        scan("def t(name, fn, *args):\n    return fn(*args)\n\ndef g(a, b):\n    return a\n\nt('g', g, 1)\n")[1] == 0,
        scan("def time_call(name, fn, *args):\n    return fn(*args)\n\ndef g(a, b):\n    return a\n\n"
             "time_call('g', g, 1)\n")[1] == 1,
        syntax_error("def h(:\n    pass\n"),
        not syntax_error(good),
        # The next strings are assembled from parts so that this file holds no address-like text itself.
        ADDRESS.search("see " + "ht" + "tps:" + "//" + "host/path") is not None,
        ADDRESS.search("at data" + ".example" + ".org today") is not None,
        ADDRESS.search("np.float32, README.md, google.colab, /content/drive/MyDrive, H // 8") is None,
        FETCH.search("urllib" + ".request." + "urlretrieve(source, target)") is not None,
        FETCH.search("write_hash_manifest(root_dir, out_tsv)") is None,
        MAGIC.search("x = 1\n" + "!" + "ls\n") is not None,
    ]
    return sum(1 for case in cases if case), len(cases)


def main(argv):
    options = argv[1:]
    if any(option != "--check" for option in options):
        print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
        return 2
    check_only = "--check" in options
    print("build_notebooks.py: %s; python %s; nothing is executed" %
          ("check only, no write" if check_only else "build, check, write", sys.version.split()[0]))
    print("build_notebooks.py sha256: %s" % hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
    passed, cases = checker_selftest()
    print("checker self-test: %d of %d cases behave as expected" % (passed, cases))
    if passed != cases:
        print("RESULT: FAIL; the checkers do not behave as expected; nothing written")
        return 1
    results, total_problems = [], 0
    for spec in NOTEBOOKS:
        notebook, data = build(spec)
        problems, facts = check_notebook(spec, notebook, data)
        path = HERE / spec["file"]
        state, state_text = disk_state(path, data)
        report(spec, problems, facts, state_text)
        total_problems += len(problems)
        results.append((spec, path, data, state))
    if total_problems:
        print("RESULT: FAIL (%d problems); nothing written" % total_problems)
        return 1
    if check_only:
        same = sum(1 for _, _, _, state in results if state == "same")
        print("RESULT: PASS (static checks only); notebooks on disk identical to this build: %d of %d; nothing written"
              % (same, len(results)))
        return 0
    if any(state == "edited" for _, _, _, state in results):
        print("RESULT: STOPPED; a notebook on disk was edited or run since it was built; nothing written")
        return 1
    for spec, path, data, state in results:
        if state == "same":
            print("unchanged: %s" % spec["file"])
            continue
        path.write_bytes(data)
        back = path.read_bytes()
        if back != data or json.loads(back.decode("ascii")) != json.loads(data.decode("ascii")):
            print("RESULT: FAIL; read-back of %s differs" % spec["file"])
            return 1
        print("%s: %s (%d bytes, read back identical)"
              % ("written" if state == "absent" else "replaced an unmodified earlier build", spec["file"], len(data)))
    print("RESULT: PASS (static checks only); notebooks written; they were not executed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
