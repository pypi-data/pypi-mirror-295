import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

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
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_nivo_sankey", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
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
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(data=data, key=key, default=0)
    return component_value
