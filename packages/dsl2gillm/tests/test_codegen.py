from pathlib import Path

from dsl2gillm.codegen import generate_models, load_schemas


def test_load_schemas_has_all_verbs() -> None:
    schemas = load_schemas()
    assert "HEALTH" in schemas
    assert "EXECUTE" in schemas
    assert len(schemas) >= 11


def test_generate_models(tmp_path: Path) -> None:
    out = tmp_path / "models.py"
    path = generate_models(out)
    text = path.read_text(encoding="utf-8")
    assert "class HealthCommand(BaseModel):" in text
    assert "MODEL_BY_VERB" in text
