import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def text_plus_slider(label,
                     key,
                     value=0,
                     min_value=-100,
                     max_value=100,
                     step=1,
                     help_dialog=None,
                     percentage=True,
                     sign=True,
                     suffix=""):
    """
    A custom widget that combines a label, a clickable help icon and a slider.
    """

    st.markdown("""
        <style>
        .small-font {
            font-size:14px !important;
        }
        </style>
        """, unsafe_allow_html=True)

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

    str_format = "%+d" if sign else "%d"
    if percentage:
        str_format += "%%"

    slider_value = st.slider(label,
                             value=value,
                             min_value=min_value,
                             max_value=max_value,
                             step=step,
                             key=key,
                             label_visibility='collapsed',
                             format=str_format + suffix)

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
    