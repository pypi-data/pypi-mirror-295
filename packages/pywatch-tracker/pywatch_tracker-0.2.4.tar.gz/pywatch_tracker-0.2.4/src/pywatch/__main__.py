import sys

from .readout.measurement import measurement_from_script
from .readout.port_access import input_ports_from_commandline
from .server import start_webapp


if len(sys.argv) > 1:
    if sys.argv[1] == "--measurement":
        path = sys.argv[2]
        measurement_from_script(path)
    elif sys.argv[1] == "--webapp":
        path = sys.argv[2]
        start_webapp(path)
    elif sys.argv[1] == "--set-ports":
        input_ports_from_commandline()
