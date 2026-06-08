"""Dict ↔ protobuf DslEnvelope / DslResult."""

from __future__ import annotations

import json
from typing import Any

from dsl2gillm.grammar import parse_line, to_text
from dsl2gillm.result import DslResult
from dsl2gillm.v1 import command_pb2, result_pb2

_BODY_MAP = {
    "HEALTH": "health",
    "ORIENT": "orient",
    "ACTIONS": "actions",
    "PARSE": "parse",
    "VALIDATE": "validate",
    "RESOLVE": "resolve",
    "CAPTURE": "capture",
    "EXECUTE": "execute",
    "SIMULATE": "simulate",
    "FOCUS": "focus",
    "INJECT": "inject",
}


def _set_body(envelope: command_pb2.DslEnvelope, cmd: dict[str, Any]) -> None:
    verb = str(cmd.get("verb", "")).upper()
    field = _BODY_MAP.get(verb)
    if not field:
        return
    msg = getattr(envelope, field)
    if verb == "PARSE":
        msg.instruction = str(cmd.get("instruction", ""))
    elif verb == "VALIDATE":
        if cmd.get("file"):
            msg.file = str(cmd["file"])
        if cmd.get("steps") is not None:
            msg.steps_json = json.dumps(cmd["steps"], ensure_ascii=False)
    elif verb == "RESOLVE":
        msg.prompt = str(cmd.get("prompt", ""))
    elif verb == "CAPTURE":
        if cmd.get("scale") is not None:
            msg.scale = float(cmd["scale"])
    elif verb == "EXECUTE":
        if cmd.get("file"):
            msg.file = str(cmd["file"])
        if cmd.get("steps") is not None:
            msg.steps_json = json.dumps(cmd["steps"], ensure_ascii=False)
        msg.dry_run = bool(cmd.get("dry_run", False))
    elif verb == "SIMULATE":
        if cmd.get("file"):
            msg.file = str(cmd["file"])
        if cmd.get("steps") is not None:
            msg.steps_json = json.dumps(cmd["steps"], ensure_ascii=False)
    elif verb == "FOCUS":
        msg.hints = str(cmd.get("hints", ""))
        msg.dry_run = bool(cmd.get("dry_run", False))
    elif verb == "INJECT":
        msg.text = str(cmd.get("text", ""))
        msg.ide = str(cmd.get("ide", "default"))
        msg.submit = bool(cmd.get("submit", True))
        msg.dry_run = bool(cmd.get("dry_run", False))


def envelope_to_dict(envelope: command_pb2.DslEnvelope) -> dict[str, Any]:
    verb = envelope.verb.upper()
    cmd: dict[str, Any] = {"verb": verb}
    field = _BODY_MAP.get(verb)
    if not field or envelope.WhichOneof("body") != field:
        return cmd
    msg = getattr(envelope, field)
    if verb == "PARSE" and msg.instruction:
        cmd["instruction"] = msg.instruction
    elif verb == "VALIDATE":
        if msg.file:
            cmd["file"] = msg.file
        if msg.steps_json:
            cmd["steps"] = json.loads(msg.steps_json)
    elif verb == "RESOLVE" and msg.prompt:
        cmd["prompt"] = msg.prompt
    elif verb == "CAPTURE" and msg.scale:
        cmd["scale"] = msg.scale
    elif verb == "EXECUTE":
        if msg.file:
            cmd["file"] = msg.file
        if msg.steps_json:
            cmd["steps"] = json.loads(msg.steps_json)
        if msg.dry_run:
            cmd["dry_run"] = True
    elif verb == "SIMULATE":
        if msg.file:
            cmd["file"] = msg.file
        if msg.steps_json:
            cmd["steps"] = json.loads(msg.steps_json)
    elif verb == "FOCUS":
        if msg.hints:
            cmd["hints"] = msg.hints
        if msg.dry_run:
            cmd["dry_run"] = True
    elif verb == "INJECT":
        if msg.text:
            cmd["text"] = msg.text
        if msg.ide:
            cmd["ide"] = msg.ide
        cmd["submit"] = msg.submit
        if msg.dry_run:
            cmd["dry_run"] = True
    return cmd


def encode_protobuf(cmd: dict[str, Any], *, default_file: str = "", correlation_id: str = "") -> bytes:
    envelope = command_pb2.DslEnvelope()
    envelope.verb = str(cmd.get("verb", "")).upper()
    _set_body(envelope, cmd)
    envelope.default_file = default_file
    envelope.correlation_id = correlation_id
    return envelope.SerializeToString()


def decode_protobuf(data: bytes) -> dict[str, Any]:
    envelope = command_pb2.DslEnvelope()
    envelope.ParseFromString(data)
    return envelope_to_dict(envelope)


def encode_text_to_protobuf(line: str, *, default_file: str = "", correlation_id: str = "") -> bytes:
    payload = parse_line(line, default_file=default_file or None)
    if not payload:
        raise ValueError("empty command")
    return encode_protobuf(payload, default_file=default_file, correlation_id=correlation_id)


def decode_protobuf_to_text(data: bytes) -> str:
    return to_text(decode_protobuf(data))


def result_to_pb(result: DslResult) -> result_pb2.DslResult:
    pb = result_pb2.DslResult()
    pb.ok = result.ok
    pb.verb = result.verb
    pb.output = result.output
    pb.data_json = json.dumps(result.data, ensure_ascii=False).encode("utf-8")
    pb.error = result.error or ""
    pb.event_id = result.event_id or ""
    pb.command = result.command
    return pb


def encode_result_protobuf(result: DslResult) -> bytes:
    return result_to_pb(result).SerializeToString()
