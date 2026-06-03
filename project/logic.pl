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
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').

