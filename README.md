# gillm


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.1.10-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$1.26-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-5.7h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $1.2638 (8 commits)
- 👤 **Human dev:** ~$575 (5.7h @ $100/h, 30min dedup)

Generated on 2026-06-03 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

## Testing

GUI injection (keyboard backends, xdotool/ydotool/wtype, OS injector profiles) is tested in this package:

```bash
cd gillm
python -m pytest tests/ -q
```

Main modules:

- `tests/test_injector.py` — :class:`gillm.injection.injector.Injector`
- `tests/test_os_injector.py` — calibrated profiles under ``~/.koru/ide-os-injector.json``

Koru keeps integration tests only (daemon wire protocol, IDE shims, CLI). Do not re-add duplicate injector unit tests under ``koru/tests/``.

---

## License

Licensed under Apache-2.0.
