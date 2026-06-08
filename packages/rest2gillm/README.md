# rest2gillm

REST API (FastAPI) — `POST /v1/dsl`, port **8220** (delegacja do [`dsl2gillm`](../dsl2gillm/README.md)).

```bash
rest2gillm serve --port 8220
curl -X POST http://127.0.0.1:8220/v1/dsl -d 'HEALTH'
```

**See also:** [Control layer](../README.md) · [dsl2gillm](../dsl2gillm/README.md) · [mcp2gillm](../mcp2gillm/README.md) · [gillm README](../../README.md#rest-api)
