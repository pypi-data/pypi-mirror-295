import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit_nivo_sankey",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_nivo_sankey", path=build_dir)


def st_nivo_sankey(data: dict,
                   height : str="400px",
                   width : str="100%",
                   use_container_width=False,
                   key=None):
    """Creates a Nivo Sankey diagram component.

    Args:
        data (dict): The data to be displayed in the Sankey diagram.
        height (str, optional): The height of the component. Defaults to "400px".
        width (str, optional): The width of the component. Defaults to "100%".
        use_container_width (bool, optional): Whether to use the full width of the container. Defaults to False.
        key (str, optional): An optional key that uniquely identifies this component. Defaults to None.

    Returns:
        Any: The value of the component after user interaction.

    Example:
        >>> import streamlit as st
        >>> from streamlit_nivo_sankey import st_nivo_sankey
        >>> 
        >>> data = {
        ...     "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
        ...     "links": [{"source": "A", "target": "B", "value": 10},
        ...               {"source": "B", "target": "C", "value": 5}]
        ... }
        >>> 
        >>> value = st_nivo_sankey(data=data, height="500px", use_container_width=True)
        >>> st.write(value)
    """
    custom_colors = None
    if len(data["nodes"]) <= 0:
        raise ValueError("data should have at least one node")
    else:
        sample_node = data["nodes"][0]
        if "nodeColor" in sample_node:
            custom_colors = [node["nodeColor"] for node in data["nodes"]]

    component_value = _component_func(data=data, 
                                      key=key, 
                                      custom_colors=custom_colors, 
                                      default=None)
    return component_value
