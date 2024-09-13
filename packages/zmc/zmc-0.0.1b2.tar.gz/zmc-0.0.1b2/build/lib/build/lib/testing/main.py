"""Test main file"""

import zmc

print(dir(zmc))

# try:
#     zmc.connect
# except:
#     print("no connect")

try:
    zmc.components
except Exception:
    print("no components")


# a = zmc.components.SingleBooleanComponent("asdf")
# b = zmc.components.button_component.ButtonComponent("d")
# c = zmc.components.BADTHING("d")
