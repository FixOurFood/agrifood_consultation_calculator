import streamlit as st
import numpy as np
from streamlit_extras.stylable_container import stylable_container

# @st.fragment
def text_plus_slider(label,
                     key,
                     value=0,
                     min_value=-100,
                     max_value=100,
                     step=1,
                     help_dialog=None,
                     percentage=True,
                     sign=True,
                     suffix="",
                     disabled=False):
    """
    A custom widget that combines a label, a clickable help icon and a slider.
    """

    style = """
        div[data-testid="stSliderTickBarMin"] {
            display: none;
        }
        div[data-testid="stSliderTickBarMax"] {
            display: none;
        }
        [data-testid=stVerticalBlock]{
            gap: 0rem;
        }
    """

    def on_slider_change(key=key):
        st.query_params.pop(key, None)
        st.query_params.pop("sbc", None)

    with stylable_container(key=key+"_container", css_styles=style):
        col1, col2, col3 = st.columns((5, 6, 1), vertical_alignment="bottom")

        with col1:
            st.write(label)
            # if st.button(label, key="help_icon_"+key, type="tertiary"):
            #     if help_dialog is not None:
            #         help_dialog()

        str_format = "%+d" if sign else "%d"
        if percentage:
            str_format += "%%"

        with col2:
            slider_value = st.slider(label,
                                    value=value,
                                    min_value=min_value,
                                    max_value=max_value,
                                    step=step,
                                    key=key,
                                    on_change=on_slider_change,
                                    label_visibility='collapsed',
                                    format=str_format + suffix,
                                    disabled=disabled
                                    )
        @st.fragment
        def help_button():
            if st.button(":material/help:", key="help_icon_"+key, type="tertiary"):
                if help_dialog is not None:
                    help_dialog()

        with col3:
            # if st.button(":material/help:", key="help_icon_"+key, type="tertiary"):
            #     if help_dialog is not None:
            #         help_dialog()
            help_button()

    return slider_value

def text_plus_segment(label,
                      options,
                      default,
                      key,
                      format_func=None,
                      help_dialog=None):
    
    """A custom widget that combines a label, a clickable help icon, and 
    a segmented control selector"""

    # st.markdown("""
    #     <style>
    #     .small-font {
    #         font-size:14px !important;
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1], vertical_alignment="top")
    with col1:
        st.markdown(f'<p class="small-font">{label}</p>', unsafe_allow_html=True)

    with col2:
        with stylable_container(
            key="stylable_container_"+key,
            css_styles="""
            button{
                float: right;
            }
            """
        ):
            if st.button(":information_source:", key="help_icon_"+key, type="tertiary"):
                if help_dialog is not None:
                    help_dialog()

    control_value = st.segmented_control(label=label,
                                         options=options,
                                         default=default,
                                         selection_mode='single',
                                         format_func=format_func,
                                         key=key,
                                         label_visibility='collapsed')

    return control_value

@st.fragment
def nested_sliders(labels,
                   keys,
                   value=0,
                   min_value=0,
                   max_value=100,
                   help_dialog=None,
                   format=None,
                   border=False
                   ):
    
    """Creates a slider with nested sliders inside. The main slider controls theç
    values of the nested sliders. 
    
    Parameters
        ----------
        labels : str or list of str
            Labels for the sliders. First label is for the main slider,
            subsequent labels are for nested sliders shown when checkbox is
            checked
        output_keys : str or list of str
            Keys for the output values of the nested sliders
        key : str
            Key for the widget and prefix for widget components
        value : int or float, optional
            Initial value for all sliders, by default 0
        min_value : int or float, optional
            Minimum value for all sliders, by default 0
        max_value : int or float, optional
            Maximum value for all sliders, by default 100
        help_dialog : function, optional
            Function that displays a help dialog, by default None
        format : str, optional
            Format string for the slider values, by default None
        border : bool, optional
            Whether to show a border around the widget, by default False

        Returns
        -------
        list
            Returns list of values for all sliders, repeating the value of the
            first slider for all other sliders if checkbox is not checked.
    
    """

    # Function to update parent slider from child sliders changes
    def update_from_child():
        vals = [st.session_state[keys[0]+"_slider_"+str(i+1)] for i in range(len(labels[1:]))]
        for k, val in zip(keys[1:], vals):
            st.session_state[k] = val
        st.session_state[keys[0]+"_slider_0"] = int(np.average(vals))
        st.session_state[keys[0]] = int(np.average(vals))
        st.session_state[keys[0]+"_last_interact"] = "child"
        st.session_state[keys[0]+"_rerun"] = True

    # Function to update child sliders from parent slider changes
    def update_from_parent():
        st.session_state[keys[0]+"_last_interact"] = "parent"
        for k in keys[1:]:
            st.session_state[k] = st.session_state[keys[0]+"_slider_0"]
        st.session_state[keys[0]] = st.session_state[keys[0]+"_slider_0"]
        st.session_state[keys[0]+"_rerun"] = True

    style = """
        div[data-testid="stSliderTickBarMin"] {
            display: none;
        }
        div[data-testid="stSliderTickBarMax"] {
            display: none;
        }
        [data-testid=stVerticalBlock]{
            gap: 0.5rem;
        }
    """

    # Convert labels to list if it is a string
    if np.isscalar(labels):
        labels = [labels]

    if np.isscalar(keys):
        keys = [keys]

    # Initialize values
    if keys[0]+"_is_open" not in st.session_state:
        st.session_state[keys[0]+"_is_open"] = False

    if keys[0]+"_last_interact" not in st.session_state:
        st.session_state[keys[0]+"_last_interact"] = "parent"

    for k in keys[1:]:
        if k not in st.session_state:
            st.session_state[k] = value

    if keys[0] not in st.session_state:
        st.session_state[keys[0]] = value

    if keys[0]+"_rerun" not in st.session_state:
        st.session_state[keys[0]+"_rerun"] = False

    if st.session_state[keys[0]+"_rerun"]:
        st.session_state[keys[0]+"_rerun"] = False
        st.rerun(scope="app")

    value_main = st.session_state[keys[0]]

    if st.session_state[keys[0]+"_is_open"]:
        icon = ":material/chevron_right:"
    else:
        icon = ":material/keyboard_arrow_down:"


    col_ratio = (0.5,5,6)
    with st.container(border=border):
        with stylable_container(key=keys[0]+"_container", css_styles=style):
            cols = st.columns(col_ratio, vertical_alignment="center")

            # Main slider
            with cols[2]:
                st.slider(labels[0],
                    min_value=min_value,
                    max_value=max_value,
                    value=int(value_main),
                    # disabled=st.session_state[key+"_is_open"],
                    label_visibility='collapsed',
                    key=keys[0]+"_slider_0",
                    on_change=update_from_parent,
                    format=format,
                    step=1
                    )
                
            # Expand/Collapse icon button
            with cols[0]:
                if len(labels) > 1:
                    if st.button(
                        label=icon,
                        type="tertiary",
                        key=keys[0]+"_opener_button"):
                        
                        st.session_state[keys[0]+"_is_open"] = not st.session_state[keys[0]+"_is_open"]
                        st.rerun(scope="fragment")

            # Slider label
            with cols[1]:
                if st.button(label=labels[0],
                             key=keys[0]+"_help_button",
                             type="tertiary"):
                    if help_dialog is not None:
                        help_dialog()

            # # Help dialog icon button
            # with cols[3]:
            #     if st.button(":information_source:",
            #                 key=keys[0]+"_help_button",
            #                 type="tertiary"):
            #         if help_dialog is not None:
            #             help_dialog()
        
            # Nested sliders
            with st.empty():
                with st.container():
                    for i, label in enumerate(labels[1:]):

                        cols_nested = st.columns(col_ratio, vertical_alignment="bottom")

                        with cols_nested[1]:
                            st.caption(labels[i+1])
                        
                        with cols_nested[2]:
                            if st.session_state[keys[0]+"_last_interact"] == "parent":
                                init_val = st.session_state[keys[0]+"_slider_0"]
                            else:
                                init_val = st.session_state[keys[i+1]]

                            st.slider(
                                label,
                                min_value=min_value,
                                max_value=max_value,
                                value=int(init_val),
                                label_visibility='collapsed',
                                key=keys[0]+"_slider_"+str(i+1),
                                on_change=update_from_child,
                                format=format,
                                step=1
                                )
                        
                if not st.session_state[keys[0]+"_is_open"]:
                    st.empty()
           
def selectbox_plus_icon(label,
                        options,
                        default,
                        key,
                        format_func=None,
                        help_dialog=None):
    
    """A custom widget that combines a selectbox and a clickable help icon"""

    col1, col2 = st.columns([6, 1], vertical_alignment="bottom")
    with col1:
        if format_func is not None:
            value = st.selectbox(
                label,
                options,
                index=options.index(default),
                format_func=format_func,
                key=key
            )
        else:
            value = st.selectbox(
                label,
                options,
                index=options.index(default),
                key=key
        )

    with col2:
        if st.button(":material/help:", key="help_icon_"+key, type="tertiary", use_container_width=True):
            if help_dialog is not None:
                help_dialog()


    return value

@st.fragment
def collapsable_text(
        text,
        key
):
    
    # Initialize values
    if key+"_is_open" not in st.session_state:
        st.session_state[key+"_is_open"] = True

    if st.session_state[key+"_is_open"]:
        button_label = "Show less"
        display_text = text

    else:
        button_label = "Show more"
        if text.startswith("**"):
            display_text = " ".join(text.split()[:10]) + "**..."
        else:
            display_text = " ".join(text.split()[:10]) + "..."

    st.caption(display_text)

    if st.button(
        label=button_label,
        type="tertiary",
        key=key+"_opener_button"):

        st.session_state[key+"_is_open"] = not st.session_state[key+"_is_open"]
        st.rerun(scope="fragment")

