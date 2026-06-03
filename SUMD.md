# gillm

GUI Control Plugin with NLP & Intent Contracts

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `gillm`
- **version**: `0.1.5`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, testql(1), app.doql.less, goal.yaml, .env.example, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: gillm;
  version: 0.1.5;
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

deploy {
  target: pip;
}

environment[name="local"] {
  runtime: python;
  env_file: .env;
  python_version: >=3.10;
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

## Configuration

```yaml
project:
  name: gillm
  version: 0.1.5
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
- **version files**: `VERSION`, `pyproject.toml:version`, `.venv/lib/python3.13/site-packages/markdown_it/__init__.py:__version__`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# gillm | 34f 3947L | python:31,shell:2,less:1 | 2026-06-03
# stats: 133 func | 26 cls | 34 mod | CC̄=3.4 | critical:0 | cycles:0
# alerts[5]: CC main=9; CC _os_injector_skip_reason=9; CC try_drive_with_profile=9; CC test_inject_with_profile_paste_path_uses_clipboard_then_ctrl_v=9; CC capture_portal_png=8
# hotspots[5]: main fan=15; type_with_backend fan=10; inject_with_profile fan=10; _parse_png_to_rgb fan=9; test_inject_with_profile_paste_path_uses_clipboard_then_ctrl_v fan=9
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[34]:
  app.doql.less,29
  project.sh,50
  src/gillm/__init__.py,21
  src/gillm/capture/__init__.py,17
  src/gillm/capture/mss_backend.py,131
  src/gillm/capture/portal_backend.py,114
  src/gillm/cli/__init__.py,6
  src/gillm/cli/main.py,81
  src/gillm/config.py,113
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
  src/gillm/injection/injector.py,358
  src/gillm/injection/os_injector.py,512
  src/gillm/intents/__init__.py,6
  src/gillm/intents/contract.py,79
  src/gillm/nlp_bridge/__init__.py,6
  src/gillm/nlp_bridge/client.py,71
  src/gillm/orchestrator/__init__.py,6
  src/gillm/orchestrator/drive.py,155
  tests/test_drive_backend.py,72
  tests/test_gillm.py,97
  tests/test_injector.py,286
  tests/test_os_injector.py,352
  tests/test_os_strategies.py,382
  tree.sh,2
D:
  src/gillm/__init__.py:
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
    e: main
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
    e: _submit_key_for,_which,_session_type,_forced_injector_backend,_unique_backend_names,_session_backend_order,_default_runner,BackendStatus,InjectionResult,Injector
    BackendStatus: to_dict(0)  # Result of probing a single backend.
    InjectionResult: to_dict(0)
    Injector: probe(0),_candidate_backends(0),_forced_backend_candidates(1),_available_backend_candidates(1),select_backend(0),_type_with_backend(3),_type_text_backends(0),_log_type_text_request(3),_dry_run_type_text_result(0),_try_type_text_backends(4),_all_type_backends_failed(1),type_text(1),submit_only(0),_probe_one(1),_call(1)  # Pick the best available backend and type text through it.
    _submit_key_for(ide)
    _which(name)
    _session_type()
    _forced_injector_backend()
    _unique_backend_names(names)
    _session_backend_order(session)
    _default_runner(cmd;stdin)
  src/gillm/injection/os_injector.py:
    e: default_config_path,iter_config_paths,os_injector_env_disabled,os_injector_env_forced,dry_run_from_env,focus_mode_from_env,input_mode_from_env,_is_wayland_session,_cmd_timeout_seconds,_post_focus_delay_seconds,try_load_profile,_read_json,load_profile,save_profile,profile_from_mouse,capture_mouse_xy,capture_from_xdotool,_run_cmd,_xdotool,_ydotool,_clipboard_backend,_set_clipboard,_resolve_input_method,_injection_result,_focus_profile_chat,_focus_with_ydotool,_focus_with_xdotool,_inject_profile_text,inject_with_profile,_os_injector_skip_reason,try_drive_with_profile,OsInjectorError,OsInjectorProfile
    OsInjectorError:  # Raised when profile config or xdotool operations fail.
    OsInjectorProfile:  # Chat anchor: pixel position under the cursor at calibration 
    default_config_path()
    iter_config_paths()
    os_injector_env_disabled()
    os_injector_env_forced()
    dry_run_from_env()
    focus_mode_from_env()
    input_mode_from_env()
    _is_wayland_session()
    _cmd_timeout_seconds()
    _post_focus_delay_seconds()
    try_load_profile(tool_id)
    _read_json(path)
    load_profile(tool_id)
    save_profile(profile)
    profile_from_mouse(tool_id)
    capture_mouse_xy()
    capture_from_xdotool()
    _run_cmd(cmd)
    _xdotool(argv_tail)
    _ydotool(argv_tail)
    _clipboard_backend()
    _set_clipboard(text)
    _resolve_input_method()
    _injection_result()
    _focus_profile_chat(profile;focus;post_focus_delay)
    _focus_with_ydotool(profile;focus)
    _focus_with_xdotool(profile;focus)
    _inject_profile_text()
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
    e: NLPBridgeClient
    NLPBridgeClient: __init__(1),parse_intent(1)  # Bridge to nlp2dsl backend for resolving natural language GUI
  src/gillm/orchestrator/__init__.py:
  src/gillm/orchestrator/drive.py:
    e: DriveOrchestrator
    DriveOrchestrator: __init__(2),log(1),focus_target_window(1),inject_text(4),capture_screenshot(1),execute_step(2),execute_workflow(2),drive_natural_language(2)  # Consolidated orchestrator for GUI drive tasks.
  tests/test_drive_backend.py:
    e: test_try_os_injector_drive_returns_none_when_no_profile,test_try_os_injector_drive_raises_on_error,test_format_os_injector_ack_includes_target,test_apply_keyboard_injection_delegates_to_injector,test_apply_keyboard_injection_propagates_injector_error
    test_try_os_injector_drive_returns_none_when_no_profile(monkeypatch)
    test_try_os_injector_drive_raises_on_error(monkeypatch)
    test_format_os_injector_ack_includes_target()
    test_apply_keyboard_injection_delegates_to_injector()
    test_apply_keyboard_injection_propagates_injector_error()
  tests/test_gillm.py:
    e: test_focus_strategies_registry,test_injector_dry_run,test_injector_empty_text_error,test_nlp_bridge_heuristic_parsing,test_orchestrator_execution,test_orchestrator_nlp_drive,test_contract_validation
    test_focus_strategies_registry()
    test_injector_dry_run()
    test_injector_empty_text_error()
    test_nlp_bridge_heuristic_parsing()
    test_orchestrator_execution()
    test_orchestrator_nlp_drive(monkeypatch)
    test_contract_validation()
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
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('gillm', '0.1.5', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 29, 'less').
project_file('project.sh', 50, 'shell').
project_file('src/gillm/__init__.py', 21, 'python').
project_file('src/gillm/capture/__init__.py', 17, 'python').
project_file('src/gillm/capture/mss_backend.py', 131, 'python').
project_file('src/gillm/capture/portal_backend.py', 114, 'python').
project_file('src/gillm/cli/__init__.py', 6, 'python').
project_file('src/gillm/cli/main.py', 81, 'python').
project_file('src/gillm/config.py', 113, 'python').
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
project_file('src/gillm/injection/injector.py', 358, 'python').
project_file('src/gillm/injection/os_injector.py', 512, 'python').
project_file('src/gillm/intents/__init__.py', 6, 'python').
project_file('src/gillm/intents/contract.py', 79, 'python').
project_file('src/gillm/nlp_bridge/__init__.py', 6, 'python').
project_file('src/gillm/nlp_bridge/client.py', 71, 'python').
project_file('src/gillm/orchestrator/__init__.py', 6, 'python').
project_file('src/gillm/orchestrator/drive.py', 155, 'python').
project_file('tests/test_drive_backend.py', 72, 'python').
project_file('tests/test_gillm.py', 97, 'python').
project_file('tests/test_injector.py', 286, 'python').
project_file('tests/test_os_injector.py', 352, 'python').
project_file('tests/test_os_strategies.py', 382, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('src/gillm/capture/mss_backend.py', 'resolve_scale', 1, 4, 5).
python_function('src/gillm/capture/mss_backend.py', 'downscale_rgb_nearest', 5, 6, 4).
python_function('src/gillm/capture/mss_backend.py', 'rgb_mostly_black', 1, 5, 3).
python_function('src/gillm/capture/mss_backend.py', 'capture_primary_rgb', 0, 2, 6).
python_function('src/gillm/capture/mss_backend.py', 'capture_primary_rgb_wayland_fallback', 0, 3, 4).
python_function('src/gillm/capture/mss_backend.py', '_parse_png_to_rgb', 1, 4, 9).
python_function('src/gillm/capture/portal_backend.py', '_portal_python', 0, 6, 4).
python_function('src/gillm/capture/portal_backend.py', 'capture_portal_png', 0, 8, 7).
python_function('src/gillm/cli/main.py', 'main', 0, 9, 15).
python_function('src/gillm/config.py', 'resolve_xdg_path', 1, 2, 3).
python_function('src/gillm/config.py', 'default_config_path', 0, 1, 1).
python_function('src/gillm/config.py', '_merge_submit_keys', 1, 7, 3).
python_function('src/gillm/config.py', 'load_config', 1, 4, 8).
python_function('src/gillm/config.py', '_cached_config', 0, 1, 2).
python_function('src/gillm/config.py', 'cached_config', 0, 6, 5).
python_function('src/gillm/config.py', 'clear_config_cache', 0, 1, 1).
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
python_function('src/gillm/injection/injector.py', '_session_type', 0, 4, 2).
python_function('src/gillm/injection/injector.py', '_forced_injector_backend', 0, 2, 3).
python_function('src/gillm/injection/injector.py', '_unique_backend_names', 1, 3, 1).
python_function('src/gillm/injection/injector.py', '_session_backend_order', 1, 4, 2).
python_function('src/gillm/injection/injector.py', '_default_runner', 2, 2, 2).
python_function('src/gillm/injection/os_injector.py', 'default_config_path', 0, 1, 1).
python_function('src/gillm/injection/os_injector.py', 'iter_config_paths', 0, 4, 7).
python_function('src/gillm/injection/os_injector.py', 'os_injector_env_disabled', 0, 1, 3).
python_function('src/gillm/injection/os_injector.py', 'os_injector_env_forced', 0, 1, 3).
python_function('src/gillm/injection/os_injector.py', 'dry_run_from_env', 0, 1, 3).
python_function('src/gillm/injection/os_injector.py', 'focus_mode_from_env', 0, 2, 3).
python_function('src/gillm/injection/os_injector.py', 'input_mode_from_env', 0, 2, 3).
python_function('src/gillm/injection/os_injector.py', '_is_wayland_session', 0, 6, 7).
python_function('src/gillm/injection/os_injector.py', '_cmd_timeout_seconds', 0, 3, 4).
python_function('src/gillm/injection/os_injector.py', '_post_focus_delay_seconds', 0, 3, 5).
python_function('src/gillm/injection/os_injector.py', 'try_load_profile', 1, 4, 3).
python_function('src/gillm/injection/os_injector.py', '_read_json', 1, 4, 5).
python_function('src/gillm/injection/os_injector.py', 'load_profile', 1, 5, 8).
python_function('src/gillm/injection/os_injector.py', 'save_profile', 1, 3, 7).
python_function('src/gillm/injection/os_injector.py', 'profile_from_mouse', 1, 1, 1).
python_function('src/gillm/injection/os_injector.py', 'capture_mouse_xy', 0, 6, 6).
python_function('src/gillm/injection/os_injector.py', 'capture_from_xdotool', 0, 1, 1).
python_function('src/gillm/injection/os_injector.py', '_run_cmd', 1, 5, 5).
python_function('src/gillm/injection/os_injector.py', '_xdotool', 1, 1, 1).
python_function('src/gillm/injection/os_injector.py', '_ydotool', 1, 2, 3).
python_function('src/gillm/injection/os_injector.py', '_clipboard_backend', 0, 3, 1).
python_function('src/gillm/injection/os_injector.py', '_set_clipboard', 1, 3, 4).
python_function('src/gillm/injection/os_injector.py', '_resolve_input_method', 0, 7, 4).
python_function('src/gillm/injection/os_injector.py', '_injection_result', 0, 1, 0).
python_function('src/gillm/injection/os_injector.py', '_focus_profile_chat', 3, 6, 6).
python_function('src/gillm/injection/os_injector.py', '_focus_with_ydotool', 2, 4, 3).
python_function('src/gillm/injection/os_injector.py', '_focus_with_xdotool', 2, 4, 3).
python_function('src/gillm/injection/os_injector.py', '_inject_profile_text', 0, 7, 7).
python_function('src/gillm/injection/os_injector.py', 'inject_with_profile', 0, 6, 10).
python_function('src/gillm/injection/os_injector.py', '_os_injector_skip_reason', 1, 9, 4).
python_function('src/gillm/injection/os_injector.py', 'try_drive_with_profile', 0, 9, 7).
python_function('src/gillm/intents/contract.py', 'gui_contract', 9, 1, 1).
python_function('src/gillm/intents/contract.py', 'validate_contract_runtime', 1, 7, 6).
python_function('tests/test_drive_backend.py', 'test_try_os_injector_drive_returns_none_when_no_profile', 1, 2, 2).
python_function('tests/test_drive_backend.py', 'test_try_os_injector_drive_raises_on_error', 1, 1, 4).
python_function('tests/test_drive_backend.py', 'test_format_os_injector_ack_includes_target', 0, 6, 1).
python_function('tests/test_drive_backend.py', 'test_apply_keyboard_injection_delegates_to_injector', 0, 2, 3).
python_function('tests/test_drive_backend.py', 'test_apply_keyboard_injection_propagates_injector_error', 0, 1, 4).
python_function('tests/test_gillm.py', 'test_focus_strategies_registry', 0, 8, 3).
python_function('tests/test_gillm.py', 'test_injector_dry_run', 0, 5, 2).
python_function('tests/test_gillm.py', 'test_injector_empty_text_error', 0, 1, 3).
python_function('tests/test_gillm.py', 'test_nlp_bridge_heuristic_parsing', 0, 6, 3).
python_function('tests/test_gillm.py', 'test_orchestrator_execution', 0, 4, 3).
python_function('tests/test_gillm.py', 'test_orchestrator_nlp_drive', 1, 5, 5).
python_function('tests/test_gillm.py', 'test_contract_validation', 0, 3, 2).
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

% ── Python Classes ───────────────────────────────────────
python_class('src/gillm/capture/mss_backend.py', 'CapturedImage').
python_class('src/gillm/capture/portal_backend.py', 'PortalCaptureError').
python_class('src/gillm/config.py', 'AutopilotConfig').
python_method('AutopilotConfig', 'submit_key_for', 1, 2, 1).
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
python_method('Injector', 'probe', 0, 1, 1).
python_method('Injector', '_candidate_backends', 0, 5, 5).
python_method('Injector', '_forced_backend_candidates', 1, 4, 2).
python_method('Injector', '_available_backend_candidates', 1, 4, 3).
python_method('Injector', 'select_backend', 0, 2, 1).
python_method('Injector', '_type_with_backend', 3, 1, 1).
python_method('Injector', '_type_text_backends', 0, 3, 3).
python_method('Injector', '_log_type_text_request', 3, 3, 3).
python_method('Injector', '_dry_run_type_text_result', 0, 3, 3).
python_method('Injector', '_try_type_text_backends', 4, 6, 6).
python_method('Injector', '_all_type_backends_failed', 1, 2, 3).
python_method('Injector', 'type_text', 1, 6, 8).
python_method('Injector', 'submit_only', 0, 9, 8).
python_method('Injector', '_probe_one', 1, 5, 2).
python_method('Injector', '_call', 1, 10, 7).
python_class('src/gillm/injection/os_injector.py', 'OsInjectorError').
python_class('src/gillm/injection/os_injector.py', 'OsInjectorProfile').
python_class('src/gillm/nlp_bridge/client.py', 'NLPBridgeClient').
python_method('NLPBridgeClient', '__init__', 1, 2, 1).
python_method('NLPBridgeClient', 'parse_intent', 1, 5, 4).
python_class('src/gillm/orchestrator/drive.py', 'DriveOrchestrator').
python_method('DriveOrchestrator', '__init__', 2, 3, 2).
python_method('DriveOrchestrator', 'log', 1, 2, 1).
python_method('DriveOrchestrator', 'focus_target_window', 1, 1, 5).
python_method('DriveOrchestrator', 'inject_text', 4, 1, 4).
python_method('DriveOrchestrator', 'capture_screenshot', 1, 1, 4).
python_method('DriveOrchestrator', 'execute_step', 2, 12, 11).
python_method('DriveOrchestrator', 'execute_workflow', 2, 3, 4).
python_method('DriveOrchestrator', 'drive_natural_language', 2, 2, 3).
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
```

## Call Graph

*82 nodes · 94 edges · 12 modules · CC̄=3.5*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `_log` *(in src.gillm.injection.backends)* | 2 | 26 | 1 | **27** |
| `inject_with_profile` *(in src.gillm.injection.os_injector)* | 6 | 1 | 12 | **13** |
| `_inject_profile_text` *(in src.gillm.injection.os_injector)* | 7 | 1 | 12 | **13** |
| `submit_only` *(in src.gillm.injection.injector.Injector)* | 9 | 0 | 13 | **13** |
| `type_with_ydotool` *(in src.gillm.injection.backends)* | 5 | 1 | 12 | **13** |
| `load_profile` *(in src.gillm.injection.os_injector)* | 5 | 1 | 12 | **13** |
| `iter_config_paths` *(in src.gillm.injection.os_injector)* | 4 | 1 | 11 | **12** |
| `_run` *(in src.gillm.focus.x11)* | 1 | 11 | 1 | **12** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/gillm
# generated in 0.11s
# nodes: 82 | edges: 94 | modules: 12
# CC̄=3.5

HUBS[20]:
  src.gillm.injection.backends._log
    CC=2  in:26  out:1  total:27
  src.gillm.injection.os_injector.inject_with_profile
    CC=6  in:1  out:12  total:13
  src.gillm.injection.os_injector._inject_profile_text
    CC=7  in:1  out:12  total:13
  src.gillm.injection.injector.Injector.submit_only
    CC=9  in:0  out:13  total:13
  src.gillm.injection.backends.type_with_ydotool
    CC=5  in:1  out:12  total:13
  src.gillm.injection.os_injector.load_profile
    CC=5  in:1  out:12  total:13
  src.gillm.injection.os_injector.iter_config_paths
    CC=4  in:1  out:11  total:12
  src.gillm.focus.x11._run
    CC=1  in:11  out:1  total:12
  src.gillm.capture.portal_backend.capture_portal_png
    CC=8  in:1  out:11  total:12
  src.gillm.injection.backends.type_with_backend
    CC=5  in:1  out:10  total:11
  src.gillm.capture.mss_backend._parse_png_to_rgb
    CC=4  in:1  out:10  total:11
  src.gillm.injection.os_injector._is_wayland_session
    CC=6  in:4  out:7  total:11
  src.gillm.config.load_config
    CC=4  in:1  out:10  total:11
  src.gillm.injection.os_injector.capture_mouse_xy
    CC=6  in:1  out:10  total:11
  src.gillm.injection.os_injector._run_cmd
    CC=5  in:4  out:7  total:11
  src.gillm.focus.x11.X11LinuxStrategy._focus_via_xdotool
    CC=11  in:0  out:10  total:10
  src.gillm.focus.wayland.WaylandLinuxStrategy._inject_via_ydotool
    CC=7  in:0  out:10  total:10
  src.gillm.capture.mss_backend.capture_primary_rgb
    CC=2  in:1  out:8  total:9
  src.gillm.injection.backends.type_with_wtype
    CC=3  in:1  out:8  total:9
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

## Intent

GUI Control Plugin with NLP & Intent Contracts
