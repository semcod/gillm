# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.5] - 2026-06-03

### Added
- `gillm.injection.drive_backend` — headless OS-profile and keyboard drive helpers (`try_os_injector_drive`, `format_os_injector_ack`, `apply_keyboard_injection`)
- Unit tests moved from koru: `tests/test_injector.py`, `tests/test_os_injector.py`, `tests/test_drive_backend.py` (114+ tests)

### Changed
- Koru `koruide.daemon.handlers_drive` delegates injection backends to `gillm.injection.drive_backend`

## [0.1.4] - 2026-06-03

### Docs
- Update CHANGELOG.md
- Update README.md

### Test
- Update tests/test_gillm.py

### Other
- Update .idea/pyLspTools.xml
- Update uv.lock

## [0.1.3] - 2026-06-03

### Docs
- Update README.md

### Test
- Update tests/test_gillm.py

## [0.1.2] - 2026-06-03

### Docs
- Update README.md

## [0.1.1] - 2026-06-03

### Docs
- Update README.md

### Test
- Update tests/test_gillm.py

### Other
- Update .env.example
- Update .idea/.gitignore
- Update .idea/gillm.iml
- Update .idea/inspectionProfiles/Project_Default.xml
- Update .idea/inspectionProfiles/profiles_settings.xml
- Update .idea/modules.xml
- Update .idea/vcs.xml
- Update uv.lock

