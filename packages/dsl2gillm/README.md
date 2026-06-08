# dsl2gillm

Grammar DSL + JSON Schema + Protobuf + CQRS bus dla sterowania GUI ([`gillm`](../../README.md)).

```bash
dsl2gillm -c 'HEALTH'
dsl2gillm validate-schema
dsl2gillm codegen
dsl2gillm encode 'HEALTH' --format protobuf
python -m dsl2gillm.codegen
```

Jedyny punkt mutacji: `dsl2gillm.dispatch()`.

**See also:** [Control layer](../README.md) · [uri2gillm](../uri2gillm/README.md) · [nlp2gillm](../nlp2gillm/README.md) · [cli2gillm](../cli2gillm/README.md) · [mcp2gillm](../mcp2gillm/README.md) · [rest2gillm](../rest2gillm/README.md) · [SUMD](../../SUMD.md)
