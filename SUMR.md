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
- **version**: `0.1.8`
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
  version: 0.1.8;
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

*104 nodes · 117 edges · 20 modules · CC̄=3.6*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `_log` *(in src.gillm.injection.backends)* | 2 | 26 | 1 | **27** |
| `execute` *(in src.gillm.drivers.composite.CompositeGuiDriver)* | 18 ⚠ | 0 | 22 | **22** |
| `diagnose_drive_reply` *(in src.gillm.recovery.diagnose)* | 9 | 0 | 21 | **21** |
| `inject_with_profile` *(in src.gillm.injection.os_injector)* | 5 | 2 | 12 | **14** |
| `type_text` *(in src.gillm.drivers.composite.CompositeGuiDriver)* | 6 | 0 | 14 | **14** |
| `submit_only` *(in src.gillm.injection.injector.Injector)* | 9 | 0 | 13 | **13** |
| `type_with_ydotool` *(in src.gillm.injection.backends)* | 5 | 1 | 12 | **13** |
| `load_profile` *(in src.gillm.runtime.profiles)* | 5 | 1 | 12 | **13** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/gillm
# generated in 0.05s
# nodes: 104 | edges: 117 | modules: 20
# CC̄=3.6

HUBS[20]:
  src.gillm.injection.backends._log
    CC=2  in:26  out:1  total:27
  src.gillm.drivers.composite.CompositeGuiDriver.execute
    CC=18  in:0  out:22  total:22
  src.gillm.recovery.diagnose.diagnose_drive_reply
    CC=9  in:0  out:21  total:21
  src.gillm.injection.os_injector.inject_with_profile
    CC=5  in:2  out:12  total:14
  src.gillm.drivers.composite.CompositeGuiDriver.type_text
    CC=6  in:0  out:14  total:14
  src.gillm.injection.injector.Injector.submit_only
    CC=9  in:0  out:13  total:13
  src.gillm.injection.backends.type_with_ydotool
    CC=5  in:1  out:12  total:13
  src.gillm.runtime.profiles.load_profile
    CC=5  in:1  out:12  total:13
  src.gillm.injection.os_injector._inject_profile_text
    CC=7  in:1  out:12  total:13
  src.gillm.focus.x11._run
    CC=1  in:11  out:1  total:12
  src.gillm.runtime.profiles.iter_config_paths
    CC=4  in:1  out:11  total:12
  src.gillm.capture.portal_backend.capture_portal_png
    CC=8  in:1  out:11  total:12
  src.gillm.config.load_config
    CC=4  in:1  out:10  total:11
  src.gillm.runtime.profiles.capture_mouse_xy
    CC=7  in:1  out:10  total:11
  src.gillm.injection.backends.type_with_backend
    CC=5  in:1  out:10  total:11
  src.gillm.capture.mss_backend._parse_png_to_rgb
    CC=4  in:1  out:10  total:11
  src.gillm.runtime.env.session_type
    CC=4  in:6  out:4  total:10
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool
    CC=7  in:0  out:10  total:10
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_xdotool
    CC=11  in:0  out:10  total:10
  src.gillm.capture.mss_backend.capture_primary_rgb
    CC=2  in:1  out:8  total:9

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
  src.gillm.drivers.composite  [5 funcs]
    __init__  CC=2  out:3
    execute  CC=18  out:22
    focus  CC=3  out:6
    probe  CC=3  out:3
    type_text  CC=6  out:14
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
  src.gillm.orchestrator.drive  [4 funcs]
    capture_screenshot  CC=1  out:4
    focus_target_window  CC=1  out:5
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
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_xdotool → src.gillm.focus.x11._run
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_wmctrl → src.gillm.focus.x11._run
  src.gillm.focus.x11.X11LinuxStrategy._inject_via_xdotool → src.gillm.focus.x11._run
  src.gillm.focus.wayland._prefer_ydotool → src.gillm.focus.wayland._gnome_compositor
  src.gillm.focus.wayland.WaylandLinuxStrategy.inject_keys → src.gillm.focus.wayland._prefer_ydotool
  src.gillm.focus.wayland.WaylandLinuxStrategy._focus_via_wmctrl → src.gillm.focus.x11._run
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_wtype → src.gillm.focus.x11._run
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool → src.gillm.focus.wayland._scan_for_key
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool → src.gillm.focus.x11._run
  src.gillm.focus.darwin.DarwinStrategy.focus_window → src.gillm.focus.x11._run
  src.gillm.orchestrator.drive.DriveOrchestrator.focus_target_window → src.gillm.intents.contract.gui_contract
  src.gillm.orchestrator.drive.DriveOrchestrator.focus_target_window → src.gillm.intents.contract.validate_contract_runtime
  src.gillm.orchestrator.drive.DriveOrchestrator.focus_target_window → src.gillm.focus.registry.resolve_active_os_strategy
  src.gillm.orchestrator.drive.DriveOrchestrator.inject_text → src.gillm.intents.contract.gui_contract
  src.gillm.orchestrator.drive.DriveOrchestrator.inject_text → src.gillm.intents.contract.validate_contract_runtime
  src.gillm.orchestrator.drive.DriveOrchestrator.capture_screenshot → src.gillm.intents.contract.gui_contract
  src.gillm.orchestrator.drive.DriveOrchestrator.capture_screenshot → src.gillm.intents.contract.validate_contract_runtime
  src.gillm.orchestrator.drive.DriveOrchestrator.capture_screenshot → src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints._hints_for_kind
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints._dedupe
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints.recovery_hints_for_reload
  src.gillm.recovery.repair_hints._hints_for_kind → src.gillm.recovery.repair_hints.recovery_hints_for_reload
  src.gillm.recovery.diagnose.probe_environment → src.gillm.runtime.env.session_type
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
# nodes: 104 | edges: 117 | modules: 20
# CC̄=3.6

HUBS[20]:
  src.gillm.injection.backends._log
    CC=2  in:26  out:1  total:27
  src.gillm.drivers.composite.CompositeGuiDriver.execute
    CC=18  in:0  out:22  total:22
  src.gillm.recovery.diagnose.diagnose_drive_reply
    CC=9  in:0  out:21  total:21
  src.gillm.injection.os_injector.inject_with_profile
    CC=5  in:2  out:12  total:14
  src.gillm.drivers.composite.CompositeGuiDriver.type_text
    CC=6  in:0  out:14  total:14
  src.gillm.injection.injector.Injector.submit_only
    CC=9  in:0  out:13  total:13
  src.gillm.injection.backends.type_with_ydotool
    CC=5  in:1  out:12  total:13
  src.gillm.runtime.profiles.load_profile
    CC=5  in:1  out:12  total:13
  src.gillm.injection.os_injector._inject_profile_text
    CC=7  in:1  out:12  total:13
  src.gillm.focus.x11._run
    CC=1  in:11  out:1  total:12
  src.gillm.runtime.profiles.iter_config_paths
    CC=4  in:1  out:11  total:12
  src.gillm.capture.portal_backend.capture_portal_png
    CC=8  in:1  out:11  total:12
  src.gillm.config.load_config
    CC=4  in:1  out:10  total:11
  src.gillm.runtime.profiles.capture_mouse_xy
    CC=7  in:1  out:10  total:11
  src.gillm.injection.backends.type_with_backend
    CC=5  in:1  out:10  total:11
  src.gillm.capture.mss_backend._parse_png_to_rgb
    CC=4  in:1  out:10  total:11
  src.gillm.runtime.env.session_type
    CC=4  in:6  out:4  total:10
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool
    CC=7  in:0  out:10  total:10
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_xdotool
    CC=11  in:0  out:10  total:10
  src.gillm.capture.mss_backend.capture_primary_rgb
    CC=2  in:1  out:8  total:9

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
  src.gillm.drivers.composite  [5 funcs]
    __init__  CC=2  out:3
    execute  CC=18  out:22
    focus  CC=3  out:6
    probe  CC=3  out:3
    type_text  CC=6  out:14
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
  src.gillm.orchestrator.drive  [4 funcs]
    capture_screenshot  CC=1  out:4
    focus_target_window  CC=1  out:5
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
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_xdotool → src.gillm.focus.x11._run
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_wmctrl → src.gillm.focus.x11._run
  src.gillm.focus.x11.X11LinuxStrategy._inject_via_xdotool → src.gillm.focus.x11._run
  src.gillm.focus.wayland._prefer_ydotool → src.gillm.focus.wayland._gnome_compositor
  src.gillm.focus.wayland.WaylandLinuxStrategy.inject_keys → src.gillm.focus.wayland._prefer_ydotool
  src.gillm.focus.wayland.WaylandLinuxStrategy._focus_via_wmctrl → src.gillm.focus.x11._run
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_wtype → src.gillm.focus.x11._run
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool → src.gillm.focus.wayland._scan_for_key
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool → src.gillm.focus.x11._run
  src.gillm.focus.darwin.DarwinStrategy.focus_window → src.gillm.focus.x11._run
  src.gillm.orchestrator.drive.DriveOrchestrator.focus_target_window → src.gillm.intents.contract.gui_contract
  src.gillm.orchestrator.drive.DriveOrchestrator.focus_target_window → src.gillm.intents.contract.validate_contract_runtime
  src.gillm.orchestrator.drive.DriveOrchestrator.focus_target_window → src.gillm.focus.registry.resolve_active_os_strategy
  src.gillm.orchestrator.drive.DriveOrchestrator.inject_text → src.gillm.intents.contract.gui_contract
  src.gillm.orchestrator.drive.DriveOrchestrator.inject_text → src.gillm.intents.contract.validate_contract_runtime
  src.gillm.orchestrator.drive.DriveOrchestrator.capture_screenshot → src.gillm.intents.contract.gui_contract
  src.gillm.orchestrator.drive.DriveOrchestrator.capture_screenshot → src.gillm.intents.contract.validate_contract_runtime
  src.gillm.orchestrator.drive.DriveOrchestrator.capture_screenshot → src.gillm.capture.mss_backend.capture_primary_rgb_wayland_fallback
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints._hints_for_kind
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints._dedupe
  src.gillm.recovery.repair_hints.recovery_hints_for_context → src.gillm.recovery.repair_hints.recovery_hints_for_reload
  src.gillm.recovery.repair_hints._hints_for_kind → src.gillm.recovery.repair_hints.recovery_hints_for_reload
  src.gillm.recovery.diagnose.probe_environment → src.gillm.runtime.env.session_type
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 49f 4632L | python:43,yaml:2,shell:2,toml:1 | 2026-06-03
# generated in 0.01s
# CC̅=3.6 | critical:4/188 | dups:0 | cycles:0

HEALTH[4]:
  🟡 CC    _hints_for_kind CC=15 (limit:15)
  🟡 CC    classify_failure CC=24 (limit:15)
  🟡 CC    execute CC=18 (limit:15)
  🟡 CC    drive_payload_to_action_plan CC=21 (limit:15)

REFACTOR[1]:
  1. split 4 high-CC methods  (CC>15)

PIPELINES[95]:
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
  [6] Src [try_os_injector_drive]: try_os_injector_drive
      PURITY: 100% pure
  [7] Src [format_os_injector_ack]: format_os_injector_ack
      PURITY: 100% pure
  [8] Src [apply_keyboard_injection]: apply_keyboard_injection
      PURITY: 100% pure
  [9] Src [register_os_strategy]: register_os_strategy
      PURITY: 100% pure
  [10] Src [list_os_strategy_ids]: list_os_strategy_ids
      PURITY: 100% pure
  [11] Src [matches_current_environment]: matches_current_environment
      PURITY: 100% pure
  [12] Src [capabilities]: capabilities
      PURITY: 100% pure
  [13] Src [focus_window]: focus_window
      PURITY: 100% pure
  [14] Src [inject_keys]: inject_keys
      PURITY: 100% pure
  [15] Src [_focus_via_xdotool]: _focus_via_xdotool → _run
      PURITY: 100% pure
  [16] Src [_focus_via_wmctrl]: _focus_via_wmctrl → _run
      PURITY: 100% pure
  [17] Src [_inject_via_xdotool]: _inject_via_xdotool → _run
      PURITY: 100% pure
  [18] Src [_run]: _run
      PURITY: 100% pure
  [19] Src [matches_current_environment]: matches_current_environment
      PURITY: 100% pure
  [20] Src [capabilities]: capabilities
      PURITY: 100% pure
  [21] Src [focus_window]: focus_window
      PURITY: 100% pure
  [22] Src [inject_keys]: inject_keys → _prefer_ydotool → _gnome_compositor
      PURITY: 100% pure
  [23] Src [_focus_via_wmctrl]: _focus_via_wmctrl → _run
      PURITY: 100% pure
  [24] Src [_inject_via_wtype]: _inject_via_wtype → _run
      PURITY: 100% pure
  [25] Src [_inject_via_ydotool]: _inject_via_ydotool → _scan_for_key
      PURITY: 100% pure
  [26] Src [__post_init__]: __post_init__
      PURITY: 100% pure
  [27] Src [_term_program_is_vscode_family]: _term_program_is_vscode_family
      PURITY: 100% pure
  [28] Src [__repr__]: __repr__
      PURITY: 100% pure
  [29] Src [_run]: _run
      PURITY: 100% pure
  [30] Src [capabilities]: capabilities
      PURITY: 100% pure
  [31] Src [focus_window]: focus_window → _run
      PURITY: 100% pure
  [32] Src [matches_current_environment]: matches_current_environment
      PURITY: 100% pure
  [33] Src [capabilities]: capabilities
      PURITY: 100% pure
  [34] Src [focus_window]: focus_window
      PURITY: 100% pure
  [35] Src [__init__]: __init__
      PURITY: 100% pure
  [36] Src [focus_target_window]: focus_target_window → gui_contract
      PURITY: 100% pure
  [37] Src [inject_text]: inject_text → gui_contract
      PURITY: 100% pure
  [38] Src [capture_screenshot]: capture_screenshot → gui_contract
      PURITY: 100% pure
  [39] Src [execute_step]: execute_step
      PURITY: 100% pure
  [40] Src [execute_workflow]: execute_workflow
      PURITY: 100% pure
  [41] Src [drive_natural_language]: drive_natural_language
      PURITY: 100% pure
  [42] Src [to_dict]: to_dict
      PURITY: 100% pure
  [43] Src [to_dict]: to_dict
      PURITY: 100% pure
  [44] Src [diagnose_drive_reply]: diagnose_drive_reply → classify_failure
      PURITY: 100% pure
  [45] Src [_which]: _which
      PURITY: 100% pure
  [46] Src [_session_type]: _session_type → session_type
      PURITY: 100% pure
  [47] Src [_default_runner]: _default_runner
      PURITY: 100% pure
  [48] Src [probe]: probe
      PURITY: 100% pure
  [49] Src [_candidate_backends]: _candidate_backends
      PURITY: 100% pure
  [50] Src [select_backend]: select_backend
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.6    ←in:0  →out:0
  │ os_injector                323L  0C   10m  CC=9      ←1
  │ injector                   276L  3C   18m  CC=10     ←0
  │ wayland                    236L  1C   11m  CC=9      ←0
  │ backends                   207L  0C   11m  CC=5      ←2
  │ !! composite                  180L  1C    8m  CC=18     ←0
  │ drive                      154L  1C    8m  CC=12     ←1
  │ !! diagnose                   150L  2C    5m  CC=24     ←1
  │ driver                     136L  7C   11m  CC=2      ←0
  │ mss_backend                130L  1C    6m  CC=6      ←1
  │ x11                        128L  1C    8m  CC=11     ←2
  │ profiles                   117L  1C    9m  CC=7      ←2
  │ portal_backend             113L  1C    2m  CC=8      ←1
  │ config                     112L  1C    8m  CC=7      ←1
  │ strategy                   108L  5C    7m  CC=5      ←0
  │ !! repair_hints                98L  0C    4m  CC=15     ←2
  │ backend_selector            96L  1C    8m  CC=6      ←0
  │ !! koru                        94L  0C    3m  CC=21     ←0
  │ dry_run                     89L  1C    8m  CC=10     ←0
  │ command_runner              88L  1C    7m  CC=7      ←1
  │ env                         87L  0C   10m  CC=6      ←6
  │ main                        80L  0C    1m  CC=9      ←0
  │ contract                    78L  0C    2m  CC=7      ←1
  │ darwin                      72L  1C    5m  CC=4      ←0
  │ client                      70L  1C    2m  CC=5      ←0
  │ drive_backend               66L  0C    3m  CC=4      ←0
  │ activity                    62L  0C    5m  CC=3      ←1
  │ __init__                    51L  0C    0m  CC=0.0    ←0
  │ registry                    50L  0C    4m  CC=5      ←1
  │ windows                     43L  1C    4m  CC=1      ←0
  │ __init__                    37L  0C    0m  CC=0.0    ←0
  │ __init__                    33L  0C    0m  CC=0.0    ←0
  │ __init__                    24L  0C    0m  CC=0.0    ←0
  │ __init__                    23L  0C    0m  CC=0.0    ←0
  │ __init__                    20L  0C    0m  CC=0.0    ←0
  │ __init__                    16L  0C    0m  CC=0.0    ←0
  │ errors                      10L  1C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │ errors                       5L  1C    0m  CC=0.0    ←0
  │ __init__                     5L  0C    0m  CC=0.0    ←0
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
# redup/duplication | 3 groups | 42f 3606L | 2026-06-03

SUMMARY:
  files_scanned: 42
  total_lines:   3606
  dup_groups:    3
  dup_fragments: 7
  saved_lines:   31
  scan_ms:       2688

HOTSPOTS[4] (files with most duplication):
  src/gillm/focus/wayland.py  dup=17L  groups=2  frags=2  (0.5%)
  src/gillm/focus/x11.py  dup=17L  groups=2  frags=2  (0.5%)
  src/gillm/injection/backends.py  dup=12L  groups=1  frags=2  (0.3%)
  src/gillm/focus/darwin.py  dup=8L  groups=1  frags=1  (0.2%)

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
# code2llm/evolution | 188 func | 28f | 2026-06-03
# generated in 0.00s

NEXT[4] (ranked by impact):
  [1] !  SPLIT-FUNC      CompositeGuiDriver.execute  CC=18  fan=14
      WHY: CC=18 exceeds 15
      EFFORT: ~1h  IMPACT: 252

  [2] !  SPLIT-FUNC      drive_payload_to_action_plan  CC=21  fan=11
      WHY: CC=21 exceeds 15
      EFFORT: ~1h  IMPACT: 231

  [3] !  SPLIT-FUNC      _hints_for_kind  CC=15  fan=3
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 45

  [4] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[1]:
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.6 → ≤2.5
  max-CC:      24 → ≤12
  god-modules: 1 → 0
  high-CC(≥15): 4 → ≤2
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
  prev CC̄=3.5 → now CC̄=3.6
```

## Intent

GUI Control Plugin with NLP & Intent Contracts
