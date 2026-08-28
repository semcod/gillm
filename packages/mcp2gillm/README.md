# mcp2gillm

MCP stdio server — narzędzia `gillm_run_command`, `gillm_run_dsl`, `gillm_run_command_pb`, `gillm_to_dsl` (delegacja do [`dsl2gillm`](../dsl2gillm/README.md)).

```bash
mcp2gillm serve
```

Live GUI actions are disabled by default. Set `GILLM_MCP_ALLOW_EXECUTE=1` to
allow non-dry-run `EXECUTE`, `FOCUS`, and `INJECT` commands. Screen capture has
a separate `GILLM_MCP_ALLOW_CAPTURE=1` opt-in. Workflow files are confined to
the current directory by default; set `GILLM_MCP_WORKSPACE_ROOT` to choose a
different root.

**See also:** [Control layer](../README.md) · [dsl2gillm](../dsl2gillm/README.md) · [rest2gillm](../rest2gillm/README.md) · [gillm README](../../README.md)
