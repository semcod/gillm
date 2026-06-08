"""Generate pydantic models from JSON Schema command definitions."""

from __future__ import annotations

import json
import re
from importlib import resources
from pathlib import Path
from typing import Any


def _schema_type(prop: dict[str, Any]) -> str:
    if "const" in prop:
        return f'Literal[{prop["const"]!r}]'
    if "enum" in prop:
        values = ", ".join(repr(v) for v in prop["enum"])
        return f"Literal[{values}]"
    schema_type = prop.get("type")
    if schema_type == "string":
        return "str"
    if schema_type == "integer":
        return "int"
    if schema_type == "number":
        return "float"
    if schema_type == "boolean":
        return "bool"
    if schema_type == "array":
        return "list[dict[str, Any]]"
    if schema_type == "object":
        return "dict[str, Any]"
    return "Any"


def _model_name(verb: str) -> str:
    parts = verb.lower().split("_")
    return "".join(p.capitalize() for p in parts) + "Command"


def _field_line(name: str, prop: dict[str, Any], *, required: bool) -> str:
    py_type = _schema_type(prop)
    if required:
        return f"    {name}: {py_type}"
    default = prop.get("default")
    if default is not None:
        return f"    {name}: {py_type} = {default!r}"
    if prop.get("type") == "boolean":
        return f"    {name}: {py_type} = False"
    return f"    {name}: {py_type} | None = None"


def render_models(schemas: dict[str, dict[str, Any]]) -> str:
    lines = [
        '"""Auto-generated pydantic models — do not edit by hand.',
        "",
        "Regenerate: python -m dsl2gillm.codegen",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any, Literal",
        "",
        "from pydantic import BaseModel, ConfigDict",
        "",
    ]
    for verb in sorted(schemas):
        schema = schemas[verb]
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        class_name = _model_name(verb)
        lines.append("")
        lines.append(f"class {class_name}(BaseModel):")
        lines.append("    model_config = ConfigDict(extra='forbid')")
        lines.append("")
        for name, prop in props.items():
            lines.append(_field_line(name, prop, required=name in required))
    lines.append("")
    lines.append("MODEL_BY_VERB: dict[str, type[BaseModel]] = {")
    for verb in sorted(schemas):
        lines.append(f'    {verb!r}: {_model_name(verb)},')
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def load_schemas() -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    pkg = resources.files("dsl2gillm").joinpath("schema/commands")
    for path in sorted(pkg.iterdir()):
        if not path.name.endswith(".schema.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        verb = str(data.get("properties", {}).get("verb", {}).get("const", ""))
        if verb:
            schemas[verb] = data
    return schemas


def generate_models(output: Path | None = None) -> Path:
    target = output or Path(__file__).resolve().parent / "models.py"
    content = render_models(load_schemas())
    target.write_text(content, encoding="utf-8")
    return target


def main() -> int:
    path = generate_models()
    print(f"generated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
