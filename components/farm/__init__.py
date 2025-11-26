import streamlit.components.v1 as components

from pathlib import Path

parent_dir = Path(__file__).resolve().parent

_farm_component = components.declare_component(
    "farm_component",
    # url="http://localhost:5173/",
    path=parent_dir / "build",
)


def farm_component(data):
    return _farm_component(data=data)
