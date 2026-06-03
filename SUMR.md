# gillm

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

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
- **version**: `0.1.6`
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
  version: 0.1.6;
}

dependencies {
  runtime: "pyyaml>=6.0, rich>=13.0, requests>=2.31.0, mss>=9.0";
  dev: "pytest>=7.0, ruff>=0.4, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60";
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="gillm"] {

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

deploy {
  target: makefile;
}

environment[name="local"] {
  runtime: docker-compose;
  env_file: .env;
  python_version: >=3.10;
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
```

## Call Graph

*82 nodes · 94 edges · 12 modules · CC̄=3.5*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `_log` *(in src.gillm.injection.backends)* | 2 | 26 | 1 | **27** |
| `inject_with_profile` *(in src.gillm.injection.os_injector)* | 6 | 1 | 12 | **13** |
| `load_profile` *(in src.gillm.injection.os_injector)* | 5 | 1 | 12 | **13** |
| `submit_only` *(in src.gillm.injection.injector.Injector)* | 9 | 0 | 13 | **13** |
| `_inject_profile_text` *(in src.gillm.injection.os_injector)* | 7 | 1 | 12 | **13** |
| `type_with_ydotool` *(in src.gillm.injection.backends)* | 5 | 1 | 12 | **13** |
| `iter_config_paths` *(in src.gillm.injection.os_injector)* | 4 | 1 | 11 | **12** |
| `_run` *(in src.gillm.focus.x11)* | 1 | 11 | 1 | **12** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/gillm
# generated in 0.05s
# nodes: 82 | edges: 94 | modules: 12
# CC̄=3.5

HUBS[20]:
  src.gillm.injection.backends._log
    CC=2  in:26  out:1  total:27
  src.gillm.injection.os_injector.inject_with_profile
    CC=6  in:1  out:12  total:13
  src.gillm.injection.os_injector.load_profile
    CC=5  in:1  out:12  total:13
  src.gillm.injection.injector.Injector.submit_only
    CC=9  in:0  out:13  total:13
  src.gillm.injection.os_injector._inject_profile_text
    CC=7  in:1  out:12  total:13
  src.gillm.injection.backends.type_with_ydotool
    CC=5  in:1  out:12  total:13
  src.gillm.injection.os_injector.iter_config_paths
    CC=4  in:1  out:11  total:12
  src.gillm.focus.x11._run
    CC=1  in:11  out:1  total:12
  src.gillm.capture.portal_backend.capture_portal_png
    CC=8  in:1  out:11  total:12
  src.gillm.injection.backends.type_with_backend
    CC=5  in:1  out:10  total:11
  src.gillm.injection.os_injector._is_wayland_session
    CC=6  in:4  out:7  total:11
  src.gillm.config.load_config
    CC=4  in:1  out:10  total:11
  src.gillm.capture.mss_backend._parse_png_to_rgb
    CC=4  in:1  out:10  total:11
  src.gillm.injection.os_injector._run_cmd
    CC=5  in:4  out:7  total:11
  src.gillm.injection.os_injector.capture_mouse_xy
    CC=6  in:1  out:10  total:11
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool
    CC=7  in:0  out:10  total:10
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_xdotool
    CC=11  in:0  out:10  total:10
  src.gillm.intents.contract.validate_contract_runtime
    CC=7  in:3  out:6  total:9
  src.gillm.capture.mss_backend.capture_primary_rgb
    CC=2  in:1  out:8  total:9
  src.gillm.injection.backends.type_with_xdotool
    CC=3  in:1  out:8  total:9

MODULES:
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
    cached_config  CC=6  out:5
    default_config_path  CC=1  out:1
    load_config  CC=4  out:10
    resolve_xdg_path  CC=2  out:3
  src.gillm.focus.darwin  [1 funcs]
    focus_window  CC=4  out:5
  src.gillm.focus.registry  [1 funcs]
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
  src.gillm.injection.injector  [8 funcs]
    _candidate_backends  CC=5  out:6
    _type_with_backend  CC=1  out:1
    submit_only  CC=9  out:13
    type_text  CC=6  out:8
    _forced_injector_backend  CC=2  out:3
    _session_backend_order  CC=4  out:2
    _submit_key_for  CC=1  out:2
    _unique_backend_names  CC=3  out:1
  src.gillm.injection.os_injector  [30 funcs]
    _clipboard_backend  CC=3  out:2
    _cmd_timeout_seconds  CC=3  out:4
    _focus_profile_chat  CC=6  out:7
    _focus_with_xdotool  CC=4  out:7
    _focus_with_ydotool  CC=4  out:7
    _inject_profile_text  CC=7  out:12
    _injection_result  CC=1  out:0
    _is_wayland_session  CC=6  out:7
    _os_injector_skip_reason  CC=9  out:7
    _post_focus_delay_seconds  CC=3  out:5
  src.gillm.intents.contract  [2 funcs]
    gui_contract  CC=1  out:1
    validate_contract_runtime  CC=7  out:6
  src.gillm.orchestrator.drive  [4 funcs]
    capture_screenshot  CC=1  out:4
    focus_target_window  CC=1  out:5
    inject_text  CC=1  out:4
    log  CC=2  out:1

EDGES:
  src.gillm.config.default_config_path → src.gillm.config.resolve_xdg_path
  src.gillm.config.load_config → src.gillm.config._merge_submit_keys
  src.gillm.config.load_config → src.gillm.config.default_config_path
  src.gillm.config._cached_config → src.gillm.config.load_config
  src.gillm.config.cached_config → src.gillm.config._cached_config
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
  src.gillm.injection.injector._session_backend_order → src.gillm.injection.injector._unique_backend_names
  src.gillm.injection.injector.Injector._candidate_backends → src.gillm.injection.injector._forced_injector_backend
  src.gillm.injection.injector.Injector._candidate_backends → src.gillm.injection.injector._session_backend_order
  src.gillm.injection.injector.Injector._type_with_backend → src.gillm.injection.backends.type_with_backend
  src.gillm.injection.injector.Injector.type_text → src.gillm.injection.injector._submit_key_for
  src.gillm.injection.injector.Injector.submit_only → src.gillm.injection.injector._submit_key_for
  src.gillm.injection.os_injector.try_load_profile → src.gillm.injection.os_injector.iter_config_paths
  src.gillm.injection.os_injector.try_load_profile → src.gillm.injection.os_injector.load_profile
  src.gillm.injection.os_injector.load_profile → src.gillm.injection.os_injector._read_json
  src.gillm.injection.os_injector.load_profile → src.gillm.injection.os_injector.default_config_path
  src.gillm.injection.os_injector.save_profile → src.gillm.injection.os_injector._read_json
  src.gillm.injection.os_injector.save_profile → src.gillm.injection.os_injector.default_config_path
  src.gillm.injection.os_injector.capture_from_xdotool → src.gillm.injection.os_injector.capture_mouse_xy
  src.gillm.injection.os_injector._run_cmd → src.gillm.injection.os_injector._cmd_timeout_seconds
  src.gillm.injection.os_injector._xdotool → src.gillm.injection.os_injector._run_cmd
  src.gillm.injection.os_injector._ydotool → src.gillm.injection.os_injector._run_cmd
  src.gillm.injection.os_injector._set_clipboard → src.gillm.injection.os_injector._run_cmd
  src.gillm.injection.os_injector._resolve_input_method → src.gillm.injection.os_injector.input_mode_from_env
  src.gillm.injection.os_injector._resolve_input_method → src.gillm.injection.os_injector._clipboard_backend
  src.gillm.injection.os_injector._resolve_input_method → src.gillm.injection.os_injector._is_wayland_session
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.backends._log
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.os_injector._is_wayland_session
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
# generated in 0.05s
# nodes: 82 | edges: 94 | modules: 12
# CC̄=3.5

HUBS[20]:
  src.gillm.injection.backends._log
    CC=2  in:26  out:1  total:27
  src.gillm.injection.os_injector.inject_with_profile
    CC=6  in:1  out:12  total:13
  src.gillm.injection.os_injector.load_profile
    CC=5  in:1  out:12  total:13
  src.gillm.injection.injector.Injector.submit_only
    CC=9  in:0  out:13  total:13
  src.gillm.injection.os_injector._inject_profile_text
    CC=7  in:1  out:12  total:13
  src.gillm.injection.backends.type_with_ydotool
    CC=5  in:1  out:12  total:13
  src.gillm.injection.os_injector.iter_config_paths
    CC=4  in:1  out:11  total:12
  src.gillm.focus.x11._run
    CC=1  in:11  out:1  total:12
  src.gillm.capture.portal_backend.capture_portal_png
    CC=8  in:1  out:11  total:12
  src.gillm.injection.backends.type_with_backend
    CC=5  in:1  out:10  total:11
  src.gillm.injection.os_injector._is_wayland_session
    CC=6  in:4  out:7  total:11
  src.gillm.config.load_config
    CC=4  in:1  out:10  total:11
  src.gillm.capture.mss_backend._parse_png_to_rgb
    CC=4  in:1  out:10  total:11
  src.gillm.injection.os_injector._run_cmd
    CC=5  in:4  out:7  total:11
  src.gillm.injection.os_injector.capture_mouse_xy
    CC=6  in:1  out:10  total:11
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool
    CC=7  in:0  out:10  total:10
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_xdotool
    CC=11  in:0  out:10  total:10
  src.gillm.intents.contract.validate_contract_runtime
    CC=7  in:3  out:6  total:9
  src.gillm.capture.mss_backend.capture_primary_rgb
    CC=2  in:1  out:8  total:9
  src.gillm.injection.backends.type_with_xdotool
    CC=3  in:1  out:8  total:9

MODULES:
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
    cached_config  CC=6  out:5
    default_config_path  CC=1  out:1
    load_config  CC=4  out:10
    resolve_xdg_path  CC=2  out:3
  src.gillm.focus.darwin  [1 funcs]
    focus_window  CC=4  out:5
  src.gillm.focus.registry  [1 funcs]
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
  src.gillm.injection.injector  [8 funcs]
    _candidate_backends  CC=5  out:6
    _type_with_backend  CC=1  out:1
    submit_only  CC=9  out:13
    type_text  CC=6  out:8
    _forced_injector_backend  CC=2  out:3
    _session_backend_order  CC=4  out:2
    _submit_key_for  CC=1  out:2
    _unique_backend_names  CC=3  out:1
  src.gillm.injection.os_injector  [30 funcs]
    _clipboard_backend  CC=3  out:2
    _cmd_timeout_seconds  CC=3  out:4
    _focus_profile_chat  CC=6  out:7
    _focus_with_xdotool  CC=4  out:7
    _focus_with_ydotool  CC=4  out:7
    _inject_profile_text  CC=7  out:12
    _injection_result  CC=1  out:0
    _is_wayland_session  CC=6  out:7
    _os_injector_skip_reason  CC=9  out:7
    _post_focus_delay_seconds  CC=3  out:5
  src.gillm.intents.contract  [2 funcs]
    gui_contract  CC=1  out:1
    validate_contract_runtime  CC=7  out:6
  src.gillm.orchestrator.drive  [4 funcs]
    capture_screenshot  CC=1  out:4
    focus_target_window  CC=1  out:5
    inject_text  CC=1  out:4
    log  CC=2  out:1

EDGES:
  src.gillm.config.default_config_path → src.gillm.config.resolve_xdg_path
  src.gillm.config.load_config → src.gillm.config._merge_submit_keys
  src.gillm.config.load_config → src.gillm.config.default_config_path
  src.gillm.config._cached_config → src.gillm.config.load_config
  src.gillm.config.cached_config → src.gillm.config._cached_config
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
  src.gillm.injection.injector._session_backend_order → src.gillm.injection.injector._unique_backend_names
  src.gillm.injection.injector.Injector._candidate_backends → src.gillm.injection.injector._forced_injector_backend
  src.gillm.injection.injector.Injector._candidate_backends → src.gillm.injection.injector._session_backend_order
  src.gillm.injection.injector.Injector._type_with_backend → src.gillm.injection.backends.type_with_backend
  src.gillm.injection.injector.Injector.type_text → src.gillm.injection.injector._submit_key_for
  src.gillm.injection.injector.Injector.submit_only → src.gillm.injection.injector._submit_key_for
  src.gillm.injection.os_injector.try_load_profile → src.gillm.injection.os_injector.iter_config_paths
  src.gillm.injection.os_injector.try_load_profile → src.gillm.injection.os_injector.load_profile
  src.gillm.injection.os_injector.load_profile → src.gillm.injection.os_injector._read_json
  src.gillm.injection.os_injector.load_profile → src.gillm.injection.os_injector.default_config_path
  src.gillm.injection.os_injector.save_profile → src.gillm.injection.os_injector._read_json
  src.gillm.injection.os_injector.save_profile → src.gillm.injection.os_injector.default_config_path
  src.gillm.injection.os_injector.capture_from_xdotool → src.gillm.injection.os_injector.capture_mouse_xy
  src.gillm.injection.os_injector._run_cmd → src.gillm.injection.os_injector._cmd_timeout_seconds
  src.gillm.injection.os_injector._xdotool → src.gillm.injection.os_injector._run_cmd
  src.gillm.injection.os_injector._ydotool → src.gillm.injection.os_injector._run_cmd
  src.gillm.injection.os_injector._set_clipboard → src.gillm.injection.os_injector._run_cmd
  src.gillm.injection.os_injector._resolve_input_method → src.gillm.injection.os_injector.input_mode_from_env
  src.gillm.injection.os_injector._resolve_input_method → src.gillm.injection.os_injector._clipboard_backend
  src.gillm.injection.os_injector._resolve_input_method → src.gillm.injection.os_injector._is_wayland_session
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.backends._log
  src.gillm.injection.os_injector._focus_profile_chat → src.gillm.injection.os_injector._is_wayland_session
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 32f 3590L | python:26,shell:2,yaml:2,toml:1 | 2026-06-03
# generated in 0.01s
# CC̅=3.5 | critical:0/137 | dups:0 | cycles:0

HEALTH[0]: ok

REFACTOR[0]: none needed

PIPELINES[63]:
  [1] Src [submit_key_for]: submit_key_for
      PURITY: 100% pure
  [2] Src [clear_config_cache]: clear_config_cache
      PURITY: 100% pure
  [3] Src [main]: main
      PURITY: 100% pure
  [4] Src [__init__]: __init__
      PURITY: 100% pure
  [5] Src [parse_intent]: parse_intent
      PURITY: 100% pure
  [6] Src [_which]: _which
      PURITY: 100% pure
  [7] Src [_session_type]: _session_type
      PURITY: 100% pure
  [8] Src [_default_runner]: _default_runner
      PURITY: 100% pure
  [9] Src [probe]: probe
      PURITY: 100% pure
  [10] Src [_candidate_backends]: _candidate_backends → _forced_injector_backend
      PURITY: 100% pure
  [11] Src [_forced_backend_candidates]: _forced_backend_candidates
      PURITY: 100% pure
  [12] Src [_available_backend_candidates]: _available_backend_candidates
      PURITY: 100% pure
  [13] Src [select_backend]: select_backend
      PURITY: 100% pure
  [14] Src [_type_with_backend]: _type_with_backend → type_with_backend → _log → log
      PURITY: 100% pure
  [15] Src [_type_text_backends]: _type_text_backends
      PURITY: 100% pure
  [16] Src [_log_type_text_request]: _log_type_text_request
      PURITY: 100% pure
  [17] Src [_dry_run_type_text_result]: _dry_run_type_text_result
      PURITY: 100% pure
  [18] Src [_try_type_text_backends]: _try_type_text_backends
      PURITY: 100% pure
  [19] Src [_all_type_backends_failed]: _all_type_backends_failed
      PURITY: 100% pure
  [20] Src [type_text]: type_text → _submit_key_for → cached_config → _cached_config → ...(2 more)
      PURITY: 100% pure
  [21] Src [submit_only]: submit_only → _submit_key_for → cached_config → _cached_config → ...(2 more)
      PURITY: 100% pure
  [22] Src [_probe_one]: _probe_one
      PURITY: 100% pure
  [23] Src [_call]: _call
      PURITY: 100% pure
  [24] Src [save_profile]: save_profile → _read_json
      PURITY: 100% pure
  [25] Src [profile_from_mouse]: profile_from_mouse
      PURITY: 100% pure
  [26] Src [capture_from_xdotool]: capture_from_xdotool → capture_mouse_xy
      PURITY: 100% pure
  [27] Src [try_drive_with_profile]: try_drive_with_profile → _os_injector_skip_reason → os_injector_env_disabled
      PURITY: 100% pure
  [28] Src [try_os_injector_drive]: try_os_injector_drive
      PURITY: 100% pure
  [29] Src [format_os_injector_ack]: format_os_injector_ack
      PURITY: 100% pure
  [30] Src [apply_keyboard_injection]: apply_keyboard_injection
      PURITY: 100% pure
  [31] Src [register_os_strategy]: register_os_strategy
      PURITY: 100% pure
  [32] Src [list_os_strategy_ids]: list_os_strategy_ids
      PURITY: 100% pure
  [33] Src [matches_current_environment]: matches_current_environment
      PURITY: 100% pure
  [34] Src [capabilities]: capabilities
      PURITY: 100% pure
  [35] Src [focus_window]: focus_window
      PURITY: 100% pure
  [36] Src [inject_keys]: inject_keys
      PURITY: 100% pure
  [37] Src [_focus_via_xdotool]: _focus_via_xdotool → _run
      PURITY: 100% pure
  [38] Src [_focus_via_wmctrl]: _focus_via_wmctrl → _run
      PURITY: 100% pure
  [39] Src [_inject_via_xdotool]: _inject_via_xdotool → _run
      PURITY: 100% pure
  [40] Src [_run]: _run
      PURITY: 100% pure
  [41] Src [matches_current_environment]: matches_current_environment
      PURITY: 100% pure
  [42] Src [capabilities]: capabilities
      PURITY: 100% pure
  [43] Src [focus_window]: focus_window
      PURITY: 100% pure
  [44] Src [inject_keys]: inject_keys → _prefer_ydotool → _gnome_compositor
      PURITY: 100% pure
  [45] Src [_focus_via_wmctrl]: _focus_via_wmctrl → _run
      PURITY: 100% pure
  [46] Src [_inject_via_wtype]: _inject_via_wtype → _run
      PURITY: 100% pure
  [47] Src [_inject_via_ydotool]: _inject_via_ydotool → _scan_for_key
      PURITY: 100% pure
  [48] Src [__post_init__]: __post_init__
      PURITY: 100% pure
  [49] Src [_term_program_is_vscode_family]: _term_program_is_vscode_family
      PURITY: 100% pure
  [50] Src [__repr__]: __repr__
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.5    ←in:0  →out:0
  │ !! os_injector                511L  2C   31m  CC=9      ←0
  │ injector                   357L  3C   24m  CC=10     ←0
  │ wayland                    236L  1C   11m  CC=9      ←0
  │ backends                   207L  0C   11m  CC=5      ←2
  │ drive                      154L  1C    8m  CC=12     ←1
  │ mss_backend                130L  1C    6m  CC=6      ←1
  │ x11                        128L  1C    8m  CC=11     ←2
  │ portal_backend             113L  1C    2m  CC=8      ←1
  │ config                     112L  1C    8m  CC=7      ←1
  │ strategy                   108L  5C    7m  CC=5      ←0
  │ main                        80L  0C    1m  CC=9      ←0
  │ contract                    78L  0C    2m  CC=7      ←1
  │ darwin                      72L  1C    5m  CC=4      ←0
  │ client                      70L  1C    2m  CC=5      ←0
  │ drive_backend               66L  0C    3m  CC=4      ←0
  │ registry                    50L  0C    4m  CC=5      ←1
  │ windows                     43L  1C    4m  CC=1      ←0
  │ __init__                    37L  0C    0m  CC=0.0    ←0
  │ __init__                    33L  0C    0m  CC=0.0    ←0
  │ __init__                    20L  0C    0m  CC=0.0    ←0
  │ __init__                    16L  0C    0m  CC=0.0    ←0
  │ errors                      10L  1C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ Makefile                   293L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              64L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │

COUPLING: no cross-package imports detected

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 4 groups | 26f 2651L | 2026-06-03

SUMMARY:
  files_scanned: 26
  total_lines:   2651
  dup_groups:    4
  dup_fragments: 10
  saved_lines:   37
  scan_ms:       2319

HOTSPOTS[5] (files with most duplication):
  src/gillm/focus/wayland.py  dup=17L  groups=2  frags=2  (0.6%)
  src/gillm/focus/x11.py  dup=17L  groups=2  frags=2  (0.6%)
  src/gillm/injection/backends.py  dup=12L  groups=1  frags=2  (0.5%)
  src/gillm/injection/os_injector.py  dup=9L  groups=1  frags=3  (0.3%)
  src/gillm/focus/darwin.py  dup=8L  groups=1  frags=1  (0.3%)

DUPLICATES[4] (ranked by impact):
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
  [cede1a8630b48984]   STRU  os_injector_env_disabled  L=3 N=3 saved=6 sim=1.00
      src/gillm/injection/os_injector.py:57-59  (os_injector_env_disabled)
      src/gillm/injection/os_injector.py:62-64  (os_injector_env_forced)
      src/gillm/injection/os_injector.py:67-69  (dry_run_from_env)

REFACTOR[4] (ranked by priority):
  [1] ○ extract_function   → src/gillm/focus/utils/_run.py
      WHY: 3 occurrences of 8-line block across 3 files — saves 16 lines
      FILES: src/gillm/focus/darwin.py, src/gillm/focus/wayland.py, src/gillm/focus/x11.py
  [2] ○ extract_function   → src/gillm/focus/utils/_focus_via_wmctrl.py
      WHY: 2 occurrences of 9-line block across 2 files — saves 9 lines
      FILES: src/gillm/focus/wayland.py, src/gillm/focus/x11.py
  [3] ○ extract_function   → src/gillm/injection/utils/ydotool_enter_keycode.py
      WHY: 2 occurrences of 6-line block across 1 files — saves 6 lines
      FILES: src/gillm/injection/backends.py
  [4] ○ extract_function   → src/gillm/injection/utils/os_injector_env_disabled.py
      WHY: 3 occurrences of 3-line block across 1 files — saves 6 lines
      FILES: src/gillm/injection/os_injector.py

QUICK_WINS[4] (low risk, high savings — do first):
  [1] extract_function   saved=16L  → src/gillm/focus/utils/_run.py
      FILES: darwin.py, wayland.py, x11.py
  [2] extract_function   saved=9L  → src/gillm/focus/utils/_focus_via_wmctrl.py
      FILES: wayland.py, x11.py
  [3] extract_function   saved=6L  → src/gillm/injection/utils/ydotool_enter_keycode.py
      FILES: backends.py
  [4] extract_function   saved=6L  → src/gillm/injection/utils/os_injector_env_disabled.py
      FILES: os_injector.py

EFFORT_ESTIMATE (total ≈ 1.2h):
  medium _run                                saved=16L  ~32min
  easy   _focus_via_wmctrl                   saved=9L  ~18min
  easy   ydotool_enter_keycode               saved=6L  ~12min
  easy   os_injector_env_disabled            saved=6L  ~12min

METRICS-TARGET:
  dup_groups:  4 → 0
  saved_lines: 37 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 137 func | 17f | 2026-06-03
# generated in 0.00s

NEXT[2] (ranked by impact):
  [1] !! SPLIT           src/gillm/injection/os_injector.py
      WHY: 511L, 2 classes, max CC=9
      EFFORT: ~4h  IMPACT: 4599

  [2] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting src/gillm/injection/os_injector.py may break 31 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.5 → ≤2.4
  max-CC:      12 → ≤6
  god-modules: 2 → 0
  high-CC(≥15): 0 → ≤0
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
  prev CC̄=3.5 → now CC̄=3.5
```

## Intent

GUI Control Plugin with NLP & Intent Contracts
