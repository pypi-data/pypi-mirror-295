# Zeta Mission Control

Simple library that helps connect to Zeta Technologies Mission Control app.

## Usage

To make a connection use `zmc.connect()` as either a context manager or a
decorator:

As a context manager:

```
import zmc

with zmc.connect():
    do_something()  # will execute while connection is established.
```

As a decorator:

```
import zmc

@zmc.connect()
def do_something():
    ...  # user implementation

do_something()  # will execute while connection is established.
```

Any code run within the context manager or decorator will only start running
once a connection is established. (see below on how to run code to ensure a
connection is made)

### Interacting with app

The library enables easily sending and receiving data from the app via
"components" found in `zmc.components`.

#### Sending data

Sending data is accomplished by calling specific functions on the components:

```
import zmc

graph = zmc.components.Graph("graphId")

with zmc.connect():
    # Update graph on GUI to show these three points.
    graph.plot(x=[0, 1, 2], y=[5, 6, 7])
```

#### Using values set in the GUI

To receive values that are set from the GUI, you can access the corresponding
component attributes as you would any other attribute or variable. When a change
is made on the GUI, the value will automatically be changed.

```
import zmc

slider = zmc.components.Slider("sliderId")

with zmc.connect():
    while True:
        if slider.value > 5:
            break  # Break once slider is changed above 5 on the GUI.
```

### Running code

A python script using the `zmc` library should not be run directly from the
terminal. Instead, it should be run through the app (so that the app can
establish its own side of the connection). If you do run it directly, you will
get a timeout stating that the connection could not be established

To run for debugging purposes, use `zmc.connect(debug=True)` which will mock out
the connection and allow you to run the rest of your code as normal. Add `verbose=True` for more logging.
