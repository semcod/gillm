def test_create_server() -> None:
    from mcp2gillm.server import create_server

    server = create_server()
    assert server.name == "gillm"
