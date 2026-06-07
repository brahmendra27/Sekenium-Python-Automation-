"""FastAPI application for the Test Results Dashboard."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from dashboard.config import load_config
from dashboard.db import Database
from dashboard.error_classifier import (
    classify_failure,
    classify_flaky,
    classify_skip,
    normalize_error_message,
)
from dashboard.flaky_detector import FlakyDetector
from dashboard.ingester import IngestionError, ReportIngester
from dashboard.models import (
    FlakyTest,
    IngestResult,
    RunDetail,
    RunSummary,
    TestResult,
    TrendPoint,
)

logger = logging.getLogger(__name__)

config = load_config()
db = Database(config.db_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    db.initialize()
    logger.info(
        f"Dashboard started: host={config.host}, port={config.port}, "
        f"db_path={config.db_path}, lookback_runs={config.lookback_runs}"
    )
    yield


app = FastAPI(title="Test Results Dashboard", lifespan=lifespan)


# --- API Routes ---


class IngestRequest(BaseModel):
    """Request body for the ingest endpoint."""

    file_path: str


@app.get("/api/runs", response_model=list[RunSummary])
async def get_runs(limit: int = Query(default=20, ge=1)):
    """Get recent test runs ordered by timestamp descending."""
    return db.get_runs(limit=limit)


@app.get("/api/runs/{run_id}", response_model=RunDetail)
async def get_run_detail(run_id: str):
    """Get full details for a specific test run."""
    detail = db.get_run_detail(run_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
    return detail


@app.get("/api/trends", response_model=list[TrendPoint])
async def get_trends(limit: int = Query(default=20, ge=1)):
    """Get trend data for the last N runs."""
    return db.get_trends(limit=limit)


@app.get("/api/flaky", response_model=list[FlakyTest])
async def get_flaky():
    """Get list of flaky tests based on outcome flip detection."""
    history = db.get_test_history(lookback=config.lookback_runs)
    detector = FlakyDetector()
    return detector.detect(history)


@app.get("/api/slowest", response_model=list[TestResult])
async def get_slowest(limit: int = Query(default=10, ge=1)):
    """Get the slowest tests from the latest run."""
    runs = db.get_runs(limit=1)
    if not runs:
        return []
    return db.get_slowest_tests(runs[0].run_id, limit=limit)


@app.post("/api/ingest", response_model=IngestResult)
async def ingest_report(request: IngestRequest):
    """Ingest a pytest-json-report file into the database."""
    ingester = ReportIngester()
    try:
        result = ingester.ingest(request.file_path, db)
        return result
    except IngestionError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/failures")
async def get_failure_summary():
    """Get failure summary with tests grouped by cause and error message.

    Returns KPI tiles (failed/flaky/skipped with sub-categories),
    error groups (tests grouped by normalized error message), and
    a detailed test list with classification metadata.
    """
    runs = db.get_runs(limit=1)
    if not runs:
        return {"kpi": {}, "error_groups": [], "tests": []}

    latest_run = runs[0]
    detail = db.get_run_detail(latest_run.run_id)
    if not detail:
        return {"kpi": {}, "error_groups": [], "tests": []}

    # Classify all tests
    failed_tests = []
    flaky_tests_list = []
    skipped_tests = []

    # Get flaky test node IDs from detector
    history = db.get_test_history(lookback=config.lookback_runs)
    detector = FlakyDetector()
    flaky_detected = {ft.nodeid for ft in detector.detect(history)}

    for test in detail.tests:
        classification = {
            "nodeid": test.nodeid,
            "outcome": test.outcome,
            "duration": test.duration,
            "domain": test.domain,
            "error_message": test.error_message,
            "longrepr": test.longrepr,
        }

        if test.nodeid in flaky_detected:
            classification["category"] = classify_flaky(
                test.error_message, test.longrepr
            )
            classification["status"] = "flaky"
            flaky_tests_list.append(classification)
        elif test.outcome == "failed":
            classification["category"] = classify_failure(
                test.error_message, test.longrepr
            )
            classification["status"] = "failed"
            failed_tests.append(classification)
        elif test.outcome == "skipped":
            classification["category"] = classify_skip(
                test.error_message, test.longrepr
            )
            classification["status"] = "skipped"
            skipped_tests.append(classification)

    # Build KPI tiles with sub-category counts
    failed_categories = {}
    for t in failed_tests:
        cat = t["category"]
        failed_categories[cat] = failed_categories.get(cat, 0) + 1

    flaky_categories = {}
    for t in flaky_tests_list:
        cat = t["category"]
        flaky_categories[cat] = flaky_categories.get(cat, 0) + 1

    skipped_categories = {}
    for t in skipped_tests:
        cat = t["category"]
        skipped_categories[cat] = skipped_categories.get(cat, 0) + 1

    kpi = {
        "failed": {
            "total": len(failed_tests),
            "categories": failed_categories,
        },
        "flaky": {
            "total": len(flaky_tests_list),
            "categories": flaky_categories,
        },
        "skipped": {
            "total": len(skipped_tests),
            "categories": skipped_categories,
        },
        "passed": detail.run.passed,
        "total": detail.run.total,
        "pass_rate": detail.run.pass_rate,
        "duration": detail.run.duration,
        "duration_display": detail.run.duration_display,
        "created_display": detail.run.created_display,
    }

    # Build error groups (group failed + flaky by normalized error message)
    error_groups_map: dict[str, dict] = {}
    for t in failed_tests + flaky_tests_list:
        normalized = normalize_error_message(t["error_message"])
        if normalized not in error_groups_map:
            error_groups_map[normalized] = {
                "error": normalized,
                "category": t["category"],
                "count": 0,
                "tests": [],
            }
        error_groups_map[normalized]["count"] += 1
        error_groups_map[normalized]["tests"].append(t)

    # Sort by count descending
    error_groups = sorted(
        error_groups_map.values(), key=lambda g: g["count"], reverse=True
    )

    # Combine all classified tests for detailed table
    all_tests = failed_tests + flaky_tests_list + skipped_tests

    return {
        "kpi": kpi,
        "error_groups": error_groups,
        "tests": all_tests,
    }


# --- Static Files and Dashboard UI ---

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/")
async def serve_dashboard():
    """Serve the dashboard HTML page."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard UI not found")
    return FileResponse(index_path, media_type="text/html")


@app.get("/failures")
async def serve_failure_summary():
    """Serve the failure summary HTML page."""
    failure_path = STATIC_DIR / "failure-summary.html"
    if not failure_path.exists():
        raise HTTPException(
            status_code=404, detail="Failure Summary UI not found"
        )
    return FileResponse(failure_path, media_type="text/html")


# Mount static files for any additional assets
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
