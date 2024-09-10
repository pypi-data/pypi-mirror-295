import pywatch.server.main as main
from pywatch.parse_setup import parse_module


def start_webapp(path: str) -> None:
    module_ = parse_module("Setup_Module", path)
    main.setup_mod = module_

    main.app.run()
