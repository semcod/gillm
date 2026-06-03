% ── Project Metadata ─────────────────────────────────────
project_metadata('gillm', '0.1.8', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 288, 'less').
project_file('project.sh', 50, 'shell').
project_file('src/gillm/__init__.py', 25, 'python').
project_file('src/gillm/adapters/__init__.py', 6, 'python').
project_file('src/gillm/adapters/koru.py', 95, 'python').
project_file('src/gillm/capture/__init__.py', 17, 'python').
project_file('src/gillm/capture/mss_backend.py', 131, 'python').
project_file('src/gillm/capture/portal_backend.py', 114, 'python').
project_file('src/gillm/cli/__init__.py', 6, 'python').
project_file('src/gillm/cli/main.py', 81, 'python').
project_file('src/gillm/config.py', 113, 'python').
project_file('src/gillm/contracts/__init__.py', 24, 'python').
project_file('src/gillm/contracts/driver.py', 137, 'python').
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
project_file('src/gillm/nlp_bridge/client.py', 71, 'python').
project_file('src/gillm/orchestrator/__init__.py', 6, 'python').
project_file('src/gillm/orchestrator/drive.py', 155, 'python').
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
project_file('tests/test_gillm.py', 97, 'python').
project_file('tests/test_gui_driver.py', 43, 'python').
project_file('tests/test_injector.py', 286, 'python').
project_file('tests/test_os_injector.py', 352, 'python').
project_file('tests/test_os_strategies.py', 382, 'python').
project_file('tests/test_recovery.py', 49, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
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
python_function('tests/test_gillm.py', 'test_nlp_bridge_heuristic_parsing', 0, 6, 3).
python_function('tests/test_gillm.py', 'test_orchestrator_execution', 0, 4, 3).
python_function('tests/test_gillm.py', 'test_orchestrator_nlp_drive', 1, 5, 5).
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

