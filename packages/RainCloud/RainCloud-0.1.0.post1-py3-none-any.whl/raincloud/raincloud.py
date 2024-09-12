import matplotlib.pyplot as plt
import seaborn as sns
import ptitprince as pt
from typing import Tuple, Literal

def create_raincloud_plot(df = None, x = None, y = None, title: str = 'Raincloud Plot',
                          xlabel: str = None, ylabel: str = None,
                          palette: str = 'Set2', alpha: float = 0.6,
                          orient: Literal['h', 'v'] = 'h',
                          figsize: Tuple[int, int] = (10, 10),
                          thunder: bool = False) -> None:
    """
    Create a raincloud plot for the given DataFrame, with an optional point plot
    to connect the means of each group (thunder).

    Parameters
    ----------
    df : Any
        The iterable containing the data to be plotted (default is `None`).
    x : Any
        The iterable/column name (if df is specified) to be plotted on the x-axis (default is `None`).
    y : Any
        The iterable/column name (if df is specified) to be plotted on the y-axis (default is `None`).
    title : str, optional
        The title of the plot (default is 'Raincloud Plot').
    xlabel : str, optional
        The label for the x-axis (default is `None`, which uses the value of `x`).
    ylabel : str, optional
        The label for the y-axis (default is `None`, which uses the value of `y`).
    palette : str, optional
        The color palette to be used for the plot (default is 'Set2').
    alpha : float, optional
        The transparency level of the plot elements (default is 0.6).
    orient : Literal['h', 'v'], optional
        The orientation of the plot, 'h' for horizontal or 'v' for vertical
        (default is 'h').
    figsize : tuple of int, optional
        The size of the figure, defined as (width, height) (default is (10, 10)).
    thunder : bool, optional
        If True, connects the means of each group with a point plot (default is False).

    Returns
    -------
    None
        Displays the raincloud plot.

    Example
    -------
    >>> create_raincloud_plot(df=df, x='city', y='temp', 
                              title='Raincloud Plot of Temperatures by City', 
                              xlabel='Temperature (°F)', ylabel='City', 
                              thunder=True)
    """

    if xlabel is None:
        xlabel = x
    if ylabel is None:
        ylabel = y

    plt.figure(figsize=figsize)
    raincloud = pt.RainCloud(
        x=x,
        y=y,
        data=df,
        palette=palette,
        alpha=alpha,
        orient=orient,
        pointplot=thunder,
        linecolor='grey',
        #point_linewidth=0.1, 
    )

    raincloud.plot(ax=plt.gca())

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)

    plt.show()