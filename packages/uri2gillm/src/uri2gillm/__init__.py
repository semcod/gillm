"""uri2gillm — gillm:// URI adapter for dsl2gillm."""

from uri2gillm.decode import uri_to_dsl
from uri2gillm.nlp2uri import UriHit, best_uri, nlp2uri
from uri2gillm.run import run_uri
from uri2gillm.uri import is_gillm_uri, parse_gillm_uri, uri_for_block, uri_for_cmd

__all__ = [
    "UriHit",
    "best_uri",
    "is_gillm_uri",
    "nlp2uri",
    "parse_gillm_uri",
    "run_uri",
    "uri_for_block",
    "uri_for_cmd",
    "uri_to_dsl",
]
