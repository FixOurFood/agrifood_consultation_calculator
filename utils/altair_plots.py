import altair as alt
import xarray as xr
import numpy as np
import pandas as pd
import streamlit as st
from glossary import *

import base64
from io import BytesIO
from PIL import Image

def plot_years_altair(food, show="Item", ylabel=None, colors=None, ymin=None, ymax=None):
    """Plots a stacked area chart for the given xarray dataarray using altair.

    Parameters
    ----------

    food : xarray.DataArray
        The dataarray to be plotted. The dataarray must have a 'Year' dimension.
    show : str
        The coordinate name to use to dissagregate the vertical chart stack.
    ylabel : str
        The label for the y-axis. Default is None.
    colors : list
        The list of colors to assign to each of the vertical stacks.
    ymin, ymax : float
        The minimum and maximum values for the y-axis. If not provided, the
        minimum and maximum values of the dataarray will be used.
    """

    # If no years are found in the dimensions, raise an exception
    sum_dims = list(food.coords)
    if "Year" not in sum_dims:
        raise TypeError("'Year' dimension not found in array data")

    # Set yaxis limits
    if ymax is None:
        ymax = food.sum(dim="Item").max().item()
    if ymin is None:
        ymin = food.sum(dim="Item").min().item()
        if ymin > 0: ymin = 0

    # Create dataframe for altair
    df = food.to_dataframe().reset_index().fillna(0)
    df = df.melt(id_vars=sum_dims, value_vars=food.name)

#     selection = alt.selection_multi(fields=[show])
    selection = alt.selection_point(on='mouseover')

    if colors is None:
        color_scale = alt.Scale(scheme='category20b')
    else:
        show_list = np.unique(food[show].values)
        color_scale = alt.Scale(domain=show_list, range=colors)

    # Create altair chart
    c = alt.Chart(df).mark_area().encode(
            x=alt.X('Year:O', axis=alt.Axis(values = np.linspace(2020, 2050, 5))),
            y=alt.Y('sum(value):Q', axis=alt.Axis(format="~s", title=ylabel, ), scale=alt.Scale(domain=[ymin, ymax])),
            # color=alt.Color(f'{show}:N', scale=alt.Scale(scheme='category20b')),
            color=alt.Color(f'{show}:N', scale=color_scale),
            # opacity=alt.condition(selection, alt.value(0.5), alt.value(0.8)),
            tooltip=[alt.Tooltip(f'{show}:N', title=show.replace("_", " ")),
                     alt.Tooltip('Year'),
                     alt.Tooltip('sum(value)', title='Total', format=".2f")],
            ).add_params(selection).properties(height=550)
    
    return c

def plot_years_total(food, ylabel=None, sumdim=None, color="red", yrange=None):
    """
    Plots the total values over years from the given food dataset using Altair.

    Parameters
    ----------
    food : xarray.DataArray 
        The dataset containing food data with 'Year' as one of the dimensions.
    ylabel : str, optional
        The label for the y-axis.
    sumdim : str, optional
        The dimension to sum over.
    color : str, optional
        The color of the line in the plot.
    yrange: list, optional
        The range for the y-axis. If None, it is set to
        [0, max value of the total].
    
    Returns
    -------
        alt.Chart: An Altair chart object representing the plot.
    """

    years = food.Year.values
    if sumdim is not None and sumdim in food.dims:
        total = food.sum(dim="Item")
    else:
        total = food
    
    if yrange is None:
        yrange = [0, float(total.max().values)]

    scale = alt.Scale(domain=[yrange[0], yrange[1]])
    y_ax = alt.Y('sum(value):Q', axis=alt.Axis(format="~s", title=ylabel), scale=scale)

    df = pd.DataFrame(data={"Year":years, "value":total})
    c = alt.Chart(df).encode(
        alt.X('Year:O', axis=alt.Axis(values = np.linspace(2020, 2050, 5))),
        y_ax
    ).mark_line(color=color).properties(height=550)

    return c

def plot_bars_altair(food, show="Item", x_axis_title='', xlimit=None, labels=None, colors=None):
    """
    Creates a horizontal stacked bar chart using Altair to visualize various
    food balance sheet quantities.
    Parameters:

    -----------
    food : xarray.Dataset
        The food balance sheet dataset.
    show : str, optional
        The coordinate to use to dissagregate quantities into the bars.
    x_axis_title : str, optional
        The title for the x-axis.
    xlimit : float, optional
        The upper limit for the x-axis. If None, the limit is determined by the data.
    labels : list, optional
        A list of labels for the bars.
    colors : list, optional
        A list of colors for the bars.

    Returns:
    --------
    alt.Chart
        An Altair Chart object representing the stacked bar chart.
    """

    n_origins = len(food.Item.values)

    df = food.to_dataframe().reset_index().fillna(0)
    df = df.melt(id_vars=show, value_vars=["production", "imports", "exports", "stock", "losses", "processing", "other", "feed", "seed", "food"])
    df["value_start"] = 0.
    df["value_end"] = 0.

    df["Item"] = df["Item"].replace("Vegetal Products", "Plant Products")
    df["Item"] = df["Item"].replace("Alternative Food", "Alternative Products")
    
    if n_origins > 1:
        for i in range(2*n_origins,10*n_origins):
            if i % n_origins==0:
                temp = df.iloc[i].copy()
                df.iloc[i] = df.iloc[i+1]
                df.iloc[i+1] = temp
            else:
                pass

    cumul = 0
    for i in range(2*n_origins):
        df.loc[i, "value_start"] = cumul
        cumul += df.loc[i, "value"]
        df.loc[i, "value_end"] = cumul

    max_cumul = cumul

    cumul = 0
    for i in reversed(range(2*n_origins,10*n_origins)):
        df.loc[i, "value_start"] = cumul
        cumul += df.loc[i, "value"]
        df.loc[i, "value_end"] = cumul

    source = df

    selection = alt.selection_point(on='mouseover')

    default_items = ["Animal Products", "Alternative Products", "Plant Products"]
    default_colors = ["red", "blue", "green"]
    
    if all(item in df["Item"].unique() for item in default_items):
        color_encoding = alt.Color('Item', scale=alt.Scale(domain=default_items, range=default_colors))
    else:
        color_encoding = alt.Color('Item', scale=alt.Scale(scheme='category20b'))

    if xlimit is not None:
        scale=alt.Scale(domain=(0, xlimit))
    else:
        scale=alt.Scale(domain=(0, max_cumul))

    c = alt.Chart(source).mark_bar().encode(
        y = alt.Y('variable', sort=None, axis=alt.Axis(title='')),
        x2 ='value_start:Q',
        x = alt.X('value_end:Q', scale=scale, axis=alt.Axis(title=x_axis_title)),
        color=color_encoding,
        opacity=alt.condition(selection, alt.value(0.9), alt.value(0.5)),
        tooltip=['Item:N', 'value:Q'],
        ).add_params(selection).properties(height=500)

    return c

def plot_land_altair(land):
    """Creates an Altair chart from a land DataArray

    Parameters
    ----------
    land : xarray.DataArray        
        The land use dataarray to be plotted.
    """

    df = land.to_dataframe().reset_index()
    df = df.melt(id_vars = ['x', 'y'], value_vars = 'grade')
    c = alt.Chart(df).mark_rect().encode(
        x=alt.X('x:O', axis=None),
        y=alt.Y('y:O', scale=alt.Scale(reverse=True), axis=None),
        color='value:Q',
        tooltip='value',
        ).properties(width=300, height=500)

    return c

def plot_single_bar_altair(da, show="Item", axis_title=None,
                                    ax_min=None, ax_max=None, unit="",
                                    vertical=True, mark_total=False,
                                    bar_width=80, show_zero=False,
                                    ax_ticks=False, color=None, legend=False,
                                    reference=None):
    
    """Creates a single bar chart using Altair to visualize the given dataarray.

    Parameters
    ----------
    da : xarray.DataArray
        The dataarray to be plotted.
    show : str, optional
        The coordinate to use to dissagregate the bars.
    axis_title : str, optional
        The title for the x or y axis.
    ax_min, ax_max : float, optional
        The minimum and maximum values for the y or x axis.
    unit : str, optional
        The units of the quantity to be displayed in the tooltip.
    vertical : bool, optional
        If True, the chart is vertical, otherwise it is horizontal.
    mark_total : bool, optional
        If True, a marker for the total value is added to the chart.
    bar_width : int, optional
        The width of the bars in the chart.
    show_zero : bool, optional
        If True, a marker for the zero value is added to the chart.
    ax_ticks : bool, optional
        If True, the axis ticks are displayed.
    color : dict, optional
        A dictionary mapping the show values to colors.
    legend : bool, optional
        If True, a legend is displayed.
    reference : float, optional
        A reference value to add to the chart.

    Returns
    -------
    alt.Chart
        An Altair chart object representing the single bar chart
    """
    
    df_pos = da.where(da>0).to_dataframe().reset_index().fillna(0)
    df_neg = da.where(da<0).to_dataframe().reset_index().fillna(0)

    df_pos = df_pos.melt(id_vars=show, value_vars=da.name)
    df_neg = df_neg.melt(id_vars=show, value_vars=da.name)
    
    # Create a new column for the tooltip with units
    df_pos['value_with_unit'] = df_pos['value'].apply(lambda x: f"{x:.2f} {unit}")
    df_pos['order'] = np.arange(len(da[show].values))
    df_neg['value_with_unit'] = df_neg['value'].apply(lambda x: f"{x:.2f} {unit}")
    df_neg['order'] = np.arange(len(da[show].values))

    for df in [df_pos, df_neg]:
        df[show] = df[show].replace("Vegetal Products", "Plant Products")
        df[show] = df[show].replace("Cukltured Product", "Alternative Products")

    # Set yaxis limits
    if ax_max is None:
        ax_max = da.where(da>0).sum(dim=show).max().item()
    if ax_min is None:
        ax_min = np.min([da.where(da<0).sum(dim=show).min().item(), 0])

    if vertical:
        chart_params = {"y":alt.Y('sum(value):Q',
                            title=axis_title,
                            axis=alt.Axis(labels=ax_ticks),
                            scale=alt.Scale(domain=(ax_min, ax_max))),
                        "x":alt.X('variable', axis=alt.Axis(labels=False, title=None))}
        icon_params = {"y": "total", "x": "variable"}
    else:
        chart_params = {"x":alt.X('sum(value):Q',
                            title=axis_title,
                            axis=alt.Axis(labels=ax_ticks),
                            scale=alt.Scale(domain=(ax_min, ax_max))),
                        "y":alt.Y('variable', axis=alt.Axis(labels=False, title=None))}
        icon_params = {"x": "total", "y": "variable"}

    if color is None:
        if legend:
            alt_color = alt.Color(show, title=None, scale=alt.Scale(scheme='category20b'),
                                  sort=list(reversed(df_pos[show].values)))
        else:
            alt_color = alt.Color(show, title=None, legend=None, scale=alt.Scale(scheme='category20b'))
    
    else:
        if legend:
            alt_color = alt.Color(show, title=None, scale=alt.Scale(domain=color.keys(),
                                  range=color.values()), sort=list(reversed(df_pos[show].values)))
        else:
            alt_color = alt.Color(show, title=None, legend=None, scale=alt.Scale(domain=color.keys(),
                                          range=color.values()))

    # Plot positive values
    c = alt.Chart(df_pos).mark_bar().encode(
        **chart_params,
        color=alt_color,
        tooltip=[alt.Tooltip(f'{show}:N'),
                 alt.Tooltip('value_with_unit:N', title='Total')],
        order=alt.Order(f'order:N', sort='ascending')
    )

    # Plot negative values
    c += alt.Chart(df_neg).mark_bar().encode(
        **chart_params,
        color=alt_color,
        tooltip=[alt.Tooltip(f'{show}:N'),
                 alt.Tooltip('value_with_unit:N', title='Total')],
        order=alt.Order(f'order:N', sort='ascending')
    )

    # Add a line for arbitrary reference
    zero_line_params = {"y": "value"} if vertical else {"x": "value"}
    if reference is not None:
        c += alt.Chart(pd.DataFrame({
            'value': reference,
            'color': ['black']
            })).mark_rule(
                color="black",
                thickness=1,
            ).encode(
                **zero_line_params,
                tooltip=[alt.Tooltip('value:Q', title='Reference')]
        )

    # Add a marker for the total
    if mark_total == True:

        img_path = "images/rhomboid.png"
        pil_image = Image.open(img_path)
        output = BytesIO()
        pil_image.save(output, format='PNG')

        base64_img = "data:image/png;base64," + base64.b64encode(output.getvalue()).decode()

        total = da.sum(dim=show).item()
        source = pd.DataFrame.from_records([
            {"variable": da.name, "total": total, "total_with_unit": f"{total:.2f} {unit}",
            "img": base64_img},
        ])        

        c += alt.Chart(source).mark_image(
            width=25,
            height=25
        ).encode(
            **icon_params,
            url='img',
            tooltip=[alt.Tooltip('total_with_unit:N', title='Total')]
        )
    
    # Add a line for zero
    if show_zero == True:
        img_path = "images/small_marker.png"
        pil_image = Image.open(img_path)
        output = BytesIO()
        pil_image.save(output, format='PNG')
        base64_img = "data:image/png;base64," + base64.b64encode(output.getvalue()).decode()

        total = 0
        source = pd.DataFrame.from_records([
            {"variable": da.name, "total": total, "total_with_unit": f"{total:.2f} {unit}",
            "img": base64_img},
        ])

        c += alt.Chart(source).mark_image(
            width=25,
            height=25
        ).encode(
            **icon_params,
            url='img',
            tooltip=[alt.Tooltip('total_with_unit:N', title='Total')]
        )



    # Set bar width
    if vertical:
        c = c.properties(width=bar_width)
    else:
        c = c.properties(height=bar_width)

    return c

def pie_chart_altair(da, show="Item", unit=""):
    """Creates a pie chart using Altair to visualize the given dataarray.

    Parameters
    ----------
    da : xarray.DataArray
        The dataarray to be plotted.
    show : str, optional
        The coordinate to use to dissagregate the pie chart.
    unit : str, optional
        The unit of the quantity to be displayed in the tooltip.

    Returns
    -------
    alt.Chart
        An Altair chart object representing the pie chart.
    """

    df = da.to_dataframe().reset_index().fillna(0)
    df = df.melt(id_vars=show, value_vars=da.name)
    df["order"] = np.arange(len(da[show].values))
    df['value_with_unit'] = df['value'].apply(lambda x: f"{x:.2f} {unit}")

    c = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta("value:Q", sort=None),
        color=alt.Color(show,
                        title="Land type",
                        scale=alt.Scale(domain=list(land_color_dict.keys()),
                                        range=list(land_color_dict.values()))),
        tooltip=[alt.Tooltip(f'{show}:N'),
                 alt.Tooltip('value_with_unit:N', title='Total')],
        order=alt.Order(f'order:N', sort='ascending')
    ).resolve_scale(theta='independent')

    return c