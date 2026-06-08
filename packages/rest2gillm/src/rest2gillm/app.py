"""FastAPI REST adapter for dsl2gillm."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dsl2gillm.bus import dispatch
from dsl2gillm.events import EventStore
from dsl2gillm.pb_codec import encode_result_protobuf
from dsl2gillm.schema_registry import schema_for_verb, validate_schemas
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response


def create_app() -> FastAPI:
    app = FastAPI(title="rest2gillm", version="0.1.0")

    @app.get("/")
    def root() -> dict[str, Any]:
        return {
            "service": "rest2gillm",
            "health": "/health",
            "dsl": "POST /v1/dsl  (text/plain | application/json | application/x-protobuf)",
            "schema": "GET /v1/schema/{verb}",
            "events": "GET /v1/events?file=.",
            "proto": "GET /v1/proto",
            "example": "curl -X POST http://127.0.0.1:8220/v1/dsl -d HEALTH",
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/v1/schema/{verb}")
    def get_schema(verb: str) -> dict[str, Any]:
        return schema_for_verb(verb)

    @app.get("/v1/schema")
    def validate_all() -> dict[str, Any]:
        errors = validate_schemas()
        return {"ok": not errors, "errors": errors}

    async def _handle(request: Request, default_file: str = "") -> Response:
        content_type = request.headers.get("content-type", "text/plain").split(";")[0].strip()
        body = await request.body()
        file_arg = default_file or None
        if content_type == "application/x-protobuf":
            result = dispatch(body, default_file=file_arg)
            return Response(encode_result_protobuf(result), media_type="application/x-protobuf")
        if content_type == "application/json":
            payload = json.loads(body.decode("utf-8"))
            result = dispatch(payload, default_file=file_arg)
            return JSONResponse(result.to_dict())
        line = body.decode("utf-8").strip()
        result = dispatch(line, default_file=file_arg)
        return JSONResponse(result.to_dict())

    @app.post("/v1/dsl")
    async def post_dsl(request: Request, file: str = "") -> Response:
        return await _handle(request, default_file=file)

    @app.post("/v1/commands")
    async def post_commands(request: Request, file: str = "") -> Response:
        return await _handle(request, default_file=file)

    @app.get("/v1/events")
    def get_events(file: str = ".") -> JSONResponse:
        store = EventStore.for_workdir(Path(file))
        events = [event.to_dict() for event in store.read_all()]
        return JSONResponse(events)

    @app.get("/v1/proto")
    def get_proto() -> Response:
        proto_dir = Path(__file__).resolve().parents[3] / "dsl2gillm" / "proto" / "dsl2gillm" / "v1"
        parts = []
        for name in ("command.proto", "result.proto"):
            path = proto_dir / name
            if path.is_file():
                parts.append(path.read_text(encoding="utf-8"))
        return Response("\n\n".join(parts) or 'syntax = "proto3";\n', media_type="text/plain")

    return app


app = create_app()
