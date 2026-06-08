# gillm

GUI Control Plugin with NLP & Intent Contracts

**See also:** [README.md](README.md) (user guide) · [SUMR.md](SUMR.md) (compact refactor view) · [packages/README.md](packages/README.md) (control layer) · [CHANGELOG.md](CHANGELOG.md) · [project/](project/README.md) (code analysis)

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `gillm`
- **version**: `0.1.10`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, goal.yaml, .env.example, project/(3 analysis files)

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

## Interfaces

### CLI Entry Points

- `gillm`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m gillm
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m gillm --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m gillm --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m gillm --help" 10000
ASSERT_EXIT_CODE 0
```

## Workflows

## Configuration

```yaml
project:
  name: gillm
  version: 0.1.10
  env: local
```

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

## Deployment

```bash markpact:run
pip install gillm

# development install
pip install -e .[dev]
```

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | `*(not set)*` | Required: OpenRouter API key (https://openrouter.ai/keys) |
| `LLM_MODEL` | `openrouter/qwen/qwen3-coder-next` | Model (default: openrouter/qwen/qwen3-coder-next) |
| `PFIX_AUTO_APPLY` | `true` | true = apply fixes without asking |
| `PFIX_AUTO_INSTALL_DEPS` | `true` | true = auto pip/uv install |
| `PFIX_AUTO_RESTART` | `false` | true = os.execv restart after fix |
| `PFIX_MAX_RETRIES` | `3` |  |
| `PFIX_DRY_RUN` | `false` |  |
| `PFIX_ENABLED` | `true` |  |
| `PFIX_GIT_COMMIT` | `false` | true = auto-commit fixes |
| `PFIX_GIT_PREFIX` | `pfix:` | commit message prefix |
| `PFIX_CREATE_BACKUPS` | `false` | false = disable .pfix_backups/ directory |

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`gillm`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `venv/lib/python3.13/site-packages/cryptography/__init__.py:__version__`

## Makefile Targets

- `VENV`
- `PYTHON`
- `PIP`
- `help` — Default target
- `venv`
- `VENV_TARGETS`
- `install`
- `dev-install`
- `test`
- `test-fast` — Fast tests - exclude slow and integration tests
- `test-slow` — Slow tests only
- `test-integration` — Integration tests only
- `test-unit` — Unit tests only
- `test-cov`
- `test-toon`
- `validate-toon`
- `test-all-formats`
- `test-comprehensive`
- `lint`
- `format`
- `typecheck`
- `check`
- `run`
- `analyze`
- `analyze-all`
- `toon-demo`
- `toon-compare`
- `toon-validate`
- `build`
- `publish-test`
- `bump-patch`
- `bump-minor`
- `bump-major`
- `publish`
- `mermaid-png`
- `install-mermaid`
- `check-mermaid`
- `clean`
- `clean-png`
- `quickstart`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# gillm | 103f 8038L | python:98,shell:4,less:1 | 2026-06-08
# stats: 275 func | 59 cls | 103 mod | CC̄=4.1 | critical:17 | cycles:0
# alerts[5]: CC parse_line=46; CC envelope_to_dict=26; CC uri_to_dsl=26; CC classify_failure=24; CC to_text=22
# hotspots[5]: create_app fan=24; _handle_subcommand fan=22; dispatch fan=17; main fan=15; parse_line fan=12
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[103]:
  app.doql.less,366
  packages/cli2gillm/src/cli2gillm/__init__.py,2
  packages/cli2gillm/src/cli2gillm/cli.py,71
  packages/cli2gillm/src/cli2gillm/shell.py,34
  packages/cli2gillm/tests/test_cli2gillm.py,7
  packages/dsl2gillm/scripts/generate-proto.sh,7
  packages/dsl2gillm/src/dsl2gillm/__init__.py,35
  packages/dsl2gillm/src/dsl2gillm/bus.py,89
  packages/dsl2gillm/src/dsl2gillm/cli.py,167
  packages/dsl2gillm/src/dsl2gillm/codec.py,67
  packages/dsl2gillm/src/dsl2gillm/codegen.py,113
  packages/dsl2gillm/src/dsl2gillm/engine.py,6
  packages/dsl2gillm/src/dsl2gillm/events.py,134
  packages/dsl2gillm/src/dsl2gillm/grammar.py,177
  packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py,245
  packages/dsl2gillm/src/dsl2gillm/models.py,97
  packages/dsl2gillm/src/dsl2gillm/pb_codec.py,152
  packages/dsl2gillm/src/dsl2gillm/result.py,29
  packages/dsl2gillm/src/dsl2gillm/schema_registry.py,50
  packages/dsl2gillm/src/dsl2gillm/v1/__init__.py,2
  packages/dsl2gillm/src/dsl2gillm/v1/command_pb2.py,59
  packages/dsl2gillm/src/dsl2gillm/v1/result_pb2.py,40
  packages/dsl2gillm/tests/test_bus.py,41
  packages/dsl2gillm/tests/test_codegen.py,19
  packages/dsl2gillm/tests/test_dry_run.py,14
  packages/dsl2gillm/tests/test_parity.py,19
  packages/dsl2gillm/tests/test_parity_adapters.py,51
  packages/dsl2gillm/tests/test_protobuf.py,18
  packages/install-dev.sh,15
  packages/mcp2gillm/src/mcp2gillm/__init__.py,6
  packages/mcp2gillm/src/mcp2gillm/cli.py,23
  packages/mcp2gillm/src/mcp2gillm/server.py,84
  packages/mcp2gillm/tests/test_mcp2gillm.py,6
  packages/nlp2gillm/src/nlp2gillm/__init__.py,7
  packages/nlp2gillm/src/nlp2gillm/cli.py,56
  packages/nlp2gillm/src/nlp2gillm/llm_backend.py,81
  packages/nlp2gillm/src/nlp2gillm/to_dsl.py,54
  packages/nlp2gillm/tests/test_llm_backend.py,12
  packages/nlp2gillm/tests/test_to_dsl.py,10
  packages/rest2gillm/src/rest2gillm/__init__.py,6
  packages/rest2gillm/src/rest2gillm/app.py,88
  packages/rest2gillm/src/rest2gillm/cli.py,28
  packages/rest2gillm/tests/test_rest2gillm.py,29
  packages/uri2gillm/src/uri2gillm/__init__.py,19
  packages/uri2gillm/src/uri2gillm/cli.py,64
  packages/uri2gillm/src/uri2gillm/decode.py,55
  packages/uri2gillm/src/uri2gillm/nlp2uri.py,55
  packages/uri2gillm/src/uri2gillm/run.py,12
  packages/uri2gillm/src/uri2gillm/uri.py,53
  packages/uri2gillm/tests/test_uri.py,15
  project.sh,50
  src/gillm/__init__.py,56
  src/gillm/adapters/__init__.py,6
  src/gillm/adapters/koru.py,95
  src/gillm/capture/__init__.py,17
  src/gillm/capture/mss_backend.py,131
  src/gillm/capture/portal_backend.py,114
  src/gillm/cli/__init__.py,6
  src/gillm/cli/main.py,98
  src/gillm/config.py,106
  src/gillm/contracts/__init__.py,24
  src/gillm/contracts/driver.py,137
  src/gillm/control.py,40
  src/gillm/drivers/__init__.py,7
  src/gillm/drivers/composite.py,181
  src/gillm/drivers/dry_run.py,90
  src/gillm/focus/__init__.py,38
  src/gillm/focus/darwin.py,73
  src/gillm/focus/registry.py,51
  src/gillm/focus/strategy.py,109
  src/gillm/focus/wayland.py,237
  src/gillm/focus/windows.py,44
  src/gillm/focus/x11.py,129
  src/gillm/injection/__init__.py,34
  src/gillm/injection/backends.py,208
  src/gillm/injection/drive_backend.py,67
  src/gillm/injection/errors.py,11
  src/gillm/injection/injector.py,277
  src/gillm/injection/os_injector.py,324
  src/gillm/intents/__init__.py,6
  src/gillm/intents/contract.py,79
  src/gillm/nlp_bridge/__init__.py,6
  src/gillm/nlp_bridge/client.py,45
  src/gillm/orchestrator/__init__.py,9
  src/gillm/orchestrator/drive.py,169
  src/gillm/recovery/__init__.py,21
  src/gillm/recovery/diagnose.py,151
  src/gillm/recovery/repair_hints.py,99
  src/gillm/runtime/__init__.py,52
  src/gillm/runtime/activity.py,63
  src/gillm/runtime/backend_selector.py,97
  src/gillm/runtime/command_runner.py,89
  src/gillm/runtime/env.py,88
  src/gillm/runtime/errors.py,6
  src/gillm/runtime/profiles.py,118
  tests/test_drive_backend.py,72
  tests/test_gillm.py,105
  tests/test_gui_driver.py,43
  tests/test_injector.py,286
  tests/test_os_injector.py,352
  tests/test_os_strategies.py,382
  tests/test_recovery.py,49
  tree.sh,2
D:
  packages/cli2gillm/src/cli2gillm/__init__.py:
  packages/cli2gillm/src/cli2gillm/cli.py:
    e: main
    main(argv)
  packages/cli2gillm/src/cli2gillm/shell.py:
    e: run_shell
    run_shell()
  packages/cli2gillm/tests/test_cli2gillm.py:
    e: test_exec_health_via_bus
    test_exec_health_via_bus()
  packages/dsl2gillm/src/dsl2gillm/__init__.py:
  packages/dsl2gillm/src/dsl2gillm/bus.py:
    e: dispatch,execute_dsl_line,execute_dsl
    dispatch(command)
    execute_dsl_line(line)
    execute_dsl(text)
  packages/dsl2gillm/src/dsl2gillm/cli.py:
    e: _run_results,main,_main_subcommand,_main_legacy,_handle_subcommand
    _run_results(results)
    main(argv)
    _main_subcommand(argv)
    _main_legacy(argv)
    _handle_subcommand(args)
  packages/dsl2gillm/src/dsl2gillm/codec.py:
    e: _validate_with_pydantic,validate_payload,parse_text,envelope_to_bytes,envelope_from_bytes,envelope_to_json,envelope_from_json,roundtrip_text
    _validate_with_pydantic(payload;verb)
    validate_payload(payload)
    parse_text(line)
    envelope_to_bytes(payload)
    envelope_from_bytes(data)
    envelope_to_json(payload)
    envelope_from_json(data)
    roundtrip_text(line)
  packages/dsl2gillm/src/dsl2gillm/codegen.py:
    e: _schema_type,_model_name,_field_line,render_models,load_schemas,generate_models,main
    _schema_type(prop)
    _model_name(verb)
    _field_line(name;prop)
    render_models(schemas)
    load_schemas()
    generate_models(output)
    main()
  packages/dsl2gillm/src/dsl2gillm/engine.py:
  packages/dsl2gillm/src/dsl2gillm/events.py:
    e: StoredEvent,EventStore
    StoredEvent: to_dict(0)
    EventStore: __init__(1),for_workdir(2),append_command(2),read_all(0),replay(0)
  packages/dsl2gillm/src/dsl2gillm/grammar.py:
    e: _steps_from_line,parse_line,to_text
    _steps_from_line(line;rest)
    parse_line(line)
    to_text(payload)
  packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py:
    e: _load_steps,run_query,run_command,_health,_orient,_actions,_parse,_validate,_resolve,_capture,_execute,_simulate,_focus,_inject,HandlerResult
    HandlerResult: to_dict(0)
    _load_steps(payload)
    run_query(payload)
    run_command(payload)
    _health()
    _orient()
    _actions()
    _parse(payload)
    _validate(payload)
    _resolve(payload)
    _capture(payload)
    _execute(payload)
    _simulate(payload)
    _focus(payload)
    _inject(payload)
  packages/dsl2gillm/src/dsl2gillm/models.py:
    e: ActionsCommand,CaptureCommand,ExecuteCommand,FocusCommand,HealthCommand,InjectCommand,OrientCommand,ParseCommand,ResolveCommand,SimulateCommand,ValidateCommand
    ActionsCommand:
    CaptureCommand:
    ExecuteCommand:
    FocusCommand:
    HealthCommand:
    InjectCommand:
    OrientCommand:
    ParseCommand:
    ResolveCommand:
    SimulateCommand:
    ValidateCommand:
  packages/dsl2gillm/src/dsl2gillm/pb_codec.py:
    e: _set_body,envelope_to_dict,encode_protobuf,decode_protobuf,encode_text_to_protobuf,decode_protobuf_to_text,result_to_pb,encode_result_protobuf
    _set_body(envelope;cmd)
    envelope_to_dict(envelope)
    encode_protobuf(cmd)
    decode_protobuf(data)
    encode_text_to_protobuf(line)
    decode_protobuf_to_text(data)
    result_to_pb(result)
    encode_result_protobuf(result)
  packages/dsl2gillm/src/dsl2gillm/result.py:
    e: DslResult
    DslResult: to_dict(0)
  packages/dsl2gillm/src/dsl2gillm/schema_registry.py:
    e: _load_schemas,schema_for_verb,all_verbs,validate_schemas
    _load_schemas()
    schema_for_verb(verb)
    all_verbs()
    validate_schemas()
  packages/dsl2gillm/src/dsl2gillm/v1/__init__.py:
  packages/dsl2gillm/src/dsl2gillm/v1/command_pb2.py:
  packages/dsl2gillm/src/dsl2gillm/v1/result_pb2.py:
  packages/dsl2gillm/tests/test_bus.py:
    e: test_health,test_orient,test_actions,test_validate_steps,test_simulate_wait
    test_health()
    test_orient()
    test_actions()
    test_validate_steps()
    test_simulate_wait()
  packages/dsl2gillm/tests/test_codegen.py:
    e: test_load_schemas_has_all_verbs,test_generate_models
    test_load_schemas_has_all_verbs()
    test_generate_models(tmp_path)
  packages/dsl2gillm/tests/test_dry_run.py:
    e: test_simulate_workflow_fixture
    test_simulate_workflow_fixture()
  packages/dsl2gillm/tests/test_parity.py:
    e: test_parity_text_vs_dict_health,test_parity_text_vs_dict_validate
    test_parity_text_vs_dict_health()
    test_parity_text_vs_dict_validate()
  packages/dsl2gillm/tests/test_parity_adapters.py:
    e: _baseline,test_parity_text_vs_protobuf,test_parity_uri_adapter,test_parity_rest_adapter,test_parity_simulate_offline
    _baseline()
    test_parity_text_vs_protobuf()
    test_parity_uri_adapter()
    test_parity_rest_adapter()
    test_parity_simulate_offline()
  packages/dsl2gillm/tests/test_protobuf.py:
    e: test_encode_decode_health,test_roundtrip_health,test_roundtrip_parse
    test_encode_decode_health()
    test_roundtrip_health()
    test_roundtrip_parse()
  packages/mcp2gillm/src/mcp2gillm/__init__.py:
  packages/mcp2gillm/src/mcp2gillm/cli.py:
    e: main
    main(argv)
  packages/mcp2gillm/src/mcp2gillm/server.py:
    e: _require_fastmcp,create_server,run_server,GillmMCPServer
    GillmMCPServer: __post_init__(0),_register_tools(0),run(0)
    _require_fastmcp()
    create_server(name)
    run_server()
  packages/mcp2gillm/tests/test_mcp2gillm.py:
    e: test_create_server
    test_create_server()
  packages/nlp2gillm/src/nlp2gillm/__init__.py:
  packages/nlp2gillm/src/nlp2gillm/cli.py:
    e: main
    main(argv)
  packages/nlp2gillm/src/nlp2gillm/llm_backend.py:
    e: get_backend,nl_to_dsl_line,LLMBackend,LitellmBackend
    LLMBackend: complete(0)
    LitellmBackend: complete(0)
    get_backend(backend)
    nl_to_dsl_line(prompt)
  packages/nlp2gillm/src/nlp2gillm/to_dsl.py:
    e: to_dsl,apply_nl
    to_dsl(prompt)
    apply_nl(prompt)
  packages/nlp2gillm/tests/test_llm_backend.py:
    e: test_nl_to_dsl_line_fake_backend,_FakeBackend
    _FakeBackend: complete(0)
    test_nl_to_dsl_line_fake_backend()
  packages/nlp2gillm/tests/test_to_dsl.py:
    e: test_to_dsl_health,test_to_dsl_capture
    test_to_dsl_health()
    test_to_dsl_capture()
  packages/rest2gillm/src/rest2gillm/__init__.py:
  packages/rest2gillm/src/rest2gillm/app.py:
    e: create_app
    create_app()
  packages/rest2gillm/src/rest2gillm/cli.py:
    e: main
    main(argv)
  packages/rest2gillm/tests/test_rest2gillm.py:
    e: test_root_endpoint,test_health_endpoint,test_post_dsl_health
    test_root_endpoint()
    test_health_endpoint()
    test_post_dsl_health()
  packages/uri2gillm/src/uri2gillm/__init__.py:
  packages/uri2gillm/src/uri2gillm/cli.py:
    e: main
    main(argv)
  packages/uri2gillm/src/uri2gillm/decode.py:
    e: uri_to_dsl
    uri_to_dsl(uri)
  packages/uri2gillm/src/uri2gillm/nlp2uri.py:
    e: nlp2uri,best_uri,UriHit
    UriHit: to_dict(0)
    nlp2uri(prompt)
    best_uri(prompt)
  packages/uri2gillm/src/uri2gillm/run.py:
    e: run_uri
    run_uri(uri)
  packages/uri2gillm/src/uri2gillm/uri.py:
    e: _encode,_decode,uri_for_block,uri_for_cmd,is_gillm_uri,parse_gillm_uri
    _encode(value)
    _decode(value)
    uri_for_block()
    uri_for_cmd(verb)
    is_gillm_uri(uri)
    parse_gillm_uri(uri)
  packages/uri2gillm/tests/test_uri.py:
    e: test_decode_health_cmd,test_nlp2uri_capture
    test_decode_health_cmd()
    test_nlp2uri_capture()
  src/gillm/__init__.py:
    e: __getattr__,__dir__
    __getattr__(name)
    __dir__()
  src/gillm/adapters/__init__.py:
  src/gillm/adapters/koru.py:
    e: drive_payload_to_action_plan,koru_drive_to_payload,_steps_from_prefer
    drive_payload_to_action_plan(payload)
    koru_drive_to_payload()
    _steps_from_prefer(prefer)
  src/gillm/capture/__init__.py:
  src/gillm/capture/mss_backend.py:
    e: resolve_scale,downscale_rgb_nearest,rgb_mostly_black,capture_primary_rgb,capture_primary_rgb_wayland_fallback,_parse_png_to_rgb,CapturedImage
    CapturedImage:  # Portable raw image container.
    resolve_scale(override)
    downscale_rgb_nearest(rgb;src_w;src_h;dst_w;dst_h)
    rgb_mostly_black(rgb)
    capture_primary_rgb()
    capture_primary_rgb_wayland_fallback()
    _parse_png_to_rgb(png_bytes)
  src/gillm/capture/portal_backend.py:
    e: _portal_python,capture_portal_png,PortalCaptureError
    PortalCaptureError:  # Portal screenshot failed.
    _portal_python()
    capture_portal_png()
  src/gillm/cli/__init__.py:
  src/gillm/cli/main.py:
    e: _print_result,main
    _print_result(result)
    main()
  src/gillm/config.py:
    e: resolve_xdg_path,default_config_path,_merge_submit_keys,load_config,_cached_config,cached_config,clear_config_cache,AutopilotConfig
    AutopilotConfig: submit_key_for(1)  # In-memory view of ``autopilot.toml`` (or defaults).
    resolve_xdg_path(relative_path)
    default_config_path()
    _merge_submit_keys(raw)
    load_config(path)
    _cached_config()
    cached_config()
    clear_config_cache()
  src/gillm/contracts/__init__.py:
  src/gillm/contracts/driver.py:
    e: WindowTarget,CapturedImage,DriverStatus,ActionResult,ActionPlan,ExecutionOutcome,GuiDriver
    WindowTarget:  # Best-effort window focus target.
    CapturedImage:
    DriverStatus: to_dict(0)
    ActionResult: to_dict(0)
    ActionPlan: chat_inject_and_submit(1)
    ExecutionOutcome: to_dict(0)
    GuiDriver: probe(0),focus(1),type_text(1),hotkey(0),click(2),screenshot(0),execute(1)  # Stable GUI control surface for orchestrators (Koru, CLI, tes
  src/gillm/control.py:
    e: dispatch_health,dispatch_parse,dispatch_execute,dispatch_validate
    dispatch_health()
    dispatch_parse(instruction)
    dispatch_execute()
    dispatch_validate()
  src/gillm/drivers/__init__.py:
  src/gillm/drivers/composite.py:
    e: CompositeGuiDriver
    CompositeGuiDriver: __init__(0),probe(0),focus(1),type_text(1),hotkey(0),click(2),screenshot(0),execute(1)  # Production GuiDriver backed by Injector + os_injector profil
  src/gillm/drivers/dry_run.py:
    e: DryRunGuiDriver
    DryRunGuiDriver: __init__(0),log(0),probe(0),focus(1),type_text(1),hotkey(0),click(2),screenshot(0),execute(1)  # Records actions without touching the OS.
  src/gillm/focus/__init__.py:
  src/gillm/focus/darwin.py:
    e: _run,DarwinStrategy
    DarwinStrategy: matches_current_environment(0),capabilities(0),focus_window(1),inject_keys(1)
    _run(argv)
  src/gillm/focus/registry.py:
    e: register_os_strategy,get_os_strategy,list_os_strategy_ids,resolve_active_os_strategy
    register_os_strategy(strategy)
    get_os_strategy(strategy_id)
    list_os_strategy_ids()
    resolve_active_os_strategy()
  src/gillm/focus/strategy.py:
    e: OsCapabilities,FocusOutcome,KeySequence,OsStrategy,StaticOsIdentityMixin
    OsCapabilities:  # Which OS-level tools are usable in the current session.
    FocusOutcome:  # Result of ``OsStrategy.focus_window``.
    KeySequence: __post_init__(0)  # Portable key sequence description used by :meth:`OsStrategy.
    OsStrategy: id(0),label(0),matches_current_environment(0),capabilities(0),focus_window(1),inject_keys(1),_term_program_is_vscode_family(0),__repr__(0)  # Per-OS knowledge object.
    StaticOsIdentityMixin: id(0),label(0)  # Provide ``id``/``label`` from class-level constants.
  src/gillm/focus/wayland.py:
    e: _run,_scan_for_key,_gnome_compositor,_prefer_ydotool,WaylandLinuxStrategy
    WaylandLinuxStrategy: matches_current_environment(0),capabilities(0),focus_window(1),inject_keys(1),_focus_via_wmctrl(1),_inject_via_wtype(1),_inject_via_ydotool(1)
    _run(argv)
    _scan_for_key(key)
    _gnome_compositor()
    _prefer_ydotool()
  src/gillm/focus/windows.py:
    e: WindowsStrategy
    WindowsStrategy: matches_current_environment(0),capabilities(0),focus_window(1),inject_keys(1)
  src/gillm/focus/x11.py:
    e: _run,X11LinuxStrategy
    X11LinuxStrategy: matches_current_environment(0),capabilities(0),focus_window(1),inject_keys(1),_focus_via_xdotool(1),_focus_via_wmctrl(1),_inject_via_xdotool(1)
    _run(argv)
  src/gillm/injection/__init__.py:
  src/gillm/injection/backends.py:
    e: ydotool_enter_keycode,ydotool_submit_mode,ydotool_ctrl_keycode,extra_enter_count,_log,type_with_xdotool,press_wtype,type_with_wtype,_ydotool_submit_command,type_with_ydotool,type_with_backend
    ydotool_enter_keycode()
    ydotool_submit_mode()
    ydotool_ctrl_keycode()
    extra_enter_count()
    _log(log;message)
    type_with_xdotool(call;log;text;submit_key;extra_enters)
    press_wtype(call;combo)
    type_with_wtype(call;log;text;submit_key;extra_enters)
    _ydotool_submit_command(submit_mode;enter_code;ctrl_code)
    type_with_ydotool(call;log;text;submit_key;extra_enters;enter_code;submit_mode;ctrl_code)
    type_with_backend(call;log;backend;text;submit_key)
  src/gillm/injection/drive_backend.py:
    e: try_os_injector_drive,format_os_injector_ack,apply_keyboard_injection
    try_os_injector_drive(target_id;text;submit)
    format_os_injector_ack(os_res)
    apply_keyboard_injection(injector;text)
  src/gillm/injection/errors.py:
    e: InjectorError
    InjectorError:  # No usable backend, or the backend call failed.
  src/gillm/injection/injector.py:
    e: _submit_key_for,_which,_session_type,_default_runner,BackendStatus,InjectionResult,Injector
    BackendStatus: to_dict(0)  # Result of probing a single backend.
    InjectionResult: to_dict(0)
    Injector: probe(0),_candidate_backends(0),select_backend(0),_type_with_backend(3),_type_text_backends(0),_log_type_text_request(3),_dry_run_type_text_result(0),_try_type_text_backends(4),_all_type_backends_failed(1),type_text(1),submit_only(0),_call(1)  # Pick the best available backend and type text through it.
    _submit_key_for(ide)
    _which(name)
    _session_type()
    _default_runner(cmd;stdin)
  src/gillm/injection/os_injector.py:
    e: _resolve_input_method,_injection_result,_focus_profile_chat,_focus_with_ydotool,_focus_with_xdotool,_inject_profile_text,focus_with_profile,inject_with_profile,_os_injector_skip_reason,try_drive_with_profile
    _resolve_input_method()
    _injection_result()
    _focus_profile_chat(profile;focus;post_focus_delay)
    _focus_with_ydotool(profile;focus)
    _focus_with_xdotool(profile;focus)
    _inject_profile_text()
    focus_with_profile(profile)
    inject_with_profile()
    _os_injector_skip_reason(tool_id)
    try_drive_with_profile()
  src/gillm/intents/__init__.py:
  src/gillm/intents/contract.py:
    e: gui_contract,validate_contract_runtime
    gui_contract(intent;scope;priority;domain;inputs;outputs;required;forbidden;meaning)
    validate_contract_runtime(func)
  src/gillm/nlp_bridge/__init__.py:
  src/gillm/nlp_bridge/client.py:
    e: _heuristic_parse_intent,NLPBridgeClient
    NLPBridgeClient: __init__(0),parse_intent(1)  # Bridge to nlp2dsl when installed; otherwise a small heuristi
    _heuristic_parse_intent(command)
  src/gillm/orchestrator/__init__.py:
  src/gillm/orchestrator/drive.py:
    e: DriveOrchestrator
    DriveOrchestrator: __init__(2),log(1),focus_target_window(1),inject_text(4),capture_screenshot(1),execute_step(2),execute_workflow(2),drive_natural_language(2)  # Consolidated orchestrator for GUI drive tasks.
  src/gillm/recovery/__init__.py:
  src/gillm/recovery/diagnose.py:
    e: probe_environment,classify_failure,diagnose_drive_reply,EnvironmentDiagnostics,DriveFailureContext
    EnvironmentDiagnostics: to_dict(0)
    DriveFailureContext: to_dict(0)
    probe_environment()
    classify_failure()
    diagnose_drive_reply(reply)
  src/gillm/recovery/repair_hints.py:
    e: recovery_hints_for_reload,recovery_hints_for_context,_hints_for_kind,_dedupe
    recovery_hints_for_reload()
    recovery_hints_for_context(ctx)
    _hints_for_kind(kind;ctx)
    _dedupe(items)
  src/gillm/runtime/__init__.py:
  src/gillm/runtime/activity.py:
    e: set_activity_sink,noop_activity_sink,emit_activity,emit_activity_warn,try_bootstrap_koru_activity_sink
    set_activity_sink(sink)
    noop_activity_sink(_category;_message;preview)
    emit_activity(category;message)
    emit_activity_warn(message)
    try_bootstrap_koru_activity_sink()
  src/gillm/runtime/backend_selector.py:
    e: unique_backend_names,session_backend_order,BackendSelector
    BackendSelector: __init__(0),candidate_backends(0),select_backend(0),_forced_backend_candidates(1),_available_backend_candidates(1),probe(0)  # Pick keyboard injection backends for the current session.
    unique_backend_names(names)
    session_backend_order(session)
  src/gillm/runtime/command_runner.py:
    e: run_cmd,run_cmd_checked,xdotool,ydotool,clipboard_backend,set_clipboard,resolve_input_method,CommandResult
    CommandResult:
    run_cmd(cmd)
    run_cmd_checked(cmd)
    xdotool(argv_tail)
    ydotool(argv_tail)
    clipboard_backend()
    set_clipboard(text)
    resolve_input_method()
  src/gillm/runtime/env.py:
    e: session_type,is_wayland_session,os_injector_env_disabled,os_injector_env_forced,dry_run_from_env,focus_mode_from_env,input_mode_from_env,cmd_timeout_seconds,post_focus_delay_seconds,forced_injector_backend
    session_type()
    is_wayland_session()
    os_injector_env_disabled()
    os_injector_env_forced()
    dry_run_from_env()
    focus_mode_from_env()
    input_mode_from_env()
    cmd_timeout_seconds()
    post_focus_delay_seconds()
    forced_injector_backend()
  src/gillm/runtime/errors.py:
    e: OsInjectorError
    OsInjectorError:  # Raised when profile config or OS injection operations fail.
  src/gillm/runtime/profiles.py:
    e: default_config_path,iter_config_paths,_read_json,load_profile,save_profile,profile_from_mouse,try_load_profile,capture_mouse_xy,capture_from_xdotool,OsInjectorProfile
    OsInjectorProfile:  # Chat anchor: pixel position under the cursor at calibration 
    default_config_path()
    iter_config_paths()
    _read_json(path)
    load_profile(tool_id)
    save_profile(profile)
    profile_from_mouse(tool_id)
    try_load_profile(tool_id)
    capture_mouse_xy()
    capture_from_xdotool()
  tests/test_drive_backend.py:
    e: test_try_os_injector_drive_returns_none_when_no_profile,test_try_os_injector_drive_raises_on_error,test_format_os_injector_ack_includes_target,test_apply_keyboard_injection_delegates_to_injector,test_apply_keyboard_injection_propagates_injector_error
    test_try_os_injector_drive_returns_none_when_no_profile(monkeypatch)
    test_try_os_injector_drive_raises_on_error(monkeypatch)
    test_format_os_injector_ack_includes_target()
    test_apply_keyboard_injection_delegates_to_injector()
    test_apply_keyboard_injection_propagates_injector_error()
  tests/test_gillm.py:
    e: test_focus_strategies_registry,test_injector_dry_run,test_injector_empty_text_error,test_nlp_bridge_heuristic_parsing,test_orchestrator_execution,test_orchestrator_dry_run_focus,test_orchestrator_nlp_drive,test_contract_validation
    test_focus_strategies_registry()
    test_injector_dry_run()
    test_injector_empty_text_error()
    test_nlp_bridge_heuristic_parsing(monkeypatch)
    test_orchestrator_execution()
    test_orchestrator_dry_run_focus()
    test_orchestrator_nlp_drive(monkeypatch)
    test_contract_validation()
  tests/test_gui_driver.py:
    e: test_session_backend_order_wayland_prefers_wtype,test_backend_selector_forced_backend,test_dry_run_driver_executes_chat_plan,test_dry_run_driver_probe,test_action_plan_chat_factory
    test_session_backend_order_wayland_prefers_wtype()
    test_backend_selector_forced_backend()
    test_dry_run_driver_executes_chat_plan()
    test_dry_run_driver_probe()
    test_action_plan_chat_factory()
  tests/test_injector.py:
    e: _fake_runner,_which_factory,test_select_backend_x11_prefers_xdotool,test_select_backend_wayland_prefers_wtype_over_ydotool,test_select_backend_wayland_falls_back_to_ydotool,test_select_backend_unknown_session_without_display_prefers_wayland_tools,test_select_backend_no_tools_returns_none,test_type_text_dry_run_does_not_call_runner,test_type_text_xdotool_types_and_submits,test_type_text_xdotool_supports_extra_enter,test_type_text_ydotool_uses_configurable_enter_key,test_type_text_ydotool_submit_newline_mode,test_type_text_ydotool_submit_ctrl_enter_mode,test_type_text_wtype_uses_modifiers_for_jetbrains,test_type_text_no_submit_only_types,test_type_text_propagates_runner_error,test_type_text_empty_raises,test_type_text_no_backend_raises,test_probe_marks_unavailable_when_missing_tool,test_probe_marks_unavailable_on_wrong_session,test_wtype_rejects_multi_modifier_submit_key,test_type_text_wayland_falls_back_when_wtype_fails,test_injector_forced_backend,test_wtype_single_modifier_still_works
    _fake_runner(commands)
    _which_factory(present)
    test_select_backend_x11_prefers_xdotool()
    test_select_backend_wayland_prefers_wtype_over_ydotool()
    test_select_backend_wayland_falls_back_to_ydotool()
    test_select_backend_unknown_session_without_display_prefers_wayland_tools(monkeypatch)
    test_select_backend_no_tools_returns_none()
    test_type_text_dry_run_does_not_call_runner()
    test_type_text_xdotool_types_and_submits()
    test_type_text_xdotool_supports_extra_enter(monkeypatch)
    test_type_text_ydotool_uses_configurable_enter_key(monkeypatch)
    test_type_text_ydotool_submit_newline_mode(monkeypatch)
    test_type_text_ydotool_submit_ctrl_enter_mode(monkeypatch)
    test_type_text_wtype_uses_modifiers_for_jetbrains()
    test_type_text_no_submit_only_types()
    test_type_text_propagates_runner_error()
    test_type_text_empty_raises()
    test_type_text_no_backend_raises()
    test_probe_marks_unavailable_when_missing_tool()
    test_probe_marks_unavailable_on_wrong_session()
    test_wtype_rejects_multi_modifier_submit_key(monkeypatch)
    test_type_text_wayland_falls_back_when_wtype_fails()
    test_injector_forced_backend(monkeypatch)
    test_wtype_single_modifier_still_works()
  tests/test_os_injector.py:
    e: test_save_and_load_profile,test_load_profile_accepts_legacy_window_id,test_profile_from_mouse_builds_profile,test_capture_from_xdotool_parses_shell_output,test_inject_with_profile_paste_path_uses_clipboard_then_ctrl_v,test_inject_with_profile_type_fallback_when_no_clip_tools,test_load_profile_missing_raises,test_inject_with_profile_paste_timeout_is_reported,test_try_load_profile_prefers_project_over_cwd,test_iter_config_paths_dedupes_project_and_cwd,test_try_drive_with_profile_skips_saved_profile_on_wayland_without_ydotool,test_try_drive_with_profile_uses_saved_profile_on_wayland_with_ydotool,test_try_drive_with_profile_forced_works_on_wayland,test_try_drive_with_profile_skips_when_env_disabled,test_try_drive_with_profile_uses_config,test_inject_post_focus_delay_env_controls_sleep,test_inject_post_focus_delay_zero_skips_sleep
    test_save_and_load_profile(tmp_path)
    test_load_profile_accepts_legacy_window_id(tmp_path)
    test_profile_from_mouse_builds_profile()
    test_capture_from_xdotool_parses_shell_output(monkeypatch)
    test_inject_with_profile_paste_path_uses_clipboard_then_ctrl_v(monkeypatch)
    test_inject_with_profile_type_fallback_when_no_clip_tools(monkeypatch)
    test_load_profile_missing_raises(tmp_path)
    test_inject_with_profile_paste_timeout_is_reported(monkeypatch)
    test_try_load_profile_prefers_project_over_cwd(tmp_path;monkeypatch)
    test_iter_config_paths_dedupes_project_and_cwd(tmp_path)
    test_try_drive_with_profile_skips_saved_profile_on_wayland_without_ydotool(tmp_path;monkeypatch)
    test_try_drive_with_profile_uses_saved_profile_on_wayland_with_ydotool(tmp_path;monkeypatch)
    test_try_drive_with_profile_forced_works_on_wayland(tmp_path;monkeypatch)
    test_try_drive_with_profile_skips_when_env_disabled(monkeypatch)
    test_try_drive_with_profile_uses_config(tmp_path;monkeypatch)
    test_inject_post_focus_delay_env_controls_sleep(monkeypatch)
    test_inject_post_focus_delay_zero_skips_sleep(monkeypatch)
  tests/test_os_strategies.py:
    e: RegistryTests,KeySequenceTests,WaylandLinuxStrategyTests,X11LinuxStrategyTests,DarwinStrategyTests,WindowsStrategyTests
    RegistryTests: test_all_shipped_strategies_registered(0),test_resolve_active_picks_a_real_strategy(0)
    KeySequenceTests: test_rejects_both_key_and_literal(0),test_rejects_neither_key_nor_literal(0),test_accepts_modifiers_plus_key(0)
    WaylandLinuxStrategyTests: test_matches_when_wayland_display_present(0),test_does_not_match_macos(0),test_capabilities_use_shutil_which(0),test_focus_returns_integrated_terminal_on_wayland_with_term_program(0),test_focus_explains_wayland_failure(0),test_inject_keys_builds_correct_wtype_argv(0),test_inject_literal_text_uses_minus_t(0),test_wtype_returncode_zero_but_stderr_unsupported_is_failure(0),test_gnome_compositor_prefers_ydotool_first(0),test_ydotool_chord_emits_press_release_in_order(0),test_ydotool_return_uses_correct_scancode(0),test_env_override_disables_gnome_preference(0)
    X11LinuxStrategyTests: test_does_not_match_when_wayland_display_present(0),test_matches_classic_x11(0),test_focus_uses_xdotool_first(0)
    DarwinStrategyTests: test_matches_only_on_darwin(0),test_focus_uses_osascript(0)
    WindowsStrategyTests: test_matches_only_on_windows(0),test_capabilities_are_empty_placeholder(0)
  tests/test_recovery.py:
    e: test_probe_environment_has_session,test_diagnose_plugin_unavailable,test_diagnose_version_mismatch,test_koru_drive_payload_maps_to_action_plan,test_recovery_hints_for_wayland_reload
    test_probe_environment_has_session()
    test_diagnose_plugin_unavailable()
    test_diagnose_version_mismatch()
    test_koru_drive_payload_maps_to_action_plan()
    test_recovery_hints_for_wayland_reload()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('gillm', '0.1.10', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 366, 'less').
project_file('packages/cli2gillm/src/cli2gillm/__init__.py', 2, 'python').
project_file('packages/cli2gillm/src/cli2gillm/cli.py', 71, 'python').
project_file('packages/cli2gillm/src/cli2gillm/shell.py', 34, 'python').
project_file('packages/cli2gillm/tests/test_cli2gillm.py', 7, 'python').
project_file('packages/dsl2gillm/scripts/generate-proto.sh', 7, 'shell').
project_file('packages/dsl2gillm/src/dsl2gillm/__init__.py', 35, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/bus.py', 89, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/cli.py', 167, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/codec.py', 67, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/codegen.py', 113, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/engine.py', 6, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/events.py', 134, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/grammar.py', 177, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', 245, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/models.py', 97, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', 152, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/result.py', 29, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/schema_registry.py', 50, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/v1/__init__.py', 2, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/v1/command_pb2.py', 59, 'python').
project_file('packages/dsl2gillm/src/dsl2gillm/v1/result_pb2.py', 40, 'python').
project_file('packages/dsl2gillm/tests/test_bus.py', 41, 'python').
project_file('packages/dsl2gillm/tests/test_codegen.py', 19, 'python').
project_file('packages/dsl2gillm/tests/test_dry_run.py', 14, 'python').
project_file('packages/dsl2gillm/tests/test_parity.py', 19, 'python').
project_file('packages/dsl2gillm/tests/test_parity_adapters.py', 51, 'python').
project_file('packages/dsl2gillm/tests/test_protobuf.py', 18, 'python').
project_file('packages/install-dev.sh', 15, 'shell').
project_file('packages/mcp2gillm/src/mcp2gillm/__init__.py', 6, 'python').
project_file('packages/mcp2gillm/src/mcp2gillm/cli.py', 23, 'python').
project_file('packages/mcp2gillm/src/mcp2gillm/server.py', 84, 'python').
project_file('packages/mcp2gillm/tests/test_mcp2gillm.py', 6, 'python').
project_file('packages/nlp2gillm/src/nlp2gillm/__init__.py', 7, 'python').
project_file('packages/nlp2gillm/src/nlp2gillm/cli.py', 56, 'python').
project_file('packages/nlp2gillm/src/nlp2gillm/llm_backend.py', 81, 'python').
project_file('packages/nlp2gillm/src/nlp2gillm/to_dsl.py', 54, 'python').
project_file('packages/nlp2gillm/tests/test_llm_backend.py', 12, 'python').
project_file('packages/nlp2gillm/tests/test_to_dsl.py', 10, 'python').
project_file('packages/rest2gillm/src/rest2gillm/__init__.py', 6, 'python').
project_file('packages/rest2gillm/src/rest2gillm/app.py', 88, 'python').
project_file('packages/rest2gillm/src/rest2gillm/cli.py', 28, 'python').
project_file('packages/rest2gillm/tests/test_rest2gillm.py', 29, 'python').
project_file('packages/uri2gillm/src/uri2gillm/__init__.py', 19, 'python').
project_file('packages/uri2gillm/src/uri2gillm/cli.py', 64, 'python').
project_file('packages/uri2gillm/src/uri2gillm/decode.py', 55, 'python').
project_file('packages/uri2gillm/src/uri2gillm/nlp2uri.py', 55, 'python').
project_file('packages/uri2gillm/src/uri2gillm/run.py', 12, 'python').
project_file('packages/uri2gillm/src/uri2gillm/uri.py', 53, 'python').
project_file('packages/uri2gillm/tests/test_uri.py', 15, 'python').
project_file('project.sh', 50, 'shell').
project_file('src/gillm/__init__.py', 56, 'python').
project_file('src/gillm/adapters/__init__.py', 6, 'python').
project_file('src/gillm/adapters/koru.py', 95, 'python').
project_file('src/gillm/capture/__init__.py', 17, 'python').
project_file('src/gillm/capture/mss_backend.py', 131, 'python').
project_file('src/gillm/capture/portal_backend.py', 114, 'python').
project_file('src/gillm/cli/__init__.py', 6, 'python').
project_file('src/gillm/cli/main.py', 98, 'python').
project_file('src/gillm/config.py', 106, 'python').
project_file('src/gillm/contracts/__init__.py', 24, 'python').
project_file('src/gillm/contracts/driver.py', 137, 'python').
project_file('src/gillm/control.py', 40, 'python').
project_file('src/gillm/drivers/__init__.py', 7, 'python').
project_file('src/gillm/drivers/composite.py', 181, 'python').
project_file('src/gillm/drivers/dry_run.py', 90, 'python').
project_file('src/gillm/focus/__init__.py', 38, 'python').
project_file('src/gillm/focus/darwin.py', 73, 'python').
project_file('src/gillm/focus/registry.py', 51, 'python').
project_file('src/gillm/focus/strategy.py', 109, 'python').
project_file('src/gillm/focus/wayland.py', 237, 'python').
project_file('src/gillm/focus/windows.py', 44, 'python').
project_file('src/gillm/focus/x11.py', 129, 'python').
project_file('src/gillm/injection/__init__.py', 34, 'python').
project_file('src/gillm/injection/backends.py', 208, 'python').
project_file('src/gillm/injection/drive_backend.py', 67, 'python').
project_file('src/gillm/injection/errors.py', 11, 'python').
project_file('src/gillm/injection/injector.py', 277, 'python').
project_file('src/gillm/injection/os_injector.py', 324, 'python').
project_file('src/gillm/intents/__init__.py', 6, 'python').
project_file('src/gillm/intents/contract.py', 79, 'python').
project_file('src/gillm/nlp_bridge/__init__.py', 6, 'python').
project_file('src/gillm/nlp_bridge/client.py', 45, 'python').
project_file('src/gillm/orchestrator/__init__.py', 9, 'python').
project_file('src/gillm/orchestrator/drive.py', 169, 'python').
project_file('src/gillm/recovery/__init__.py', 21, 'python').
project_file('src/gillm/recovery/diagnose.py', 151, 'python').
project_file('src/gillm/recovery/repair_hints.py', 99, 'python').
project_file('src/gillm/runtime/__init__.py', 52, 'python').
project_file('src/gillm/runtime/activity.py', 63, 'python').
project_file('src/gillm/runtime/backend_selector.py', 97, 'python').
project_file('src/gillm/runtime/command_runner.py', 89, 'python').
project_file('src/gillm/runtime/env.py', 88, 'python').
project_file('src/gillm/runtime/errors.py', 6, 'python').
project_file('src/gillm/runtime/profiles.py', 118, 'python').
project_file('tests/test_drive_backend.py', 72, 'python').
project_file('tests/test_gillm.py', 105, 'python').
project_file('tests/test_gui_driver.py', 43, 'python').
project_file('tests/test_injector.py', 286, 'python').
project_file('tests/test_os_injector.py', 352, 'python').
project_file('tests/test_os_strategies.py', 382, 'python').
project_file('tests/test_recovery.py', 49, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('packages/cli2gillm/src/cli2gillm/cli.py', 'main', 1, 16, 15).
python_function('packages/cli2gillm/src/cli2gillm/shell.py', 'run_shell', 0, 9, 8).
python_function('packages/cli2gillm/tests/test_cli2gillm.py', 'test_exec_health_via_bus', 0, 2, 1).
python_function('packages/dsl2gillm/src/dsl2gillm/bus.py', 'dispatch', 1, 15, 17).
python_function('packages/dsl2gillm/src/dsl2gillm/bus.py', 'execute_dsl_line', 1, 1, 1).
python_function('packages/dsl2gillm/src/dsl2gillm/bus.py', 'execute_dsl', 1, 4, 5).
python_function('packages/dsl2gillm/src/dsl2gillm/cli.py', '_run_results', 1, 6, 4).
python_function('packages/dsl2gillm/src/dsl2gillm/cli.py', 'main', 1, 4, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/cli.py', '_main_subcommand', 1, 1, 6).
python_function('packages/dsl2gillm/src/dsl2gillm/cli.py', '_main_legacy', 1, 5, 11).
python_function('packages/dsl2gillm/src/dsl2gillm/cli.py', '_handle_subcommand', 1, 19, 22).
python_function('packages/dsl2gillm/src/dsl2gillm/codec.py', '_validate_with_pydantic', 2, 3, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/codec.py', 'validate_payload', 1, 2, 7).
python_function('packages/dsl2gillm/src/dsl2gillm/codec.py', 'parse_text', 1, 2, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/codec.py', 'envelope_to_bytes', 1, 1, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/codec.py', 'envelope_from_bytes', 1, 1, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/codec.py', 'envelope_to_json', 1, 1, 3).
python_function('packages/dsl2gillm/src/dsl2gillm/codec.py', 'envelope_from_json', 1, 2, 5).
python_function('packages/dsl2gillm/src/dsl2gillm/codec.py', 'roundtrip_text', 1, 1, 4).
python_function('packages/dsl2gillm/src/dsl2gillm/codegen.py', '_schema_type', 1, 10, 3).
python_function('packages/dsl2gillm/src/dsl2gillm/codegen.py', '_model_name', 1, 2, 4).
python_function('packages/dsl2gillm/src/dsl2gillm/codegen.py', '_field_line', 2, 4, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/codegen.py', 'render_models', 1, 4, 8).
python_function('packages/dsl2gillm/src/dsl2gillm/codegen.py', 'load_schemas', 0, 4, 9).
python_function('packages/dsl2gillm/src/dsl2gillm/codegen.py', 'generate_models', 1, 2, 5).
python_function('packages/dsl2gillm/src/dsl2gillm/codegen.py', 'main', 0, 1, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/grammar.py', '_steps_from_line', 2, 8, 9).
python_function('packages/dsl2gillm/src/dsl2gillm/grammar.py', 'parse_line', 1, 46, 12).
python_function('packages/dsl2gillm/src/dsl2gillm/grammar.py', 'to_text', 1, 22, 8).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_load_steps', 1, 6, 6).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', 'run_query', 1, 8, 10).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', 'run_command', 1, 5, 7).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_health', 0, 4, 8).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_orient', 0, 2, 6).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_actions', 0, 1, 3).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_parse', 1, 2, 7).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_validate', 1, 6, 10).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_resolve', 1, 2, 4).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_capture', 1, 1, 5).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_execute', 1, 4, 9).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_simulate', 1, 1, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_focus', 1, 4, 10).
python_function('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', '_inject', 1, 2, 9).
python_function('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', '_set_body', 2, 17, 7).
python_function('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', 'envelope_to_dict', 1, 26, 5).
python_function('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', 'encode_protobuf', 1, 1, 6).
python_function('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', 'decode_protobuf', 1, 1, 3).
python_function('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', 'encode_text_to_protobuf', 1, 3, 3).
python_function('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', 'decode_protobuf_to_text', 1, 1, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', 'result_to_pb', 1, 3, 3).
python_function('packages/dsl2gillm/src/dsl2gillm/pb_codec.py', 'encode_result_protobuf', 1, 1, 2).
python_function('packages/dsl2gillm/src/dsl2gillm/schema_registry.py', '_load_schemas', 0, 4, 9).
python_function('packages/dsl2gillm/src/dsl2gillm/schema_registry.py', 'schema_for_verb', 1, 2, 4).
python_function('packages/dsl2gillm/src/dsl2gillm/schema_registry.py', 'all_verbs', 0, 1, 3).
python_function('packages/dsl2gillm/src/dsl2gillm/schema_registry.py', 'validate_schemas', 0, 5, 5).
python_function('packages/dsl2gillm/tests/test_bus.py', 'test_health', 0, 3, 1).
python_function('packages/dsl2gillm/tests/test_bus.py', 'test_orient', 0, 3, 1).
python_function('packages/dsl2gillm/tests/test_bus.py', 'test_actions', 0, 3, 1).
python_function('packages/dsl2gillm/tests/test_bus.py', 'test_validate_steps', 0, 2, 1).
python_function('packages/dsl2gillm/tests/test_bus.py', 'test_simulate_wait', 0, 3, 1).
python_function('packages/dsl2gillm/tests/test_codegen.py', 'test_load_schemas_has_all_verbs', 0, 4, 2).
python_function('packages/dsl2gillm/tests/test_codegen.py', 'test_generate_models', 1, 3, 2).
python_function('packages/dsl2gillm/tests/test_dry_run.py', 'test_simulate_workflow_fixture', 0, 5, 4).
python_function('packages/dsl2gillm/tests/test_parity.py', 'test_parity_text_vs_dict_health', 0, 3, 1).
python_function('packages/dsl2gillm/tests/test_parity.py', 'test_parity_text_vs_dict_validate', 0, 3, 3).
python_function('packages/dsl2gillm/tests/test_parity_adapters.py', '_baseline', 0, 1, 2).
python_function('packages/dsl2gillm/tests/test_parity_adapters.py', 'test_parity_text_vs_protobuf', 0, 3, 2).
python_function('packages/dsl2gillm/tests/test_parity_adapters.py', 'test_parity_uri_adapter', 0, 4, 5).
python_function('packages/dsl2gillm/tests/test_parity_adapters.py', 'test_parity_rest_adapter', 0, 4, 5).
python_function('packages/dsl2gillm/tests/test_parity_adapters.py', 'test_parity_simulate_offline', 0, 3, 1).
python_function('packages/dsl2gillm/tests/test_protobuf.py', 'test_encode_decode_health', 0, 2, 2).
python_function('packages/dsl2gillm/tests/test_protobuf.py', 'test_roundtrip_health', 0, 2, 1).
python_function('packages/dsl2gillm/tests/test_protobuf.py', 'test_roundtrip_parse', 0, 2, 2).
python_function('packages/mcp2gillm/src/mcp2gillm/cli.py', 'main', 1, 2, 5).
python_function('packages/mcp2gillm/src/mcp2gillm/server.py', '_require_fastmcp', 0, 2, 1).
python_function('packages/mcp2gillm/src/mcp2gillm/server.py', 'create_server', 1, 1, 1).
python_function('packages/mcp2gillm/src/mcp2gillm/server.py', 'run_server', 0, 1, 2).
python_function('packages/mcp2gillm/tests/test_mcp2gillm.py', 'test_create_server', 0, 2, 1).
python_function('packages/nlp2gillm/src/nlp2gillm/cli.py', 'main', 1, 10, 12).
python_function('packages/nlp2gillm/src/nlp2gillm/llm_backend.py', 'get_backend', 1, 2, 1).
python_function('packages/nlp2gillm/src/nlp2gillm/llm_backend.py', 'nl_to_dsl_line', 1, 6, 8).
python_function('packages/nlp2gillm/src/nlp2gillm/to_dsl.py', 'to_dsl', 1, 13, 10).
python_function('packages/nlp2gillm/src/nlp2gillm/to_dsl.py', 'apply_nl', 1, 1, 3).
python_function('packages/nlp2gillm/tests/test_llm_backend.py', 'test_nl_to_dsl_line_fake_backend', 0, 2, 2).
python_function('packages/nlp2gillm/tests/test_to_dsl.py', 'test_to_dsl_health', 0, 2, 1).
python_function('packages/nlp2gillm/tests/test_to_dsl.py', 'test_to_dsl_capture', 0, 2, 1).
python_function('packages/rest2gillm/src/rest2gillm/app.py', 'create_app', 0, 1, 24).
python_function('packages/rest2gillm/src/rest2gillm/cli.py', 'main', 1, 2, 7).
python_function('packages/rest2gillm/tests/test_rest2gillm.py', 'test_root_endpoint', 0, 4, 4).
python_function('packages/rest2gillm/tests/test_rest2gillm.py', 'test_health_endpoint', 0, 3, 4).
python_function('packages/rest2gillm/tests/test_rest2gillm.py', 'test_post_dsl_health', 0, 4, 4).
python_function('packages/uri2gillm/src/uri2gillm/cli.py', 'main', 1, 12, 12).
python_function('packages/uri2gillm/src/uri2gillm/decode.py', 'uri_to_dsl', 1, 26, 8).
python_function('packages/uri2gillm/src/uri2gillm/nlp2uri.py', 'nlp2uri', 1, 12, 8).
python_function('packages/uri2gillm/src/uri2gillm/nlp2uri.py', 'best_uri', 1, 2, 1).
python_function('packages/uri2gillm/src/uri2gillm/run.py', 'run_uri', 1, 1, 2).
python_function('packages/uri2gillm/src/uri2gillm/uri.py', '_encode', 1, 1, 1).
python_function('packages/uri2gillm/src/uri2gillm/uri.py', '_decode', 1, 2, 1).
python_function('packages/uri2gillm/src/uri2gillm/uri.py', 'uri_for_block', 0, 4, 2).
python_function('packages/uri2gillm/src/uri2gillm/uri.py', 'uri_for_cmd', 1, 4, 4).
python_function('packages/uri2gillm/src/uri2gillm/uri.py', 'is_gillm_uri', 1, 1, 2).
python_function('packages/uri2gillm/src/uri2gillm/uri.py', 'parse_gillm_uri', 1, 7, 5).
python_function('packages/uri2gillm/tests/test_uri.py', 'test_decode_health_cmd', 0, 2, 2).
python_function('packages/uri2gillm/tests/test_uri.py', 'test_nlp2uri_capture', 0, 3, 1).
python_function('src/gillm/__init__.py', '__getattr__', 1, 3, 3).
python_function('src/gillm/__init__.py', '__dir__', 0, 1, 2).
python_function('src/gillm/adapters/koru.py', 'drive_payload_to_action_plan', 1, 21, 8).
python_function('src/gillm/adapters/koru.py', 'koru_drive_to_payload', 0, 5, 1).
python_function('src/gillm/adapters/koru.py', '_steps_from_prefer', 1, 8, 6).
python_function('src/gillm/capture/mss_backend.py', 'resolve_scale', 1, 4, 5).
python_function('src/gillm/capture/mss_backend.py', 'downscale_rgb_nearest', 5, 6, 4).
python_function('src/gillm/capture/mss_backend.py', 'rgb_mostly_black', 1, 5, 3).
python_function('src/gillm/capture/mss_backend.py', 'capture_primary_rgb', 0, 2, 6).
python_function('src/gillm/capture/mss_backend.py', 'capture_primary_rgb_wayland_fallback', 0, 3, 4).
python_function('src/gillm/capture/mss_backend.py', '_parse_png_to_rgb', 1, 4, 9).
python_function('src/gillm/capture/portal_backend.py', '_portal_python', 0, 6, 4).
python_function('src/gillm/capture/portal_backend.py', 'capture_portal_png', 0, 8, 7).
python_function('src/gillm/cli/main.py', '_print_result', 1, 6, 4).
python_function('src/gillm/cli/main.py', 'main', 0, 14, 12).
python_function('src/gillm/config.py', 'resolve_xdg_path', 1, 2, 3).
python_function('src/gillm/config.py', 'default_config_path', 0, 1, 1).
python_function('src/gillm/config.py', '_merge_submit_keys', 1, 7, 3).
python_function('src/gillm/config.py', 'load_config', 1, 4, 8).
python_function('src/gillm/config.py', '_cached_config', 0, 1, 2).
python_function('src/gillm/config.py', 'cached_config', 0, 1, 1).
python_function('src/gillm/config.py', 'clear_config_cache', 0, 1, 1).
python_function('src/gillm/control.py', 'dispatch_health', 0, 1, 2).
python_function('src/gillm/control.py', 'dispatch_parse', 1, 1, 2).
python_function('src/gillm/control.py', 'dispatch_execute', 0, 3, 2).
python_function('src/gillm/control.py', 'dispatch_validate', 0, 3, 2).
python_function('src/gillm/focus/darwin.py', '_run', 1, 1, 1).
python_function('src/gillm/focus/registry.py', 'register_os_strategy', 1, 5, 2).
python_function('src/gillm/focus/registry.py', 'get_os_strategy', 1, 3, 0).
python_function('src/gillm/focus/registry.py', 'list_os_strategy_ids', 0, 2, 1).
python_function('src/gillm/focus/registry.py', 'resolve_active_os_strategy', 0, 4, 2).
python_function('src/gillm/focus/wayland.py', '_run', 1, 1, 1).
python_function('src/gillm/focus/wayland.py', '_scan_for_key', 1, 5, 1).
python_function('src/gillm/focus/wayland.py', '_gnome_compositor', 0, 4, 2).
python_function('src/gillm/focus/wayland.py', '_prefer_ydotool', 0, 3, 4).
python_function('src/gillm/focus/x11.py', '_run', 1, 1, 1).
python_function('src/gillm/injection/backends.py', 'ydotool_enter_keycode', 0, 2, 3).
python_function('src/gillm/injection/backends.py', 'ydotool_submit_mode', 0, 3, 3).
python_function('src/gillm/injection/backends.py', 'ydotool_ctrl_keycode', 0, 2, 3).
python_function('src/gillm/injection/backends.py', 'extra_enter_count', 0, 3, 4).
python_function('src/gillm/injection/backends.py', '_log', 2, 2, 1).
python_function('src/gillm/injection/backends.py', 'type_with_xdotool', 5, 3, 4).
python_function('src/gillm/injection/backends.py', 'press_wtype', 2, 4, 5).
python_function('src/gillm/injection/backends.py', 'type_with_wtype', 5, 3, 5).
python_function('src/gillm/injection/backends.py', '_ydotool_submit_command', 3, 3, 0).
python_function('src/gillm/injection/backends.py', 'type_with_ydotool', 8, 5, 5).
python_function('src/gillm/injection/backends.py', 'type_with_backend', 5, 5, 10).
python_function('src/gillm/injection/drive_backend.py', 'try_os_injector_drive', 3, 2, 3).
python_function('src/gillm/injection/drive_backend.py', 'format_os_injector_ack', 1, 4, 4).
python_function('src/gillm/injection/drive_backend.py', 'apply_keyboard_injection', 2, 1, 1).
python_function('src/gillm/injection/injector.py', '_submit_key_for', 1, 1, 2).
python_function('src/gillm/injection/injector.py', '_which', 1, 1, 1).
python_function('src/gillm/injection/injector.py', '_session_type', 0, 1, 1).
python_function('src/gillm/injection/injector.py', '_default_runner', 2, 2, 2).
python_function('src/gillm/injection/os_injector.py', '_resolve_input_method', 0, 7, 4).
python_function('src/gillm/injection/os_injector.py', '_injection_result', 0, 1, 0).
python_function('src/gillm/injection/os_injector.py', '_focus_profile_chat', 3, 6, 6).
python_function('src/gillm/injection/os_injector.py', '_focus_with_ydotool', 2, 4, 3).
python_function('src/gillm/injection/os_injector.py', '_focus_with_xdotool', 2, 4, 3).
python_function('src/gillm/injection/os_injector.py', '_inject_profile_text', 0, 7, 7).
python_function('src/gillm/injection/os_injector.py', 'focus_with_profile', 1, 2, 4).
python_function('src/gillm/injection/os_injector.py', 'inject_with_profile', 0, 5, 10).
python_function('src/gillm/injection/os_injector.py', '_os_injector_skip_reason', 1, 9, 4).
python_function('src/gillm/injection/os_injector.py', 'try_drive_with_profile', 0, 8, 7).
python_function('src/gillm/intents/contract.py', 'gui_contract', 9, 1, 1).
python_function('src/gillm/intents/contract.py', 'validate_contract_runtime', 1, 7, 6).
python_function('src/gillm/nlp_bridge/client.py', '_heuristic_parse_intent', 1, 2, 4).
python_function('src/gillm/recovery/diagnose.py', 'probe_environment', 0, 3, 6).
python_function('src/gillm/recovery/diagnose.py', 'classify_failure', 0, 24, 1).
python_function('src/gillm/recovery/diagnose.py', 'diagnose_drive_reply', 1, 9, 8).
python_function('src/gillm/recovery/repair_hints.py', 'recovery_hints_for_reload', 0, 4, 0).
python_function('src/gillm/recovery/repair_hints.py', 'recovery_hints_for_context', 1, 3, 3).
python_function('src/gillm/recovery/repair_hints.py', '_hints_for_kind', 2, 15, 3).
python_function('src/gillm/recovery/repair_hints.py', '_dedupe', 1, 4, 5).
python_function('src/gillm/runtime/activity.py', 'set_activity_sink', 1, 1, 0).
python_function('src/gillm/runtime/activity.py', 'noop_activity_sink', 3, 1, 0).
python_function('src/gillm/runtime/activity.py', 'emit_activity', 2, 3, 1).
python_function('src/gillm/runtime/activity.py', 'emit_activity_warn', 1, 3, 1).
python_function('src/gillm/runtime/activity.py', 'try_bootstrap_koru_activity_sink', 0, 3, 3).
python_function('src/gillm/runtime/backend_selector.py', 'unique_backend_names', 1, 3, 1).
python_function('src/gillm/runtime/backend_selector.py', 'session_backend_order', 1, 4, 2).
python_function('src/gillm/runtime/command_runner.py', 'run_cmd', 1, 2, 3).
python_function('src/gillm/runtime/command_runner.py', 'run_cmd_checked', 1, 4, 4).
python_function('src/gillm/runtime/command_runner.py', 'xdotool', 1, 1, 1).
python_function('src/gillm/runtime/command_runner.py', 'ydotool', 1, 2, 3).
python_function('src/gillm/runtime/command_runner.py', 'clipboard_backend', 0, 3, 1).
python_function('src/gillm/runtime/command_runner.py', 'set_clipboard', 1, 3, 4).
python_function('src/gillm/runtime/command_runner.py', 'resolve_input_method', 0, 7, 4).
python_function('src/gillm/runtime/env.py', 'session_type', 0, 4, 2).
python_function('src/gillm/runtime/env.py', 'is_wayland_session', 0, 6, 5).
python_function('src/gillm/runtime/env.py', 'os_injector_env_disabled', 0, 1, 3).
python_function('src/gillm/runtime/env.py', 'os_injector_env_forced', 0, 1, 3).
python_function('src/gillm/runtime/env.py', 'dry_run_from_env', 0, 1, 3).
python_function('src/gillm/runtime/env.py', 'focus_mode_from_env', 0, 2, 3).
python_function('src/gillm/runtime/env.py', 'input_mode_from_env', 0, 2, 3).
python_function('src/gillm/runtime/env.py', 'cmd_timeout_seconds', 0, 3, 4).
python_function('src/gillm/runtime/env.py', 'post_focus_delay_seconds', 0, 3, 5).
python_function('src/gillm/runtime/env.py', 'forced_injector_backend', 0, 2, 3).
python_function('src/gillm/runtime/profiles.py', 'default_config_path', 0, 1, 1).
python_function('src/gillm/runtime/profiles.py', 'iter_config_paths', 0, 4, 7).
python_function('src/gillm/runtime/profiles.py', '_read_json', 1, 4, 5).
python_function('src/gillm/runtime/profiles.py', 'load_profile', 1, 5, 8).
python_function('src/gillm/runtime/profiles.py', 'save_profile', 1, 3, 7).
python_function('src/gillm/runtime/profiles.py', 'profile_from_mouse', 1, 1, 1).
python_function('src/gillm/runtime/profiles.py', 'try_load_profile', 1, 4, 3).
python_function('src/gillm/runtime/profiles.py', 'capture_mouse_xy', 0, 7, 6).
python_function('src/gillm/runtime/profiles.py', 'capture_from_xdotool', 0, 1, 1).
python_function('tests/test_drive_backend.py', 'test_try_os_injector_drive_returns_none_when_no_profile', 1, 2, 2).
python_function('tests/test_drive_backend.py', 'test_try_os_injector_drive_raises_on_error', 1, 1, 4).
python_function('tests/test_drive_backend.py', 'test_format_os_injector_ack_includes_target', 0, 6, 1).
python_function('tests/test_drive_backend.py', 'test_apply_keyboard_injection_delegates_to_injector', 0, 2, 3).
python_function('tests/test_drive_backend.py', 'test_apply_keyboard_injection_propagates_injector_error', 0, 1, 4).
python_function('tests/test_gillm.py', 'test_focus_strategies_registry', 0, 8, 3).
python_function('tests/test_gillm.py', 'test_injector_dry_run', 0, 5, 2).
python_function('tests/test_gillm.py', 'test_injector_empty_text_error', 0, 1, 3).
python_function('tests/test_gillm.py', 'test_nlp_bridge_heuristic_parsing', 1, 6, 4).
python_function('tests/test_gillm.py', 'test_orchestrator_execution', 0, 4, 3).
python_function('tests/test_gillm.py', 'test_orchestrator_dry_run_focus', 0, 4, 3).
python_function('tests/test_gillm.py', 'test_orchestrator_nlp_drive', 1, 6, 4).
python_function('tests/test_gillm.py', 'test_contract_validation', 0, 3, 2).
python_function('tests/test_gui_driver.py', 'test_session_backend_order_wayland_prefers_wtype', 0, 3, 1).
python_function('tests/test_gui_driver.py', 'test_backend_selector_forced_backend', 0, 3, 2).
python_function('tests/test_gui_driver.py', 'test_dry_run_driver_executes_chat_plan', 0, 5, 4).
python_function('tests/test_gui_driver.py', 'test_dry_run_driver_probe', 0, 3, 3).
python_function('tests/test_gui_driver.py', 'test_action_plan_chat_factory', 0, 4, 1).
python_function('tests/test_injector.py', '_fake_runner', 1, 2, 2).
python_function('tests/test_injector.py', '_which_factory', 1, 1, 0).
python_function('tests/test_injector.py', 'test_select_backend_x11_prefers_xdotool', 0, 2, 3).
python_function('tests/test_injector.py', 'test_select_backend_wayland_prefers_wtype_over_ydotool', 0, 2, 3).
python_function('tests/test_injector.py', 'test_select_backend_wayland_falls_back_to_ydotool', 0, 2, 3).
python_function('tests/test_injector.py', 'test_select_backend_unknown_session_without_display_prefers_wayland_tools', 1, 2, 4).
python_function('tests/test_injector.py', 'test_select_backend_no_tools_returns_none', 0, 2, 4).
python_function('tests/test_injector.py', 'test_type_text_dry_run_does_not_call_runner', 0, 4, 4).
python_function('tests/test_injector.py', 'test_type_text_xdotool_types_and_submits', 0, 7, 4).
python_function('tests/test_injector.py', 'test_type_text_xdotool_supports_extra_enter', 1, 4, 7).
python_function('tests/test_injector.py', 'test_type_text_ydotool_uses_configurable_enter_key', 1, 6, 6).
python_function('tests/test_injector.py', 'test_type_text_ydotool_submit_newline_mode', 1, 3, 7).
python_function('tests/test_injector.py', 'test_type_text_ydotool_submit_ctrl_enter_mode', 1, 5, 6).
python_function('tests/test_injector.py', 'test_type_text_wtype_uses_modifiers_for_jetbrains', 0, 6, 4).
python_function('tests/test_injector.py', 'test_type_text_no_submit_only_types', 0, 2, 5).
python_function('tests/test_injector.py', 'test_type_text_propagates_runner_error', 0, 1, 5).
python_function('tests/test_injector.py', 'test_type_text_empty_raises', 0, 1, 4).
python_function('tests/test_injector.py', 'test_type_text_no_backend_raises', 0, 1, 5).
python_function('tests/test_injector.py', 'test_probe_marks_unavailable_when_missing_tool', 0, 5, 3).
python_function('tests/test_injector.py', 'test_probe_marks_unavailable_on_wrong_session', 0, 4, 3).
python_function('tests/test_injector.py', 'test_wtype_rejects_multi_modifier_submit_key', 1, 3, 8).
python_function('tests/test_injector.py', 'test_type_text_wayland_falls_back_when_wtype_fails', 0, 4, 6).
python_function('tests/test_injector.py', 'test_injector_forced_backend', 1, 2, 5).
python_function('tests/test_injector.py', 'test_wtype_single_modifier_still_works', 0, 2, 4).
python_function('tests/test_os_injector.py', 'test_save_and_load_profile', 1, 4, 5).
python_function('tests/test_os_injector.py', 'test_load_profile_accepts_legacy_window_id', 1, 3, 3).
python_function('tests/test_os_injector.py', 'test_profile_from_mouse_builds_profile', 0, 2, 2).
python_function('tests/test_os_injector.py', 'test_capture_from_xdotool_parses_shell_output', 1, 2, 3).
python_function('tests/test_os_injector.py', 'test_inject_with_profile_paste_path_uses_clipboard_then_ctrl_v', 1, 9, 9).
python_function('tests/test_os_injector.py', 'test_inject_with_profile_type_fallback_when_no_clip_tools', 1, 6, 7).
python_function('tests/test_os_injector.py', 'test_load_profile_missing_raises', 1, 1, 2).
python_function('tests/test_os_injector.py', 'test_inject_with_profile_paste_timeout_is_reported', 1, 1, 7).
python_function('tests/test_os_injector.py', 'test_try_load_profile_prefers_project_over_cwd', 2, 3, 5).
python_function('tests/test_os_injector.py', 'test_iter_config_paths_dedupes_project_and_cwd', 1, 2, 4).
python_function('tests/test_os_injector.py', 'test_try_drive_with_profile_skips_saved_profile_on_wayland_without_ydotool', 2, 3, 8).
python_function('tests/test_os_injector.py', 'test_try_drive_with_profile_uses_saved_profile_on_wayland_with_ydotool', 2, 5, 8).
python_function('tests/test_os_injector.py', 'test_try_drive_with_profile_forced_works_on_wayland', 2, 3, 7).
python_function('tests/test_os_injector.py', 'test_try_drive_with_profile_skips_when_env_disabled', 1, 2, 3).
python_function('tests/test_os_injector.py', 'test_try_drive_with_profile_uses_config', 2, 4, 7).
python_function('tests/test_os_injector.py', 'test_inject_post_focus_delay_env_controls_sleep', 1, 2, 8).
python_function('tests/test_os_injector.py', 'test_inject_post_focus_delay_zero_skips_sleep', 1, 2, 9).
python_function('tests/test_recovery.py', 'test_probe_environment_has_session', 0, 3, 2).
python_function('tests/test_recovery.py', 'test_diagnose_plugin_unavailable', 0, 3, 2).
python_function('tests/test_recovery.py', 'test_diagnose_version_mismatch', 0, 3, 2).
python_function('tests/test_recovery.py', 'test_koru_drive_payload_maps_to_action_plan', 0, 4, 4).
python_function('tests/test_recovery.py', 'test_recovery_hints_for_wayland_reload', 0, 2, 2).

% ── Python Classes ───────────────────────────────────────
python_class('packages/dsl2gillm/src/dsl2gillm/events.py', 'StoredEvent').
python_method('StoredEvent', 'to_dict', 0, 1, 1).
python_class('packages/dsl2gillm/src/dsl2gillm/events.py', 'EventStore').
python_method('EventStore', '__init__', 1, 3, 0).
python_method('EventStore', 'for_workdir', 2, 2, 4).
python_method('EventStore', 'append_command', 2, 3, 22).
python_method('EventStore', 'read_all', 0, 8, 17).
python_method('EventStore', 'replay', 0, 1, 1).
python_class('packages/dsl2gillm/src/dsl2gillm/handlers/__init__.py', 'HandlerResult').
python_method('HandlerResult', 'to_dict', 0, 1, 0).
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'ActionsCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'CaptureCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'ExecuteCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'FocusCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'HealthCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'InjectCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'OrientCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'ParseCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'ResolveCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'SimulateCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/models.py', 'ValidateCommand').
python_class('packages/dsl2gillm/src/dsl2gillm/result.py', 'DslResult').
python_method('DslResult', 'to_dict', 0, 1, 0).
python_class('packages/mcp2gillm/src/mcp2gillm/server.py', 'GillmMCPServer').
python_method('GillmMCPServer', '__post_init__', 0, 1, 3).
python_method('GillmMCPServer', '_register_tools', 0, 1, 6).
python_method('GillmMCPServer', 'run', 0, 1, 1).
python_class('packages/nlp2gillm/src/nlp2gillm/llm_backend.py', 'LLMBackend').
python_method('LLMBackend', 'complete', 0, 3, 0).
python_class('packages/nlp2gillm/src/nlp2gillm/llm_backend.py', 'LitellmBackend').
python_method('LitellmBackend', 'complete', 0, 3, 2).
python_class('packages/nlp2gillm/tests/test_llm_backend.py', '_FakeBackend').
python_method('_FakeBackend', 'complete', 0, 1, 0).
python_class('packages/uri2gillm/src/uri2gillm/nlp2uri.py', 'UriHit').
python_method('UriHit', 'to_dict', 0, 1, 0).
python_class('src/gillm/capture/mss_backend.py', 'CapturedImage').
python_class('src/gillm/capture/portal_backend.py', 'PortalCaptureError').
python_class('src/gillm/config.py', 'AutopilotConfig').
python_method('AutopilotConfig', 'submit_key_for', 1, 2, 1).
python_class('src/gillm/contracts/driver.py', 'WindowTarget').
python_class('src/gillm/contracts/driver.py', 'CapturedImage').
python_class('src/gillm/contracts/driver.py', 'DriverStatus').
python_method('DriverStatus', 'to_dict', 0, 2, 1).
python_class('src/gillm/contracts/driver.py', 'ActionResult').
python_method('ActionResult', 'to_dict', 0, 2, 1).
python_class('src/gillm/contracts/driver.py', 'ActionPlan').
python_method('ActionPlan', 'chat_inject_and_submit', 1, 2, 3).
python_class('src/gillm/contracts/driver.py', 'ExecutionOutcome').
python_method('ExecutionOutcome', 'to_dict', 0, 2, 2).
python_class('src/gillm/contracts/driver.py', 'GuiDriver').
python_method('GuiDriver', 'probe', 0, 1, 0).
python_method('GuiDriver', 'focus', 1, 1, 0).
python_method('GuiDriver', 'type_text', 1, 1, 0).
python_method('GuiDriver', 'hotkey', 0, 1, 0).
python_method('GuiDriver', 'click', 2, 1, 0).
python_method('GuiDriver', 'screenshot', 0, 1, 0).
python_method('GuiDriver', 'execute', 1, 1, 0).
python_class('src/gillm/drivers/composite.py', 'CompositeGuiDriver').
python_method('CompositeGuiDriver', '__init__', 0, 2, 3).
python_method('CompositeGuiDriver', 'probe', 0, 3, 3).
python_method('CompositeGuiDriver', 'focus', 1, 3, 4).
python_method('CompositeGuiDriver', 'type_text', 1, 6, 7).
python_method('CompositeGuiDriver', 'hotkey', 0, 5, 4).
python_method('CompositeGuiDriver', 'click', 2, 1, 1).
python_method('CompositeGuiDriver', 'screenshot', 0, 1, 1).
python_method('CompositeGuiDriver', 'execute', 1, 18, 14).
python_class('src/gillm/drivers/dry_run.py', 'DryRunGuiDriver').
python_method('DryRunGuiDriver', '__init__', 0, 1, 0).
python_method('DryRunGuiDriver', 'log', 0, 1, 1).
python_method('DryRunGuiDriver', 'probe', 0, 1, 1).
python_method('DryRunGuiDriver', 'focus', 1, 1, 2).
python_method('DryRunGuiDriver', 'type_text', 1, 1, 3).
python_method('DryRunGuiDriver', 'hotkey', 0, 1, 3).
python_method('DryRunGuiDriver', 'click', 2, 1, 2).
python_method('DryRunGuiDriver', 'screenshot', 0, 1, 2).
python_method('DryRunGuiDriver', 'execute', 1, 10, 8).
python_class('src/gillm/focus/darwin.py', 'DarwinStrategy').
python_method('DarwinStrategy', 'matches_current_environment', 0, 1, 0).
python_method('DarwinStrategy', 'capabilities', 0, 4, 3).
python_method('DarwinStrategy', 'focus_window', 1, 4, 3).
python_method('DarwinStrategy', 'inject_keys', 1, 1, 0).
python_class('src/gillm/focus/strategy.py', 'OsCapabilities').
python_class('src/gillm/focus/strategy.py', 'FocusOutcome').
python_class('src/gillm/focus/strategy.py', 'KeySequence').
python_method('KeySequence', '__post_init__', 0, 5, 1).
python_class('src/gillm/focus/strategy.py', 'OsStrategy').
python_method('OsStrategy', 'id', 0, 1, 0).
python_method('OsStrategy', 'label', 0, 1, 0).
python_method('OsStrategy', 'matches_current_environment', 0, 1, 0).
python_method('OsStrategy', 'capabilities', 0, 1, 0).
python_method('OsStrategy', 'focus_window', 1, 1, 0).
python_method('OsStrategy', 'inject_keys', 1, 1, 0).
python_method('OsStrategy', '_term_program_is_vscode_family', 0, 1, 3).
python_method('OsStrategy', '__repr__', 0, 1, 1).
python_class('src/gillm/focus/strategy.py', 'StaticOsIdentityMixin').
python_method('StaticOsIdentityMixin', 'id', 0, 1, 0).
python_method('StaticOsIdentityMixin', 'label', 0, 1, 0).
python_class('src/gillm/focus/wayland.py', 'WaylandLinuxStrategy').
python_method('WaylandLinuxStrategy', 'matches_current_environment', 0, 3, 3).
python_method('WaylandLinuxStrategy', 'capabilities', 0, 5, 6).
python_method('WaylandLinuxStrategy', 'focus_window', 1, 3, 3).
python_method('WaylandLinuxStrategy', 'inject_keys', 1, 9, 5).
python_method('WaylandLinuxStrategy', '_focus_via_wmctrl', 1, 4, 3).
python_method('WaylandLinuxStrategy', '_inject_via_wtype', 1, 9, 4).
python_method('WaylandLinuxStrategy', '_inject_via_ydotool', 1, 7, 4).
python_class('src/gillm/focus/windows.py', 'WindowsStrategy').
python_method('WindowsStrategy', 'matches_current_environment', 0, 1, 1).
python_method('WindowsStrategy', 'capabilities', 0, 1, 1).
python_method('WindowsStrategy', 'focus_window', 1, 1, 1).
python_method('WindowsStrategy', 'inject_keys', 1, 1, 0).
python_class('src/gillm/focus/x11.py', 'X11LinuxStrategy').
python_method('X11LinuxStrategy', 'matches_current_environment', 0, 4, 4).
python_method('X11LinuxStrategy', 'capabilities', 0, 6, 5).
python_method('X11LinuxStrategy', 'focus_window', 1, 3, 3).
python_method('X11LinuxStrategy', 'inject_keys', 1, 3, 4).
python_method('X11LinuxStrategy', '_focus_via_xdotool', 1, 11, 5).
python_method('X11LinuxStrategy', '_focus_via_wmctrl', 1, 4, 3).
python_method('X11LinuxStrategy', '_inject_via_xdotool', 1, 3, 3).
python_class('src/gillm/injection/errors.py', 'InjectorError').
python_class('src/gillm/injection/injector.py', 'BackendStatus').
python_method('BackendStatus', 'to_dict', 0, 1, 0).
python_class('src/gillm/injection/injector.py', 'InjectionResult').
python_method('InjectionResult', 'to_dict', 0, 1, 0).
python_class('src/gillm/injection/injector.py', 'Injector').
python_method('Injector', 'probe', 0, 2, 3).
python_method('Injector', '_candidate_backends', 0, 1, 2).
python_method('Injector', 'select_backend', 0, 1, 2).
python_method('Injector', '_type_with_backend', 3, 1, 1).
python_method('Injector', '_type_text_backends', 0, 3, 3).
python_method('Injector', '_log_type_text_request', 3, 3, 3).
python_method('Injector', '_dry_run_type_text_result', 0, 3, 3).
python_method('Injector', '_try_type_text_backends', 4, 6, 6).
python_method('Injector', '_all_type_backends_failed', 1, 2, 3).
python_method('Injector', 'type_text', 1, 6, 8).
python_method('Injector', 'submit_only', 0, 9, 8).
python_method('Injector', '_call', 1, 10, 7).
python_class('src/gillm/nlp_bridge/client.py', 'NLPBridgeClient').
python_method('NLPBridgeClient', '__init__', 0, 2, 1).
python_method('NLPBridgeClient', 'parse_intent', 1, 2, 2).
python_class('src/gillm/orchestrator/drive.py', 'DriveOrchestrator').
python_method('DriveOrchestrator', '__init__', 2, 3, 2).
python_method('DriveOrchestrator', 'log', 1, 2, 1).
python_method('DriveOrchestrator', 'focus_target_window', 1, 2, 6).
python_method('DriveOrchestrator', 'inject_text', 4, 1, 4).
python_method('DriveOrchestrator', 'capture_screenshot', 1, 3, 6).
python_method('DriveOrchestrator', 'execute_step', 2, 12, 11).
python_method('DriveOrchestrator', 'execute_workflow', 2, 3, 4).
python_method('DriveOrchestrator', 'drive_natural_language', 2, 2, 3).
python_class('src/gillm/recovery/diagnose.py', 'EnvironmentDiagnostics').
python_method('EnvironmentDiagnostics', 'to_dict', 0, 2, 1).
python_class('src/gillm/recovery/diagnose.py', 'DriveFailureContext').
python_method('DriveFailureContext', 'to_dict', 0, 2, 2).
python_class('src/gillm/runtime/backend_selector.py', 'BackendSelector').
python_method('BackendSelector', '__init__', 0, 3, 2).
python_method('BackendSelector', 'candidate_backends', 0, 5, 5).
python_method('BackendSelector', 'select_backend', 0, 2, 1).
python_method('BackendSelector', '_forced_backend_candidates', 1, 4, 2).
python_method('BackendSelector', '_available_backend_candidates', 1, 4, 3).
python_method('BackendSelector', 'probe', 0, 6, 2).
python_class('src/gillm/runtime/command_runner.py', 'CommandResult').
python_class('src/gillm/runtime/errors.py', 'OsInjectorError').
python_class('src/gillm/runtime/profiles.py', 'OsInjectorProfile').
python_class('tests/test_os_strategies.py', 'RegistryTests').
python_method('RegistryTests', 'test_all_shipped_strategies_registered', 0, 2, 2).
python_method('RegistryTests', 'test_resolve_active_picks_a_real_strategy', 0, 1, 3).
python_class('tests/test_os_strategies.py', 'KeySequenceTests').
python_method('KeySequenceTests', 'test_rejects_both_key_and_literal', 0, 1, 2).
python_method('KeySequenceTests', 'test_rejects_neither_key_nor_literal', 0, 1, 2).
python_method('KeySequenceTests', 'test_accepts_modifiers_plus_key', 0, 1, 2).
python_class('tests/test_os_strategies.py', 'WaylandLinuxStrategyTests').
python_method('WaylandLinuxStrategyTests', 'test_matches_when_wayland_display_present', 0, 1, 5).
python_method('WaylandLinuxStrategyTests', 'test_does_not_match_macos', 0, 1, 4).
python_method('WaylandLinuxStrategyTests', 'test_capabilities_use_shutil_which', 0, 1, 7).
python_method('WaylandLinuxStrategyTests', 'test_focus_returns_integrated_terminal_on_wayland_with_term_program', 0, 1, 6).
python_method('WaylandLinuxStrategyTests', 'test_focus_explains_wayland_failure', 0, 1, 6).
python_method('WaylandLinuxStrategyTests', 'test_inject_keys_builds_correct_wtype_argv', 0, 2, 10).
python_method('WaylandLinuxStrategyTests', 'test_inject_literal_text_uses_minus_t', 0, 2, 9).
python_method('WaylandLinuxStrategyTests', 'test_wtype_returncode_zero_but_stderr_unsupported_is_failure', 0, 2, 9).
python_method('WaylandLinuxStrategyTests', 'test_gnome_compositor_prefers_ydotool_first', 0, 2, 10).
python_method('WaylandLinuxStrategyTests', 'test_ydotool_chord_emits_press_release_in_order', 0, 2, 10).
python_method('WaylandLinuxStrategyTests', 'test_ydotool_return_uses_correct_scancode', 0, 2, 10).
python_method('WaylandLinuxStrategyTests', 'test_env_override_disables_gnome_preference', 0, 2, 10).
python_class('tests/test_os_strategies.py', 'X11LinuxStrategyTests').
python_method('X11LinuxStrategyTests', 'test_does_not_match_when_wayland_display_present', 0, 1, 5).
python_method('X11LinuxStrategyTests', 'test_matches_classic_x11', 0, 1, 5).
python_method('X11LinuxStrategyTests', 'test_focus_uses_xdotool_first', 0, 1, 8).
python_class('tests/test_os_strategies.py', 'DarwinStrategyTests').
python_method('DarwinStrategyTests', 'test_matches_only_on_darwin', 0, 1, 5).
python_method('DarwinStrategyTests', 'test_focus_uses_osascript', 0, 2, 6).
python_class('tests/test_os_strategies.py', 'WindowsStrategyTests').
python_method('WindowsStrategyTests', 'test_matches_only_on_windows', 0, 1, 5).
python_method('WindowsStrategyTests', 'test_capabilities_are_empty_placeholder', 0, 1, 4).

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('VENV', '').
makefile_target('PYTHON', '').
makefile_target('PIP', '').
makefile_target('help', 'Default target').
makefile_target('venv', '').
makefile_target('VENV_TARGETS', '').
makefile_target('install', '').
makefile_target('dev-install', '').
makefile_target('test', '').
makefile_target('test-fast', 'Fast tests - exclude slow and integration tests').
makefile_target('test-slow', 'Slow tests only').
makefile_target('test-integration', 'Integration tests only').
makefile_target('test-unit', 'Unit tests only').
makefile_target('test-cov', '').
makefile_target('test-toon', '').
makefile_target('validate-toon', '').
makefile_target('test-all-formats', '').
makefile_target('test-comprehensive', '').
makefile_target('lint', '').
makefile_target('format', '').
makefile_target('typecheck', '').
makefile_target('check', '').
makefile_target('run', '').
makefile_target('analyze', '').
makefile_target('analyze-all', '').
makefile_target('toon-demo', '').
makefile_target('toon-compare', '').
makefile_target('toon-validate', '').
makefile_target('build', '').
makefile_target('publish-test', '').
makefile_target('bump-patch', '').
makefile_target('bump-minor', '').
makefile_target('bump-major', '').
makefile_target('publish', '').
makefile_target('mermaid-png', '').
makefile_target('install-mermaid', '').
makefile_target('check-mermaid', '').
makefile_target('clean', '').
makefile_target('clean-png', '').
makefile_target('quickstart', '').

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────
env_variable('OPENROUTER_API_KEY', '*(not set)*', 'Required: OpenRouter API key (https://openrouter.ai/keys)').
env_variable('LLM_MODEL', 'openrouter/qwen/qwen3-coder-next', 'Model (default: openrouter/qwen/qwen3-coder-next)').
env_variable('PFIX_AUTO_APPLY', 'true', 'true = apply fixes without asking').
env_variable('PFIX_AUTO_INSTALL_DEPS', 'true', 'true = auto pip/uv install').
env_variable('PFIX_AUTO_RESTART', 'false', 'true = os.execv restart after fix').
env_variable('PFIX_MAX_RETRIES', '3', '').
env_variable('PFIX_DRY_RUN', 'false', '').
env_variable('PFIX_ENABLED', 'true', '').
env_variable('PFIX_GIT_COMMIT', 'false', 'true = auto-commit fixes').
env_variable('PFIX_GIT_PREFIX', 'pfix:', 'commit message prefix').
env_variable('PFIX_CREATE_BACKUPS', 'false', 'false = disable .pfix_backups/ directory').

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('api', '').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_workflow('venv', 'manual').
sumd_workflow_step('venv', 1, 'if [ ! -x "$(PYTHON)" ]').
sumd_workflow_step('venv', 2, 'echo "Creating virtual environment in $(VENV)..."').
sumd_workflow_step('venv', 3, 'python3 -m venv "$(VENV)"').
sumd_workflow_step('venv', 4, 'fi').
sumd_workflow('install', 'manual').
sumd_workflow_step('install', 1, '$(PIP) install -e .').
sumd_workflow_step('install', 2, 'echo "✓ code2llm installed with TOON format support"').
sumd_workflow('dev-install', 'manual').
sumd_workflow_step('dev-install', 1, '$(PIP) install -e ".[dev]"').
sumd_workflow_step('dev-install', 2, 'echo "✓ code2llm installed with dev dependencies"').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, '$(PYTHON) -m pytest tests/ -v --tb=short').
sumd_workflow('test-fast', 'manual').
sumd_workflow_step('test-fast', 1, '$(PYTHON) -m pytest -m "not slow and not integration" -v --tb=short -n auto').
sumd_workflow('test-slow', 'manual').
sumd_workflow_step('test-slow', 1, '$(PYTHON) -m pytest -m "slow" -v --tb=short').
sumd_workflow('test-integration', 'manual').
sumd_workflow_step('test-integration', 1, '$(PYTHON) -m pytest -m "integration" -v --tb=short').
sumd_workflow('test-unit', 'manual').
sumd_workflow_step('test-unit', 1, '$(PYTHON) -m pytest -m "unit" -v --tb=short').
sumd_workflow('test-cov', 'manual').
sumd_workflow_step('test-cov', 1, '$(PYTHON) -m pytest tests/ --cov=code2llm --cov-report=html --cov-report=term 2>/dev/null || echo "No tests yet"').
sumd_workflow('test-toon', 'manual').
sumd_workflow_step('test-toon', 1, 'echo "🎯 Testing TOON format..."').
sumd_workflow_step('test-toon', 2, '$(PYTHON) -m code2llm ./ -v -o ./test_toon -m hybrid -f toon').
sumd_workflow_step('test-toon', 3, '$(PYTHON) validate_toon.py test_toon/analysis.toon').
sumd_workflow_step('test-toon', 4, 'echo "✓ TOON format test complete"').
sumd_workflow('validate-toon', 'manual').
sumd_workflow('test-all-formats', 'manual').
sumd_workflow_step('test-all-formats', 1, 'echo "📊 Testing all output formats..."').
sumd_workflow_step('test-all-formats', 2, '$(PYTHON) -m code2llm ./ -v -o ./test_all -m hybrid -f all').
sumd_workflow_step('test-all-formats', 3, '$(PYTHON) validate_toon.py test_all/analysis.toon').
sumd_workflow_step('test-all-formats', 4, 'echo "✓ All formats test complete"').
sumd_workflow('test-comprehensive', 'manual').
sumd_workflow_step('test-comprehensive', 1, 'echo "🚀 Running comprehensive test suite..."').
sumd_workflow_step('test-comprehensive', 2, 'bash project.sh').
sumd_workflow_step('test-comprehensive', 3, 'echo "✓ Comprehensive tests complete"').
sumd_workflow('lint', 'manual').
sumd_workflow_step('lint', 1, '$(PYTHON) -m flake8 code2llm/ --max-line-length=100 --ignore=E203,W503 2>/dev/null || echo "flake8 not installed"').
sumd_workflow_step('lint', 2, '$(PYTHON) -m black --check code2llm/ 2>/dev/null || echo "black not installed"').
sumd_workflow_step('lint', 3, 'echo "✓ Linting complete"').
sumd_workflow('format', 'manual').
sumd_workflow_step('format', 1, '$(PYTHON) -m black code2llm/ --line-length=100 2>/dev/null || echo "black not installed, run: pip install black"').
sumd_workflow_step('format', 2, 'echo "✓ Code formatted"').
sumd_workflow('typecheck', 'manual').
sumd_workflow_step('typecheck', 1, '$(PYTHON) -m mypy code2llm/ --ignore-missing-imports 2>/dev/null || echo "mypy not installed"').
sumd_workflow('check', 'manual').
sumd_workflow_step('check', 1, 'echo "✓ All checks passed"').
sumd_workflow('run', 'manual').
sumd_workflow_step('run', 1, '$(PYTHON) -m code2llm ../python/stts_core -v -o ./output').
sumd_workflow('analyze', 'manual').
sumd_workflow_step('analyze', 1, 'echo "🎯 Running TOON format analysis on current project..."').
sumd_workflow_step('analyze', 2, '$(PYTHON) -m code2llm ./ -v -o ./analysis -m hybrid -f toon').
sumd_workflow_step('analyze', 3, '$(PYTHON) validate_toon.py analysis/analysis.toon').
sumd_workflow_step('analyze', 4, 'echo "✓ TOON analysis complete - check analysis/analysis.toon"').
sumd_workflow('analyze-all', 'manual').
sumd_workflow_step('analyze-all', 1, 'echo "📊 Running analysis with all formats..."').
sumd_workflow_step('analyze-all', 2, '$(PYTHON) -m code2llm ./ -v -o ./analysis_all -m hybrid -f all').
sumd_workflow_step('analyze-all', 3, '$(PYTHON) validate_toon.py analysis_all/analysis.toon').
sumd_workflow_step('analyze-all', 4, 'echo "✓ All formats analysis complete - check analysis_all/"').
sumd_workflow('toon-demo', 'manual').
sumd_workflow_step('toon-demo', 1, 'echo "🎯 Quick TOON format demo..."').
sumd_workflow_step('toon-demo', 2, '$(PYTHON) -m code2llm ./ -v -o ./demo -m hybrid -f toon').
sumd_workflow_step('toon-demo', 3, 'echo "📁 Generated: demo/analysis.toon"').
sumd_workflow_step('toon-demo', 4, 'echo "📊 Size: $$(du -h demo/analysis.toon | cut -f1)"').
sumd_workflow_step('toon-demo', 5, 'echo "🔍 Preview:"').
sumd_workflow_step('toon-demo', 6, 'head -20 demo/analysis.toon').
sumd_workflow('toon-compare', 'manual').
sumd_workflow_step('toon-compare', 1, 'echo "📊 Comparing TOON vs YAML formats..."').
sumd_workflow_step('toon-compare', 2, '$(PYTHON) -m code2llm ./ -v -o ./compare -m hybrid -f toon,yaml').
sumd_workflow_step('toon-compare', 3, 'echo "📁 Files generated:"').
sumd_workflow_step('toon-compare', 4, 'echo "  - TOON:  compare/analysis.toon  ($$(du -h compare/analysis.toon | cut -f1))"').
sumd_workflow_step('toon-compare', 5, 'echo "  - YAML:  compare/analysis.yaml  ($$(du -h compare/analysis.yaml | cut -f1))"').
sumd_workflow_step('toon-compare', 6, 'echo "  - Ratio: $$(echo "scale=1').
sumd_workflow_step('toon-compare', 7, '$(PYTHON) validate_toon.py compare/analysis.yaml compare/analysis.toon').
sumd_workflow('toon-validate', 'manual').
sumd_workflow_step('toon-validate', 1, 'echo "🔍 Validating TOON format structure..."').
sumd_workflow_step('toon-validate', 2, '$(PYTHON) validate_toon.py analysis/analysis.toon 2>/dev/null || $(PYTHON) validate_toon.py test_toon/analysis.toon 2>/dev/null || echo "Run \'make test-toon\' first"').
sumd_workflow('build', 'manual').
sumd_workflow_step('build', 1, 'rm -rf build/ dist/ *.egg-info').
sumd_workflow_step('build', 2, '$(PYTHON) -m build').
sumd_workflow_step('build', 3, 'echo "✓ Build complete - check dist/"').
sumd_workflow('publish-test', 'manual').
sumd_workflow_step('publish-test', 1, 'echo "🚀 Publishing to TestPyPI..."').
sumd_workflow('bump-patch', 'manual').
sumd_workflow_step('bump-patch', 1, 'echo "🔢 Bumping patch version..."').
sumd_workflow_step('bump-patch', 2, '$(PYTHON) scripts/bump_version.py patch 2>/dev/null || echo "Create scripts/bump_version.py or edit pyproject.toml manually"').
sumd_workflow('bump-minor', 'manual').
sumd_workflow_step('bump-minor', 1, 'echo "🔢 Bumping minor version..."').
sumd_workflow_step('bump-minor', 2, '$(PYTHON) scripts/bump_version.py minor 2>/dev/null || echo "Create scripts/bump_version.py or edit pyproject.toml manually"').
sumd_workflow('bump-major', 'manual').
sumd_workflow_step('bump-major', 1, 'echo "🔢 Bumping major version..."').
sumd_workflow_step('bump-major', 2, '$(PYTHON) scripts/bump_version.py major 2>/dev/null || echo "Create scripts/bump_version.py or edit pyproject.toml manually"').
sumd_workflow('publish', 'manual').
sumd_workflow_step('publish', 1, 'echo "🚀 Publishing to PyPI..."').
sumd_workflow('mermaid-png', 'manual').
sumd_workflow_step('mermaid-png', 1, '$(PYTHON) mermaid_to_png.py --batch output output').
sumd_workflow('install-mermaid', 'manual').
sumd_workflow_step('install-mermaid', 1, 'npm install -g @mermaid-js/mermaid-cli').
sumd_workflow('check-mermaid', 'manual').
sumd_workflow_step('check-mermaid', 1, 'echo "Checking available Mermaid renderers..."').
sumd_workflow_step('check-mermaid', 2, 'which mmdc > /dev/null && echo "✓ mmdc (mermaid-cli)" || echo "✗ mmdc (run: npm install -g @mermaid-js/mermaid-cli)"').
sumd_workflow_step('check-mermaid', 3, 'which npx > /dev/null && echo "✓ npx (for @mermaid-js/mermaid-cli)" || echo "✗ npx (install Node.js)"').
sumd_workflow_step('check-mermaid', 4, 'which puppeteer > /dev/null && echo "✓ puppeteer" || echo "✗ puppeteer (run: npm install -g puppeteer)"').
sumd_workflow('clean', 'manual').
sumd_workflow_step('clean', 1, 'rm -rf build/ dist/ *.egg-info').
sumd_workflow_step('clean', 2, 'rm -rf .pytest_cache .coverage htmlcov/').
sumd_workflow_step('clean', 3, 'rm -rf code2llm/__pycache__ code2llm/*/__pycache__').
sumd_workflow_step('clean', 4, 'rm -rf test_* demo compare analysis analysis_all output_* 2>/dev/null || true').
sumd_workflow_step('clean', 5, 'find . -name "*.pyc" -delete 2>/dev/null || true').
sumd_workflow('clean-png', 'manual').
sumd_workflow_step('clean-png', 1, 'rm -f output/*.png').
sumd_workflow_step('clean-png', 2, 'echo "✓ Cleaned PNG files"').
sumd_workflow('quickstart', 'manual').
sumd_workflow_step('quickstart', 1, 'echo "🚀 Quick Start with code2llm TOON format:"').
sumd_workflow_step('quickstart', 2, 'echo ""').
sumd_workflow_step('quickstart', 3, 'echo "1. Install:        make install"').
sumd_workflow_step('quickstart', 4, 'echo "2. Test TOON:      make test-toon"').
sumd_workflow_step('quickstart', 5, 'echo "3. Analyze:        make analyze"').
sumd_workflow_step('quickstart', 6, 'echo "4. Compare:        make toon-compare"').
sumd_workflow_step('quickstart', 7, 'echo "5. All formats:    make test-all-formats"').
sumd_workflow_step('quickstart', 8, 'echo ""').
sumd_workflow_step('quickstart', 9, 'echo "📖 For more: make help"').
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

## Intent

GUI Control Plugin with NLP & Intent Contracts

**Navigation:** [README.md](README.md) · [packages/README.md](packages/README.md) · [project/context.md](project/context.md) · [CHANGELOG.md](CHANGELOG.md)
