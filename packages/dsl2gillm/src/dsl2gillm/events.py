"""Append-only event store for dsl2gillm commands (protobuf + jsonl)."""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

from dsl2gillm.pb_codec import encode_protobuf, envelope_to_dict, result_to_pb
from dsl2gillm.result import DslResult
from dsl2gillm.v1 import result_pb2

StoreFormat = Literal["protobuf", "jsonl"]


@dataclass(frozen=True)
class StoredEvent:
    id: str
    ts_unix: int
    command: dict[str, Any]
    result: dict[str, Any]
    correlation_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EventStore:
    def __init__(self, path: Path, *, fmt: StoreFormat | None = None) -> None:
        self.path = path
        if fmt is not None:
            self.fmt = fmt
        elif self.path.suffix == ".pb":
            self.fmt = "protobuf"
        else:
            self.fmt = "jsonl"

    @classmethod
    def for_workdir(cls, workdir: Path, *, prefer_pb: bool = True) -> EventStore:
        root = workdir.expanduser().resolve()
        events_dir = root / ".gillm" / "events"
        events_dir.mkdir(parents=True, exist_ok=True)
        if prefer_pb:
            return cls(events_dir / "app.gillm.events.pb", fmt="protobuf")
        return cls(events_dir / "app.gillm.events.jsonl", fmt="jsonl")

    def append_command(self, command: dict[str, Any], result: dict[str, Any], *, correlation_id: str = "") -> str:
        event_id = uuid.uuid4().hex
        event = StoredEvent(
            id=event_id,
            ts_unix=int(time.time()),
            command=command,
            result=result,
            correlation_id=correlation_id,
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.fmt == "protobuf":
            pb = result_pb2.DslEvent()
            pb.id = event.id
            pb.ts_unix = event.ts_unix
            pb.correlation_id = correlation_id
            pb.command.ParseFromString(encode_protobuf(command, correlation_id=correlation_id))
            dsl_result = DslResult(
                ok=bool(result.get("ok")),
                verb=str(result.get("verb", command.get("verb", ""))),
                command=str(result.get("command", "")),
                output=str(result.get("output", "")),
                data=dict(result.get("data") or {}),
                error=result.get("error"),
                event_id=event_id,
            )
            pb.result.CopyFrom(result_to_pb(dsl_result))
            data = pb.SerializeToString()
            with self.path.open("ab") as fh:
                fh.write(len(data).to_bytes(4, "big"))
                fh.write(data)
        else:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
        return event_id

    def read_all(self) -> list[StoredEvent]:
        if not self.path.is_file():
            return []
        if self.fmt == "protobuf":
            events: list[StoredEvent] = []
            data = self.path.read_bytes()
            offset = 0
            while offset + 4 <= len(data):
                size = int.from_bytes(data[offset : offset + 4], "big")
                offset += 4
                chunk = data[offset : offset + size]
                offset += size
                pb = result_pb2.DslEvent()
                pb.ParseFromString(chunk)
                events.append(
                    StoredEvent(
                        id=pb.id,
                        ts_unix=int(pb.ts_unix),
                        command=envelope_to_dict(pb.command),
                        result={
                            "ok": pb.result.ok,
                            "verb": pb.result.verb,
                            "command": pb.result.command,
                            "output": pb.result.output,
                            "error": pb.result.error or None,
                            "event_id": pb.result.event_id or None,
                        },
                        correlation_id=pb.correlation_id,
                    ),
                )
            return events
        events = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            events.append(
                StoredEvent(
                    id=str(row["id"]),
                    ts_unix=int(row["ts_unix"]),
                    command=dict(row["command"]),
                    result=dict(row["result"]),
                    correlation_id=str(row.get("correlation_id", "")),
                ),
            )
        return events

    def replay(self) -> list[StoredEvent]:
        return self.read_all()
