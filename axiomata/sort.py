import os
import random
import sys
import time
from enum import Enum

MAX_ELEMENTS = 10
BAR_HEIGHT = 10

_ansi_ready = False


class Type(Enum):
    BUBBLE = "bubble"
    SELECTION = "selection"
    INSERTION = "insertion"


class Animation(Enum):
    ANSI = "ansi"
    MATPLOTLIB = "matplotlib"


def _prepare(count, array):
    if array is not None:
        values = list(array)
        if len(values) > MAX_ELEMENTS:
            raise ValueError(f"array must have at most {MAX_ELEMENTS} elements for now")
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
            raise ValueError("array must contain only numbers")
        if len(set(values)) != len(values):
            raise ValueError("array must contain distinct numbers")
        return values

    if count > MAX_ELEMENTS:
        raise ValueError(f"array count must be at most {MAX_ELEMENTS} for now")

    return random.sample(range(1, count * 10 + 1), count)


def _bubble_frames(values):
    values = list(values)
    n = len(values)
    yield list(values), ()
    for i in range(n):
        for j in range(n - i - 1):
            yield list(values), (j, j + 1)
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
                yield list(values), (j, j + 1)


def _selection_frames(values):
    values = list(values)
    n = len(values)
    yield list(values), ()
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            yield list(values), (min_index, j)
            if values[j] < values[min_index]:
                min_index = j
        values[i], values[min_index] = values[min_index], values[i]
        yield list(values), (i, min_index)


def _insertion_frames(values):
    values = list(values)
    yield list(values), ()
    for i in range(1, len(values)):
        key = values[i]
        j = i - 1
        while j >= 0 and values[j] > key:
            yield list(values), (j, j + 1)
            values[j + 1] = values[j]
            j -= 1
        values[j + 1] = key
        yield list(values), (j + 1,)


_FRAME_FUNCTIONS = {
    Type.BUBBLE: _bubble_frames,
    Type.SELECTION: _selection_frames,
    Type.INSERTION: _insertion_frames,
}


def _label(index, total):
    if index == 0:
        return "Before"
    if index == total - 1:
        return "After"
    return f"Step {index}/{total - 1}"


def _ensure_ansi_enabled():
    global _ansi_ready
    if _ansi_ready:
        return
    if os.name == "nt":
        os.system("")  # enables ANSI escape processing on legacy Windows consoles
    _ansi_ready = True


def _render_frame(values, active, width, label):
    max_value = max(values)
    heights = [max(1, round(v / max_value * BAR_HEIGHT)) for v in values]

    rows = [label]
    for row in range(BAR_HEIGHT, 0, -1):
        cells = []
        for i, h in enumerate(heights):
            bar = ("#" * width) if h >= row else (" " * width)
            if i in active and h >= row:
                bar = f"\033[7m{bar}\033[0m"
            cells.append(bar)
        rows.append(" ".join(cells))

    rows.append(" ".join(f"{v:>{width}}" for v in values))
    return "\n".join(rows)


def _play_ansi(frames, delay):
    _ensure_ansi_enabled()

    total = len(frames)
    first = True

    for index, (values, active) in enumerate(frames):
        width = max(3, max(len(str(v)) for v in values) + 1)
        frame_text = _render_frame(values, active, width, _label(index, total))

        if not first:
            sys.stdout.write(f"\033[{frame_text.count(chr(10)) + 1}F")
        sys.stdout.write(frame_text + "\n")
        sys.stdout.flush()

        first = False
        time.sleep(delay)

    return frames[-1][0]


def _in_notebook():
    try:
        from IPython import get_ipython
    except ImportError:
        return False
    shell = get_ipython()
    return shell is not None and shell.__class__.__name__ == "ZMQInteractiveShell"


def _play_matplotlib(frames, delay):
    import matplotlib.pyplot as plt

    in_notebook = _in_notebook()
    if in_notebook:
        from IPython.display import display, clear_output

    total = len(frames)
    fig, ax = plt.subplots()
    interactive = fig.canvas.required_interactive_framework is not None

    if not in_notebook and interactive:
        plt.ion()
        fig.show()

    for index, (values, active) in enumerate(frames):
        ax.clear()
        colors = ["#ff7f0e" if i in active else "#1f77b4" for i in range(len(values))]
        bars = ax.bar(range(len(values)), values, color=colors)
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(v), ha="center", va="bottom")
        ax.set_title(_label(index, total))
        ax.set_xticks([])
        ax.set_ylim(0, max(values) * 1.15)

        if in_notebook:
            clear_output(wait=True)
            display(fig)
        elif interactive:
            fig.canvas.draw_idle()
            fig.canvas.flush_events()
        else:
            fig.canvas.draw()

        time.sleep(delay)

    plt.close(fig)
    return frames[-1][0]


class Sort:
    def __init__(self, algorithm):
        self._algorithm = algorithm
        self._array = None
        self._count = MAX_ELEMENTS
        self._delay = 1
        self._values = None

    def array(self, values=None):
        self._values = None
        if values is None:
            self._array = None
            self._count = MAX_ELEMENTS
        elif isinstance(values, int) and not isinstance(values, bool):
            self._array = None
            self._count = values
        else:
            self._array = list(values)
        return self

    def delay(self, seconds):
        self._delay = seconds
        return self

    def _start(self):
        if self._values is None:
            self._values = _prepare(self._count, self._array)
        return list(self._values)

    def run(self):
        frames = list(_FRAME_FUNCTIONS[self._algorithm](self._start()))
        before, _active = frames[0]
        after, _active = frames[-1]

        width = max(3, max(len(str(v)) for v in before) + 1)
        print(_render_frame(before, (), width, "Before"))
        print()
        print(_render_frame(after, (), width, "After"))

        return after

    def animate(self, animation=Animation.ANSI):
        frames = list(_FRAME_FUNCTIONS[self._algorithm](self._start()))

        if animation is Animation.ANSI:
            return _play_ansi(frames, self._delay)

        if animation is Animation.MATPLOTLIB:
            return _play_matplotlib(frames, self._delay)

        raise ValueError(
            f"animation must be Animation.ANSI or Animation.MATPLOTLIB, got {animation!r}; "
            "use .run() for a quiet, non-animated result"
        )
