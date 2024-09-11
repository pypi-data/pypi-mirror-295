import os
import streamlit.components.v1 as components
from typing import Callable, Optional

_RELEASE = True


if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_tree_independent_components",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_tree_independent_components", path=build_dir)


def tree_independent_components(treeItems={},checkItems=[], disable=False, single_select=False, on_change: Optional[Callable[[], None]] = None, y_scroll=False, x_scroll=False, x_scroll_width=60, frameHeight=50, border=False ,key=None):

    component_value = _component_func(treeItems=treeItems,checkItems=checkItems, disable=disable,single_select=single_select, on_change=on_change, y_scroll=y_scroll,x_scroll=x_scroll, default=checkItems, x_scroll_width=x_scroll_width, frameHeight=frameHeight,border=border, key=key)
    if on_change is not None:
        on_change()
    return component_value


