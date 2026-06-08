# gillm

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

**See also:** [README.md](README.md) (user guide) · [SUMD.md](SUMD.md) (full descriptor) · [packages/README.md](packages/README.md) (control layer) · [project/](project/README.md) (analysis artifacts)

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `gillm`
- **version**: `0.1.10`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, goal.yaml, .env.example, project/(5 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: gillm;
  version: 0.1.10;
}

dependencies {
  runtime: "pyyaml>=6.0, rich>=13.0, requests>=2.31.0, mss>=9.0";
  control: "dsl2gillm>=0.1.0, uri2gillm>=0.1.0, nlp2gillm>=0.1.0, cli2gillm>=0.1.0, mcp2gillm>=0.1.0, rest2gillm>=0.1.0";
  dev: "pytest>=7.0, ruff>=0.4, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60, dsl2gillm>=0.1.0, uri2gillm>=0.1.0, nlp2gillm>=0.1.0, rest2gillm>=0.1.0";
}

entity[name="ActionsCommand"] {
  verb: Literal[!;
}

entity[name="CaptureCommand"] {
  verb: Literal[!;
  scale: float!;
}

entity[name="ExecuteCommand"] {
  verb: Literal[!;
  file: str | None;
  steps: list[dict[str, Any]] | None;
  dry_run: bool!;
}

entity[name="FocusCommand"] {
  verb: Literal[!;
  hints: string!;
  dry_run: bool!;
}

entity[name="HealthCommand"] {
  verb: Literal[!;
}

entity[name="InjectCommand"] {
  verb: Literal[!;
  text: string!;
  ide: string!;
  submit: bool!;
  dry_run: bool!;
}

entity[name="OrientCommand"] {
  verb: Literal[!;
}

entity[name="ParseCommand"] {
  verb: Literal[!;
  instruction: string!;
}

entity[name="ResolveCommand"] {
  verb: Literal[!;
  prompt: string!;
}

entity[name="SimulateCommand"] {
  verb: Literal[!;
  file: str | None;
  steps: list[dict[str, Any]] | None;
}

entity[name="ValidateCommand"] {
  verb: Literal[!;
  file: str | None;
  steps: list[dict[str, Any]] | None;
}

interface[type="api"] {
  type: rest;
  framework: fastapi;
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="gillm"] {
  entry: gillm.cli:main;
}

workflow[name="venv"] {
  trigger: manual;
  step-1: run cmd=if [ ! -x "$(PYTHON)" ]; then \;
  step-2: run cmd=echo "Creating virtual environment in $(VENV)..."; \;
  step-3: run cmd=python3 -m venv "$(VENV)"; \;
  step-4: run cmd=fi;
}

workflow[name="install"] {
  trigger: manual;
  step-1: run cmd=$(PIP) install -e .;
  step-2: run cmd=echo "✓ code2llm installed with TOON format support";
}

workflow[name="dev-install"] {
  trigger: manual;
  step-1: run cmd=$(PIP) install -e ".[dev]";
  step-2: run cmd=echo "✓ code2llm installed with dev dependencies";
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m pytest tests/ -v --tb=short;
}

workflow[name="test-fast"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m pytest -m "not slow and not integration" -v --tb=short -n auto;
}

workflow[name="test-slow"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m pytest -m "slow" -v --tb=short;
}

workflow[name="test-integration"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m pytest -m "integration" -v --tb=short;
}

workflow[name="test-unit"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m pytest -m "unit" -v --tb=short;
}

workflow[name="test-cov"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m pytest tests/ --cov=code2llm --cov-report=html --cov-report=term 2>/dev/null || echo "No tests yet";
}

workflow[name="test-toon"] {
  trigger: manual;
  step-1: run cmd=echo "🎯 Testing TOON format...";
  step-2: run cmd=$(PYTHON) -m code2llm ./ -v -o ./test_toon -m hybrid -f toon;
  step-3: run cmd=$(PYTHON) validate_toon.py test_toon/analysis.toon;
  step-4: run cmd=echo "✓ TOON format test complete";
}

workflow[name="validate-toon"] {
  trigger: manual;
  step-1: depend target=test-toon;
}

workflow[name="test-all-formats"] {
  trigger: manual;
  step-1: run cmd=echo "📊 Testing all output formats...";
  step-2: run cmd=$(PYTHON) -m code2llm ./ -v -o ./test_all -m hybrid -f all;
  step-3: run cmd=$(PYTHON) validate_toon.py test_all/analysis.toon;
  step-4: run cmd=echo "✓ All formats test complete";
}

workflow[name="test-comprehensive"] {
  trigger: manual;
  step-1: run cmd=echo "🚀 Running comprehensive test suite...";
  step-2: run cmd=bash project.sh;
  step-3: run cmd=echo "✓ Comprehensive tests complete";
}

workflow[name="lint"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m flake8 code2llm/ --max-line-length=100 --ignore=E203,W503 2>/dev/null || echo "flake8 not installed";
  step-2: run cmd=$(PYTHON) -m black --check code2llm/ 2>/dev/null || echo "black not installed";
  step-3: run cmd=echo "✓ Linting complete";
}

workflow[name="format"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m black code2llm/ --line-length=100 2>/dev/null || echo "black not installed, run: pip install black";
  step-2: run cmd=echo "✓ Code formatted";
}

workflow[name="typecheck"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m mypy code2llm/ --ignore-missing-imports 2>/dev/null || echo "mypy not installed";
}

workflow[name="check"] {
  trigger: manual;
  step-1: run cmd=echo "✓ All checks passed";
}

workflow[name="run"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m code2llm ../python/stts_core -v -o ./output;
}

workflow[name="analyze"] {
  trigger: manual;
  step-1: run cmd=echo "🎯 Running TOON format analysis on current project...";
  step-2: run cmd=$(PYTHON) -m code2llm ./ -v -o ./analysis -m hybrid -f toon;
  step-3: run cmd=$(PYTHON) validate_toon.py analysis/analysis.toon;
  step-4: run cmd=echo "✓ TOON analysis complete - check analysis/analysis.toon";
}

workflow[name="analyze-all"] {
  trigger: manual;
  step-1: run cmd=echo "📊 Running analysis with all formats...";
  step-2: run cmd=$(PYTHON) -m code2llm ./ -v -o ./analysis_all -m hybrid -f all;
  step-3: run cmd=$(PYTHON) validate_toon.py analysis_all/analysis.toon;
  step-4: run cmd=echo "✓ All formats analysis complete - check analysis_all/";
}

workflow[name="toon-demo"] {
  trigger: manual;
  step-1: run cmd=echo "🎯 Quick TOON format demo...";
  step-2: run cmd=$(PYTHON) -m code2llm ./ -v -o ./demo -m hybrid -f toon;
  step-3: run cmd=echo "📁 Generated: demo/analysis.toon";
  step-4: run cmd=echo "📊 Size: $$(du -h demo/analysis.toon | cut -f1)";
  step-5: run cmd=echo "🔍 Preview:";
  step-6: run cmd=head -20 demo/analysis.toon;
}

workflow[name="toon-compare"] {
  trigger: manual;
  step-1: run cmd=echo "📊 Comparing TOON vs YAML formats...";
  step-2: run cmd=$(PYTHON) -m code2llm ./ -v -o ./compare -m hybrid -f toon,yaml;
  step-3: run cmd=echo "📁 Files generated:";
  step-4: run cmd=echo "  - TOON:  compare/analysis.toon  ($$(du -h compare/analysis.toon | cut -f1))";
  step-5: run cmd=echo "  - YAML:  compare/analysis.yaml  ($$(du -h compare/analysis.yaml | cut -f1))";
  step-6: run cmd=echo "  - Ratio: $$(echo "scale=1; $$(du -k compare/analysis.yaml | cut -f1) / $$(du -k compare/analysis.toon | cut -f1)" | bc)x smaller";
  step-7: run cmd=$(PYTHON) validate_toon.py compare/analysis.yaml compare/analysis.toon;
}

workflow[name="toon-validate"] {
  trigger: manual;
  step-1: run cmd=echo "🔍 Validating TOON format structure...";
  step-2: run cmd=$(PYTHON) validate_toon.py analysis/analysis.toon 2>/dev/null || $(PYTHON) validate_toon.py test_toon/analysis.toon 2>/dev/null || echo "Run 'make test-toon' first";
}

workflow[name="build"] {
  trigger: manual;
  step-1: run cmd=rm -rf build/ dist/ *.egg-info;
  step-2: run cmd=$(PYTHON) -m build;
  step-3: run cmd=echo "✓ Build complete - check dist/";
}

workflow[name="publish-test"] {
  trigger: manual;
  step-1: run cmd=echo "🚀 Publishing to TestPyPI...";
  step-2: run cmd=bash -c 'if [ -z "$${TWINE_USERNAME}" ] && [ -z "$${TWINE_PASSWORD}" ] && [ -z "$${PYPI_API_TOKEN}" ]; then \;
  step-3: run cmd=echo "⚠️  No PyPI credentials found. Set TWINE_USERNAME and TWINE_PASSWORD or PYPI_API_TOKEN"; \;
  step-4: run cmd=echo "   Example: TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-xxx make publish-test"; \;
  step-5: run cmd=echo "   Skipping publish-test."; \;
  step-6: run cmd=else \;
  step-7: run cmd=$(PYTHON) -m venv publish-test-env && \;
  step-8: run cmd=publish-test-env/bin/pip install twine && \;
  step-9: run cmd=publish-test-env/bin/python -m twine upload --repository testpypi dist/* && \;
  step-10: run cmd=rm -rf publish-test-env && \;
  step-11: run cmd=echo "✓ Published to TestPyPI"; \;
  step-12: run cmd=fi';
}

workflow[name="bump-patch"] {
  trigger: manual;
  step-1: run cmd=echo "🔢 Bumping patch version...";
  step-2: run cmd=$(PYTHON) scripts/bump_version.py patch 2>/dev/null || echo "Create scripts/bump_version.py or edit pyproject.toml manually";
}

workflow[name="bump-minor"] {
  trigger: manual;
  step-1: run cmd=echo "🔢 Bumping minor version...";
  step-2: run cmd=$(PYTHON) scripts/bump_version.py minor 2>/dev/null || echo "Create scripts/bump_version.py or edit pyproject.toml manually";
}

workflow[name="bump-major"] {
  trigger: manual;
  step-1: run cmd=echo "🔢 Bumping major version...";
  step-2: run cmd=$(PYTHON) scripts/bump_version.py major 2>/dev/null || echo "Create scripts/bump_version.py or edit pyproject.toml manually";
}

workflow[name="publish"] {
  trigger: manual;
  step-1: run cmd=echo "🚀 Publishing to PyPI...";
  step-2: run cmd=bash -c 'if [ -z "$${TWINE_USERNAME}" ] && [ -z "$${TWINE_PASSWORD}" ] && [ -z "$${PYPI_API_TOKEN}" ]; then \;
  step-3: run cmd=echo "⚠️  No PyPI credentials found. Set TWINE_USERNAME and TWINE_PASSWORD or PYPI_API_TOKEN"; \;
  step-4: run cmd=echo "   Example: TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-xxx make publish"; \;
  step-5: run cmd=echo "   Skipping publish."; \;
  step-6: run cmd=else \;
  step-7: run cmd=echo "🔢 Bumping patch version..."; \;
  step-8: run cmd=$(MAKE) bump-patch; \;
  step-9: run cmd=echo "🔨 Rebuilding package with new version..."; \;
  step-10: run cmd=$(MAKE) build; \;
  step-11: run cmd=echo "📦 Publishing to PyPI..."; \;
  step-12: run cmd=$(PYTHON) -m venv publish-env; \;
  step-13: run cmd=publish-env/bin/pip install twine; \;
  step-14: run cmd=publish-env/bin/python -m twine upload dist/*; \;
  step-15: run cmd=rm -rf publish-env; \;
  step-16: run cmd=echo "✓ Published to PyPI"; \;
  step-17: run cmd=fi';
}

workflow[name="mermaid-png"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) mermaid_to_png.py --batch output output;
}

workflow[name="install-mermaid"] {
  trigger: manual;
  step-1: run cmd=npm install -g @mermaid-js/mermaid-cli;
}

workflow[name="check-mermaid"] {
  trigger: manual;
  step-1: run cmd=echo "Checking available Mermaid renderers...";
  step-2: run cmd=which mmdc > /dev/null && echo "✓ mmdc (mermaid-cli)" || echo "✗ mmdc (run: npm install -g @mermaid-js/mermaid-cli)";
  step-3: run cmd=which npx > /dev/null && echo "✓ npx (for @mermaid-js/mermaid-cli)" || echo "✗ npx (install Node.js)";
  step-4: run cmd=which puppeteer > /dev/null && echo "✓ puppeteer" || echo "✗ puppeteer (run: npm install -g puppeteer)";
}

workflow[name="clean"] {
  trigger: manual;
  step-1: run cmd=rm -rf build/ dist/ *.egg-info;
  step-2: run cmd=rm -rf .pytest_cache .coverage htmlcov/;
  step-3: run cmd=rm -rf code2llm/__pycache__ code2llm/*/__pycache__;
  step-4: run cmd=rm -rf test_* demo compare analysis analysis_all output_* 2>/dev/null || true;
  step-5: run cmd=find . -name "*.pyc" -delete 2>/dev/null || true;
  step-6: run cmd=find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true;
  step-7: run cmd=echo "✓ Cleaned build artifacts and test outputs";
}

workflow[name="clean-png"] {
  trigger: manual;
  step-1: run cmd=rm -f output/*.png;
  step-2: run cmd=echo "✓ Cleaned PNG files";
}

workflow[name="quickstart"] {
  trigger: manual;
  step-1: run cmd=echo "🚀 Quick Start with code2llm TOON format:";
  step-2: run cmd=echo "";
  step-3: run cmd=echo "1. Install:        make install";
  step-4: run cmd=echo "2. Test TOON:      make test-toon";
  step-5: run cmd=echo "3. Analyze:        make analyze";
  step-6: run cmd=echo "4. Compare:        make toon-compare";
  step-7: run cmd=echo "5. All formats:    make test-all-formats";
  step-8: run cmd=echo "";
  step-9: run cmd=echo "📖 For more: make help";
}

tests {
  import: testql-scenarios/**/*.testql.toon.yaml;
}

env_vars {
  keys: OPENROUTER_API_KEY, LLM_MODEL, PFIX_AUTO_APPLY, PFIX_AUTO_INSTALL_DEPS, PFIX_AUTO_RESTART, PFIX_MAX_RETRIES, PFIX_DRY_RUN, PFIX_ENABLED, PFIX_GIT_COMMIT, PFIX_GIT_PREFIX, PFIX_CREATE_BACKUPS, XDG_CONFIG_HOME, KORU_PORTAL_PYTHON, KORU_VISION_SCALE, KORU_YDOTOOL_ENTER_KEYCODE, KORU_YDOTOOL_SUBMIT_MODE, KORU_YDOTOOL_CTRL_KEYCODE, KORU_INJECTOR_EXTRA_ENTER, WAYLAND_DISPLAY, XDG_SESSION_TYPE, DISPLAY, XDG_CURRENT_DESKTOP, GNOME_DESKTOP_SESSION_ID, KORU_OS_PREFER_YDOTOOL, TERM_PROGRAM, KORU_OS_INJECTOR, KORU_OS_INJECTOR_DRY_RUN, KORU_OS_INJECTOR_FOCUS, KORU_OS_INJECTOR_INPUT, KORU_OS_INJECTOR_CMD_TIMEOUT, KORU_OS_INJECTOR_POST_FOCUS_DELAY, KORU_INJECTOR_BACKEND;
}

deploy {
  target: makefile;
}

environment[name="local"] {
  runtime: python;
  env_file: .env;
  template_file: .env.example;
  python_version: >=3.10;
  vars: LLM_MODEL, OPENROUTER_API_KEY, PFIX_AUTO_APPLY, PFIX_AUTO_INSTALL_DEPS, PFIX_AUTO_RESTART, PFIX_CREATE_BACKUPS, PFIX_DRY_RUN, PFIX_ENABLED, PFIX_GIT_COMMIT, PFIX_GIT_PREFIX, PFIX_MAX_RETRIES;
  runtime_llm: OPENROUTER_API_KEY;
  runtime_pfix: PFIX_AUTO_APPLY, PFIX_AUTO_INSTALL_DEPS, PFIX_AUTO_RESTART, PFIX_CREATE_BACKUPS, PFIX_DRY_RUN, PFIX_ENABLED, PFIX_GIT_COMMIT, PFIX_GIT_PREFIX, PFIX_MAX_RETRIES;
}
```

## Workflows

## Dependencies

### Runtime

```text markpact:deps python
pyyaml>=6.0
rich>=13.0
requests>=2.31.0
mss>=9.0
```

### Development

```text markpact:deps python scope=dev
pytest>=7.0
ruff>=0.4
goal>=2.1.0
costs>=0.1.20
pfix>=0.1.60
dsl2gillm>=0.1.0
uri2gillm>=0.1.0
nlp2gillm>=0.1.0
rest2gillm>=0.1.0
```

## Call Graph

*187 nodes · 203 edges · 42 modules · CC̄=4.0*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `dispatch` *(in packages.dsl2gillm.src.dsl2gillm.bus)* | 15 ⚠ | 22 | 29 | **51** |
| `parse_line` *(in packages.dsl2gillm.src.dsl2gillm.grammar)* | 46 ⚠ | 2 | 48 | **50** |
| `to_text` *(in packages.dsl2gillm.src.dsl2gillm.grammar)* | 22 ⚠ | 2 | 43 | **45** |
| `create_app` *(in packages.rest2gillm.src.rest2gillm.app)* | 1 | 1 | 42 | **43** |
| `_set_body` *(in packages.dsl2gillm.src.dsl2gillm.pb_codec)* | 17 ⚠ | 1 | 37 | **38** |
| `append_command` *(in packages.dsl2gillm.src.dsl2gillm.events.EventStore)* | 3 | 0 | 33 | **33** |
| `_handle_subcommand` *(in packages.dsl2gillm.src.dsl2gillm.cli)* | 19 ⚠ | 1 | 32 | **33** |
| `nlp2uri` *(in packages.uri2gillm.src.uri2gillm.nlp2uri)* | 12 ⚠ | 2 | 26 | **28** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/gillm
# generated in 0.08s
# nodes: 187 | edges: 203 | modules: 42
# CC̄=4.0

HUBS[20]:
  packages.dsl2gillm.src.dsl2gillm.bus.dispatch
    CC=15  in:22  out:29  total:51
  packages.dsl2gillm.src.dsl2gillm.grammar.parse_line
    CC=46  in:2  out:48  total:50
  packages.dsl2gillm.src.dsl2gillm.grammar.to_text
    CC=22  in:2  out:43  total:45
  packages.rest2gillm.src.rest2gillm.app.create_app
    CC=1  in:1  out:42  total:43
  packages.dsl2gillm.src.dsl2gillm.pb_codec._set_body
    CC=17  in:1  out:37  total:38
  packages.dsl2gillm.src.dsl2gillm.events.EventStore.append_command
    CC=3  in:0  out:33  total:33
  packages.dsl2gillm.src.dsl2gillm.cli._handle_subcommand
    CC=19  in:1  out:32  total:33
  packages.uri2gillm.src.uri2gillm.nlp2uri.nlp2uri
    CC=12  in:2  out:26  total:28
  src.gillm.injection.backends._log
    CC=2  in:26  out:1  total:27
  packages.dsl2gillm.src.dsl2gillm.cli._main_subcommand
    CC=1  in:1  out:24  total:25
  packages.uri2gillm.src.uri2gillm.decode.uri_to_dsl
    CC=26  in:2  out:20  total:22
  src.gillm.drivers.composite.CompositeGuiDriver.execute
    CC=18  in:0  out:22  total:22
  packages.dsl2gillm.src.dsl2gillm.codegen.render_models
    CC=4  in:1  out:20  total:21
  src.gillm.recovery.diagnose.diagnose_drive_reply
    CC=9  in:0  out:21  total:21
  packages.mcp2gillm.src.mcp2gillm.server.GillmMCPServer._register_tools
    CC=1  in:0  out:20  total:20
  packages.dsl2gillm.src.dsl2gillm.cli._main_legacy
    CC=5  in:1  out:17  total:18
  packages.dsl2gillm.src.dsl2gillm.handlers._inject
    CC=2  in:1  out:15  total:16
  packages.dsl2gillm.src.dsl2gillm.grammar._steps_from_line
    CC=8  in:3  out:12  total:15
  packages.dsl2gillm.src.dsl2gillm.schema_registry._load_schemas
    CC=4  in:4  out:11  total:15
  packages.nlp2gillm.src.nlp2gillm.to_dsl.to_dsl
    CC=13  in:4  out:10  total:14

MODULES:
  packages.cli2gillm.src.cli2gillm.shell  [1 funcs]
    run_shell  CC=9  out:12
  packages.dsl2gillm.src.dsl2gillm.bus  [3 funcs]
    dispatch  CC=15  out:29
    execute_dsl  CC=4  out:6
    execute_dsl_line  CC=1  out:1
  packages.dsl2gillm.src.dsl2gillm.cli  [5 funcs]
    _handle_subcommand  CC=19  out:32
    _main_legacy  CC=5  out:17
    _main_subcommand  CC=1  out:24
    _run_results  CC=6  out:6
    main  CC=4  out:2
  packages.dsl2gillm.src.dsl2gillm.codec  [8 funcs]
    _validate_with_pydantic  CC=3  out:2
    envelope_from_bytes  CC=1  out:2
    envelope_from_json  CC=2  out:5
    envelope_to_bytes  CC=1  out:2
    envelope_to_json  CC=1  out:3
    parse_text  CC=2  out:2
    roundtrip_text  CC=1  out:4
    validate_payload  CC=2  out:7
  packages.dsl2gillm.src.dsl2gillm.codegen  [7 funcs]
    _field_line  CC=4  out:3
    _model_name  CC=2  out:4
    _schema_type  CC=10  out:3
    generate_models  CC=2  out:5
    load_schemas  CC=4  out:11
    main  CC=1  out:2
    render_models  CC=4  out:20
  packages.dsl2gillm.src.dsl2gillm.events  [1 funcs]
    append_command  CC=3  out:33
  packages.dsl2gillm.src.dsl2gillm.grammar  [3 funcs]
    _steps_from_line  CC=8  out:12
    parse_line  CC=46  out:48
    to_text  CC=22  out:43
  packages.dsl2gillm.src.dsl2gillm.handlers  [14 funcs]
    _actions  CC=1  out:3
    _capture  CC=1  out:5
    _execute  CC=4  out:11
    _focus  CC=4  out:12
    _health  CC=4  out:10
    _inject  CC=2  out:15
    _load_steps  CC=6  out:10
    _orient  CC=2  out:6
    _parse  CC=2  out:7
    _resolve  CC=2  out:6
  packages.dsl2gillm.src.dsl2gillm.pb_codec  [8 funcs]
    _set_body  CC=17  out:37
    decode_protobuf  CC=1  out:3
    decode_protobuf_to_text  CC=1  out:2
    encode_protobuf  CC=1  out:6
    encode_result_protobuf  CC=1  out:2
    encode_text_to_protobuf  CC=3  out:3
    envelope_to_dict  CC=26  out:7
    result_to_pb  CC=3  out:3
  packages.dsl2gillm.src.dsl2gillm.schema_registry  [4 funcs]
    _load_schemas  CC=4  out:11
    all_verbs  CC=1  out:3
    schema_for_verb  CC=2  out:4
    validate_schemas  CC=5  out:9
  packages.mcp2gillm.src.mcp2gillm.cli  [1 funcs]
    main  CC=2  out:5
  packages.mcp2gillm.src.mcp2gillm.server  [5 funcs]
    __post_init__  CC=1  out:3
    _register_tools  CC=1  out:20
    _require_fastmcp  CC=2  out:1
    create_server  CC=1  out:1
    run_server  CC=1  out:2
  packages.nlp2gillm.src.nlp2gillm.llm_backend  [2 funcs]
    get_backend  CC=2  out:1
    nl_to_dsl_line  CC=6  out:8
  packages.nlp2gillm.src.nlp2gillm.to_dsl  [2 funcs]
    apply_nl  CC=1  out:3
    to_dsl  CC=13  out:10
  packages.rest2gillm.src.rest2gillm.app  [1 funcs]
    create_app  CC=1  out:42
  packages.rest2gillm.src.rest2gillm.cli  [1 funcs]
    main  CC=2  out:8
  packages.uri2gillm.src.uri2gillm.decode  [1 funcs]
    uri_to_dsl  CC=26  out:20
  packages.uri2gillm.src.uri2gillm.nlp2uri  [2 funcs]
    best_uri  CC=2  out:1
    nlp2uri  CC=12  out:26
  packages.uri2gillm.src.uri2gillm.run  [1 funcs]
    run_uri  CC=1  out:2
  packages.uri2gillm.src.uri2gillm.uri  [6 funcs]
    _decode  CC=2  out:1
    _encode  CC=1  out:1
    is_gillm_uri  CC=1  out:2
    parse_gillm_uri  CC=7  out:9
    uri_for_block  CC=4  out:3
    uri_for_cmd  CC=4  out:5
  src.gillm.capture.mss_backend  [6 funcs]
    _parse_png_to_rgb  CC=4  out:10
    capture_primary_rgb  CC=2  out:8
    capture_primary_rgb_wayland_fallback  CC=3  out:4
    downscale_rgb_nearest  CC=6  out:5
    resolve_scale  CC=4  out:5
    rgb_mostly_black  CC=5  out:4
  src.gillm.capture.portal_backend  [2 funcs]
    _portal_python  CC=6  out:4
    capture_portal_png  CC=8  out:11
  src.gillm.config  [6 funcs]
    _cached_config  CC=1  out:2
    _merge_submit_keys  CC=7  out:5
    cached_config  CC=1  out:1
    default_config_path  CC=1  out:1
    load_config  CC=4  out:10
    resolve_xdg_path  CC=2  out:3
  src.gillm.control  [4 funcs]
    dispatch_execute  CC=3  out:2
    dispatch_health  CC=1  out:2
    dispatch_parse  CC=1  out:2
    dispatch_validate  CC=3  out:2
  src.gillm.drivers.composite  [5 funcs]
    __init__  CC=2  out:3
    execute  CC=18  out:22
    focus  CC=3  out:6
    probe  CC=3  out:3
    type_text  CC=6  out:14
  src.gillm.focus.darwin  [1 funcs]
    focus_window  CC=4  out:5
  src.gillm.focus.registry  [2 funcs]
    list_os_strategy_ids  CC=2  out:1
    resolve_active_os_strategy  CC=4  out:2
  src.gillm.focus.wayland  [7 funcs]
    _focus_via_wmctrl  CC=4  out:3
    _inject_via_wtype  CC=9  out:7
    _inject_via_ydotool  CC=7  out:10
    inject_keys  CC=9  out:8
    _gnome_compositor  CC=4  out:3
    _prefer_ydotool  CC=3  out:4
    _scan_for_key  CC=5  out:1
  src.gillm.focus.x11  [4 funcs]
    _focus_via_wmctrl  CC=4  out:3
    _focus_via_xdotool  CC=11  out:10
    _inject_via_xdotool  CC=3  out:4
    _run  CC=1  out:1
  src.gillm.injection.backends  [11 funcs]
    _log  CC=2  out:1
    _ydotool_submit_command  CC=3  out:0
    extra_enter_count  CC=3  out:4
    press_wtype  CC=4  out:6
    type_with_backend  CC=5  out:10
    type_with_wtype  CC=3  out:8
    type_with_xdotool  CC=3  out:8
    type_with_ydotool  CC=5  out:12
    ydotool_ctrl_keycode  CC=2  out:3
    ydotool_enter_keycode  CC=2  out:3
  src.gillm.injection.injector  [5 funcs]
    _type_with_backend  CC=1  out:1
    submit_only  CC=9  out:13
    type_text  CC=6  out:8
    _session_type  CC=1  out:1
    _submit_key_for  CC=1  out:2
  src.gillm.injection.os_injector  [10 funcs]
    _focus_profile_chat  CC=6  out:7
    _focus_with_xdotool  CC=4  out:7
    _focus_with_ydotool  CC=4  out:7
    _inject_profile_text  CC=7  out:12
    _injection_result  CC=1  out:0
    _os_injector_skip_reason  CC=9  out:7
    _resolve_input_method  CC=7  out:4
    focus_with_profile  CC=2  out:5
    inject_with_profile  CC=5  out:12
    try_drive_with_profile  CC=8  out:9
  src.gillm.intents.contract  [2 funcs]
    gui_contract  CC=1  out:1
    validate_contract_runtime  CC=7  out:6
  src.gillm.nlp_bridge.client  [2 funcs]
    parse_intent  CC=2  out:2
    _heuristic_parse_intent  CC=2  out:7
  src.gillm.orchestrator.drive  [4 funcs]
    capture_screenshot  CC=3  out:7
    focus_target_window  CC=2  out:7
    inject_text  CC=1  out:4
    log  CC=2  out:1
  src.gillm.recovery.diagnose  [3 funcs]
    classify_failure  CC=24  out:1
    diagnose_drive_reply  CC=9  out:21
    probe_environment  CC=3  out:6
  src.gillm.recovery.repair_hints  [4 funcs]
    _dedupe  CC=4  out:5
    _hints_for_kind  CC=15  out:4
    recovery_hints_for_context  CC=3  out:3
    recovery_hints_for_reload  CC=4  out:0
  src.gillm.runtime.activity  [4 funcs]
    emit_activity  CC=3  out:1
    emit_activity_warn  CC=3  out:1
    set_activity_sink  CC=1  out:0
    try_bootstrap_koru_activity_sink  CC=3  out:3
  src.gillm.runtime.backend_selector  [4 funcs]
    __init__  CC=3  out:2
    candidate_backends  CC=5  out:6
    session_backend_order  CC=4  out:2
    unique_backend_names  CC=3  out:1
  src.gillm.runtime.command_runner  [7 funcs]
    clipboard_backend  CC=3  out:2
    resolve_input_method  CC=7  out:4
    run_cmd  CC=2  out:4
    run_cmd_checked  CC=4  out:4
    set_clipboard  CC=3  out:6
    xdotool  CC=1  out:1
    ydotool  CC=2  out:3
  src.gillm.runtime.env  [10 funcs]
    cmd_timeout_seconds  CC=3  out:4
    dry_run_from_env  CC=1  out:3
    focus_mode_from_env  CC=2  out:3
    forced_injector_backend  CC=2  out:3
    input_mode_from_env  CC=2  out:3
    is_wayland_session  CC=6  out:5
    os_injector_env_disabled  CC=1  out:3
    os_injector_env_forced  CC=1  out:3
    post_focus_delay_seconds  CC=3  out:5
    session_type  CC=4  out:4
  src.gillm.runtime.profiles  [8 funcs]
    _read_json  CC=4  out:5
    capture_from_xdotool  CC=1  out:1
    capture_mouse_xy  CC=7  out:10
    default_config_path  CC=1  out:1
    iter_config_paths  CC=4  out:11
    load_profile  CC=5  out:12
    save_profile  CC=3  out:7
    try_load_profile  CC=4  out:3

EDGES:
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints._hints_for_kind
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints._dedupe
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints.recovery_hints_for_reload
  src.gillm.recovery.repair_hints._hints_for_kind → src.gillm.recovery.repair_hints.recovery_hints_for_reload
  src.gillm.recovery.diagnose.probe_environment → src.gillm.runtime.env.session_type
  src.gillm.recovery.diagnose.probe_environment → src.gillm.runtime.env.is_wayland_session
  src.gillm.recovery.diagnose.diagnose_drive_reply → src.gillm.recovery.diagnose.classify_failure
  src.gillm.recovery.diagnose.diagnose_drive_reply → src.gillm.recovery.diagnose.probe_environment
  src.gillm.recovery.diagnose.diagnose_drive_reply → src.gillm.recovery.repair_hints.recovery_hints_for_context
  src.gillm.capture.portal_backend.capture_portal_png → src.gillm.capture.portal_backend._portal_python
  src.gillm.capture.mss_backend.capture_primary_rgb → src.gillm.capture.mss_backend.resolve_scale
  src.gillm.capture.mss_backend.capture_primary_rgb → src.gillm.capture.mss_backend.downscale_rgb_nearest
  src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback → src.gillm.capture.portal_backend.capture_portal_png
  src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback → src.gillm.capture.mss_backend._parse_png_to_rgb
  src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback → src.gillm.capture.mss_backend.capture_primary_rgb
  src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback → src.gillm.capture.mss_backend.rgb_mostly_black
  src.gillm.capture.mss_backend._parse_png_to_rgb → src.gillm.capture.mss_backend.resolve_scale
  src.gillm.injection.backends._log → src.gillm.orchestrator.drive.DriveOrchestrator.log
  src.gillm.injection.backends.type_with_xdotool → src.gillm.injection.backends._log
  src.gillm.injection.backends.type_with_wtype → src.gillm.injection.backends._log
  src.gillm.injection.backends.type_with_wtype → src.gillm.injection.backends.press_wtype
  src.gillm.injection.backends.type_with_ydotool → src.gillm.injection.backends._log
  src.gillm.injection.backends.type_with_ydotool → src.gillm.injection.backends._ydotool_submit_command
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends._log
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.extra_enter_count
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.type_with_xdotool
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.type_with_wtype
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.type_with_ydotool
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.ydotool_enter_keycode
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.ydotool_submit_mode
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.ydotool_ctrl_keycode
  src.gillm.injection.injector._submit_key_for → src.gillm.config.cached_config
  src.gillm.injection.injector._session_type → src.gillm.runtime.env.session_type
  src.gillm.injection.injector.Injector._type_with_backend → src.gillm.injection.backends.type_with_backend
  src.gillm.injection.injector.Injector.type_text → src.gillm.injection.injector._submit_key_for
  src.gillm.injection.injector.Injector.submit_only → src.gillm.injection.injector._submit_key_for
  src.gillm.injection.os_injector._resolve_input_method → src.gillm.runtime.env.input_mode_from_env
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.backends._log
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.os_injector._focus_with_ydotool
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.os_injector._focus_with_xdotool
  src.gillm.injection.os_injector._focus_with_ydotool → src.gillm.injection.backends._log
  src.gillm.injection.os_injector._focus_with_xdotool → src.gillm.injection.backends._log
  src.gillm.injection.os_injector._inject_profile_text → src.gillm.injection.backends._log
  src.gillm.injection.os_injector.focus_with_profile → src.gillm.runtime.env.focus_mode_from_env
  src.gillm.injection.os_injector.focus_with_profile → src.gillm.runtime.env.post_focus_delay_seconds
  src.gillm.injection.os_injector.focus_with_profile → src.gillm.injection.os_injector._focus_profile_chat
  src.gillm.injection.os_injector.focus_with_profile → src.gillm.injection.os_injector._injection_result
  src.gillm.injection.os_injector.inject_with_profile → src.gillm.runtime.env.focus_mode_from_env
  src.gillm.injection.os_injector.inject_with_profile → src.gillm.injection.os_injector._resolve_input_method
  src.gillm.injection.os_injector.inject_with_profile → src.gillm.runtime.env.post_focus_delay_seconds
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/gillm
# generated in 0.08s
# nodes: 187 | edges: 203 | modules: 42
# CC̄=4.0

HUBS[20]:
  packages.dsl2gillm.src.dsl2gillm.bus.dispatch
    CC=15  in:22  out:29  total:51
  packages.dsl2gillm.src.dsl2gillm.grammar.parse_line
    CC=46  in:2  out:48  total:50
  packages.dsl2gillm.src.dsl2gillm.grammar.to_text
    CC=22  in:2  out:43  total:45
  packages.rest2gillm.src.rest2gillm.app.create_app
    CC=1  in:1  out:42  total:43
  packages.dsl2gillm.src.dsl2gillm.pb_codec._set_body
    CC=17  in:1  out:37  total:38
  packages.dsl2gillm.src.dsl2gillm.events.EventStore.append_command
    CC=3  in:0  out:33  total:33
  packages.dsl2gillm.src.dsl2gillm.cli._handle_subcommand
    CC=19  in:1  out:32  total:33
  packages.uri2gillm.src.uri2gillm.nlp2uri.nlp2uri
    CC=12  in:2  out:26  total:28
  src.gillm.injection.backends._log
    CC=2  in:26  out:1  total:27
  packages.dsl2gillm.src.dsl2gillm.cli._main_subcommand
    CC=1  in:1  out:24  total:25
  packages.uri2gillm.src.uri2gillm.decode.uri_to_dsl
    CC=26  in:2  out:20  total:22
  src.gillm.drivers.composite.CompositeGuiDriver.execute
    CC=18  in:0  out:22  total:22
  packages.dsl2gillm.src.dsl2gillm.codegen.render_models
    CC=4  in:1  out:20  total:21
  src.gillm.recovery.diagnose.diagnose_drive_reply
    CC=9  in:0  out:21  total:21
  packages.mcp2gillm.src.mcp2gillm.server.GillmMCPServer._register_tools
    CC=1  in:0  out:20  total:20
  packages.dsl2gillm.src.dsl2gillm.cli._main_legacy
    CC=5  in:1  out:17  total:18
  packages.dsl2gillm.src.dsl2gillm.handlers._inject
    CC=2  in:1  out:15  total:16
  packages.dsl2gillm.src.dsl2gillm.grammar._steps_from_line
    CC=8  in:3  out:12  total:15
  packages.dsl2gillm.src.dsl2gillm.schema_registry._load_schemas
    CC=4  in:4  out:11  total:15
  packages.nlp2gillm.src.nlp2gillm.to_dsl.to_dsl
    CC=13  in:4  out:10  total:14

MODULES:
  packages.cli2gillm.src.cli2gillm.shell  [1 funcs]
    run_shell  CC=9  out:12
  packages.dsl2gillm.src.dsl2gillm.bus  [3 funcs]
    dispatch  CC=15  out:29
    execute_dsl  CC=4  out:6
    execute_dsl_line  CC=1  out:1
  packages.dsl2gillm.src.dsl2gillm.cli  [5 funcs]
    _handle_subcommand  CC=19  out:32
    _main_legacy  CC=5  out:17
    _main_subcommand  CC=1  out:24
    _run_results  CC=6  out:6
    main  CC=4  out:2
  packages.dsl2gillm.src.dsl2gillm.codec  [8 funcs]
    _validate_with_pydantic  CC=3  out:2
    envelope_from_bytes  CC=1  out:2
    envelope_from_json  CC=2  out:5
    envelope_to_bytes  CC=1  out:2
    envelope_to_json  CC=1  out:3
    parse_text  CC=2  out:2
    roundtrip_text  CC=1  out:4
    validate_payload  CC=2  out:7
  packages.dsl2gillm.src.dsl2gillm.codegen  [7 funcs]
    _field_line  CC=4  out:3
    _model_name  CC=2  out:4
    _schema_type  CC=10  out:3
    generate_models  CC=2  out:5
    load_schemas  CC=4  out:11
    main  CC=1  out:2
    render_models  CC=4  out:20
  packages.dsl2gillm.src.dsl2gillm.events  [1 funcs]
    append_command  CC=3  out:33
  packages.dsl2gillm.src.dsl2gillm.grammar  [3 funcs]
    _steps_from_line  CC=8  out:12
    parse_line  CC=46  out:48
    to_text  CC=22  out:43
  packages.dsl2gillm.src.dsl2gillm.handlers  [14 funcs]
    _actions  CC=1  out:3
    _capture  CC=1  out:5
    _execute  CC=4  out:11
    _focus  CC=4  out:12
    _health  CC=4  out:10
    _inject  CC=2  out:15
    _load_steps  CC=6  out:10
    _orient  CC=2  out:6
    _parse  CC=2  out:7
    _resolve  CC=2  out:6
  packages.dsl2gillm.src.dsl2gillm.pb_codec  [8 funcs]
    _set_body  CC=17  out:37
    decode_protobuf  CC=1  out:3
    decode_protobuf_to_text  CC=1  out:2
    encode_protobuf  CC=1  out:6
    encode_result_protobuf  CC=1  out:2
    encode_text_to_protobuf  CC=3  out:3
    envelope_to_dict  CC=26  out:7
    result_to_pb  CC=3  out:3
  packages.dsl2gillm.src.dsl2gillm.schema_registry  [4 funcs]
    _load_schemas  CC=4  out:11
    all_verbs  CC=1  out:3
    schema_for_verb  CC=2  out:4
    validate_schemas  CC=5  out:9
  packages.mcp2gillm.src.mcp2gillm.cli  [1 funcs]
    main  CC=2  out:5
  packages.mcp2gillm.src.mcp2gillm.server  [5 funcs]
    __post_init__  CC=1  out:3
    _register_tools  CC=1  out:20
    _require_fastmcp  CC=2  out:1
    create_server  CC=1  out:1
    run_server  CC=1  out:2
  packages.nlp2gillm.src.nlp2gillm.llm_backend  [2 funcs]
    get_backend  CC=2  out:1
    nl_to_dsl_line  CC=6  out:8
  packages.nlp2gillm.src.nlp2gillm.to_dsl  [2 funcs]
    apply_nl  CC=1  out:3
    to_dsl  CC=13  out:10
  packages.rest2gillm.src.rest2gillm.app  [1 funcs]
    create_app  CC=1  out:42
  packages.rest2gillm.src.rest2gillm.cli  [1 funcs]
    main  CC=2  out:8
  packages.uri2gillm.src.uri2gillm.decode  [1 funcs]
    uri_to_dsl  CC=26  out:20
  packages.uri2gillm.src.uri2gillm.nlp2uri  [2 funcs]
    best_uri  CC=2  out:1
    nlp2uri  CC=12  out:26
  packages.uri2gillm.src.uri2gillm.run  [1 funcs]
    run_uri  CC=1  out:2
  packages.uri2gillm.src.uri2gillm.uri  [6 funcs]
    _decode  CC=2  out:1
    _encode  CC=1  out:1
    is_gillm_uri  CC=1  out:2
    parse_gillm_uri  CC=7  out:9
    uri_for_block  CC=4  out:3
    uri_for_cmd  CC=4  out:5
  src.gillm.capture.mss_backend  [6 funcs]
    _parse_png_to_rgb  CC=4  out:10
    capture_primary_rgb  CC=2  out:8
    capture_primary_rgb_wayland_fallback  CC=3  out:4
    downscale_rgb_nearest  CC=6  out:5
    resolve_scale  CC=4  out:5
    rgb_mostly_black  CC=5  out:4
  src.gillm.capture.portal_backend  [2 funcs]
    _portal_python  CC=6  out:4
    capture_portal_png  CC=8  out:11
  src.gillm.config  [6 funcs]
    _cached_config  CC=1  out:2
    _merge_submit_keys  CC=7  out:5
    cached_config  CC=1  out:1
    default_config_path  CC=1  out:1
    load_config  CC=4  out:10
    resolve_xdg_path  CC=2  out:3
  src.gillm.control  [4 funcs]
    dispatch_execute  CC=3  out:2
    dispatch_health  CC=1  out:2
    dispatch_parse  CC=1  out:2
    dispatch_validate  CC=3  out:2
  src.gillm.drivers.composite  [5 funcs]
    __init__  CC=2  out:3
    execute  CC=18  out:22
    focus  CC=3  out:6
    probe  CC=3  out:3
    type_text  CC=6  out:14
  src.gillm.focus.darwin  [1 funcs]
    focus_window  CC=4  out:5
  src.gillm.focus.registry  [2 funcs]
    list_os_strategy_ids  CC=2  out:1
    resolve_active_os_strategy  CC=4  out:2
  src.gillm.focus.wayland  [7 funcs]
    _focus_via_wmctrl  CC=4  out:3
    _inject_via_wtype  CC=9  out:7
    _inject_via_ydotool  CC=7  out:10
    inject_keys  CC=9  out:8
    _gnome_compositor  CC=4  out:3
    _prefer_ydotool  CC=3  out:4
    _scan_for_key  CC=5  out:1
  src.gillm.focus.x11  [4 funcs]
    _focus_via_wmctrl  CC=4  out:3
    _focus_via_xdotool  CC=11  out:10
    _inject_via_xdotool  CC=3  out:4
    _run  CC=1  out:1
  src.gillm.injection.backends  [11 funcs]
    _log  CC=2  out:1
    _ydotool_submit_command  CC=3  out:0
    extra_enter_count  CC=3  out:4
    press_wtype  CC=4  out:6
    type_with_backend  CC=5  out:10
    type_with_wtype  CC=3  out:8
    type_with_xdotool  CC=3  out:8
    type_with_ydotool  CC=5  out:12
    ydotool_ctrl_keycode  CC=2  out:3
    ydotool_enter_keycode  CC=2  out:3
  src.gillm.injection.injector  [5 funcs]
    _type_with_backend  CC=1  out:1
    submit_only  CC=9  out:13
    type_text  CC=6  out:8
    _session_type  CC=1  out:1
    _submit_key_for  CC=1  out:2
  src.gillm.injection.os_injector  [10 funcs]
    _focus_profile_chat  CC=6  out:7
    _focus_with_xdotool  CC=4  out:7
    _focus_with_ydotool  CC=4  out:7
    _inject_profile_text  CC=7  out:12
    _injection_result  CC=1  out:0
    _os_injector_skip_reason  CC=9  out:7
    _resolve_input_method  CC=7  out:4
    focus_with_profile  CC=2  out:5
    inject_with_profile  CC=5  out:12
    try_drive_with_profile  CC=8  out:9
  src.gillm.intents.contract  [2 funcs]
    gui_contract  CC=1  out:1
    validate_contract_runtime  CC=7  out:6
  src.gillm.nlp_bridge.client  [2 funcs]
    parse_intent  CC=2  out:2
    _heuristic_parse_intent  CC=2  out:7
  src.gillm.orchestrator.drive  [4 funcs]
    capture_screenshot  CC=3  out:7
    focus_target_window  CC=2  out:7
    inject_text  CC=1  out:4
    log  CC=2  out:1
  src.gillm.recovery.diagnose  [3 funcs]
    classify_failure  CC=24  out:1
    diagnose_drive_reply  CC=9  out:21
    probe_environment  CC=3  out:6
  src.gillm.recovery.repair_hints  [4 funcs]
    _dedupe  CC=4  out:5
    _hints_for_kind  CC=15  out:4
    recovery_hints_for_context  CC=3  out:3
    recovery_hints_for_reload  CC=4  out:0
  src.gillm.runtime.activity  [4 funcs]
    emit_activity  CC=3  out:1
    emit_activity_warn  CC=3  out:1
    set_activity_sink  CC=1  out:0
    try_bootstrap_koru_activity_sink  CC=3  out:3
  src.gillm.runtime.backend_selector  [4 funcs]
    __init__  CC=3  out:2
    candidate_backends  CC=5  out:6
    session_backend_order  CC=4  out:2
    unique_backend_names  CC=3  out:1
  src.gillm.runtime.command_runner  [7 funcs]
    clipboard_backend  CC=3  out:2
    resolve_input_method  CC=7  out:4
    run_cmd  CC=2  out:4
    run_cmd_checked  CC=4  out:4
    set_clipboard  CC=3  out:6
    xdotool  CC=1  out:1
    ydotool  CC=2  out:3
  src.gillm.runtime.env  [10 funcs]
    cmd_timeout_seconds  CC=3  out:4
    dry_run_from_env  CC=1  out:3
    focus_mode_from_env  CC=2  out:3
    forced_injector_backend  CC=2  out:3
    input_mode_from_env  CC=2  out:3
    is_wayland_session  CC=6  out:5
    os_injector_env_disabled  CC=1  out:3
    os_injector_env_forced  CC=1  out:3
    post_focus_delay_seconds  CC=3  out:5
    session_type  CC=4  out:4
  src.gillm.runtime.profiles  [8 funcs]
    _read_json  CC=4  out:5
    capture_from_xdotool  CC=1  out:1
    capture_mouse_xy  CC=7  out:10
    default_config_path  CC=1  out:1
    iter_config_paths  CC=4  out:11
    load_profile  CC=5  out:12
    save_profile  CC=3  out:7
    try_load_profile  CC=4  out:3

EDGES:
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints._hints_for_kind
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints._dedupe
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints.recovery_hints_for_reload
  src.gillm.recovery.repair_hints._hints_for_kind → src.gillm.recovery.repair_hints.recovery_hints_for_reload
  src.gillm.recovery.diagnose.probe_environment → src.gillm.runtime.env.session_type
  src.gillm.recovery.diagnose.probe_environment → src.gillm.runtime.env.is_wayland_session
  src.gillm.recovery.diagnose.diagnose_drive_reply → src.gillm.recovery.diagnose.classify_failure
  src.gillm.recovery.diagnose.diagnose_drive_reply → src.gillm.recovery.diagnose.probe_environment
  src.gillm.recovery.diagnose.diagnose_drive_reply → src.gillm.recovery.repair_hints.recovery_hints_for_context
  src.gillm.capture.portal_backend.capture_portal_png → src.gillm.capture.portal_backend._portal_python
  src.gillm.capture.mss_backend.capture_primary_rgb → src.gillm.capture.mss_backend.resolve_scale
  src.gillm.capture.mss_backend.capture_primary_rgb → src.gillm.capture.mss_backend.downscale_rgb_nearest
  src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback → src.gillm.capture.portal_backend.capture_portal_png
  src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback → src.gillm.capture.mss_backend._parse_png_to_rgb
  src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback → src.gillm.capture.mss_backend.capture_primary_rgb
  src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback → src.gillm.capture.mss_backend.rgb_mostly_black
  src.gillm.capture.mss_backend._parse_png_to_rgb → src.gillm.capture.mss_backend.resolve_scale
  src.gillm.injection.backends._log → src.gillm.orchestrator.drive.DriveOrchestrator.log
  src.gillm.injection.backends.type_with_xdotool → src.gillm.injection.backends._log
  src.gillm.injection.backends.type_with_wtype → src.gillm.injection.backends._log
  src.gillm.injection.backends.type_with_wtype → src.gillm.injection.backends.press_wtype
  src.gillm.injection.backends.type_with_ydotool → src.gillm.injection.backends._log
  src.gillm.injection.backends.type_with_ydotool → src.gillm.injection.backends._ydotool_submit_command
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends._log
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.extra_enter_count
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.type_with_xdotool
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.type_with_wtype
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.type_with_ydotool
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.ydotool_enter_keycode
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.ydotool_submit_mode
  src.gillm.injection.backends.type_with_backend → src.gillm.injection.backends.ydotool_ctrl_keycode
  src.gillm.injection.injector._submit_key_for → src.gillm.config.cached_config
  src.gillm.injection.injector._session_type → src.gillm.runtime.env.session_type
  src.gillm.injection.injector.Injector._type_with_backend → src.gillm.injection.backends.type_with_backend
  src.gillm.injection.injector.Injector.type_text → src.gillm.injection.injector._submit_key_for
  src.gillm.injection.injector.Injector.submit_only → src.gillm.injection.injector._submit_key_for
  src.gillm.injection.os_injector._resolve_input_method → src.gillm.runtime.env.input_mode_from_env
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.backends._log
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.os_injector._focus_with_ydotool
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.os_injector._focus_with_xdotool
  src.gillm.injection.os_injector._focus_with_ydotool → src.gillm.injection.backends._log
  src.gillm.injection.os_injector._focus_with_xdotool → src.gillm.injection.backends._log
  src.gillm.injection.os_injector._inject_profile_text → src.gillm.injection.backends._log
  src.gillm.injection.os_injector.focus_with_profile → src.gillm.runtime.env.focus_mode_from_env
  src.gillm.injection.os_injector.focus_with_profile → src.gillm.runtime.env.post_focus_delay_seconds
  src.gillm.injection.os_injector.focus_with_profile → src.gillm.injection.os_injector._focus_profile_chat
  src.gillm.injection.os_injector.focus_with_profile → src.gillm.injection.os_injector._injection_result
  src.gillm.injection.os_injector.inject_with_profile → src.gillm.runtime.env.focus_mode_from_env
  src.gillm.injection.os_injector.inject_with_profile → src.gillm.injection.os_injector._resolve_input_method
  src.gillm.injection.os_injector.inject_with_profile → src.gillm.runtime.env.post_focus_delay_seconds
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 108f 7357L | python:79,json:13,toml:7,shell:4,yaml:2,proto:2 | 2026-06-08
# generated in 0.02s
# CC̅=4.0 | critical:12/286 | dups:0 | cycles:0

HEALTH[12]:
  🟡 CC    _hints_for_kind CC=15 (limit:15)
  🟡 CC    classify_failure CC=24 (limit:15)
  🟡 CC    execute CC=18 (limit:15)
  🟡 CC    drive_payload_to_action_plan CC=21 (limit:15)
  🟡 CC    main CC=16 (limit:15)
  🟡 CC    dispatch CC=15 (limit:15)
  🟡 CC    _handle_subcommand CC=19 (limit:15)
  🟡 CC    _set_body CC=17 (limit:15)
  🟡 CC    envelope_to_dict CC=26 (limit:15)
  🟡 CC    uri_to_dsl CC=26 (limit:15)
  🟡 CC    parse_line CC=46 (limit:15)
  🟡 CC    to_text CC=22 (limit:15)

REFACTOR[1]:
  1. split 12 high-CC methods  (CC>15)

PIPELINES[119]:
  [1] Src [to_dict]: to_dict
      PURITY: 100% pure
  [2] Src [to_dict]: to_dict
      PURITY: 100% pure
  [3] Src [diagnose_drive_reply]: diagnose_drive_reply → classify_failure
      PURITY: 100% pure
  [4] Src [_which]: _which
      PURITY: 100% pure
  [5] Src [_session_type]: _session_type → session_type
      PURITY: 100% pure
  [6] Src [_default_runner]: _default_runner
      PURITY: 100% pure
  [7] Src [probe]: probe
      PURITY: 100% pure
  [8] Src [_candidate_backends]: _candidate_backends
      PURITY: 100% pure
  [9] Src [select_backend]: select_backend
      PURITY: 100% pure
  [10] Src [_type_with_backend]: _type_with_backend → type_with_backend → _log → log
      PURITY: 100% pure
  [11] Src [_type_text_backends]: _type_text_backends
      PURITY: 100% pure
  [12] Src [_log_type_text_request]: _log_type_text_request
      PURITY: 100% pure
  [13] Src [_dry_run_type_text_result]: _dry_run_type_text_result
      PURITY: 100% pure
  [14] Src [_try_type_text_backends]: _try_type_text_backends
      PURITY: 100% pure
  [15] Src [_all_type_backends_failed]: _all_type_backends_failed
      PURITY: 100% pure
  [16] Src [type_text]: type_text → _submit_key_for → cached_config → _cached_config → ...(2 more)
      PURITY: 100% pure
  [17] Src [submit_only]: submit_only → _submit_key_for → cached_config → _cached_config → ...(2 more)
      PURITY: 100% pure
  [18] Src [_call]: _call
      PURITY: 100% pure
  [19] Src [try_drive_with_profile]: try_drive_with_profile → _os_injector_skip_reason → os_injector_env_disabled
      PURITY: 100% pure
  [20] Src [try_os_injector_drive]: try_os_injector_drive
      PURITY: 100% pure
  [21] Src [format_os_injector_ack]: format_os_injector_ack
      PURITY: 100% pure
  [22] Src [apply_keyboard_injection]: apply_keyboard_injection
      PURITY: 100% pure
  [23] Src [register_os_strategy]: register_os_strategy
      PURITY: 100% pure
  [24] Src [matches_current_environment]: matches_current_environment
      PURITY: 100% pure
  [25] Src [capabilities]: capabilities
      PURITY: 100% pure
  [26] Src [focus_window]: focus_window
      PURITY: 100% pure
  [27] Src [inject_keys]: inject_keys
      PURITY: 100% pure
  [28] Src [_focus_via_xdotool]: _focus_via_xdotool → _run
      PURITY: 100% pure
  [29] Src [_focus_via_wmctrl]: _focus_via_wmctrl → _run
      PURITY: 100% pure
  [30] Src [_inject_via_xdotool]: _inject_via_xdotool → _run
      PURITY: 100% pure
  [31] Src [_run]: _run
      PURITY: 100% pure
  [32] Src [matches_current_environment]: matches_current_environment
      PURITY: 100% pure
  [33] Src [capabilities]: capabilities
      PURITY: 100% pure
  [34] Src [focus_window]: focus_window
      PURITY: 100% pure
  [35] Src [inject_keys]: inject_keys → _prefer_ydotool → _gnome_compositor
      PURITY: 100% pure
  [36] Src [_focus_via_wmctrl]: _focus_via_wmctrl → _run
      PURITY: 100% pure
  [37] Src [_inject_via_wtype]: _inject_via_wtype → _run
      PURITY: 100% pure
  [38] Src [_inject_via_ydotool]: _inject_via_ydotool → _scan_for_key
      PURITY: 100% pure
  [39] Src [__post_init__]: __post_init__
      PURITY: 100% pure
  [40] Src [_term_program_is_vscode_family]: _term_program_is_vscode_family
      PURITY: 100% pure
  [41] Src [__repr__]: __repr__
      PURITY: 100% pure
  [42] Src [_run]: _run
      PURITY: 100% pure
  [43] Src [capabilities]: capabilities
      PURITY: 100% pure
  [44] Src [focus_window]: focus_window → _run
      PURITY: 100% pure
  [45] Src [matches_current_environment]: matches_current_environment
      PURITY: 100% pure
  [46] Src [capabilities]: capabilities
      PURITY: 100% pure
  [47] Src [focus_window]: focus_window
      PURITY: 100% pure
  [48] Src [__init__]: __init__ → session_type
      PURITY: 100% pure
  [49] Src [probe]: probe → session_type
      PURITY: 100% pure
  [50] Src [focus]: focus → try_load_profile → iter_config_paths
      PURITY: 100% pure

LAYERS:
  packages/                       CC̄=5.0    ←in:0  →out:0
  │ __init__                   244L  1C   15m  CC=8      ←1
  │ !! grammar                    176L  0C    3m  CC=46     ←2
  │ !! cli                        166L  0C    5m  CC=19     ←0
  │ !! pb_codec                   151L  0C    8m  CC=26     ←4
  │ events                     133L  2C    6m  CC=8      ←0
  │ codegen                    112L  0C    7m  CC=10     ←1
  │ models                      96L  11C    0m  CC=0.0    ←0
  │ !! bus                         88L  0C    3m  CC=15     ←9
  │ app                         87L  0C    1m  CC=1      ←1
  │ server                      83L  1C    6m  CC=2      ←1
  │ llm_backend                 80L  2C    4m  CC=6      ←1
  │ !! cli                         70L  0C    1m  CC=16     ←0
  │ command.proto               67L  0C    0m  CC=0.0    ←0
  │ codec                       66L  0C    8m  CC=3      ←2
  │ cli                         63L  0C    1m  CC=12     ←0
  │ command_pb2                 58L  0C    0m  CC=0.0    ←0
  │ cli                         55L  0C    1m  CC=10     ←0
  │ !! decode                      54L  0C    1m  CC=26     ←2
  │ nlp2uri                     54L  1C    3m  CC=12     ←2
  │ to_dsl                      53L  0C    2m  CC=13     ←3
  │ uri                         52L  0C    6m  CC=7      ←2
  │ schema_registry             49L  0C    4m  CC=5      ←3
  │ result_pb2                  39L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              35L  0C    0m  CC=0.0    ←0
  │ __init__                    34L  0C    0m  CC=0.0    ←0
  │ shell                       33L  0C    1m  CC=9      ←1
  │ pyproject.toml              31L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              31L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              31L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              29L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              29L  0C    0m  CC=0.0    ←0
  │ result                      28L  1C    1m  CC=1      ←0
  │ cli                         27L  0C    1m  CC=2      ←0
  │ cli                         22L  0C    1m  CC=2      ←0
  │ result.proto                22L  0C    0m  CC=0.0    ←0
  │ __init__                    18L  0C    0m  CC=0.0    ←0
  │ install-dev.sh              14L  0C    0m  CC=0.0    ←0
  │ inject.schema.json          13L  0C    0m  CC=0.0    ←0
  │ execute.schema.json         12L  0C    0m  CC=0.0    ←0
  │ run                         11L  0C    1m  CC=1      ←1
  │ focus.schema.json           11L  0C    0m  CC=0.0    ←0
  │ validate.schema.json        11L  0C    0m  CC=0.0    ←0
  │ simulate.schema.json        11L  0C    0m  CC=0.0    ←0
  │ capture.schema.json         10L  0C    0m  CC=0.0    ←0
  │ resolve.schema.json         10L  0C    0m  CC=0.0    ←0
  │ parse.schema.json           10L  0C    0m  CC=0.0    ←0
  │ health.schema.json           9L  0C    0m  CC=0.0    ←0
  │ actions.schema.json          9L  0C    0m  CC=0.0    ←0
  │ orient.schema.json           9L  0C    0m  CC=0.0    ←0
  │ generate-proto.sh            6L  0C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │ engine                       5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │
  src/                            CC̄=3.5    ←in:0  →out:0
  │ os_injector                323L  0C   10m  CC=9      ←1
  │ injector                   276L  3C   18m  CC=10     ←0
  │ wayland                    236L  1C   11m  CC=9      ←0
  │ backends                   207L  0C   11m  CC=5      ←2
  │ !! composite                  180L  1C    8m  CC=18     ←0
  │ drive                      168L  1C    8m  CC=12     ←1
  │ !! diagnose                   150L  2C    5m  CC=24     ←1
  │ driver                     136L  7C   11m  CC=2      ←0
  │ mss_backend                130L  1C    6m  CC=6      ←1
  │ x11                        128L  1C    8m  CC=11     ←2
  │ profiles                   117L  1C    9m  CC=7      ←2
  │ portal_backend             113L  1C    2m  CC=8      ←1
  │ strategy                   108L  5C    7m  CC=5      ←0
  │ config                     105L  1C    8m  CC=7      ←1
  │ !! repair_hints                98L  0C    4m  CC=15     ←2
  │ main                        97L  0C    2m  CC=14     ←0
  │ backend_selector            96L  1C    8m  CC=6      ←0
  │ !! koru                        94L  0C    3m  CC=21     ←0
  │ dry_run                     89L  1C    8m  CC=10     ←0
  │ command_runner              88L  1C    7m  CC=7      ←1
  │ env                         87L  0C   10m  CC=6      ←6
  │ contract                    78L  0C    2m  CC=7      ←1
  │ darwin                      72L  1C    5m  CC=4      ←0
  │ drive_backend               66L  0C    3m  CC=4      ←0
  │ activity                    62L  0C    5m  CC=3      ←1
  │ __init__                    55L  0C    2m  CC=3      ←0
  │ __init__                    51L  0C    0m  CC=0.0    ←0
  │ registry                    50L  0C    4m  CC=5      ←2
  │ client                      44L  1C    3m  CC=2      ←0
  │ windows                     43L  1C    4m  CC=1      ←0
  │ control                     39L  0C    4m  CC=3      ←0
  │ __init__                    37L  0C    0m  CC=0.0    ←0
  │ __init__                    33L  0C    0m  CC=0.0    ←0
  │ __init__                    23L  0C    0m  CC=0.0    ←0
  │ __init__                    20L  0C    0m  CC=0.0    ←0
  │ __init__                    16L  0C    0m  CC=0.0    ←0
  │ errors                      10L  1C    0m  CC=0.0    ←0
  │ __init__                     8L  0C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │ errors                       5L  1C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ Makefile                   293L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              76L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │
  fixtures/                       CC̄=0.0    ←in:0  →out:0
  │ workflow-dry.json            4L  0C    0m  CC=0.0    ←0
  │ workflow.json                3L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                        packages.dsl2gillm            src.gillm   packages.mcp2gillm  packages.rest2gillm   packages.nlp2gillm   packages.cli2gillm   packages.uri2gillm
   packages.dsl2gillm                   ──                    4                   ←7                   ←6                    1                   ←3                   ←1  hub
            src.gillm                    8                   ──                                                                                                           !! fan-out
   packages.mcp2gillm                    7                                        ──                                         1                                            !! fan-out
  packages.rest2gillm                    6                                                             ──                                                               
   packages.nlp2gillm                    1                                        ←1                                        ──                                         1
   packages.cli2gillm                    3                                                                                                       ──                     
   packages.uri2gillm                    1                                                                                  ←1                                        ──
  CYCLES: none
  HUB: packages.dsl2gillm/ (fan-in=26)
  SMELL: src.gillm/ fan-out=8 → split needed
  SMELL: packages.mcp2gillm/ fan-out=8 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 3 groups | 78f 5902L | 2026-06-08

SUMMARY:
  files_scanned: 78
  total_lines:   5902
  dup_groups:    3
  dup_fragments: 7
  saved_lines:   31
  scan_ms:       2243

HOTSPOTS[4] (files with most duplication):
  src/gillm/focus/wayland.py  dup=17L  groups=2  frags=2  (0.3%)
  src/gillm/focus/x11.py  dup=17L  groups=2  frags=2  (0.3%)
  src/gillm/injection/backends.py  dup=12L  groups=1  frags=2  (0.2%)
  src/gillm/focus/darwin.py  dup=8L  groups=1  frags=1  (0.1%)

DUPLICATES[3] (ranked by impact):
  [f4d731ab73329152]   EXAC  _run  L=8 N=3 saved=16 sim=1.00
      src/gillm/focus/darwin.py:20-27  (_run)
      src/gillm/focus/wayland.py:21-28  (_run)
      src/gillm/focus/x11.py:21-28  (_run)
  [d9985d8bb1d9ca01]   EXAC  _focus_via_wmctrl  L=9 N=2 saved=9 sim=1.00
      src/gillm/focus/wayland.py:180-188  (_focus_via_wmctrl)
      src/gillm/focus/x11.py:106-114  (_focus_via_wmctrl)
  [c66988d54f59cb9c]   STRU  ydotool_enter_keycode  L=6 N=2 saved=6 sim=1.00
      src/gillm/injection/backends.py:14-19  (ydotool_enter_keycode)
      src/gillm/injection/backends.py:32-37  (ydotool_ctrl_keycode)

REFACTOR[3] (ranked by priority):
  [1] ○ extract_function   → src/gillm/focus/utils/_run.py
      WHY: 3 occurrences of 8-line block across 3 files — saves 16 lines
      FILES: src/gillm/focus/darwin.py, src/gillm/focus/wayland.py, src/gillm/focus/x11.py
  [2] ○ extract_function   → src/gillm/focus/utils/_focus_via_wmctrl.py
      WHY: 2 occurrences of 9-line block across 2 files — saves 9 lines
      FILES: src/gillm/focus/wayland.py, src/gillm/focus/x11.py
  [3] ○ extract_function   → src/gillm/injection/utils/ydotool_enter_keycode.py
      WHY: 2 occurrences of 6-line block across 1 files — saves 6 lines
      FILES: src/gillm/injection/backends.py

QUICK_WINS[3] (low risk, high savings — do first):
  [1] extract_function   saved=16L  → src/gillm/focus/utils/_run.py
      FILES: darwin.py, wayland.py, x11.py
  [2] extract_function   saved=9L  → src/gillm/focus/utils/_focus_via_wmctrl.py
      FILES: wayland.py, x11.py
  [3] extract_function   saved=6L  → src/gillm/injection/utils/ydotool_enter_keycode.py
      FILES: backends.py

EFFORT_ESTIMATE (total ≈ 1.0h):
  medium _run                                saved=16L  ~32min
  easy   _focus_via_wmctrl                   saved=9L  ~18min
  easy   ydotool_enter_keycode               saved=6L  ~12min

METRICS-TARGET:
  dup_groups:  3 → 0
  saved_lines: 31 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 286 func | 54f | 2026-06-08
# generated in 0.00s

NEXT[10] (ranked by impact):
  [1] !! SPLIT-FUNC      parse_line  CC=46  fan=16
      WHY: CC=46 exceeds 15
      EFFORT: ~1h  IMPACT: 736

  [2] !  SPLIT-FUNC      _handle_subcommand  CC=19  fan=22
      WHY: CC=19 exceeds 15
      EFFORT: ~1h  IMPACT: 418

  [3] !  SPLIT-FUNC      main  CC=16  fan=17
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 272

  [4] !  SPLIT-FUNC      dispatch  CC=15  fan=18
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 270

  [5] !  SPLIT-FUNC      CompositeGuiDriver.execute  CC=18  fan=14
      WHY: CC=18 exceeds 15
      EFFORT: ~1h  IMPACT: 252

  [6] !  SPLIT-FUNC      drive_payload_to_action_plan  CC=21  fan=11
      WHY: CC=21 exceeds 15
      EFFORT: ~1h  IMPACT: 231

  [7] !! SPLIT-FUNC      uri_to_dsl  CC=26  fan=8
      WHY: CC=26 exceeds 15
      EFFORT: ~1h  IMPACT: 208

  [8] !  SPLIT-FUNC      to_text  CC=22  fan=8
      WHY: CC=22 exceeds 15
      EFFORT: ~1h  IMPACT: 176

  [9] !  SPLIT-FUNC      _set_body  CC=17  fan=8
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 136

  [10] !! SPLIT-FUNC      envelope_to_dict  CC=26  fan=5
      WHY: CC=26 exceeds 15
      EFFORT: ~1h  IMPACT: 130


RISKS[1]:
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          4.0 → ≤2.8
  max-CC:      46 → ≤20
  god-modules: 1 → 0
  high-CC(≥15): 12 → ≤6
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  prev CC̄=3.6 → now CC̄=4.0
```

## Intent

GUI Control Plugin with NLP & Intent Contracts

**Navigation:** [README.md](README.md) · [SUMD.md](SUMD.md) (full) · [packages/README.md](packages/README.md) · [project/](project/README.md)
