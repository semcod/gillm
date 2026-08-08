# nlp2gillm

Natural language → linia DSL (bez side-effect); opcjonalnie `apply` = [`dsl2gillm.dispatch()`](../dsl2gillm/README.md).

```bash
nlp2gillm to-dsl "check health"
nlp2gillm apply "capture screen"
```

## LLM output contract

The LLM boundary accepts only a complete `DslLineResponse` v1 JSON object.
Its packaged `contracts/v1` bundle contains equivalent GBNF, Protobuf, JSON
Schema and a manifest naming the runtime consumer. The schema is sent through
LiteLLM structured output and applied locally before `dsl2gillm` parses the
command. Markdown, extra fields, unknown verbs and version drift fail closed.

OpenRouter calls use `OPENROUTER_APP_NAME`, falling back to the current project
folder, and optionally attach `OPENROUTER_APP_URL` as the referer.

**See also:** [Control layer](../README.md) · [dsl2gillm](../dsl2gillm/README.md) · [uri2gillm](../uri2gillm/README.md) · [gillm README](../../README.md)
