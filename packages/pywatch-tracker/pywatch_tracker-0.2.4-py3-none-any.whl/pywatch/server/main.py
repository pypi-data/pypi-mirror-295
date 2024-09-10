import typing
from types import ModuleType
import pathlib
from quart import Quart, render_template, websocket

from .detector_logic_calculation import *
from ..readout import DetectorPool, EventData, PoolThread
from .simulation import SimulationPool


setup_mod: typing.Optional[ModuleType] = None
app = Quart(__name__, template_folder="../dist/", static_folder="../dist/assets")

detectors = []


@app.route("/")
async def main():
    if setup_mod is None:
        raise RuntimeError("Setup Script was not set")
    return await render_template("index.html")


@app.websocket("/measurement")
async def ws():
    if setup_mod.EVENT_COUNT is not None:
        await websocket.send_json({
            "type" : "event_count",
            "count": setup_mod.EVENT_COUNT,
        })
    while True:
        data = (await websocket.receive_json())["data"]
        if data["type"] == "start":
            print("start measurement")
            event_count = data["eventCount"]

            async def callback(event: EventData, thread: PoolThread):
                amp = sum([hit_data.amplitude for hit_data in event.values()]) / len(event)

                msg: dict = {
                    "type": "event",
                    "data": event.to_dict(),
                    "amp": amp,
                }

                await websocket.send_json(msg)

            if len(detectors) is None:
                print("No Detector geometry was given. Try Again")
                continue

            if setup_mod.SIMULATION:
                pool = SimulationPool(detectors, 1, 0.1)
                await pool.async_run(event_count, callback)
            else:
                pool = DetectorPool(*setup_mod.PORTS, threshold=setup_mod.THRESHOLD)
                await pool.async_run(event_count, callback)
        else:
            continue


@app.websocket("/logic")
async def ws_logic():
    global detectors

    if setup_mod.GEOMETRY_FILE is not None:
        detectors, coin = load_from_json(setup_mod.SEGMENTATION, setup_mod.GEOMETRY_FILE)
        with open(setup_mod.GEOMETRY_FILE, "r") as f:
            file_output = f.read()
        await websocket.send_json(coin.to_dict("mean"))
        await websocket.send_json({
            "type": "detectors",
            "file": file_output,
        })
        print("logic send")

    while True:
        data = await websocket.receive_json()
        # TODO load rotation
        for d in data:
            position = Vector(*d["position"].values())
            rot_values = [0, 0, 0, "XYZ"]
            v = d.get("rotation")
            if v is not None:
                rot_values = list(v.values())[1:]

            detectors.append(Detector(setup_mod.SEGMENTATION, position, (rot_values[-1], Vector(*rot_values[:-1]))))

        coin = calculate_coincidences(detectors)
        await websocket.send_json(coin.to_dict("mean"))
        print("logic send")

        # pprint(detectors)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True)
