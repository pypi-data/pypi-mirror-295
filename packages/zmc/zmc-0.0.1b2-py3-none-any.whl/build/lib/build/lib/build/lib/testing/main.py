"""Test main file"""

import time

import zmc

# print("zmc", dir(zmc))
# print()
# print("zmc.components", dir(zmc.components))
# print()
# print("zmc.components.core", dir(zmc.components.core))

graph = zmc.components.Graph("sdf")

with zmc.connect(debug=True, verbose=False):
    for i in range(1, 50 + 1):
        graph.plot([0] * i, [0] * i)
        print(i)
        time.sleep(0.01)


# print("websockets", dir(websockets))
# websockets.framing
# print("websockets", dir(websockets))


# try:
#     zmc.connect
# except:
#     print("no connect")

# try:
#     zmc.components
# except Exception:
#     print("no components")


# a = zmc.components.SingleBooleanComponent("asdf")
# b = zmc.components.button_component.ButtonComponent("d")
# c = zmc.components.BADTHING("d")


# base -> receiver / registry -> websocket -> connector_context -> sender
