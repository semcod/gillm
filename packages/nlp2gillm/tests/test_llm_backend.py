from nlp2gillm.llm_backend import LLMBackend, nl_to_dsl_line


class _FakeBackend:
    def complete(self, *, model, messages, temperature=0.2, response_format=None) -> str:
        return '{"dsl": "HEALTH"}'


def test_nl_to_dsl_line_fake_backend() -> None:
    line = nl_to_dsl_line("check status", backend=_FakeBackend())
    assert line == "HEALTH"
