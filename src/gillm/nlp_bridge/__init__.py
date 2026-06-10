"""NLP translation bridge using nlp2dsl."""

from gillm.nlp_bridge.client import NLPBridgeClient
from gillm.nlp_bridge.heuristic_parser import parse_intent_heuristic

__all__ = ["NLPBridgeClient", "parse_intent_heuristic"]
