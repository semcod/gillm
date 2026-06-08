"""NL → gillm:// URI hits (minimal offline heuristics)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from uri2gillm.uri import uri_for_block, uri_for_cmd


@dataclass
class UriHit:
    uri: str
    dsl: str
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {"uri": self.uri, "dsl": self.dsl, "confidence": self.confidence}


def nlp2uri(prompt: str, *, file: str | None = None) -> list[UriHit]:
    text = prompt.strip().lower()
    hits: list[UriHit] = []
    workflow_file = file or "workflow.json"

    if any(word in text for word in ("health", "status", "alive")):
        dsl = "HEALTH"
        hits.append(UriHit(uri=uri_for_cmd("HEALTH"), dsl=dsl, confidence=0.9))
    if any(word in text for word in ("orient", "environment", "display")):
        dsl = "ORIENT"
        hits.append(UriHit(uri=uri_for_cmd("ORIENT"), dsl=dsl, confidence=0.85))
    if any(word in text for word in ("capture", "screenshot", "screen")):
        dsl = "CAPTURE"
        hits.append(UriHit(uri=uri_for_cmd("CAPTURE"), dsl=dsl, confidence=0.9))
    if "focus" in text and "type" in text:
        dsl = f'PARSE "{prompt.strip()}"'
        hits.append(UriHit(uri=uri_for_cmd("PARSE", instruction=prompt.strip()), dsl=dsl, confidence=0.8))
        hits.append(
            UriHit(
                uri=uri_for_block("workflow", "execute", file=workflow_file),
                dsl=f"EXECUTE FILE {workflow_file}",
                confidence=0.6,
            ),
        )
    if "validate" in text and file:
        dsl = f"VALIDATE FILE {file}"
        hits.append(UriHit(uri=uri_for_cmd("VALIDATE", file=file), dsl=dsl, confidence=0.85))

    return sorted(hits, key=lambda h: h.confidence, reverse=True)


def best_uri(prompt: str, *, file: str | None = None) -> UriHit | None:
    hits = nlp2uri(prompt, file=file)
    return hits[0] if hits else None
