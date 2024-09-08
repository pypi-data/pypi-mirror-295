# streamlit-nivo-sankey
[![Build and Publish](https://github.com/Navxihziq/streamlit-nivo-sankey/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Navxihziq/streamlit-nivo-sankey/actions/workflows/python-publish.yml)

This is a Streamlit component that lets you create Nivo Sankey diagrams. Please check out Nivo's amazing page on [Sankey](https://nivo.rocks/sankey/) for more information.

This project is still in early development. More granular control, testing, and documentation, and development guide will come soon. Stay tuned!

## Installation instructions

```sh
pip install streamlit-nivo-sankey
```

## Basic Usage Example

```python
import streamlit as st

from streamlit_nivo_sankey import st_nivo_sankey

data = {
    "nodes": [
        {"id": "a", "nodeColor": "hsl(160, 70%, 50%)"},
        {"id": "b", "nodeColor": "hsl(160, 70%, 50%)"},
        {"id": "c", "nodeColor": "hsl(160, 70%, 50%)"},
    ],
    "links": [
        {"source": "a", "target": "b", "value": 1},
        {"source": "a", "target": "c", "value": 5},
    ]
}
value = st_nivo_sankey(data)    # returns clicked node/link and value
```

![image](./assets/demo-1.png)
