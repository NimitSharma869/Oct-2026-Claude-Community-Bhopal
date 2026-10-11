"""Creates the full Jal Drishti project: backend + frontend + empty data/ folder.

Usage:
    python make_jal_drishti.py                 # creates ./jal-drishti
    python make_jal_drishti.py some/folder     # creates it there
    python make_jal_drishti.py some/folder --force   # overwrite existing files
"""
import sys
from pathlib import Path

FILES = {}

# =====================================================================  BACKEND

FILES["backend/requirements.txt"] = r'''
fastapi>=0.110,<1.0
uvicorn>=0.27
httpx>=0.27
pytest>=8.0
'''

FILES["backend/pytest.ini"] = r'''
[pytest]
testpaths = tests
pythonpath = .
'''

FILES["backend/run.py"] = r'''
"""Start the Jal Drishti server: python run.py  (then open http://localhost:8000/)"""
import os

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Jal Drishti running at http://localhost:{port}/  (API docs at /docs). Press Ctrl+C to stop.")
    uvicorn.run("jal_drishti.api:app", host="127.0.0.1", port=port)
'''

FILES["backend/jal_drishti/__init__.py"] = r'''
"""Jal Drishti backend: Bhopal visarjan-ghat readings compared with CPCB criteria."""
__version__ = "0.1.0"
'''

FILES["backend/jal_drishti/config.py"] = r'''
"""Static configuration. Every value here comes from the track data pack / participant guide."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR_ENV = "JAL_DRISHTI_DATA_DIR"
FRONTEND_DIR_ENV = "JAL_DRISHTI_FRONTEND_DIR"
CORS_ENV = "JAL_DRISHTI_CORS_ORIGINS"
READINGS_FILENAME = "bhopal_ghats_2023_2025.csv"
CRITERIA_FILENAME = "cpcb_water_quality_criteria.csv"


def resolve_data_dir(override: Optional[Union[str, Path]] = None) -> Path:
    if override is not None:
        return Path(override)
    env = os.environ.get(DATA_DIR_ENV)
    return Path(env) if env else REPO_ROOT / "data"


def resolve_frontend_dir() -> Path:
    env = os.environ.get(FRONTEND_DIR_ENV)
    return Path(env) if env else REPO_ROOT / "frontend"


DEFAULT_CPCB_CLASS = "B"  # organised outdoor bathing
PHASES = ("pre", "during", "after")
FESTIVALS = ("Ganesh", "Durga")  # within a year, Ganesh comes before Durga

PHASE_LABELS_EN = {"pre": "before immersion", "during": "during immersion", "after": "one week after immersion"}
PHASE_LABELS_HI = {"pre": "विसर्जन से पहले", "during": "विसर्जन के दौरान", "after": "विसर्जन के एक सप्ताह बाद"}
PHASE_SHORT_EN = {"pre": "before", "during": "during", "after": "after"}
PHASE_SHORT_HI = {"pre": "पहले", "during": "दौरान", "after": "बाद"}
FESTIVAL_LABELS_HI = {"Ganesh": "गणेश", "Durga": "दुर्गा"}

# CPCB criteria-file parameter name -> parameter name used in the readings file.
CRITERIA_TO_DATASET_PARAMETER = {
    "pH": "pH",
    "Dissolved oxygen": "Dissolved oxygen",
    "BOD (5 days 20C)": "BOD",
    "Electrical conductivity at 25C": "Conductivity",  # micromhos/cm == µS/cm
}

PARAMETER_LABELS_EN = {"Dissolved oxygen": "dissolved oxygen", "BOD": "BOD", "pH": "pH", "Conductivity": "conductivity"}
BRIEF_LABELS_EN = {"Dissolved oxygen": "DO", "BOD": "BOD", "pH": "pH", "Conductivity": "Conductivity"}
PARAMETER_LABELS_HI = {"Dissolved oxygen": "घुलित ऑक्सीजन (DO)", "BOD": "BOD", "pH": "pH", "Conductivity": "चालकता"}
BRIEF_LABELS_HI = {"Dissolved oxygen": "DO", "BOD": "BOD", "pH": "pH", "Conductivity": "चालकता"}

CLASS_USE_HI = {
    "A": "बिना पारंपरिक उपचार, कीटाणुशोधन के बाद पेयजल स्रोत",
    "B": "संगठित बाहरी स्नान",
    "C": "पारंपरिक उपचार और कीटाणुशोधन के बाद पेयजल स्रोत",
    "D": "वन्यजीव और मत्स्य पालन",
    "E": "सिंचाई, औद्योगिक शीतलन, नियंत्रित अपशिष्ट निपटान",
}

# Devanagari transliterations of the standard names. Please have a Hindi speaker check them.
SITE_NAMES_HI = {
    "Bairagarh (Sant Hirdaram) kund": "बैरागढ़ (संत हिरदाराम) कुंड",
    "Khatlapura ghat": "खटलापुरा घाट",
    "Prempura ghat": "प्रेमपुरा घाट",
    "Rani Kamlapati ghat / Kamla Park kund": "रानी कमलापति घाट / कमला पार्क कुंड",
    "Hathaikheda dam / kund": "हथाईखेड़ा डैम / कुंड",
    "Malikhedi kund": "मालीखेड़ी कुंड",
    "Shahpura lake ghat": "शाहपुरा झील घाट",
}

SITE_CAVEATS = {
    "Rani Kamlapati ghat / Kamla Park kund": (
        "Site match confidence is medium. Ganesh tables print a 'Kamla Park ... murti visarjan kund' name and "
        "Durga tables print 'Rani Kamlapati visarjan ghat (lower lake)'. These may be two different places, "
        "so readings under this name may mix two locations."
    ),
}
SITE_CAVEATS_HI = {
    "Rani Kamlapati ghat / Kamla Park kund":
        "'रानी कमलापति घाट / कमला पार्क कुंड' दो अलग स्थान हो सकते हैं (नाम मिलान का विश्वास: मध्यम)।",
}

SOURCE_REPORTS = {
    2023: {"title": "MPPCB Idol Immersion Report 2023 (CPCB format)",
           "url": "https://www.mppcb.mp.gov.in/proc/mon/Idol_immer._Report_23_CPCB.pdf"},
    2024: {"title": "MPPCB Ganesh and Durga Visarjan Report 2024",
           "url": "https://www.mppcb.mp.gov.in/proc/mon/Ganesh_and_Durga_visarjan_report-2024.pdf"},
    2025: {"title": "MPPCB Ganesh and Durga Visarjan Report 2025",
           "url": "https://www.mppcb.mp.gov.in/proc/mon/Ganesh_and_Durga_visarjan_report-2025.pdf"},
}
CRITERIA_SOURCE = {"file": f"data/{CRITERIA_FILENAME}", "url": "https://cpcb.gov.in/water-quality-criteria/"}

GLOBAL_CAVEATS = [
    "Units are assumed: the MPPCB reports print no units, so the standard unit for each test is used.",
    "Blank cells, '_', '-', '*', '**' and 'not sampled' mean the reading is missing. Missing readings are never treated as meeting a criterion.",
    "BDL/ND mean below the detection limit: very low, but not zero and not missing. They are not converted to 0.",
    "Only four metals were tested (chromium, lead, zinc, copper). CPCB Class B sets no limit for them, so they are reported but not compared.",
    "Results compare readings with CPCB limits only. They do not describe health effects.",
    "Source pages are PDF page numbers in that year's MPPCB report.",
]
'''

FILES["backend/jal_drishti/models.py"] = r'''
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

Event = Tuple[int, str]                       # (year, festival)
ReadingKey = Tuple[int, str, str, str, str]   # (year, festival, site, phase, parameter)


@dataclass(frozen=True)
class Reading:
    line: int
    year: int
    festival: str
    site: str
    site_id: str
    water_body: str
    phase: str
    parameter: str
    value: Optional[float]
    unit_assumed: str
    flag: str
    value_as_printed: str
    parameter_as_printed: str
    site_as_printed: str
    site_match_confidence: str
    source_page: Optional[int]
    measurement_status: str  # "measured" | "below_detection" | "missing"

    @property
    def key(self) -> ReadingKey:
        return (self.year, self.festival, self.site, self.phase, self.parameter)


@dataclass(frozen=True)
class Criterion:
    cpcb_class: str
    designated_best_use: str
    parameter: str                     # as printed in the criteria CSV
    dataset_parameter: Optional[str]   # matching readings parameter, or None if not measured
    limit_type: str                    # "min" | "max" | "range"
    limit_raw: str
    lower: Optional[float]
    upper: Optional[float]
    unit: str


@dataclass
class SiteInfo:
    name: str
    site_id: str
    water_bodies: Set[str] = field(default_factory=set)
    confidences: Set[str] = field(default_factory=set)
    names_as_printed: Set[str] = field(default_factory=set)
    events: Set[Event] = field(default_factory=set)


@dataclass
class Catalog:
    years: List[int]
    events: List[Event]
    event_parameters: Dict[Event, Set[str]]
    sites: Dict[str, SiteInfo]
    site_ids: Dict[str, str]
    parameters: List[str]
    parameter_units: Dict[str, str]
    classes: List[str]


@dataclass
class Dataset:
    readings: List[Reading]
    criteria: List[Criterion]
    catalog: Catalog
    index: Dict[ReadingKey, Reading]
    readings_path: str
    criteria_path: str
    loaded_at: str
'''

FILES["backend/jal_drishti/data_loader.py"] = r'''
"""Load and validate the CSV source-of-truth files. Fails loudly with useful messages."""
from __future__ import annotations

import csv
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union

from .config import (CRITERIA_FILENAME, CRITERIA_TO_DATASET_PARAMETER, FESTIVALS, PHASES,
                     READINGS_FILENAME)
from .models import Catalog, Criterion, Dataset, Event, Reading, SiteInfo

READINGS_REQUIRED_COLUMNS = (
    "year", "festival", "site", "water_body", "phase", "parameter", "value", "unit_assumed", "flag",
    "value_as_printed", "parameter_as_printed", "site_as_printed", "site_match_confidence", "source_page",
)
CRITERIA_REQUIRED_COLUMNS = ("class", "designated_best_use", "parameter", "limit_type", "limit", "unit")
BELOW_DETECTION_CODES = frozenset({"BDL", "ND"})
MAX_REPORTED_ERRORS = 20
_RANGE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$")


class DataFileError(Exception):
    def __init__(self, message: str, *, path: Optional[str] = None, details: Optional[List[str]] = None):
        super().__init__(message)
        self.message = message
        self.path = path
        self.details = details or []

    def to_dict(self) -> dict:
        return {"message": self.message, "path": self.path, "details": self.details}


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def classify_measurement(value: Optional[float], flag: str, value_as_printed: str) -> str:
    """measured | below_detection (BDL/ND, never zero) | missing (blank, _, -, *, **, not sampled)."""
    if value is not None:
        return "measured"
    codes = {flag.strip().upper(), value_as_printed.strip().upper()}
    if codes & BELOW_DETECTION_CODES:
        return "below_detection"
    return "missing"


def _cell(row: dict, key: str) -> str:
    v = row.get(key)
    return v.strip() if isinstance(v, str) else ""


def _raw(row: dict, key: str) -> str:
    v = row.get(key)
    return v if isinstance(v, str) else ""


def _read_rows(path: Path, required: Sequence[str]) -> List[dict]:
    if not path.is_file():
        raise DataFileError(
            f"Data file not found: {path}. Put it in the data/ folder or set JAL_DRISHTI_DATA_DIR.",
            path=str(path))
    try:
        with path.open(newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            header = [h.strip() for h in (reader.fieldnames or [])]
            missing = [c for c in required if c not in header]
            if missing:
                raise DataFileError(
                    f"{path.name} is missing required column(s): {', '.join(missing)}.",
                    path=str(path), details=[f"found columns: {', '.join(header) or '(none)'}"])
            reader.fieldnames = header
            rows = list(reader)
    except UnicodeDecodeError as exc:
        raise DataFileError(f"{path.name} is not valid UTF-8 text: {exc}", path=str(path)) from exc
    except csv.Error as exc:
        raise DataFileError(f"{path.name} could not be parsed as CSV: {exc}", path=str(path)) from exc
    except OSError as exc:
        raise DataFileError(f"{path.name} could not be read: {exc}", path=str(path)) from exc
    if not rows:
        raise DataFileError(f"{path.name} has a header but no data rows.", path=str(path))
    return rows


def _parse_reading(line: int, row: dict) -> Reading:
    year_text = _cell(row, "year")
    try:
        year = int(year_text)
    except ValueError:
        raise ValueError(f"year {year_text!r} is not a whole number") from None
    festival_text = _cell(row, "festival")
    festival = next((f for f in FESTIVALS if f.lower() == festival_text.lower()), None)
    if festival is None:
        raise ValueError(f"festival {festival_text!r} is not one of {', '.join(FESTIVALS)}")
    phase = _cell(row, "phase").lower()
    if phase not in PHASES:
        raise ValueError(f"phase {phase!r} is not one of {', '.join(PHASES)}")
    site = _cell(row, "site")
    if not site or not slugify(site):
        raise ValueError("site is empty")
    parameter = _cell(row, "parameter")
    if not parameter:
        raise ValueError("parameter is empty")

    value_text = _cell(row, "value")
    value: Optional[float] = None
    if value_text:
        try:
            value = float(value_text)
        except ValueError:
            raise ValueError(f"value {value_text!r} is not a number") from None
        if not math.isfinite(value):
            raise ValueError(f"value {value_text!r} is not a finite number")

    page_text = _cell(row, "source_page")
    page: Optional[int] = None
    if page_text:
        try:
            page_f = float(page_text)
        except ValueError:
            raise ValueError(f"source_page {page_text!r} is not a number") from None
        if page_f < 1 or page_f != int(page_f):
            raise ValueError(f"source_page {page_text!r} is not a positive whole number")
        page = int(page_f)

    flag = _cell(row, "flag")
    printed = _raw(row, "value_as_printed")  # preserved exactly
    return Reading(
        line=line, year=year, festival=festival, site=site, site_id=slugify(site),
        water_body=_cell(row, "water_body"), phase=phase, parameter=parameter, value=value,
        unit_assumed=_cell(row, "unit_assumed"), flag=flag, value_as_printed=printed,
        parameter_as_printed=_raw(row, "parameter_as_printed"), site_as_printed=_raw(row, "site_as_printed"),
        site_match_confidence=_cell(row, "site_match_confidence").lower(), source_page=page,
        measurement_status=classify_measurement(value, flag, printed),
    )


def load_readings(path: Path) -> List[Reading]:
    rows = _read_rows(path, READINGS_REQUIRED_COLUMNS)
    readings, errors = [], []
    for line, row in enumerate(rows, start=2):  # line 1 is the header
        try:
            readings.append(_parse_reading(line, row))
        except ValueError as exc:
            errors.append(f"line {line}: {exc}")
    if errors:
        raise DataFileError(f"{len(errors)} malformed row(s) in {path.name}.", path=str(path),
                            details=errors[:MAX_REPORTED_ERRORS])
    return readings


def _parse_criterion(row: dict) -> Criterion:
    cls = _cell(row, "class").upper()
    if not cls:
        raise ValueError("class is empty")
    param = _cell(row, "parameter")
    if not param:
        raise ValueError("parameter is empty")
    limit_type = _cell(row, "limit_type").lower()
    limit = _cell(row, "limit")
    lower = upper = None
    if limit_type in ("min", "max"):
        try:
            v = float(limit)
        except ValueError:
            raise ValueError(f"limit {limit!r} is not a number") from None
        lower, upper = (v, None) if limit_type == "min" else (None, v)
    elif limit_type == "range":
        m = _RANGE_RE.match(limit)
        if not m:
            raise ValueError(f"range limit {limit!r} is not in 'low-high' form")
        lower, upper = float(m.group(1)), float(m.group(2))
        if lower >= upper:
            raise ValueError(f"range limit {limit!r} has low >= high")
    else:
        raise ValueError(f"limit_type {limit_type!r} must be min, max or range")
    return Criterion(cpcb_class=cls, designated_best_use=_cell(row, "designated_best_use"), parameter=param,
                     dataset_parameter=CRITERIA_TO_DATASET_PARAMETER.get(param), limit_type=limit_type,
                     limit_raw=limit, lower=lower, upper=upper, unit=_cell(row, "unit"))


def load_criteria(path: Path) -> List[Criterion]:
    rows = _read_rows(path, CRITERIA_REQUIRED_COLUMNS)
    out, errors, seen = [], [], {}
    for line, row in enumerate(rows, start=2):
        try:
            c = _parse_criterion(row)
        except ValueError as exc:
            errors.append(f"line {line}: {exc}")
            continue
        key = (c.cpcb_class, c.parameter)
        if key in seen:
            errors.append(f"line {line}: duplicate criterion for class {c.cpcb_class} {c.parameter} (first at line {seen[key]})")
            continue
        seen[key] = line
        out.append(c)
    if errors:
        raise DataFileError(f"{len(errors)} malformed row(s) in {path.name}.", path=str(path),
                            details=errors[:MAX_REPORTED_ERRORS])
    return out


def _event_key(e: Event):
    return (e[0], FESTIVALS.index(e[1]))


def build_catalog(readings: List[Reading], criteria: List[Criterion]) -> Catalog:
    sites: Dict[str, SiteInfo] = {}
    event_params: Dict[Event, set] = {}
    param_order: List[str] = []
    units: Dict[str, str] = {}
    for r in readings:
        info = sites.setdefault(r.site, SiteInfo(name=r.site, site_id=r.site_id))
        info.water_bodies.add(r.water_body)
        info.confidences.add(r.site_match_confidence)
        info.names_as_printed.add(r.site_as_printed)
        info.events.add((r.year, r.festival))
        event_params.setdefault((r.year, r.festival), set()).add(r.parameter)
        if r.parameter not in units:
            param_order.append(r.parameter)
            units[r.parameter] = r.unit_assumed
        elif not units[r.parameter] and r.unit_assumed:
            units[r.parameter] = r.unit_assumed
    sites = dict(sorted(sites.items()))
    site_ids: Dict[str, str] = {}
    for name, info in sites.items():
        if info.site_id in site_ids:
            raise DataFileError(f"Site names {site_ids[info.site_id]!r} and {name!r} produce the same id {info.site_id!r}.")
        site_ids[info.site_id] = name
    events = sorted(event_params, key=_event_key)
    return Catalog(years=sorted({y for y, _ in events}), events=events, event_parameters=event_params,
                   sites=sites, site_ids=site_ids, parameters=param_order, parameter_units=units,
                   classes=sorted({c.cpcb_class for c in criteria}))


def build_dataset(readings: List[Reading], criteria: List[Criterion],
                  readings_path: str = "", criteria_path: str = "") -> Dataset:
    index = {}
    for r in readings:
        if r.key in index:
            raise DataFileError(f"Duplicate reading for {r.key} at lines {index[r.key].line} and {r.line}.",
                                path=readings_path or None)
        index[r.key] = r
    return Dataset(readings=list(readings), criteria=list(criteria), catalog=build_catalog(readings, criteria),
                   index=index, readings_path=readings_path, criteria_path=criteria_path,
                   loaded_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))


def load_dataset(data_dir: Union[str, Path]) -> Dataset:
    d = Path(data_dir)
    rp, cp = d / READINGS_FILENAME, d / CRITERIA_FILENAME
    return build_dataset(load_readings(rp), load_criteria(cp), str(rp), str(cp))
'''

FILES["backend/jal_drishti/store.py"] = r'''
import threading
from pathlib import Path
from typing import Optional, Union

from .config import resolve_data_dir
from .data_loader import load_dataset
from .models import Dataset


class DataStore:
    """Loads the CSVs lazily, once. A failed load is retried on the next request (fix the file, no restart)."""

    def __init__(self, data_dir: Optional[Union[str, Path]] = None):
        self.data_dir: Path = resolve_data_dir(data_dir)
        self._dataset: Optional[Dataset] = None
        self._lock = threading.Lock()

    def get(self) -> Dataset:
        ds = self._dataset
        if ds is not None:
            return ds
        with self._lock:
            if self._dataset is None:
                self._dataset = load_dataset(self.data_dir)
            return self._dataset

    def reload(self) -> Dataset:
        with self._lock:
            self._dataset = None
        return self.get()
'''

FILES["backend/jal_drishti/filters.py"] = r'''
"""Query-filter parsing and validation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Iterable, List, Mapping, Optional

from .config import DEFAULT_CPCB_CLASS, FESTIVALS, PHASES
from .data_loader import slugify
from .models import Catalog, Reading

FILTER_FIELDS = ("year", "festival", "phase", "site", "parameter")


class FilterError(ValueError):
    def __init__(self, field: str, message: str, allowed: Optional[list] = None):
        super().__init__(message)
        self.field, self.message, self.allowed = field, message, allowed

    def to_dict(self) -> dict:
        d = {"field": self.field}
        if self.allowed is not None:
            d["allowed"] = self.allowed
        return d


@dataclass(frozen=True)
class Filters:
    years: Optional[FrozenSet[int]] = None
    festivals: Optional[FrozenSet[str]] = None
    phases: Optional[FrozenSet[str]] = None
    sites: Optional[FrozenSet[str]] = None
    parameters: Optional[FrozenSet[str]] = None

    def matches_event(self, year: int, festival: str) -> bool:
        return (self.years is None or year in self.years) and (self.festivals is None or festival in self.festivals)

    def matches(self, r: Reading) -> bool:
        return (self.matches_event(r.year, r.festival)
                and (self.phases is None or r.phase in self.phases)
                and (self.sites is None or r.site in self.sites)
                and (self.parameters is None or r.parameter in self.parameters))

    def with_sites(self, sites: Iterable[str]) -> "Filters":
        return Filters(self.years, self.festivals, self.phases, frozenset(sites), self.parameters)

    def as_dict(self) -> dict:
        def s(v, key=None):
            return None if v is None else sorted(v, key=key)
        return {"year": s(self.years), "festival": s(self.festivals, FESTIVALS.index),
                "phase": s(self.phases, PHASES.index), "site": s(self.sites), "parameter": s(self.parameters)}


def split_values(raw: Optional[str]) -> List[str]:
    return [] if raw is None else [p.strip() for p in raw.split(",") if p.strip()]


def resolve_site(token: str, catalog: Catalog) -> Optional[str]:
    t = token.strip()
    for name in catalog.sites:
        if name.lower() == t.lower():
            return name
    return catalog.site_ids.get(slugify(t))


def parse_filters(raw: Mapping[str, Optional[str]], catalog: Catalog,
                  allowed_fields: Iterable[str] = FILTER_FIELDS) -> Filters:
    allowed_fields = set(allowed_fields)
    years = festivals = phases = sites = params = None

    if "year" in allowed_fields and split_values(raw.get("year")):
        out = set()
        for v in split_values(raw.get("year")):
            try:
                y = int(v)
            except ValueError:
                raise FilterError("year", f"year must be a whole number such as 2024; got {v!r}.", catalog.years) from None
            if y not in catalog.years:
                raise FilterError("year", f"No readings for year {y}.", catalog.years)
            out.add(y)
        years = frozenset(out)

    if "festival" in allowed_fields and split_values(raw.get("festival")):
        present = [f for f in FESTIVALS if any(e[1] == f for e in catalog.events)]
        out = set()
        for v in split_values(raw.get("festival")):
            match = next((f for f in present if f.lower() == v.lower()), None)
            if match is None:
                raise FilterError("festival", f"Unknown festival {v!r}.", present)
            out.add(match)
        festivals = frozenset(out)

    if "phase" in allowed_fields and split_values(raw.get("phase")):
        out = set()
        for v in split_values(raw.get("phase")):
            if v.lower() not in PHASES:
                raise FilterError("phase", f"Unknown phase {v!r}. Use pre (before), during or after (one week after).", list(PHASES))
            out.add(v.lower())
        phases = frozenset(out)

    if "site" in allowed_fields and split_values(raw.get("site")):
        out = set()
        for v in split_values(raw.get("site")):
            name = resolve_site(v, catalog)
            if name is None:
                raise FilterError("site", f"Unknown ghat {v!r}. Use a name or id from /api/ghats.",
                                  [{"site": n, "site_id": i.site_id} for n, i in catalog.sites.items()])
            out.add(name)
        sites = frozenset(out)

    if "parameter" in allowed_fields and split_values(raw.get("parameter")):
        out = set()
        for v in split_values(raw.get("parameter")):
            match = next((p for p in catalog.parameters if p.lower() == v.lower() or slugify(p) == slugify(v)), None)
            if match is None:
                raise FilterError("parameter", f"Unknown parameter {v!r}.", catalog.parameters)
            out.add(match)
        params = frozenset(out)

    return Filters(years, festivals, phases, sites, params)


def parse_cpcb_class(raw: Optional[str], classes: List[str], default: Optional[str] = DEFAULT_CPCB_CLASS) -> Optional[str]:
    vals = split_values(raw)
    if not vals:
        return default
    if len(vals) > 1:
        raise FilterError("cpcb_class", "Give one CPCB class, e.g. B.", classes)
    v = vals[0].upper()
    if v not in classes:
        raise FilterError("cpcb_class", f"Unknown CPCB class {vals[0]!r}.", classes)
    return v


def parse_int(raw: Optional[str], field: str, default: int, minimum: int, maximum: Optional[int]) -> int:
    if raw is None or not raw.strip():
        return default
    try:
        v = int(raw.strip())
    except ValueError:
        raise FilterError(field, f"{field} must be a whole number; got {raw!r}.") from None
    if v < minimum or (maximum is not None and v > maximum):
        rng = f"{minimum}–{maximum}" if maximum is not None else f">= {minimum}"
        raise FilterError(field, f"{field} must be in {rng}; got {v}.")
    return v
'''

FILES["backend/jal_drishti/criteria.py"] = r'''
"""Direction-aware comparison of readings with CPCB criteria."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from .models import Criterion, Reading

MEETS, FAILS, MISSING, NOT_COMPARED, NO_CRITERION = "meets", "does_not_meet", "missing", "not_compared", "no_criterion"


def fmt(x: float) -> str:
    return f"{x:g}"


def unit_suffix(unit: str) -> str:
    return f" {unit}" if unit else ""


def available_classes(criteria: Iterable[Criterion]) -> List[str]:
    return sorted({c.cpcb_class for c in criteria})


def criteria_for_class(criteria: Iterable[Criterion], cls: str) -> List[Criterion]:
    return [c for c in criteria if c.cpcb_class == cls]


def criteria_map(criteria: Iterable[Criterion], cls: str, measured_parameters: Iterable[str]) -> Dict[str, Criterion]:
    """dataset parameter -> criterion, only for criteria whose parameter was actually measured."""
    measured = set(measured_parameters)
    return {c.dataset_parameter: c for c in criteria_for_class(criteria, cls) if c.dataset_parameter in measured}


def limit_text(c: Criterion) -> str:
    u = unit_suffix(c.unit)
    if c.limit_type == "min":
        return f"minimum of {fmt(c.lower)}{u}"
    if c.limit_type == "max":
        return f"maximum of {fmt(c.upper)}{u}"
    return f"range of {fmt(c.lower)}–{fmt(c.upper)}{u}"


def limit_phrase(c: Criterion) -> str:
    return f"Class {c.cpcb_class} {limit_text(c)}"


def criterion_to_dict(c: Criterion) -> dict:
    return {"cpcb_class": c.cpcb_class, "designated_best_use": c.designated_best_use, "parameter": c.parameter,
            "dataset_parameter": c.dataset_parameter, "limit_type": c.limit_type, "limit": c.limit_raw,
            "lower": c.lower, "upper": c.upper, "unit": c.unit or None, "description": limit_phrase(c)}


def severity_scale(c: Criterion) -> float:
    if c.limit_type == "min":
        return c.lower
    if c.limit_type == "max":
        return c.upper
    return (c.upper - c.lower) / 2


@dataclass(frozen=True)
class Comparison:
    status: str
    criterion: Optional[Criterion]
    explanation: str
    deviation: Optional[str] = None   # below_min | above_max | below_range | above_range
    gap: Optional[float] = None
    severity: Optional[float] = None  # min(gap / scale, 1)

    def to_dict(self) -> dict:
        d = {"status": self.status, "explanation": self.explanation}
        if self.criterion is not None:
            c = self.criterion
            d["criterion"] = {"cpcb_class": c.cpcb_class, "limit_type": c.limit_type, "limit": c.limit_raw,
                              "unit": c.unit or None}
        if self.status == FAILS:
            d.update(deviation=self.deviation, gap=round(self.gap, 4), severity=round(self.severity, 3))
        return d


def compare(reading: Reading, c: Criterion) -> Comparison:
    p = reading.parameter
    if reading.measurement_status == "missing":
        return Comparison(MISSING, c, f"{p}: not sampled / no value in the report. Not counted as meeting or failing the {limit_phrase(c)}.")
    if reading.measurement_status == "below_detection":
        return Comparison(NOT_COMPARED, c, f"{p}: reported below detection limit ({reading.value_as_printed.strip() or reading.flag}). The detection limit is not stated, so it is not compared.")
    v = reading.value
    shown = f"{p} {fmt(v)}{unit_suffix(reading.unit_assumed)}"
    phrase = limit_phrase(c)
    if c.limit_type == "min":
        if v >= c.lower:
            return Comparison(MEETS, c, f"{shown} is at or above the {phrase} (meets the criterion).")
        gap, dev, text = c.lower - v, "below_min", f"{shown} is below the {phrase}."
    elif c.limit_type == "max":
        if v <= c.upper:
            return Comparison(MEETS, c, f"{shown} is at or below the {phrase} (meets the criterion).")
        gap, dev, text = v - c.upper, "above_max", f"{shown} exceeds the {phrase}."
    else:
        if c.lower <= v <= c.upper:
            return Comparison(MEETS, c, f"{shown} is within the {phrase} (meets the criterion).")
        if v < c.lower:
            gap, dev, text = c.lower - v, "below_range", f"{shown} is below the {phrase}."
        else:
            gap, dev, text = v - c.upper, "above_range", f"{shown} is above the {phrase}."
    scale = severity_scale(c)
    severity = min(gap / scale, 1.0) if scale > 0 else 1.0
    return Comparison(FAILS, c, text, dev, gap, severity)


def no_criterion(reading: Reading, cls: str) -> Comparison:
    return Comparison(NO_CRITERION, None, f"CPCB Class {cls} sets no limit for {reading.parameter}; the value is reported without comparison.")


def compare_with_class(reading: Reading, cmap: Dict[str, Criterion], cls: str) -> Comparison:
    c = cmap.get(reading.parameter)
    return compare(reading, c) if c else no_criterion(reading, cls)
'''

FILES["backend/jal_drishti/serializers.py"] = r'''
from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, List, Optional

from .config import (GLOBAL_CAVEATS, PHASE_LABELS_EN, READINGS_FILENAME, SITE_CAVEATS,
                     SITE_NAMES_HI, SOURCE_REPORTS)
from .criteria import compare_with_class
from .models import Criterion, Dataset, Reading


def source_ref(r: Reading) -> dict:
    rep = SOURCE_REPORTS.get(r.year, {})
    return {"report": rep.get("title"), "url": rep.get("url"), "page": r.source_page,
            "csv_file": f"data/{READINGS_FILENAME}", "csv_line": r.line}


def reading_to_dict(r: Reading, comparison: Optional[dict] = None) -> dict:
    return {
        "year": r.year, "festival": r.festival, "site": r.site, "site_id": r.site_id, "water_body": r.water_body,
        "phase": r.phase, "phase_label": PHASE_LABELS_EN[r.phase], "parameter": r.parameter,
        "value": r.value, "unit_assumed": r.unit_assumed or None, "unit_is_assumed": True,
        "measurement_status": r.measurement_status, "flag": r.flag or None,
        "value_as_printed": r.value_as_printed, "parameter_as_printed": r.parameter_as_printed,
        "site_as_printed": r.site_as_printed, "site_match_confidence": r.site_match_confidence,
        "source": source_ref(r), "comparison": comparison,
    }


def reading_with_comparison(r: Reading, cmap: Dict[str, Criterion], cls: str) -> dict:
    return reading_to_dict(r, compare_with_class(r, cmap, cls).to_dict())


def site_caveats(ds: Dataset, site: str) -> List[str]:
    info = ds.catalog.sites[site]
    out = []
    if site in SITE_CAVEATS:
        out.append(SITE_CAVEATS[site])
    elif "medium" in info.confidences:
        out.append("Site match confidence is medium: the standard name may not map cleanly to one place.")
    for y, f in ds.catalog.events:
        if (y, f) not in info.events:
            out.append(f"No {f} {y} table for this ghat in the report: those readings are missing, not clean.")
    return out


def caveats_for(ds: Dataset, sites: Iterable[str]) -> List[str]:
    out = list(GLOBAL_CAVEATS)
    for s in sites:
        out.extend(f"{s}: {c}" for c in site_caveats(ds, s))
    return out


def ghat_info(ds: Dataset, site: str) -> dict:
    info = ds.catalog.sites[site]
    rows = [r for r in ds.readings if r.site == site]
    counts = Counter(r.measurement_status for r in rows)
    ev = lambda e: {"year": e[0], "festival": e[1]}
    return {
        "site": site, "site_id": info.site_id, "name_hi": SITE_NAMES_HI.get(site, site),
        "water_body": ", ".join(sorted(info.water_bodies)),
        "site_match_confidence": ", ".join(sorted(info.confidences)),
        "names_as_printed": sorted(info.names_as_printed),
        "events_with_table": [ev(e) for e in ds.catalog.events if e in info.events],
        "events_without_table": [ev(e) for e in ds.catalog.events if e not in info.events],
        "reading_counts": {"rows": len(rows), "measured": counts["measured"],
                           "below_detection": counts["below_detection"], "missing": counts["missing"]},
        "caveats": site_caveats(ds, site),
    }
'''

FILES["backend/jal_drishti/coverage.py"] = r'''
"""Expected-reading grid and missing-data accounting.

A slot is one (event, phase, parameter) that the report's table for that event covers (the parameter was
reported for at least one ghat in that event). For each ghat a slot is:
  measured | below_detection | not_sampled (row present, no value)
  | no_table_for_site (ghat has no table for that event) | row_absent (ghat has a table but not this row)
"""
from __future__ import annotations

from collections import Counter, OrderedDict
from dataclasses import dataclass
from typing import Iterable, List, Optional

from .config import PHASES
from .filters import Filters
from .models import Dataset, Event, Reading

MEASURED, BDL, NOT_SAMPLED, NO_TABLE, ROW_ABSENT = "measured", "below_detection", "not_sampled", "no_table_for_site", "row_absent"
MISSING_STATUSES = (NOT_SAMPLED, NO_TABLE, ROW_ABSENT)
MISSING_REASONS_EN = {NOT_SAMPLED: "not sampled", NO_TABLE: "no table for this ghat in the report",
                      ROW_ABSENT: "not printed in the report table"}


@dataclass(frozen=True)
class Slot:
    year: int
    festival: str
    phase: str
    parameter: str
    status: str
    reading: Optional[Reading]

    @property
    def event(self) -> Event:
        return (self.year, self.festival)


def scope_events(ds: Dataset, f: Filters) -> List[Event]:
    return [e for e in ds.catalog.events if f.matches_event(*e)]


def scope_phases(f: Filters) -> List[str]:
    return [p for p in PHASES if f.phases is None or p in f.phases]


def scope_parameters(ds: Dataset, f: Filters, restrict: Optional[Iterable[str]] = None) -> List[str]:
    r = None if restrict is None else set(restrict)
    return [p for p in ds.catalog.parameters
            if (f.parameters is None or p in f.parameters) and (r is None or p in r)]


def scope_sites(ds: Dataset, f: Filters) -> List[str]:
    return [s for s in ds.catalog.sites if f.sites is None or s in f.sites]


def site_slots(ds: Dataset, site: str, events: List[Event], phases: List[str], params: List[str]) -> List[Slot]:
    info = ds.catalog.sites[site]
    slots = []
    for (year, fest) in events:
        has_table = (year, fest) in info.events
        reported = ds.catalog.event_parameters.get((year, fest), set())
        for phase in phases:
            for p in params:
                if p not in reported:
                    continue  # parameter not in that event's tables at all (e.g. suspended solids, Durga 2023)
                r = ds.index.get((year, fest, site, phase, p))
                if r is None:
                    status = ROW_ABSENT if has_table else NO_TABLE
                elif r.measurement_status == "missing":
                    status = NOT_SAMPLED
                else:
                    status = r.measurement_status
                slots.append(Slot(year, fest, phase, p, status, r))
    return slots


def coverage_level(reported: int, expected: int) -> str:
    if expected == 0 or reported == 0:
        return "none"
    ratio = reported / expected
    return "high" if ratio >= 0.9 else "medium" if ratio >= 0.6 else "low"


def summarize_slots(slots: List[Slot]) -> dict:
    c = Counter(s.status for s in slots)
    expected = len(slots)
    reported = c[MEASURED] + c[BDL]
    return {"expected_readings": expected, "reported_readings": reported, "measured": c[MEASURED],
            "below_detection": c[BDL], "missing": expected - reported,
            "missing_breakdown": {k: c[k] for k in MISSING_STATUSES},
            "coverage_ratio": round(reported / expected, 3) if expected else None,
            "coverage_level": coverage_level(reported, expected)}


def event_breakdown(slots: List[Slot]) -> List[dict]:
    groups = OrderedDict()
    for s in slots:
        groups.setdefault(s.event, []).append(s)
    out = []
    for (year, fest), ev in groups.items():
        summ = summarize_slots(ev)
        if all(s.status == NO_TABLE for s in ev):
            status = "no_table_in_report"
        elif summ["missing"] == 0:
            status = "complete"
        elif summ["reported_readings"] == 0:
            status = "none_reported"
        else:
            status = "partial"
        entry = {"year": year, "festival": fest, "status": status, **summ}
        if status == "no_table_in_report":
            entry["note"] = f"No {fest} {year} table for this ghat in the report. Missing, not clean."
        else:
            entry["missing_slots"] = [{"phase": s.phase, "parameter": s.parameter, "reason": s.status}
                                      for s in ev if s.status in MISSING_STATUSES]
        out.append(entry)
    return out


def site_coverage(ds: Dataset, site: str, f: Filters) -> dict:
    slots = site_slots(ds, site, scope_events(ds, f), scope_phases(f), scope_parameters(ds, f))
    return {**summarize_slots(slots), "events": event_breakdown(slots)}


def build_coverage(ds: Dataset, f: Filters) -> dict:
    events, phases, params = scope_events(ds, f), scope_phases(f), scope_parameters(ds, f)
    sites_out, all_slots = [], []
    for site in scope_sites(ds, f):
        slots = site_slots(ds, site, events, phases, params)
        all_slots.extend(slots)
        info = ds.catalog.sites[site]
        sites_out.append({"site": site, "site_id": info.site_id,
                          "water_body": ", ".join(sorted(info.water_bodies)),
                          "site_match_confidence": ", ".join(sorted(info.confidences)),
                          **summarize_slots(slots), "events": event_breakdown(slots)})
    return {"scope": {"events": [{"year": y, "festival": fe} for y, fe in events], "phases": phases,
                      "parameters": params},
            "totals": summarize_slots(all_slots), "sites": sites_out}
'''

FILES["backend/jal_drishti/ranking.py"] = r'''
"""Deterministic, explainable ghat ranking. See README 'Ranking method'."""
from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .config import FESTIVALS, PHASE_LABELS_EN, PHASES, SITE_NAMES_HI
from .coverage import (BDL, MISSING_REASONS_EN, MISSING_STATUSES, Slot, coverage_level, scope_events,
                       scope_parameters, scope_phases, scope_sites, site_slots)
from .criteria import (FAILS, MEETS, NOT_COMPARED, Comparison, compare, criteria_for_class, criteria_map,
                       criterion_to_dict, fmt, limit_phrase, unit_suffix)
from .filters import FilterError, Filters
from .models import Criterion, Dataset, Event, Reading
from .serializers import reading_to_dict, site_caveats

EVIDENCE_LIMIT = 5


def _chron(r: Reading):
    return (r.year, FESTIVALS.index(r.festival), PHASES.index(r.phase))


def _badness(v: float, c: Criterion) -> float:
    if c.limit_type == "min":
        return -v
    if c.limit_type == "max":
        return v
    return abs(v - (c.lower + c.upper) / 2)


@dataclass
class ParamStats:
    parameter: str
    criterion: Criterion
    expected: int = 0
    compared: int = 0
    meets: int = 0
    does_not_meet: int = 0
    not_compared: int = 0
    missing: int = 0
    points: float = 0.0
    max_severity: float = 0.0
    items: List[Tuple[Reading, Comparison]] = field(default_factory=list)

    @property
    def worst(self) -> Optional[Tuple[Reading, Comparison]]:
        if not self.items:
            return None
        return sorted(self.items, key=lambda it: (-_badness(it[0].value, self.criterion), _chron(it[0])))[0]

    @property
    def failures(self) -> List[Tuple[Reading, Comparison]]:
        return [it for it in self.items if it[1].status == FAILS]


@dataclass
class SiteAssessment:
    site: str
    site_id: str
    stats: List[ParamStats]
    slots: List[Slot]
    rank: Optional[int] = None

    compared = property(lambda s: sum(p.compared for p in s.stats))
    expected = property(lambda s: sum(p.expected for p in s.stats))
    does_not_meet = property(lambda s: sum(p.does_not_meet for p in s.stats))
    not_compared = property(lambda s: sum(p.not_compared for p in s.stats))
    missing = property(lambda s: sum(p.missing for p in s.stats))
    points = property(lambda s: sum(p.points for p in s.stats))
    max_severity = property(lambda s: max([p.max_severity for p in s.stats] or [0.0]))

    @property
    def score(self) -> Optional[float]:
        return self.points / self.compared if self.compared else None

    @property
    def coverage_level(self) -> str:
        return coverage_level(self.compared, self.expected)


@dataclass
class RankingResult:
    cpcb_class: str
    criteria: List[Criterion]
    events: List[Event]
    phases: List[str]
    assessments: List[SiteAssessment]


def assess_site(ds: Dataset, site: str, events, phases, params, cmap: Dict[str, Criterion]) -> SiteAssessment:
    slots = site_slots(ds, site, events, phases, params)
    stats = OrderedDict((p, ParamStats(p, cmap[p])) for p in params)
    for s in slots:
        st = stats[s.parameter]
        st.expected += 1
        if s.reading is None or s.reading.measurement_status == "missing":
            st.missing += 1
            continue
        cmp = compare(s.reading, st.criterion)
        if cmp.status == NOT_COMPARED:
            st.not_compared += 1
            continue
        st.compared += 1
        st.items.append((s.reading, cmp))
        if cmp.status == MEETS:
            st.meets += 1
        else:
            st.does_not_meet += 1
            st.points += 1.0 + cmp.severity
            st.max_severity = max(st.max_severity, cmp.severity)
    return SiteAssessment(site, ds.catalog.sites[site].site_id, list(stats.values()), slots)


def _ranking_scope(ds: Dataset, f: Filters, cls: str):
    cmap = criteria_map(ds.criteria, cls, ds.catalog.parameters)
    params = scope_parameters(ds, f, restrict=cmap)
    return cmap, params


def rank_ghats(ds: Dataset, f: Filters, cls: str) -> RankingResult:
    cmap, params = _ranking_scope(ds, f, cls)
    if not params:
        raise FilterError("parameter", f"None of the selected parameters has a CPCB Class {cls} criterion, so there is nothing to rank.",
                          sorted(cmap))
    events, phases = scope_events(ds, f), scope_phases(f)
    assessments = [assess_site(ds, s, events, phases, params, cmap) for s in scope_sites(ds, f)]
    ranked = sorted((a for a in assessments if a.score is not None),
                    key=lambda a: (-round(a.score, 9), -a.does_not_meet, -round(a.max_severity, 9), a.site))
    unranked = sorted((a for a in assessments if a.score is None), key=lambda a: a.site)
    for i, a in enumerate(ranked, start=1):
        a.rank = i
    return RankingResult(cls, [cmap[p] for p in params], events, phases, ranked + unranked)


# ---------- explanation ----------

def event_text(r: Reading) -> str:
    return f"{r.festival} {r.year}, {PHASE_LABELS_EN[r.phase]}, report p. {r.source_page}"


def param_reason(st: ParamStats) -> str:
    c, label, phrase = st.criterion, st.parameter, limit_phrase(st.criterion)
    if st.compared == 0:
        return f"{label}: no measured readings in this selection ({st.missing} missing), so it could not be compared with the {phrase}."
    if st.does_not_meet == 0:
        return f"{label} met the {phrase} in all {st.compared} measured readings."
    r, _ = st.worst
    verb = {"min": "was below", "max": "was above", "range": "was outside"}[c.limit_type]
    word = {"min": "lowest", "max": "highest", "range": "furthest from the range"}[c.limit_type]
    return (f"{label} {verb} the {phrase} in {st.does_not_meet} of {st.compared} measured readings; "
            f"{word} {fmt(r.value)}{unit_suffix(r.unit_assumed)} ({event_text(r)}).")


def missing_groups(a: SiteAssessment) -> List[dict]:
    groups = OrderedDict()
    for s in a.slots:
        if s.status in MISSING_STATUSES or s.status == BDL:
            key = (s.year, s.festival, s.status)
            groups[key] = groups.get(key, 0) + 1
    return [{"year": y, "festival": f, "reason": st, "count": n} for (y, f, st), n in groups.items()]


def coverage_reason(a: SiteAssessment) -> str:
    if a.expected == 0:
        return "No readings were expected for this selection."
    text = f"Assessed on {a.compared} of {a.expected} expected readings ({round(100 * a.compared / a.expected)}%)."
    parts = [f"{g['festival']} {g['year']}: "
             f"{MISSING_REASONS_EN.get(g['reason'], 'below detection, not compared')} ({g['count']})"
             for g in missing_groups(a)]
    if parts:
        text += " Not compared: " + "; ".join(parts) + "."
    if a.coverage_level in ("medium", "low"):
        text += " With fewer readings the result is less certain; missing readings are not treated as meeting the criteria."
    return text


def reasons(a: SiteAssessment) -> List[str]:
    if a.score is None:
        return ["No comparable readings in this selection. This ghat is not ranked; that is not evidence that its water meets the criteria.",
                coverage_reason(a)]
    failing = sorted((s for s in a.stats if s.does_not_meet), key=lambda s: -s.does_not_meet)
    others = [s for s in a.stats if not s.does_not_meet]
    return [param_reason(s) for s in failing + others] + [coverage_reason(a)]


def param_to_dict(st: ParamStats) -> dict:
    w = st.worst
    return {"parameter": st.parameter, "criterion": criterion_to_dict(st.criterion), "expected": st.expected,
            "compared": st.compared, "meets": st.meets, "does_not_meet": st.does_not_meet, "missing": st.missing,
            "below_detection_not_compared": st.not_compared, "points": round(st.points, 3),
            "worst_reading": reading_to_dict(w[0], w[1].to_dict()) if w else None}


def assessment_to_dict(a: SiteAssessment, ds: Dataset) -> dict:
    info = ds.catalog.sites[a.site]
    fails = sorted((it for st in a.stats for it in st.failures),
                   key=lambda it: (-it[1].severity, _chron(it[0]), it[0].parameter))
    return {
        "rank": a.rank, "assessable": a.score is not None, "site": a.site, "site_id": a.site_id,
        "name_hi": SITE_NAMES_HI.get(a.site, a.site), "water_body": ", ".join(sorted(info.water_bodies)),
        "site_match_confidence": ", ".join(sorted(info.confidences)),
        "score": round(a.score, 3) if a.score is not None else None,
        "score_detail": {"points": round(a.points, 3), "readings_compared": a.compared,
                         "max_single_severity": round(a.max_severity, 3)},
        "readings_compared": a.compared, "readings_outside_criteria": a.does_not_meet,
        "share_outside_criteria": round(a.does_not_meet / a.compared, 3) if a.compared else None,
        "readings_expected": a.expected, "readings_missing": a.missing,
        "readings_below_detection_not_compared": a.not_compared,
        "coverage_ratio": round(a.compared / a.expected, 3) if a.expected else None,
        "coverage_level": a.coverage_level, "low_coverage_warning": a.coverage_level != "high",
        "parameters": [param_to_dict(s) for s in a.stats], "reasons": reasons(a),
        "evidence": [reading_to_dict(r, c.to_dict()) for r, c in fails[:EVIDENCE_LIMIT]],
        "missing": missing_groups(a), "caveats": site_caveats(ds, a.site),
    }


def method_description(ds: Dataset, res: RankingResult) -> dict:
    cls = res.cpcb_class
    crit_all = criteria_for_class(ds.criteria, cls)
    used = {c.dataset_parameter for c in res.criteria}
    return {
        "cpcb_class": cls,
        "designated_best_use": crit_all[0].designated_best_use if crit_all else None,
        "parameters": [criterion_to_dict(c) for c in res.criteria],
        "score": ("Mean points per compared reading. A reading that meets its criterion scores 0. A reading that does "
                  "not meet it scores 1 + severity, where severity = min(gap / scale, 1); gap is the distance beyond "
                  "the limit; scale is the limit itself for minimum/maximum limits (5 mg/l for DO, 3 mg/l for BOD) "
                  "and half the range width for range limits (1 pH unit for 6.5–8.5). Score runs from 0 to 2."),
        "phases": "Before, during and after readings are weighted equally, so water already outside the criteria "
                  "before immersion also raises the score. Use phase=during,after to focus on the immersion period.",
        "missing_data": "Missing readings (not sampled, no table, not printed) are excluded from both numerator and "
                        "denominator; they never count as meeting or failing. BDL/ND readings are not compared "
                        "because the detection limit is not reported.",
        "tie_break": ["higher score", "more readings outside criteria", "larger single worst severity", "site name A–Z"],
        "coverage_levels": {"high": ">= 90% of expected readings compared", "medium": "60–89%", "low": "< 60%",
                            "none": "no comparable readings (not ranked)"},
        "not_scored": [p for p in ds.catalog.parameters if p not in used],
    }


def ranking_to_dict(res: RankingResult, ds: Dataset) -> dict:
    return {"method": method_description(ds, res),
            "scope": {"events": [{"year": y, "festival": f} for y, f in res.events], "phases": res.phases},
            "rankings": [assessment_to_dict(a, ds) for a in res.assessments]}


def assess_one_site(ds: Dataset, site: str, f: Filters, cls: str) -> Optional[dict]:
    cmap, params = _ranking_scope(ds, f, cls)
    if not params:
        return None
    a = assess_site(ds, site, scope_events(ds, f), scope_phases(f), params, cmap)
    d = assessment_to_dict(a, ds)
    d["rank_note"] = "Rank among ghats is only available from /api/rankings."
    return d
'''

FILES["backend/jal_drishti/summary.py"] = r'''
from __future__ import annotations

from collections import Counter
from statistics import median

from .config import PARAMETER_LABELS_EN
from .coverage import scope_events, scope_parameters, scope_phases, scope_sites, site_slots, summarize_slots
from .criteria import FAILS, MEETS, MISSING, NOT_COMPARED, compare, criteria_map, criterion_to_dict, limit_phrase
from .filters import Filters
from .models import Dataset


def _headline(param, c, fails, compared, missing):
    label = PARAMETER_LABELS_EN.get(param, param)
    verb = {"min": "below", "max": "above", "range": "outside"}[c.limit_type]
    text = f"{fails} of {compared} measured {label} readings are {verb} the {limit_phrase(c)}."
    if missing:
        text += f" {missing} missing readings are not counted."
    return text


def build_summary(ds: Dataset, f: Filters, cls: str) -> dict:
    cat = ds.catalog
    rows = [r for r in ds.readings if f.matches(r)]
    cmap = criteria_map(ds.criteria, cls, cat.parameters)
    params_out, headlines = [], []
    for p in cat.parameters:
        prow = [r for r in rows if r.parameter == p]
        if not prow:
            continue
        vals = [r.value for r in prow if r.measurement_status == "measured"]
        sc = Counter(r.measurement_status for r in prow)
        entry = {"parameter": p, "unit_assumed": cat.parameter_units.get(p) or None, "rows": len(prow),
                 "measured": sc["measured"], "below_detection": sc["below_detection"], "missing": sc["missing"],
                 "min": min(vals) if vals else None, "max": max(vals) if vals else None,
                 "median": round(median(vals), 4) if vals else None}
        c = cmap.get(p)
        if c:
            cc = Counter(compare(r, c).status for r in prow)
            compared = cc[MEETS] + cc[FAILS]
            entry["criterion"] = criterion_to_dict(c)
            entry["comparison"] = {"compared": compared, "meets": cc[MEETS], "does_not_meet": cc[FAILS],
                                   "not_compared_below_detection": cc[NOT_COMPARED], "missing": cc[MISSING],
                                   "share_not_meeting": round(cc[FAILS] / compared, 3) if compared else None}
            if compared:
                headlines.append(_headline(p, c, cc[FAILS], compared, cc[MISSING]))
        else:
            entry["criterion"] = None
            entry["comparison"] = {"status": "no_criterion",
                                   "note": f"CPCB Class {cls} sets no limit for {p}; values are reported without comparison."}
        params_out.append(entry)

    events, phases, params = scope_events(ds, f), scope_phases(f), scope_parameters(ds, f)
    slots = [s for site in scope_sites(ds, f) for s in site_slots(ds, site, events, phases, params)]
    sc = Counter(r.measurement_status for r in rows)
    return {"scope": {"events": [{"year": y, "festival": fe} for y, fe in events], "phases": phases,
                      "sites": scope_sites(ds, f)},
            "counts": {"rows": len(rows), "measured": sc["measured"], "below_detection": sc["below_detection"],
                       "missing": sc["missing"]},
            "coverage": summarize_slots(slots), "headlines": headlines, "parameters": params_out}
'''

FILES["backend/jal_drishti/brief.py"] = r'''
"""Short officer brief in English and Hindi, generated only from the ranking and its evidence."""
from __future__ import annotations

from typing import List

from .config import (BRIEF_LABELS_EN, BRIEF_LABELS_HI, CLASS_USE_HI, FESTIVAL_LABELS_HI, FESTIVALS,
                     PARAMETER_LABELS_EN, PARAMETER_LABELS_HI, PHASE_LABELS_EN, PHASE_LABELS_HI, PHASE_SHORT_EN,
                     PHASE_SHORT_HI, PHASES, SITE_CAVEATS, SITE_CAVEATS_HI, SITE_NAMES_HI)
from .criteria import criteria_for_class, fmt, unit_suffix
from .filters import Filters
from .models import Criterion, Dataset
from .ranking import ParamStats, rank_ghats


def _years_text(years: List[int]) -> str:
    if not years:
        return "—"
    if len(years) > 1 and years == list(range(years[0], years[-1] + 1)):
        return f"{years[0]}–{years[-1]}"
    return ", ".join(str(y) for y in years)


def _std_en(c: Criterion) -> str:
    label, u = PARAMETER_LABELS_EN.get(c.dataset_parameter, c.dataset_parameter), unit_suffix(c.unit)
    if c.limit_type == "min":
        return f"{label} at least {fmt(c.lower)}{u}"
    if c.limit_type == "max":
        return f"{label} at most {fmt(c.upper)}{u}"
    return f"{label} {fmt(c.lower)}–{fmt(c.upper)}"


def _std_hi(c: Criterion) -> str:
    label, u = PARAMETER_LABELS_HI.get(c.dataset_parameter, c.dataset_parameter), unit_suffix(c.unit)
    if c.limit_type == "min":
        return f"{label} कम से कम {fmt(c.lower)}{u}"
    if c.limit_type == "max":
        return f"{label} अधिकतम {fmt(c.upper)}{u}"
    return f"{label} {fmt(c.lower)}–{fmt(c.upper)}"


def _frag_en(st: ParamStats) -> str:
    label, c = BRIEF_LABELS_EN.get(st.parameter, st.parameter), st.criterion
    if st.compared == 0:
        return f"{label} not available"
    if st.does_not_meet == 0:
        return f"{label} within the limit in all {st.compared}"
    r, _ = st.worst
    u = unit_suffix(c.unit)
    lim = {"min": f"below {fmt(c.lower or 0)}{u}", "max": f"above {fmt(c.upper or 0)}{u}",
           "range": f"outside {fmt(c.lower or 0)}–{fmt(c.upper or 0)}"}[c.limit_type]
    word = {"min": "lowest", "max": "highest", "range": "worst"}[c.limit_type]
    return (f"{label} {lim} in {st.does_not_meet} of {st.compared} ({word} {fmt(r.value)}{unit_suffix(r.unit_assumed)}, "
            f"{r.festival} {r.year} {PHASE_SHORT_EN[r.phase]}, p. {r.source_page})")


def _frag_hi(st: ParamStats) -> str:
    label, c = BRIEF_LABELS_HI.get(st.parameter, st.parameter), st.criterion
    if st.compared == 0:
        return f"{label} उपलब्ध नहीं"
    if st.does_not_meet == 0:
        return f"{label} सभी {st.compared} रीडिंग में मानक के भीतर"
    r, _ = st.worst
    u = unit_suffix(c.unit)
    lim = {"min": f"{fmt(c.lower or 0)}{u} से कम", "max": f"{fmt(c.upper or 0)}{u} से अधिक",
           "range": f"{fmt(c.lower or 0)}–{fmt(c.upper or 0)} की सीमा से बाहर"}[c.limit_type]
    word = {"min": "न्यूनतम", "max": "अधिकतम", "range": "सबसे दूर"}[c.limit_type]
    return (f"{label} {st.compared} में से {st.does_not_meet} रीडिंग में {lim} ({word} {fmt(r.value)}{unit_suffix(r.unit_assumed)}, "
            f"{FESTIVAL_LABELS_HI[r.festival]} {r.year} {PHASE_SHORT_HI[r.phase]}, पृष्ठ {r.source_page})")


def build_brief(ds: Dataset, f: Filters, cls: str, top: int) -> dict:
    res = rank_ghats(ds, f, cls)
    ranked = [a for a in res.assessments if a.rank is not None]
    unassessed = [a for a in res.assessments if a.rank is None]
    chosen = ranked[:top]
    limited = [a for a in ranked if a.coverage_level in ("medium", "low")]
    years = sorted({y for y, _ in res.events})
    fests = [x for x in FESTIVALS if any(e[1] == x for e in res.events)]
    yt = _years_text(years)
    all_phases = len(res.phases) == len(PHASES)
    scope_en = f"{' and '.join(fests)} visarjan, {yt}, " + ("all phases" if all_phases else ", ".join(PHASE_LABELS_EN[p] for p in res.phases))
    scope_hi = f"{' और '.join(FESTIVAL_LABELS_HI[x] for x in fests)} विसर्जन, {yt}, " + ("सभी चरण" if all_phases else ", ".join(PHASE_LABELS_HI[p] for p in res.phases))
    crit_all = criteria_for_class(ds.criteria, cls)
    use_en = crit_all[0].designated_best_use if crit_all else ""
    use_hi = CLASS_USE_HI.get(cls, use_en)
    total = sum(a.compared for a in ranked)
    name_hi = lambda a: SITE_NAMES_HI.get(a.site, a.site)

    en = [f"Based on MPPCB visarjan test reports ({yt}): {total} readings at {len(ranked)} ghats compared with "
          f"CPCB Class {cls} ({use_en}): " + ", ".join(_std_en(c) for c in res.criteria) + ".",
          "Ghats in order of priority for attention (how often and how far readings fall outside the criteria):"]
    hi = [f"आधार: MPPCB विसर्जन जाँच रिपोर्ट ({yt}); {len(ranked)} घाटों की {total} रीडिंग की तुलना CPCB श्रेणी {cls} "
          f"({use_hi}) मानक से: " + ", ".join(_std_hi(c) for c in res.criteria) + "।",
          "प्राथमिकता क्रम में घाट (मानक से बाहर रीडिंग कितनी बार और कितनी दूर):"]
    for a in chosen:
        en.append(f"{a.rank}. {a.site}: " + "; ".join(_frag_en(s) for s in a.stats)
                  + f". Data: {a.compared} of {a.expected} expected readings.")
        hi.append(f"{a.rank}. {name_hi(a)}: " + "; ".join(_frag_hi(s) for s in a.stats)
                  + f"। आँकड़े: {a.expected} में से {a.compared} अपेक्षित रीडिंग उपलब्ध।")
    if limited:
        en.append("Limited data: " + ", ".join(f"{a.site} ({a.compared} of {a.expected})" for a in limited)
                  + ". Missing readings are not counted as clean, and a lower rank is not evidence of better water.")
        hi.append("सीमित आँकड़े: " + ", ".join(f"{name_hi(a)} ({a.expected} में से {a.compared})" for a in limited)
                  + "। अनुपलब्ध रीडिंग को 'साफ़' नहीं माना गया है; निचली रैंक बेहतर पानी का प्रमाण नहीं है।")
    if unassessed:
        en.append("No comparable readings, not assessed: " + ", ".join(a.site for a in unassessed) + ".")
        hi.append("तुलना योग्य रीडिंग नहीं, आकलन नहीं हुआ: " + ", ".join(name_hi(a) for a in unassessed) + "।")
    for a in chosen:
        if a.site in SITE_CAVEATS:
            en.append(f"Note: {SITE_CAVEATS[a.site]}")
            hi.append(f"ध्यान दें: {SITE_CAVEATS_HI.get(a.site, SITE_CAVEATS[a.site])}")
    en.append("This brief compares measured values with CPCB limits only; it does not assess health effects. "
              "Units are assumed (the reports print none).")
    hi.append("यह सारांश केवल मापे गए मानों की तुलना CPCB मानकों से करता है; यह स्वास्थ्य प्रभाव का आकलन नहीं है। "
              "इकाइयाँ मानी गई हैं (रिपोर्ट में इकाइयाँ नहीं छपी हैं)।")
    en.append(f"Source: MPPCB visarjan reports {yt}; 'p.' = PDF page of that year's report.")
    hi.append(f"स्रोत: MPPCB विसर्जन रिपोर्ट {yt}; 'पृष्ठ' = उस वर्ष की रिपोर्ट का PDF पृष्ठ।")

    title_en, title_hi = f"Jal Drishti ghat brief — {scope_en}", f"जल दृष्टि घाट सारांश — {scope_hi}"
    return {
        "scope": {"label_en": scope_en, "label_hi": scope_hi, "cpcb_class": cls,
                  "events": [{"year": y, "festival": x} for y, x in res.events], "phases": res.phases},
        "top_sites": [a.site_id for a in chosen],
        "en": {"title": title_en, "lines": en, "text": "\n".join([title_en] + en)},
        "hi": {"title": title_hi, "lines": hi, "text": "\n".join([title_hi] + hi)},
        "notes": ["Generated from /api/rankings for the same filters.",
                  "Hindi text is template-generated; have a Hindi speaker review before forwarding."],
    }
'''

FILES["backend/jal_drishti/api.py"] = r'''
"""HTTP layer. Run: python run.py   (or: python -m uvicorn jal_drishti.api:app --port 8000)"""
import os
from collections import Counter
from typing import Dict, Iterable, Optional

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import __version__
from .brief import build_brief
from .config import CORS_ENV, CRITERIA_SOURCE, DEFAULT_CPCB_CLASS, resolve_frontend_dir
from .coverage import build_coverage, site_coverage
from .criteria import available_classes, criteria_for_class, criteria_map, criterion_to_dict
from .data_loader import DataFileError
from .filters import FILTER_FIELDS, FilterError, parse_cpcb_class, parse_filters, parse_int, resolve_site
from .ranking import assess_one_site, rank_ghats, ranking_to_dict
from .serializers import caveats_for, ghat_info, reading_with_comparison
from .store import DataStore
from .summary import build_summary

SERVICE = "jal-drishti-backend"
MAX_PAGE_SIZE = 2000


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.status, self.code, self.message, self.details = status, code, message, details or {}


def _error(status: int, code: str, message: str, details: Optional[dict] = None) -> JSONResponse:
    return JSONResponse(status_code=status,
                        content={"error": {"status": status, "code": code, "message": message, "details": details or {}}})


def _query(request: Request, allowed: Iterable[str]) -> Dict[str, str]:
    allowed = set(allowed)
    keys = list(dict.fromkeys(request.query_params.keys()))
    unknown = [k for k in keys if k not in allowed]
    if unknown:
        raise ApiError(400, "unknown_query_parameter", f"Unknown query parameter(s): {', '.join(unknown)}.",
                       {"allowed": sorted(allowed)})
    return {k: ",".join(request.query_params.getlist(k)) for k in keys}


def _q(desc: str):
    return Query(None, description=desc)


D_YEAR = "Year(s), comma-separated, e.g. 2024 or 2023,2025."
D_FEST = "Ganesh and/or Durga (case-insensitive)."
D_PHASE = "pre, during, after (comma-separated)."
D_SITE = "Ghat name or site_id from /api/ghats (comma-separated)."
D_PARAM = "Parameter name, e.g. BOD or 'Dissolved oxygen' (comma-separated)."
D_CLASS = f"CPCB class for comparisons (default {DEFAULT_CPCB_CLASS})."


def create_app(data_dir=None) -> FastAPI:
    store = DataStore(data_dir)
    app = FastAPI(title="Jal Drishti API", version=__version__,
                  description="Bhopal visarjan-ghat readings (MPPCB 2023–2025) compared with CPCB criteria. "
                              "Read-only, local, CSV-backed.")
    app.state.store = store
    origins = [o.strip() for o in os.environ.get(CORS_ENV, "*").split(",") if o.strip()]
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET"], allow_headers=["*"])

    @app.exception_handler(ApiError)
    async def _api_err(_r, exc: ApiError):
        return _error(exc.status, exc.code, exc.message, exc.details)

    @app.exception_handler(FilterError)
    async def _filter_err(_r, exc: FilterError):
        return _error(400, "invalid_query", exc.message, exc.to_dict())

    @app.exception_handler(DataFileError)
    async def _data_err(_r, exc: DataFileError):
        return _error(503, "data_unavailable", exc.message, exc.to_dict())

    @app.exception_handler(StarletteHTTPException)
    async def _http_err(_r, exc: StarletteHTTPException):
        if exc.status_code == 404:
            return _error(404, "not_found", "No such endpoint. See /docs.")
        return _error(exc.status_code, "http_error", str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def _val_err(_r, exc: RequestValidationError):
        return _error(400, "invalid_request", "Request could not be validated.",
                      {"errors": [{"loc": list(e.get("loc", ())), "msg": e.get("msg")} for e in exc.errors()]})

    def meta(ds, filters=None, cls=None, sites=(), **extra):
        m = {"caveats": caveats_for(ds, sites)}
        if filters is not None:
            m["filters"] = filters.as_dict()
        if cls is not None:
            m["cpcb_class"] = cls
        m.update(extra)
        return m

    @app.get("/api/health", tags=["service"])
    def health():
        try:
            ds = store.get()
        except DataFileError as exc:
            return JSONResponse(status_code=503, content={"data": {
                "status": "error", "service": SERVICE, "version": __version__,
                "data_dir": str(store.data_dir), "error": exc.to_dict()}, "meta": {}})
        cat = ds.catalog
        return {"data": {"status": "ok", "service": SERVICE, "version": __version__,
                         "files": {"readings": ds.readings_path, "criteria": ds.criteria_path},
                         "row_counts": {"readings": len(ds.readings), "criteria": len(ds.criteria)},
                         "sites": len(cat.sites), "events": [{"year": y, "festival": f} for y, f in cat.events],
                         "loaded_at": ds.loaded_at}, "meta": {}}

    @app.get("/api/ghats", tags=["ghats"])
    def ghats(request: Request):
        _query(request, ())
        ds = store.get()
        sites = list(ds.catalog.sites)
        return {"data": [ghat_info(ds, s) for s in sites], "meta": meta(ds, sites=sites, count=len(sites))}

    @app.get("/api/readings", tags=["readings"])
    def readings(request: Request, year: Optional[str] = _q(D_YEAR), festival: Optional[str] = _q(D_FEST),
                 phase: Optional[str] = _q(D_PHASE), site: Optional[str] = _q(D_SITE),
                 parameter: Optional[str] = _q(D_PARAM), cpcb_class: Optional[str] = _q(D_CLASS),
                 limit: Optional[str] = _q(f"Page size 1–{MAX_PAGE_SIZE} (default {MAX_PAGE_SIZE})."),
                 offset: Optional[str] = _q("Rows to skip (default 0).")):
        q = _query(request, set(FILTER_FIELDS) | {"cpcb_class", "limit", "offset"})
        ds = store.get()
        f = parse_filters(q, ds.catalog)
        cls = parse_cpcb_class(q.get("cpcb_class"), available_classes(ds.criteria))
        lim = parse_int(q.get("limit"), "limit", MAX_PAGE_SIZE, 1, MAX_PAGE_SIZE)
        off = parse_int(q.get("offset"), "offset", 0, 0, None)
        rows = [r for r in ds.readings if f.matches(r)]
        cmap = criteria_map(ds.criteria, cls, ds.catalog.parameters)
        page = rows[off:off + lim]
        sc = Counter(r.measurement_status for r in rows)
        return {"data": [reading_with_comparison(r, cmap, cls) for r in page],
                "meta": meta(ds, f, cls, sorted({r.site for r in rows}), total=len(rows), returned=len(page),
                             limit=lim, offset=off,
                             status_counts={k: sc[k] for k in ("measured", "below_detection", "missing")})}

    @app.get("/api/criteria", tags=["criteria"])
    def criteria(request: Request, cpcb_class: Optional[str] = _q("One class (A–E). Omit for all.")):
        q = _query(request, {"cpcb_class"})
        ds = store.get()
        classes = available_classes(ds.criteria)
        sel = parse_cpcb_class(q.get("cpcb_class"), classes, default=None)
        measured = set(ds.catalog.parameters)
        out = []
        for c in ([sel] if sel else classes):
            crits = criteria_for_class(ds.criteria, c)
            cmap = criteria_map(ds.criteria, c, measured)
            out.append({"cpcb_class": c, "designated_best_use": crits[0].designated_best_use,
                        "default_for_comparisons": c == DEFAULT_CPCB_CLASS,
                        "criteria": [{**criterion_to_dict(x), "measured_in_dataset": x.dataset_parameter in measured}
                                     for x in crits],
                        "dataset_parameters_without_criterion": [p for p in ds.catalog.parameters if p not in cmap]})
        return {"data": {"default_class": DEFAULT_CPCB_CLASS, "selected_class": sel, "source": CRITERIA_SOURCE,
                         "classes": out,
                         "notes": ["Class B (organised outdoor bathing) is used by default for immersion ghats.",
                                   "Conductivity is in µS/cm, which equals micromhos/cm."]},
                "meta": meta(ds)}

    @app.get("/api/summary", tags=["summary"])
    def summary(request: Request, year: Optional[str] = _q(D_YEAR), festival: Optional[str] = _q(D_FEST),
                phase: Optional[str] = _q(D_PHASE), site: Optional[str] = _q(D_SITE),
                parameter: Optional[str] = _q(D_PARAM), cpcb_class: Optional[str] = _q(D_CLASS)):
        q = _query(request, set(FILTER_FIELDS) | {"cpcb_class"})
        ds = store.get()
        f = parse_filters(q, ds.catalog)
        cls = parse_cpcb_class(q.get("cpcb_class"), available_classes(ds.criteria))
        data = build_summary(ds, f, cls)
        return {"data": data, "meta": meta(ds, f, cls, data["scope"]["sites"])}

    @app.get("/api/coverage", tags=["summary"])
    def coverage(request: Request, year: Optional[str] = _q(D_YEAR), festival: Optional[str] = _q(D_FEST),
                 phase: Optional[str] = _q(D_PHASE), site: Optional[str] = _q(D_SITE),
                 parameter: Optional[str] = _q(D_PARAM)):
        q = _query(request, FILTER_FIELDS)
        ds = store.get()
        f = parse_filters(q, ds.catalog)
        data = build_coverage(ds, f)
        return {"data": data, "meta": meta(ds, f, None, [s["site"] for s in data["sites"]])}

    @app.get("/api/rankings", tags=["rankings"])
    def rankings(request: Request, year: Optional[str] = _q(D_YEAR), festival: Optional[str] = _q(D_FEST),
                 phase: Optional[str] = _q(D_PHASE), site: Optional[str] = _q(D_SITE),
                 parameter: Optional[str] = _q(D_PARAM), cpcb_class: Optional[str] = _q(D_CLASS)):
        q = _query(request, set(FILTER_FIELDS) | {"cpcb_class"})
        ds = store.get()
        f = parse_filters(q, ds.catalog)
        cls = parse_cpcb_class(q.get("cpcb_class"), available_classes(ds.criteria))
        data = ranking_to_dict(rank_ghats(ds, f, cls), ds)
        return {"data": data, "meta": meta(ds, f, cls, [r["site"] for r in data["rankings"]])}

    @app.get("/api/ghats/{site_id:path}/readings", tags=["ghats"])
    def ghat_readings(site_id: str, request: Request, year: Optional[str] = _q(D_YEAR),
                      festival: Optional[str] = _q(D_FEST), phase: Optional[str] = _q(D_PHASE),
                      parameter: Optional[str] = _q(D_PARAM), cpcb_class: Optional[str] = _q(D_CLASS)):
        q = _query(request, {"year", "festival", "phase", "parameter", "cpcb_class"})
        ds = store.get()
        name = resolve_site(site_id, ds.catalog)
        if name is None:
            raise ApiError(404, "ghat_not_found", f"No ghat matches {site_id!r}. Use a site_id from /api/ghats.",
                           {"available_ids": [i.site_id for i in ds.catalog.sites.values()]})
        f = parse_filters(q, ds.catalog, ("year", "festival", "phase", "parameter")).with_sites([name])
        cls = parse_cpcb_class(q.get("cpcb_class"), available_classes(ds.criteria))
        cmap = criteria_map(ds.criteria, cls, ds.catalog.parameters)
        rows = [r for r in ds.readings if f.matches(r)]
        return {"data": {"ghat": ghat_info(ds, name), "assessment": assess_one_site(ds, name, f, cls),
                         "coverage": site_coverage(ds, name, f),
                         "readings": [reading_with_comparison(r, cmap, cls) for r in rows]},
                "meta": meta(ds, f, cls, [name], total=len(rows))}

    @app.get("/api/brief", tags=["brief"])
    def brief(request: Request, year: Optional[str] = _q(D_YEAR), festival: Optional[str] = _q(D_FEST),
              phase: Optional[str] = _q(D_PHASE), cpcb_class: Optional[str] = _q(D_CLASS),
              top: Optional[str] = _q("Number of ghats to list (default 3)."),
              lang: Optional[str] = _q("en, hi or both (default both).")):
        q = _query(request, {"year", "festival", "phase", "cpcb_class", "top", "lang"})
        ds = store.get()
        f = parse_filters(q, ds.catalog, ("year", "festival", "phase"))
        cls = parse_cpcb_class(q.get("cpcb_class"), available_classes(ds.criteria))
        top_n = parse_int(q.get("top"), "top", 3, 1, len(ds.catalog.sites))
        lg = (q.get("lang") or "both").strip().lower()
        if lg not in ("en", "hi", "both"):
            raise FilterError("lang", f"lang must be en, hi or both; got {lg!r}.", ["en", "hi", "both"])
        data = build_brief(ds, f, cls, top_n)
        if lg != "both":
            data.pop("hi" if lg == "en" else "en")
        return {"data": data, "meta": meta(ds, f, cls)}

    frontend = resolve_frontend_dir()
    if (frontend / "index.html").is_file():
        # Mounted last so every /api route takes priority.
        app.mount("/", StaticFiles(directory=str(frontend), html=True), name="frontend")

    return app


app = create_app()
'''

# ---------------------------------------------------------------- tests

FILES["backend/tests/helpers.py"] = r'''
import csv
from pathlib import Path

PHASES = ("pre", "during", "after")
READINGS_HEADER = ["year", "festival", "site", "water_body", "phase", "parameter", "value", "unit_assumed", "flag",
                   "value_as_printed", "parameter_as_printed", "site_as_printed", "site_match_confidence", "source_page"]
CRITERIA_HEADER = ["class", "designated_best_use", "parameter", "limit_type", "limit", "unit"]
CRITERIA_ROWS = [
    {"class": "B", "designated_best_use": "Outdoor bathing (organised)", "parameter": "pH", "limit_type": "range", "limit": "6.5-8.5", "unit": ""},
    {"class": "B", "designated_best_use": "Outdoor bathing (organised)", "parameter": "Dissolved oxygen", "limit_type": "min", "limit": "5", "unit": "mg/l"},
    {"class": "B", "designated_best_use": "Outdoor bathing (organised)", "parameter": "BOD (5 days 20C)", "limit_type": "max", "limit": "3", "unit": "mg/l"},
    {"class": "E", "designated_best_use": "Irrigation industrial cooling controlled waste disposal", "parameter": "Electrical conductivity at 25C", "limit_type": "max", "limit": "2250", "unit": "micromhos/cm"},
]


def make_row(**kw):
    row = {"year": "2025", "festival": "Durga", "site": "Alpha ghat", "water_body": "Test lake", "phase": "pre",
           "parameter": "BOD", "value": "", "unit_assumed": "mg/l", "flag": "", "value_as_printed": None,
           "parameter_as_printed": None, "site_as_printed": None, "site_match_confidence": "high", "source_page": "1"}
    row.update({k: (str(v) if isinstance(v, (int, float)) else v) for k, v in kw.items()})
    if row["value_as_printed"] is None:
        row["value_as_printed"] = row["value"] or row["flag"]
    if row["parameter_as_printed"] is None:
        row["parameter_as_printed"] = row["parameter"]
    if row["site_as_printed"] is None:
        row["site_as_printed"] = row["site"]
    return row


def site_rows(site, do, bod, ph, year=2025, festival="Durga"):
    """do/bod/ph: 3 values for pre/during/after; None means 'not sampled'."""
    rows = []
    for param, vals, unit in (("Dissolved oxygen", do, "mg/l"), ("BOD", bod, "mg/l"), ("pH", ph, "")):
        for phase, v in zip(PHASES, vals):
            if v is None:
                rows.append(make_row(site=site, year=year, festival=festival, phase=phase, parameter=param,
                                     unit_assumed=unit, flag="not sampled", value_as_printed="_"))
            else:
                rows.append(make_row(site=site, year=year, festival=festival, phase=phase, parameter=param,
                                     unit_assumed=unit, value=v))
    return rows


def write_data(directory: Path, readings_rows, criteria_rows=CRITERIA_ROWS, readings_header=READINGS_HEADER):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "bhopal_ghats_2023_2025.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=readings_header, extrasaction="ignore")
        w.writeheader()
        w.writerows(readings_rows)
    with (directory / "cpcb_water_quality_criteria.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CRITERIA_HEADER)
        w.writeheader()
        w.writerows(criteria_rows)
    return directory
'''

FILES["backend/tests/conftest.py"] = r'''
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from jal_drishti.api import create_app
from jal_drishti.data_loader import load_dataset

REPO_DATA = Path(__file__).resolve().parents[2] / "data"


@pytest.fixture(scope="session")
def real_data_dir():
    if not (REPO_DATA / "bhopal_ghats_2023_2025.csv").is_file():
        pytest.skip("real data files not present in ../data")
    return REPO_DATA


@pytest.fixture(scope="session")
def real_dataset(real_data_dir):
    return load_dataset(real_data_dir)


@pytest.fixture(scope="session")
def client(real_data_dir):
    return TestClient(create_app(real_data_dir))
'''

FILES["backend/tests/test_loader.py"] = r'''
import pytest
from helpers import READINGS_HEADER, make_row, write_data

from jal_drishti.data_loader import DataFileError, load_dataset


def test_real_dataset_shape(real_dataset):
    assert len(real_dataset.readings) == 1524
    assert len(real_dataset.catalog.sites) == 7
    assert real_dataset.catalog.events == [(2023, "Ganesh"), (2023, "Durga"), (2024, "Ganesh"),
                                           (2024, "Durga"), (2025, "Ganesh"), (2025, "Durga")]


def test_bdl_is_below_detection_not_zero(real_dataset):
    r = real_dataset.index[(2023, "Ganesh", "Khatlapura ghat", "pre", "Chromium")]
    assert r.value is None and r.measurement_status == "below_detection" and r.value_as_printed == "BDL"


@pytest.mark.parametrize("key,printed", [
    ((2023, "Ganesh", "Khatlapura ghat", "during", "Chromium"), "_"),
    ((2025, "Ganesh", "Malikhedi kund", "pre", "pH"), "*"),
    ((2025, "Ganesh", "Malikhedi kund", "after", "pH"), "**"),
    ((2025, "Ganesh", "Malikhedi kund", "pre", "BOD"), ""),
])
def test_blank_and_star_codes_are_missing(real_dataset, key, printed):
    r = real_dataset.index[key]
    assert r.value is None and r.measurement_status == "missing" and r.value_as_printed == printed


def test_zero_is_a_measurement(real_dataset):
    r = real_dataset.index[(2025, "Ganesh", "Bairagarh (Sant Hirdaram) kund", "during", "Dissolved oxygen")]
    assert r.value == 0.0 and r.measurement_status == "measured"


def test_provenance_preserved(real_dataset):
    r = real_dataset.index[(2025, "Durga", "Shahpura lake ghat", "pre", "Dissolved oxygen")]
    assert (r.value, r.unit_assumed, r.source_page, r.parameter_as_printed) == (2.5, "mg/l", 65, "D.Oxygen")


def test_nd_flag_is_below_detection(tmp_path):
    write_data(tmp_path, [make_row(parameter="Lead", flag="ND")])
    r = load_dataset(tmp_path).readings[0]
    assert r.measurement_status == "below_detection" and r.value is None


def test_missing_file(tmp_path):
    with pytest.raises(DataFileError) as e:
        load_dataset(tmp_path)
    assert "not found" in e.value.message


def test_missing_column(tmp_path):
    write_data(tmp_path, [make_row(value=2)], readings_header=[h for h in READINGS_HEADER if h != "source_page"])
    with pytest.raises(DataFileError) as e:
        load_dataset(tmp_path)
    assert "source_page" in e.value.message


def test_non_numeric_value_reports_line(tmp_path):
    write_data(tmp_path, [make_row(value="abc")])
    with pytest.raises(DataFileError) as e:
        load_dataset(tmp_path)
    assert "malformed" in e.value.message and any("line 2" in d for d in e.value.details)


def test_duplicate_reading_rejected(tmp_path):
    write_data(tmp_path, [make_row(value=2), make_row(value=3)])
    with pytest.raises(DataFileError) as e:
        load_dataset(tmp_path)
    assert "Duplicate" in e.value.message


def test_bad_criteria_range(tmp_path):
    bad = [{"class": "B", "designated_best_use": "x", "parameter": "pH", "limit_type": "range", "limit": "8.5", "unit": ""}]
    write_data(tmp_path, [make_row(value=2)], criteria_rows=bad)
    with pytest.raises(DataFileError):
        load_dataset(tmp_path)
'''

FILES["backend/tests/test_criteria.py"] = r'''
import pytest

from jal_drishti.criteria import FAILS, MEETS, MISSING, NOT_COMPARED, compare
from jal_drishti.data_loader import classify_measurement
from jal_drishti.models import Criterion, Reading

BOD = Criterion("B", "Outdoor bathing (organised)", "BOD (5 days 20C)", "BOD", "max", "3", None, 3.0, "mg/l")
DO = Criterion("B", "Outdoor bathing (organised)", "Dissolved oxygen", "Dissolved oxygen", "min", "5", 5.0, None, "mg/l")
PH = Criterion("B", "Outdoor bathing (organised)", "pH", "pH", "range", "6.5-8.5", 6.5, 8.5, "")


def reading(param, value, flag="", printed=None):
    printed = printed if printed is not None else ("" if value is None else str(value))
    return Reading(2, 2025, "Durga", "Alpha ghat", "alpha-ghat", "x", "pre", param, value, "mg/l", flag, printed,
                   param, "Alpha ghat", "high", 1, classify_measurement(value, flag, printed))


@pytest.mark.parametrize("v,status,dev", [(2.4, MEETS, None), (3.0, MEETS, None), (3.1, FAILS, "above_max"), (11.2, FAILS, "above_max")])
def test_bod_direction(v, status, dev):
    c = compare(reading("BOD", v), BOD)
    assert c.status == status and c.deviation == dev
    if status == FAILS:
        assert "exceeds" in c.explanation


def test_bod_severity_is_relative_and_capped():
    assert compare(reading("BOD", 4.5), BOD).severity == pytest.approx(0.5)
    assert compare(reading("BOD", 22), BOD).severity == 1.0


@pytest.mark.parametrize("v,status,dev", [(6.4, MEETS, None), (5.0, MEETS, None), (4.9, FAILS, "below_min"), (0.0, FAILS, "below_min")])
def test_do_direction(v, status, dev):
    c = compare(reading("Dissolved oxygen", v), DO)
    assert c.status == status and c.deviation == dev


def test_do_zero_has_full_severity():
    assert compare(reading("Dissolved oxygen", 0.0), DO).severity == 1.0


@pytest.mark.parametrize("v,status,dev", [(6.5, MEETS, None), (8.5, MEETS, None), (6.49, FAILS, "below_range"), (8.92, FAILS, "above_range")])
def test_ph_range(v, status, dev):
    c = compare(reading("pH", v), PH)
    assert c.status == status and c.deviation == dev


def test_missing_is_never_meets():
    c = compare(reading("BOD", None, flag="not sampled", printed="_"), BOD)
    assert c.status == MISSING and c.status != MEETS


def test_bdl_is_not_compared():
    c = compare(reading("BOD", None, flag="BDL", printed="BDL"), BOD)
    assert c.status == NOT_COMPARED


def test_guide_headline_counts(client):
    params = {p["parameter"]: p for p in client.get("/api/summary").json()["data"]["parameters"]}
    do, bod, ph = (params[k]["comparison"] for k in ("Dissolved oxygen", "BOD", "pH"))
    assert (do["does_not_meet"], do["compared"], do["missing"]) == (42, 116, 4)
    assert (bod["does_not_meet"], bod["compared"], bod["missing"]) == (100, 112, 8)
    assert (ph["does_not_meet"], ph["compared"]) == (6, 115)
'''

FILES["backend/tests/test_ranking.py"] = r'''
import random

from helpers import site_rows, write_data

from jal_drishti.data_loader import build_dataset, load_dataset
from jal_drishti.filters import Filters
from jal_drishti.ranking import rank_ghats, ranking_to_dict


def _synthetic(tmp_path):
    rows = (site_rows("A worst", [2, 2, 2], [10, 10, 10], [7, 7, 7])
            + site_rows("B mild", [6, 6, 6], [4, 4, 4], [7, 7, 7])
            + site_rows("C meets", [6, 6, 6], [2, 2, 2], [7, 7, 7])
            + site_rows("D sparse", [None, None, None], [10, None, None], [None, None, None])
            + site_rows("E empty", [None] * 3, [None] * 3, [None] * 3))
    return load_dataset(write_data(tmp_path, rows))


def _by_site(ds, f=Filters()):
    return {r["site"]: r for r in ranking_to_dict(rank_ghats(ds, f, "B"), ds)["rankings"]}


def test_more_and_worse_exceedances_rank_higher(tmp_path):
    r = _by_site(_synthetic(tmp_path))
    assert r["A worst"]["rank"] < r["B mild"]["rank"] < r["C meets"]["rank"]
    assert r["C meets"]["score"] == 0


def test_bod_direction_in_ranking(tmp_path):
    r = _by_site(_synthetic(tmp_path))
    assert r["B mild"]["parameters"][1]["does_not_meet"] == 3   # BOD 4 > 3
    assert r["C meets"]["parameters"][1]["does_not_meet"] == 0  # BOD 2 <= 3


def test_missing_not_counted_as_pass_or_fail(tmp_path):
    d = _by_site(_synthetic(tmp_path))["D sparse"]
    assert d["readings_compared"] == 1 and d["readings_missing"] == 8
    assert d["share_outside_criteria"] == 1.0
    assert d["coverage_level"] == "low" and d["low_coverage_warning"] is True


def test_no_data_is_not_ranked(tmp_path):
    e = _by_site(_synthetic(tmp_path))["E empty"]
    assert e["rank"] is None and e["assessable"] is False and e["score"] is None
    assert "not evidence" in e["reasons"][0]


def test_tie_break_by_name(tmp_path):
    rows = site_rows("Beta", [4, 4, 4], [5, 5, 5], [7, 7, 7]) + site_rows("Alpha", [4, 4, 4], [5, 5, 5], [7, 7, 7])
    r = _by_site(load_dataset(write_data(tmp_path, rows)))
    assert r["Alpha"]["rank"] == 1 and r["Beta"]["rank"] == 2


def test_deterministic_regardless_of_row_order(real_dataset):
    base = ranking_to_dict(rank_ghats(real_dataset, Filters(), "B"), real_dataset)
    shuffled = list(real_dataset.readings)
    random.Random(7).shuffle(shuffled)
    ds2 = build_dataset(shuffled, real_dataset.criteria)
    again = ranking_to_dict(rank_ghats(ds2, Filters(), "B"), ds2)
    key = lambda d: [(r["site"], r["rank"], r["score"], r["reasons"]) for r in d["rankings"]]
    assert key(base) == key(again)


def test_real_ranking_evidence_traceable(real_dataset):
    res = ranking_to_dict(rank_ghats(real_dataset, Filters(), "B"), real_dataset)["rankings"]
    assert res[0]["site"] == "Bairagarh (Sant Hirdaram) kund"
    assert res[-1]["site"] == "Prempura ghat"
    top = res[0]
    assert (top["readings_compared"], top["readings_expected"], top["coverage_level"]) == (39, 54, "medium")
    for ev in top["evidence"]:
        assert ev["source"]["page"] and ev["comparison"]["status"] == "does_not_meet"
'''

FILES["backend/tests/test_api.py"] = r'''
from fastapi.testclient import TestClient

from jal_drishti.api import create_app


def test_health_ok(client):
    body = client.get("/api/health").json()
    assert body["data"]["status"] == "ok" and body["data"]["row_counts"]["readings"] == 1524


def test_health_and_endpoints_report_missing_data_files(tmp_path):
    c = TestClient(create_app(tmp_path))
    assert c.get("/api/health").status_code == 503
    r = c.get("/api/readings")
    assert r.status_code == 503 and r.json()["error"]["code"] == "data_unavailable"


def test_ghats_list_and_rani_caveat(client):
    data = {g["site"]: g for g in client.get("/api/ghats").json()["data"]}
    assert len(data) == 7
    rani = data["Rani Kamlapati ghat / Kamla Park kund"]
    assert rani["site_match_confidence"] == "medium" and any("two different places" in c for c in rani["caveats"])
    assert {"year": 2025, "festival": "Durga"} in data["Malikhedi kund"]["events_without_table"]


def test_filters(client):
    assert client.get("/api/readings?year=2025").json()["meta"]["total"] == 453
    assert client.get("/api/readings?year=2025&festival=durga").json()["meta"]["total"] == 180
    rows = client.get("/api/readings?site=prempura-ghat&phase=during&parameter=BOD").json()["data"]
    assert rows and all(r["site"] == "Prempura ghat" and r["phase"] == "during" and r["parameter"] == "BOD" for r in rows)
    by_name = client.get("/api/readings", params={"site": "Prempura ghat"}).json()["meta"]["total"]
    assert by_name == client.get("/api/readings?site=prempura-ghat").json()["meta"]["total"]
    assert client.get("/api/readings?year=2023,2024").json()["meta"]["total"] == 1524 - 453


def test_reading_comparisons(client):
    rows = client.get("/api/readings?parameter=Chromium&year=2023").json()["data"]
    assert all(r["comparison"]["status"] == "no_criterion" for r in rows)
    bdl = [r for r in rows if r["measurement_status"] == "below_detection"]
    assert bdl and all(r["value"] is None and r["value_as_printed"] == "BDL" for r in bdl)


def test_summary_bdl_not_zero(client):
    p = client.get("/api/summary?year=2023&parameter=Chromium").json()["data"]["parameters"][0]
    assert (p["measured"], p["below_detection"], p["missing"], p["min"]) == (0, 41, 1, None)


def test_coverage_marks_missing_table(client):
    sites = client.get("/api/coverage?year=2025&festival=Durga").json()["data"]["sites"]
    bair = next(s for s in sites if s["site_id"] == "bairagarh-sant-hirdaram-kund")
    assert bair["events"][0]["status"] == "no_table_in_report" and bair["reported_readings"] == 0


def test_ghat_detail_and_404(client):
    r = client.get("/api/ghats/rani-kamlapati-ghat-kamla-park-kund/readings?festival=Durga")
    assert r.status_code == 200 and r.json()["data"]["assessment"]["readings_compared"] > 0
    r = client.get("/api/ghats/nowhere/readings")
    assert r.status_code == 404 and r.json()["error"]["code"] == "ghat_not_found"


def test_rankings_shape(client):
    rows = client.get("/api/rankings?festival=Durga").json()["data"]["rankings"]
    assert all(r["reasons"] and "readings_missing" in r for r in rows)


def test_brief(client):
    d = client.get("/api/brief?festival=Durga&top=3").json()["data"]
    assert len(d["top_sites"]) == 3
    assert any("\u0900" <= ch <= "\u097F" for ch in d["hi"]["text"])
    assert "health effects" in d["en"]["text"] and "स्वास्थ्य" in d["hi"]["text"]
    assert "hi" not in client.get("/api/brief?lang=en").json()["data"]


def test_errors(client):
    for url, field in [("/api/readings?year=2019", "year"), ("/api/readings?year=abc", "year"),
                       ("/api/readings?phase=later", "phase"), ("/api/readings?site=xyz", "site"),
                       ("/api/readings?parameter=Mercury", "parameter"), ("/api/criteria?cpcb_class=Z", "cpcb_class"),
                       ("/api/brief?top=0", "top"), ("/api/brief?top=abc", "top"), ("/api/brief?lang=fr", "lang"),
                       ("/api/rankings?parameter=Zinc", "parameter")]:
        r = client.get(url)
        assert r.status_code == 400, url
        assert r.json()["error"]["details"]["field"] == field
    r = client.get("/api/readings?festval=Durga")
    assert r.status_code == 400 and r.json()["error"]["code"] == "unknown_query_parameter"
    r = client.get("/api/nope")
    assert r.status_code == 404 and r.json()["error"]["code"] == "not_found"
'''

# =====================================================================  FRONTEND

FILES["frontend/index.html"] = r'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Jal Drishti — ghats that need attention before Durga visarjan</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <h1>Jal Drishti <span lang="hi">जल दृष्टि</span></h1>
      <p>Which immersion ghats need attention before Durga visarjan. Built from MPPCB test reports 2023–2025 and
        compared with CPCB Class B (organised outdoor bathing) limits.</p>
    </div>
    <div class="countdown" id="countdown" aria-live="polite"></div>
  </header>

  <div id="banner" class="banner" role="alert" hidden></div>

  <section class="filters" aria-label="Filters">
    <label>Festival
      <select id="f-festival">
        <option value="Durga" selected>Durga</option>
        <option value="Ganesh">Ganesh</option>
        <option value="">Both festivals</option>
      </select>
    </label>
    <fieldset>
      <legend>Years</legend>
      <div id="f-years" class="years"></div>
    </fieldset>
    <label>Phase
      <select id="f-phase">
        <option value="" selected>All phases</option>
        <option value="during,after">During + 1 week after immersion</option>
        <option value="pre">Before immersion</option>
        <option value="during">During immersion</option>
        <option value="after">1 week after immersion</option>
      </select>
    </label>
    <span id="loading" class="loading" hidden>Loading…</span>
  </section>

  <main>
    <section class="panel" aria-labelledby="summary-h">
      <h2 id="summary-h">At a glance</h2>
      <div id="summary-cards" class="cards"></div>
      <ul id="headlines" class="headlines"></ul>
    </section>

    <div class="layout">
      <section class="panel" aria-labelledby="rank-h">
        <h2 id="rank-h">Ghats ranked by readings outside CPCB Class B</h2>
        <p class="muted" id="rank-scope"></p>
        <p class="muted small">Ranked by how often and how far dissolved oxygen, BOD and pH fall outside the limits.
          Missing readings are never counted as clean.</p>
        <div id="rankings"></div>
        <details id="method" class="method"></details>
      </section>

      <aside class="panel brief" aria-labelledby="brief-h">
        <h2 id="brief-h">Officer brief <span lang="hi">अधिकारी सारांश</span></h2>
        <div class="brief-controls">
          <div class="tabs" role="tablist" aria-label="Brief language">
            <button class="tab" role="tab" data-lang="en" aria-selected="true">English</button>
            <button class="tab" role="tab" data-lang="hi" aria-selected="false" lang="hi">हिंदी</button>
          </div>
          <label>Ghats listed
            <select id="brief-top">
              <option value="3" selected>3</option>
              <option value="5">5</option>
              <option value="7">7</option>
            </select>
          </label>
        </div>
        <h3 id="brief-title" class="brief-title"></h3>
        <div id="brief-body" class="brief-body"></div>
        <div class="brief-actions">
          <button id="copy-brief" class="btn">Copy</button>
          <button id="copy-both" class="btn-secondary">Copy EN + HI</button>
          <button id="download-brief" class="btn-secondary">Download .txt</button>
        </div>
        <p class="muted small">The Hindi text is generated from templates. Please have it checked before forwarding.</p>
      </aside>
    </div>

    <section class="panel" aria-labelledby="cov-h">
      <h2 id="cov-h">Data coverage</h2>
      <p class="muted small">Readings reported out of readings expected, for all 13 parameters, in each test round.
        "No table" means the report has no table for that ghat in that round.</p>
      <div id="coverage"></div>
      <div class="legend">
        <span class="chip cov-complete">Complete</span>
        <span class="chip cov-partial">Some readings missing</span>
        <span class="chip cov-none_reported">Nothing reported</span>
        <span class="chip cov-no_table_in_report">No table in report</span>
      </div>
    </section>

    <section class="panel" aria-labelledby="cav-h">
      <h2 id="cav-h">What this data does not tell you</h2>
      <ul id="caveats" class="caveats"></ul>
    </section>
  </main>

  <dialog id="ghat-dialog" aria-labelledby="ghat-title">
    <div class="dialog-head">
      <h2 id="ghat-title">Ghat readings</h2>
      <button class="btn-close" id="ghat-close" aria-label="Close">×</button>
    </div>
    <div id="ghat-body"></div>
  </dialog>

  <footer>
    Data: MPPCB Ganesh and Durga visarjan reports 2023, 2024 and 2025; CPCB water-quality criteria.
    Source page numbers are PDF pages of that year's report. Compares readings with limits only;
    it does not assess health effects.
  </footer>

  <script src="app.js"></script>
</body>
</html>
'''

FILES["frontend/styles.css"] = r'''
:root {
  --ink: #1d2939; --muted: #667085; --line: #e4e7ec; --bg: #f5f7f8; --panel: #fff;
  --accent: #0e7490; --accent-soft: #e6f4f7;
  --fail: #b42318; --fail-bg: #fef3f2;
  --ok: #067647; --ok-bg: #ecfdf3;
  --miss: #475467; --miss-bg: #f2f4f7;
  --bdl: #5925dc; --bdl-bg: #f4f3ff;
  --warn: #93370d; --warn-bg: #fffaeb;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", "Noto Sans Devanagari",
    "Nirmala UI", Mangal, sans-serif;
  color: var(--ink); background: var(--bg); line-height: 1.5;
}
* { box-sizing: border-box; }
body { margin: 0; }
[lang="hi"] { font-family: "Noto Sans Devanagari", "Nirmala UI", Mangal, system-ui, sans-serif; }
h1, h2, h3 { line-height: 1.25; margin: 0 0 .5rem; }
h2 { font-size: 1.15rem; }
h3 { font-size: 1rem; }
.muted { color: var(--muted); }
.small { font-size: .85rem; }

.topbar { display: flex; gap: 1rem; justify-content: space-between; align-items: center;
  padding: 1rem 1.5rem; background: var(--accent); color: #fff; }
.topbar h1 { font-size: 1.5rem; }
.topbar h1 span { font-weight: 500; opacity: .9; margin-left: .4rem; }
.topbar p { margin: .25rem 0 0; max-width: 60ch; opacity: .95; }
.countdown { text-align: right; white-space: nowrap; }
.countdown strong { font-size: 2rem; display: block; line-height: 1; }
.countdown span { display: block; font-size: .85rem; opacity: .9; }

.banner { margin: 1rem 1.5rem 0; padding: .75rem 1rem; border-radius: 8px;
  background: var(--fail-bg); color: var(--fail); border: 1px solid #fecdca; }

.filters { display: flex; flex-wrap: wrap; gap: 1rem 1.5rem; align-items: flex-end;
  padding: 1rem 1.5rem; background: var(--panel); border-bottom: 1px solid var(--line);
  position: sticky; top: 0; z-index: 5; }
.filters label, .brief-controls label, .dialog-filters label { display: flex; flex-direction: column;
  font-size: .85rem; color: var(--muted); gap: .25rem; }
.filters fieldset { border: 0; padding: 0; margin: 0; }
.filters legend { font-size: .85rem; color: var(--muted); margin-bottom: .25rem; }
.years { display: flex; gap: .75rem; }
.chk { flex-direction: row !important; align-items: center; gap: .35rem !important; color: var(--ink) !important; }
select { font: inherit; padding: .4rem .5rem; border: 1px solid #d0d5dd; border-radius: 6px;
  background: #fff; color: var(--ink); }
.loading { color: var(--accent); font-weight: 600; }

main { padding: 1rem 1.5rem 2rem; display: grid; gap: 1rem; }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 1rem 1.25rem; }
.layout { display: grid; grid-template-columns: minmax(0, 2fr) minmax(300px, 1fr); gap: 1rem; align-items: start; }
.brief { position: sticky; top: 5.5rem; }

.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: .75rem; }
.card { border: 1px solid var(--line); border-radius: 8px; padding: .75rem; }
.card-label { font-size: .8rem; color: var(--muted); text-transform: uppercase; letter-spacing: .03em; }
.card-value { font-size: 1.6rem; font-weight: 700; }
.card-sub { font-size: .8rem; color: var(--muted); }
.headlines { margin: .75rem 0 0; padding-left: 1.2rem; }

.ghat-card { border: 1px solid var(--line); border-radius: 10px; padding: 1rem; margin-bottom: .9rem; }
.ghat-card.unranked { background: var(--miss-bg); }
.ghat-card header { display: grid; grid-template-columns: auto 1fr auto; gap: 1rem; align-items: start; }
.rank { width: 2.4rem; height: 2.4rem; border-radius: 50%; background: var(--accent); color: #fff;
  display: grid; place-items: center; font-weight: 700; font-size: 1.1rem; }
.unranked .rank { background: var(--miss); }
.ghat-name h3 { margin: 0; font-size: 1.05rem; }
.ghat-name p { margin: 0; }
.hi { color: var(--ink); }
.score { min-width: 150px; text-align: right; }
.score-num { font-size: 1.4rem; font-weight: 700; }
.score-num small { font-size: .8rem; color: var(--muted); font-weight: 400; }
.bar { height: 6px; background: var(--line); border-radius: 3px; overflow: hidden; margin: .25rem 0; }
.bar span { display: block; height: 100%; background: var(--fail); }

.chips { display: flex; flex-wrap: wrap; gap: .4rem; margin: .75rem 0 .25rem; }
.chip { display: inline-block; padding: .15rem .55rem; border-radius: 999px; font-size: .8rem;
  border: 1px solid transparent; white-space: nowrap; }
.chip-fail { background: var(--fail-bg); color: var(--fail); border-color: #fecdca; }
.chip-ok { background: var(--ok-bg); color: var(--ok); border-color: #abefc6; }
.chip-missing { background: var(--miss-bg); color: var(--miss); border: 1px dashed #98a2b3; }
.chip-bdl { background: var(--bdl-bg); color: var(--bdl); border-color: #d9d6fe; }
.chip-none { background: #fff; color: var(--muted); border-color: var(--line); }

.warn { background: var(--warn-bg); color: var(--warn); border-radius: 6px; padding: .5rem .75rem;
  font-size: .9rem; margin: .5rem 0; }
.reasons { margin: .5rem 0; padding-left: 1.2rem; }
.reasons li { margin-bottom: .25rem; }
.card-caveats { margin: .5rem 0; padding-left: 1.2rem; font-size: .85rem; color: var(--warn); }
.evidence summary, .method summary { cursor: pointer; color: var(--accent); font-weight: 600; margin: .5rem 0; }
.method p { margin: .4rem 0; font-size: .9rem; }

.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: .88rem; }
th, td { text-align: left; padding: .4rem .5rem; border-bottom: 1px solid var(--line); vertical-align: top; }
thead th { background: #f9fafb; font-weight: 600; white-space: nowrap; }
.unit { color: var(--muted); font-size: .8rem; }

.btn, .btn-secondary { font: inherit; border-radius: 6px; padding: .45rem .9rem; cursor: pointer; }
.btn { background: var(--accent); color: #fff; border: 1px solid var(--accent); }
.btn-secondary { background: #fff; color: var(--accent); border: 1px solid #b2dde5; }
.btn:hover, .btn-secondary:hover { filter: brightness(.95); }
.link { background: none; border: 0; padding: 0; font: inherit; color: var(--accent); cursor: pointer;
  text-align: left; text-decoration: underline; }
a { color: var(--accent); }

.brief-controls { display: flex; justify-content: space-between; align-items: flex-end; gap: .75rem; margin-bottom: .75rem; }
.tabs { display: flex; border: 1px solid #d0d5dd; border-radius: 6px; overflow: hidden; }
.tab { font: inherit; border: 0; background: #fff; padding: .4rem .9rem; cursor: pointer; color: var(--ink); }
.tab[aria-selected="true"] { background: var(--accent); color: #fff; }
.brief-title { font-size: .95rem; }
.brief-body { font-size: .92rem; max-height: 60vh; overflow-y: auto; border: 1px solid var(--line);
  border-radius: 8px; padding: .5rem .75rem; background: #fcfcfd; }
.brief-body p { margin: .4rem 0; }
.brief-actions { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: .75rem; }

.cov { text-align: center; white-space: nowrap; }
.cov-complete { background: #d1fadf; }
.cov-partial { background: #fef0c7; }
.cov-none_reported, .cov-no_table_in_report {
  background: repeating-linear-gradient(45deg, #f2f4f7, #f2f4f7 6px, #e4e7ec 6px, #e4e7ec 12px); color: var(--miss); }
.cov-na { color: var(--muted); }
.legend { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: .75rem; }
.legend .chip { color: var(--ink); }
.caveats { padding-left: 1.2rem; margin: 0; }
.caveats li { margin-bottom: .3rem; }

dialog { width: min(1100px, 95vw); max-height: 90vh; border: 0; border-radius: 12px; padding: 0; }
dialog::backdrop { background: rgba(16, 24, 40, .5); }
.dialog-head { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--line); position: sticky; top: 0; background: #fff; }
#ghat-body { padding: 1rem 1.25rem; }
.btn-close { font-size: 1.6rem; line-height: 1; background: none; border: 0; cursor: pointer; color: var(--muted); }
.dialog-filters { display: flex; flex-wrap: wrap; gap: 1rem; align-items: flex-end; margin-bottom: .75rem; }

footer { padding: 1rem 1.5rem 2rem; color: var(--muted); font-size: .85rem; }

@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .brief { position: static; }
  .ghat-card header { grid-template-columns: auto 1fr; }
  .score { grid-column: 1 / -1; text-align: left; }
  .filters { position: static; }
}
@media print {
  .filters, .brief-actions, .btn-secondary, .tabs, footer, .topbar .countdown { display: none !important; }
  body { background: #fff; }
  .layout { grid-template-columns: 1fr; }
  .brief-body { max-height: none; }
}
'''

FILES["frontend/app.js"] = r'''
"use strict";

/* Jal Drishti dashboard. Talks only to the local Jal Drishti API (no government systems). */

const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];
const esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const num = (v) => (v == null ? "—" : String(Number(Number(v).toFixed(3))));

// API location: ?api=http://host:port overrides; same origin when served by the backend;
// localhost:8000 when index.html is opened directly from disk.
const API_BASE = (() => {
  const fromQuery = new URLSearchParams(location.search).get("api");
  if (fromQuery) return fromQuery.replace(/\/+$/, "");
  if (window.JAL_API_BASE) return String(window.JAL_API_BASE).replace(/\/+$/, "");
  if (location.protocol === "file:") return "http://localhost:8000";
  return "";
})();

const VISARJAN_DATE = new Date("2026-10-20T00:00:00+05:30"); // Durga visarjan date from the participant guide
const SHORT = { "Dissolved oxygen": "DO", BOD: "BOD", pH: "pH", Conductivity: "Conductivity" };
const PHASE = { pre: "Before", during: "During", after: "1 week after" };

const state = { allYears: [], brief: null, lang: "en", top: 3, ghat: null, loadSeq: 0 };

/* ---------- API ---------- */

async function api(path, params = {}) {
  const qs = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) if (v !== "" && v != null) qs.set(k, v);
  const query = qs.toString();
  const url = `${API_BASE}${path}${query ? `?${query}` : ""}`;
  let res;
  try {
    res = await fetch(url, { headers: { Accept: "application/json" } });
  } catch {
    throw new Error(`Cannot reach the Jal Drishti API at ${API_BASE || location.origin}. Is the backend running?`);
  }
  let body;
  try {
    body = await res.json();
  } catch {
    throw new Error(`Unexpected response (${res.status}) from ${path}.`);
  }
  if (!res.ok) {
    const err = body.error || (body.data && body.data.error) || {};
    throw new Error(err.message || `Request to ${path} failed (${res.status}).`);
  }
  return body;
}

/* ---------- helpers ---------- */

function showError(msg) { const b = $("#banner"); b.textContent = msg; b.hidden = false; }
function clearError() { $("#banner").hidden = true; }
function setLoading(on) {
  $("#loading").hidden = !on;
  document.body.setAttribute("aria-busy", on ? "true" : "false");
}

function currentParams() {
  const checked = $$("#f-years input:checked").map((i) => i.value);
  const params = { festival: $("#f-festival").value, phase: $("#f-phase").value };
  if (checked.length && checked.length < state.allYears.length) params.year = checked.join(",");
  return { params, noYears: checked.length === 0 };
}

function sourceLink(src) {
  if (!src || !src.page) return "—";
  const title = esc(src.report || "Source report");
  if (!src.url) return `<span title="${title}">p. ${src.page}</span>`;
  return `<a href="${esc(`${src.url}#page=${src.page}`)}" target="_blank" rel="noopener" title="${title}">p. ${src.page}</a>`;
}

function valueCell(r) {
  if (r.measurement_status === "measured") {
    return `${num(r.value)}${r.unit_assumed ? ` <span class="unit">${esc(r.unit_assumed)}*</span>` : ""}`;
  }
  if (r.measurement_status === "below_detection") {
    return `<span class="chip chip-bdl" title="Below detection limit: very low, not zero">${esc(r.value_as_printed.trim() || "BDL")}</span>`;
  }
  const printed = r.value_as_printed.trim();
  return `<span class="chip chip-missing" title="Not sampled. Not treated as clean">Missing${printed ? ` (“${esc(printed)}”)` : ""}</span>`;
}

function limitText(cmp) {
  const c = cmp && cmp.criterion;
  if (!c) return "—";
  const op = { min: "≥ ", max: "≤ ", range: "" }[c.limit_type] || "";
  return `${op}${esc(c.limit)}${c.unit ? ` ${esc(c.unit)}` : ""}`;
}

function statusChip(r) {
  const c = r.comparison || {};
  const cls = c.criterion ? c.criterion.cpcb_class : "B";
  switch (c.status) {
    case "meets": return `<span class="chip chip-ok">Meets Class ${esc(cls)}</span>`;
    case "does_not_meet": return `<span class="chip chip-fail">Outside Class ${esc(cls)}</span>`;
    case "missing": return `<span class="chip chip-missing">Not compared (missing)</span>`;
    case "not_compared": return `<span class="chip chip-bdl">Not compared (BDL)</span>`;
    default: return `<span class="chip chip-none">No limit set</span>`;
  }
}

function paramChip(p) {
  const label = SHORT[p.parameter] || p.parameter;
  const c = p.criterion;
  if (p.compared === 0) return `<span class="chip chip-missing">${esc(label)}: no readings (${p.missing} missing)</span>`;
  const unit = c.unit ? ` ${c.unit}` : "";
  const dir = c.limit_type === "min" ? `below ${num(c.lower)}${unit}`
    : c.limit_type === "max" ? `above ${num(c.upper)}${unit}`
    : `outside ${num(c.lower)}–${num(c.upper)}`;
  const missing = p.missing ? ` · ${p.missing} missing` : "";
  return `<span class="chip ${p.does_not_meet ? "chip-fail" : "chip-ok"}" title="${esc(c.description)}">` +
    `${esc(label)} ${esc(dir)}: ${p.does_not_meet} of ${p.compared}${esc(missing)}</span>`;
}

/* ---------- renderers ---------- */

function renderCountdown() {
  const days = Math.ceil((VISARJAN_DATE - new Date()) / 86400000);
  const when = "Durga visarjan: 20 October 2026";
  $("#countdown").innerHTML = days > 0
    ? `<strong>${days}</strong><span>day${days === 1 ? "" : "s"} to go</span><span>${when}</span>`
    : `<span>${when}</span>`;
}

function renderSummary(d) {
  const cov = d.coverage;
  const b = cov.missing_breakdown;
  const cards = [
    ["Ghats in view", d.scope.sites.length, `${d.scope.events.length} festival test round(s)`],
    ["Readings reported", `${cov.reported_readings} / ${cov.expected_readings}`,
      `${Math.round((cov.coverage_ratio || 0) * 100)}% of expected readings`],
    ["Missing readings", cov.missing,
      `${b.not_sampled} not sampled · ${b.no_table_for_site} no table · ${b.row_absent} not printed`],
    ["Below detection (BDL)", d.counts.below_detection, "Very low, but not zero and not missing"],
  ];
  $("#summary-cards").innerHTML = cards.map(([t, v, s]) =>
    `<div class="card"><div class="card-label">${esc(t)}</div><div class="card-value">${esc(v)}</div>` +
    `<div class="card-sub">${esc(s)}</div></div>`).join("");
  $("#headlines").innerHTML = d.headlines.length
    ? d.headlines.map((h) => `<li>${esc(h)}</li>`).join("")
    : "<li>No readings with a CPCB limit in this selection.</li>";
}

function evidenceTable(rows) {
  return `<div class="table-wrap"><table><thead><tr><th>Round</th><th>Phase</th><th>Parameter</th>` +
    `<th>Value</th><th>Limit</th><th>Explanation</th><th>Source</th></tr></thead><tbody>` +
    rows.map((r) => `<tr><td>${esc(r.festival)} ${r.year}</td><td>${esc(PHASE[r.phase])}</td>` +
      `<td>${esc(r.parameter)}</td><td>${valueCell(r)}</td><td>${limitText(r.comparison)}</td>` +
      `<td>${esc(r.comparison && r.comparison.explanation)}</td><td>${sourceLink(r.source)}</td></tr>`).join("") +
    `</tbody></table></div>`;
}

function rankCard(r) {
  const pct = r.score == null ? 0 : Math.min(100, (r.score / 2) * 100);
  let warn = "";
  if (!r.assessable) {
    warn = `<p class="warn">Not ranked: no comparable readings in this selection. This is not evidence that the water meets the criteria.</p>`;
  } else if (r.low_coverage_warning) {
    warn = `<p class="warn">Limited data: ${r.readings_compared} of ${r.readings_expected} expected readings (${esc(r.coverage_level)} coverage). ` +
      `Missing readings are not treated as clean, so this result is less certain.</p>`;
  }
  const evidence = r.evidence.length
    ? `<details class="evidence"><summary>Evidence: ${r.evidence.length} readings furthest outside the limits</summary>${evidenceTable(r.evidence)}</details>`
    : "";
  const caveats = r.caveats.length
    ? `<ul class="card-caveats">${r.caveats.map((c) => `<li>${esc(c)}</li>`).join("")}</ul>` : "";
  return `<article class="ghat-card${r.assessable ? "" : " unranked"}">
    <header>
      <div class="rank" aria-label="Rank ${r.rank ?? "none"}">${r.rank ?? "—"}</div>
      <div class="ghat-name">
        <h3>${esc(r.site)}</h3>
        <p class="hi" lang="hi">${esc(r.name_hi)}</p>
        <p class="muted small">${esc(r.water_body)} · site match: ${esc(r.site_match_confidence)}</p>
      </div>
      <div class="score" title="Score 0–2: mean points per compared reading (see 'How the ranking works')">
        <div class="score-num">${r.score == null ? "—" : num(r.score)}<small> / 2</small></div>
        <div class="bar"><span style="width:${pct}%"></span></div>
        <div class="muted small">${r.readings_outside_criteria} of ${r.readings_compared} readings outside limits</div>
      </div>
    </header>
    <div class="chips">${r.parameters.map(paramChip).join("")}</div>
    ${warn}
    <ul class="reasons">${r.reasons.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>
    ${evidence}${caveats}
    <button class="btn-secondary" data-site="${esc(r.site_id)}">All readings for this ghat</button>
  </article>`;
}

function renderMethod(m) {
  $("#method").innerHTML = `<summary>How the ranking works</summary>
    <p>${esc(m.score)}</p><p>${esc(m.phases)}</p><p>${esc(m.missing_data)}</p>
    <p>Ties are broken by: ${esc(m.tie_break.join(" → "))}.</p>
    <p>Not used in the score (no Class ${esc(m.cpcb_class)} limit): ${esc(m.not_scored.join(", "))}.</p>`;
}

function renderRankings(d, scopeLabel) {
  $("#rank-scope").textContent = scopeLabel ? `Selection: ${scopeLabel}.` : "";
  $("#rankings").innerHTML = d.rankings.length ? d.rankings.map(rankCard).join("") : "<p>No ghats in this selection.</p>";
  renderMethod(d.method);
}

function renderCoverage(d) {
  const events = d.scope.events;
  const head = events.map((e) => `<th>${esc(e.festival)} ${e.year}</th>`).join("");
  const rows = d.sites.map((s) => {
    const byKey = Object.fromEntries(s.events.map((e) => [`${e.year}-${e.festival}`, e]));
    const cells = events.map((e) => {
      const ev = byKey[`${e.year}-${e.festival}`];
      if (!ev) return `<td class="cov cov-na">—</td>`;
      const b = ev.missing_breakdown;
      const tip = `${ev.reported_readings} of ${ev.expected_readings} reported. Missing: ${b.not_sampled} not sampled, ` +
        `${b.no_table_for_site} no table, ${b.row_absent} not printed. BDL: ${ev.below_detection}.`;
      const label = ev.status === "no_table_in_report" ? "No table" : `${ev.reported_readings}/${ev.expected_readings}`;
      return `<td class="cov cov-${esc(ev.status)}" title="${esc(tip)}">${label}</td>`;
    }).join("");
    return `<tr><th scope="row"><button class="link" data-site="${esc(s.site_id)}">${esc(s.site)}</button></th>${cells}` +
      `<td>${s.reported_readings}/${s.expected_readings} (${Math.round((s.coverage_ratio || 0) * 100)}%)</td></tr>`;
  }).join("");
  $("#coverage").innerHTML = `<div class="table-wrap"><table><thead><tr><th>Ghat</th>${head}<th>Total</th></tr></thead>` +
    `<tbody>${rows}</tbody></table></div>`;
}

function renderBrief() {
  const b = state.brief;
  if (!b) return;
  const part = b[state.lang];
  $("#brief-title").textContent = part.title;
  const body = $("#brief-body");
  body.lang = state.lang;
  body.innerHTML = part.lines.map((l) => `<p>${esc(l)}</p>`).join("");
  $$(".tab").forEach((t) => t.setAttribute("aria-selected", String(t.dataset.lang === state.lang)));
}

function renderCaveats(list) {
  $("#caveats").innerHTML = [...new Set(list)].map((c) => `<li>${esc(c)}</li>`).join("");
}

/* ---------- ghat detail dialog ---------- */

async function openGhat(siteId) {
  const dlg = $("#ghat-dialog");
  const { params } = currentParams();
  $("#ghat-title").textContent = "Loading…";
  $("#ghat-body").innerHTML = "<p>Loading readings…</p>";
  if (!dlg.open) dlg.showModal();
  try {
    const res = await api(`/api/ghats/${encodeURIComponent(siteId)}/readings`, params);
    renderGhat(res.data);
  } catch (e) {
    $("#ghat-title").textContent = "Could not load ghat";
    $("#ghat-body").innerHTML = `<p class="banner">${esc(e.message)}</p>`;
  }
}

function renderGhat(d) {
  state.ghat = d;
  const g = d.ghat;
  const a = d.assessment;
  const params = [...new Set(d.readings.map((r) => r.parameter))];
  $("#ghat-title").textContent = g.site;
  $("#ghat-body").innerHTML = `
    <p class="hi" lang="hi">${esc(g.name_hi)}</p>
    <p class="muted small">${esc(g.water_body)} · site match: ${esc(g.site_match_confidence)} ·
      printed in reports as: ${g.names_as_printed.map(esc).join(" | ")}</p>
    ${g.caveats.length ? `<ul class="card-caveats">${g.caveats.map((c) => `<li>${esc(c)}</li>`).join("")}</ul>` : ""}
    ${a ? `<h3>Against CPCB Class B (this selection)</h3>
      <div class="chips">${a.parameters.map(paramChip).join("")}</div>
      <ul class="reasons">${a.reasons.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
    <h3>Coverage by test round</h3>
    <div class="chips">${d.coverage.events.map((e) =>
      `<span class="chip cov-${esc(e.status)}">${esc(e.festival)} ${e.year}: ${e.status === "no_table_in_report"
        ? "no table in report" : `${e.reported_readings}/${e.expected_readings} reported`}</span>`).join("")}</div>
    <h3>Readings</h3>
    <div class="dialog-filters">
      <label>Parameter
        <select id="g-param"><option value="">All parameters</option>
          ${params.map((p) => `<option value="${esc(p)}">${esc(p)}</option>`).join("")}</select>
      </label>
      <label class="chk"><input type="checkbox" id="g-flagged"> Only readings outside limits or missing</label>
    </div>
    <div id="g-table"></div>
    <p class="muted small">* Units are assumed because the reports print none. BDL = below detection limit (very low, not zero).</p>`;
  $("#g-param").addEventListener("change", renderGhatTable);
  $("#g-flagged").addEventListener("change", renderGhatTable);
  renderGhatTable();
}

function renderGhatTable() {
  const d = state.ghat;
  if (!d) return;
  const p = $("#g-param").value;
  const flagged = $("#g-flagged").checked;
  const rows = d.readings.filter((r) => (!p || r.parameter === p) &&
    (!flagged || r.measurement_status === "missing" || (r.comparison && r.comparison.status === "does_not_meet")));
  $("#g-table").innerHTML = rows.length
    ? `<div class="table-wrap"><table><thead><tr><th>Round</th><th>Phase</th><th>Parameter</th><th>Value</th>` +
      `<th>Status</th><th>Explanation</th><th>Source</th></tr></thead><tbody>` +
      rows.map((r) => `<tr><td>${esc(r.festival)} ${r.year}</td><td>${esc(PHASE[r.phase])}</td>` +
        `<td>${esc(r.parameter)}${r.parameter_as_printed && r.parameter_as_printed !== r.parameter
          ? ` <span class="unit">(${esc(r.parameter_as_printed)})</span>` : ""}</td>` +
        `<td>${valueCell(r)}</td><td>${statusChip(r)}</td>` +
        `<td>${esc(r.comparison && r.comparison.explanation)}</td><td>${sourceLink(r.source)}</td></tr>`).join("") +
      `</tbody></table></div>`
    : "<p>No readings match these filters.</p>";
}

/* ---------- actions ---------- */

async function copyText(text, buttonSel) {
  if (!text) return;
  const btn = $(buttonSel);
  const original = btn.textContent;
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
  }
  btn.textContent = "Copied ✓";
  setTimeout(() => { btn.textContent = original; }, 1500);
}

function downloadBrief() {
  const b = state.brief;
  if (!b) return;
  const text = `${b.en.text}\n\n${b.hi.text}\n`;
  const url = URL.createObjectURL(new Blob([text], { type: "text/plain;charset=utf-8" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = `jal-drishti-brief-${new Date().toISOString().slice(0, 10)}.txt`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

/* ---------- loading ---------- */

async function load() {
  const { params, noYears } = currentParams();
  if (noYears) { showError("Select at least one year."); return; }
  clearError();
  const seq = ++state.loadSeq;
  setLoading(true);
  try {
    const [summary, rankings, coverage, brief] = await Promise.all([
      api("/api/summary", params),
      api("/api/rankings", params),
      api("/api/coverage", params),
      api("/api/brief", { ...params, top: state.top }),
    ]);
    if (seq !== state.loadSeq) return; // a newer filter change is in flight
    state.brief = brief.data;
    renderSummary(summary.data);
    renderRankings(rankings.data, brief.data.scope.label_en);
    renderCoverage(coverage.data);
    renderBrief();
    renderCaveats(rankings.meta.caveats);
  } catch (e) {
    if (seq === state.loadSeq) showError(e.message);
  } finally {
    if (seq === state.loadSeq) setLoading(false);
  }
}

async function loadBrief() {
  const { params, noYears } = currentParams();
  if (noYears) return;
  try {
    const b = await api("/api/brief", { ...params, top: state.top });
    state.brief = b.data;
    renderBrief();
  } catch (e) {
    showError(e.message);
  }
}

function bindEvents() {
  $("#f-festival").addEventListener("change", load);
  $("#f-phase").addEventListener("change", load);
  $("#brief-top").addEventListener("change", (e) => { state.top = Number(e.target.value); loadBrief(); });
  $$(".tab").forEach((t) => t.addEventListener("click", () => { state.lang = t.dataset.lang; renderBrief(); }));
  $("#copy-brief").addEventListener("click", () => copyText(state.brief && state.brief[state.lang].text, "#copy-brief"));
  $("#copy-both").addEventListener("click", () =>
    state.brief && copyText(`${state.brief.en.text}\n\n${state.brief.hi.text}`, "#copy-both"));
  $("#download-brief").addEventListener("click", downloadBrief);
  const dlg = $("#ghat-dialog");
  $("#ghat-close").addEventListener("click", () => dlg.close());
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-site]");
    if (btn) openGhat(btn.dataset.site);
  });
}

async function init() {
  renderCountdown();
  bindEvents();
  try {
    const health = await api("/api/health");
    state.allYears = [...new Set(health.data.events.map((e) => e.year))].sort();
    $("#f-years").innerHTML = state.allYears.map((y) =>
      `<label class="chk"><input type="checkbox" value="${y}" checked> ${y}</label>`).join("");
    $("#f-years").addEventListener("change", load);
  } catch (e) {
    showError(e.message);
    return;
  }
  load();
}

document.addEventListener("DOMContentLoaded", init);
'''

# =====================================================================  WRITER


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv[1:]
    root = Path(args[0] if args else "jal-drishti").resolve()

    existing = [rel for rel in FILES if (root / rel).exists()]
    if existing and not force:
        print(f"These files already exist in {root}:")
        for rel in existing:
            print(f"  {rel}")
        print("Nothing was written. Re-run with --force to overwrite them.")
        sys.exit(1)

    for rel, content in FILES.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.lstrip("\n"), encoding="utf-8")
        print(f"wrote  {rel}")

    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    print("made   data/  (empty)")

    print(f"""
Done. Project created in: {root}

Next steps:
  1. Copy these two files into {data_dir}:
       bhopal_ghats_2023_2025.csv
       cpcb_water_quality_criteria.csv
  2. cd "{root / 'backend'}"
  3. python -m pip install -r requirements.txt
  4. python run.py
  5. Open http://localhost:8000/   (API docs: http://localhost:8000/docs)

Tests: python -m pytest   (tests that need the real data are skipped until the CSVs are in data/)
""")


if __name__ == "__main__":
    main()