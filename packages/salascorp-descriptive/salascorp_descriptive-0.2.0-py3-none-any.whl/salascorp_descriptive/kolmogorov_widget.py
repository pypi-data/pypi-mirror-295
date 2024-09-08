# kolmogorov_widget.py

import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats
import ipywidgets as widgets

# Función para el test de Kolmogorov-Smirnov
def kolmogorov_test(
    dataset,
    variable: str,
    transformation: str = None,
    plot_histogram: bool = False,
    bins: int = 30,
    color: str = None,
    print_test: bool = True,
    return_test: bool = False,
    plotly_renderer: str = "notebook",
):
    if type(dataset) == dict:
        dataset = pd.DataFrame(dataset)

    dataset = dataset.dropna(subset=[variable]).copy()

    if transformation == "yeo_johnson":
        x = stats.yeojohnson(dataset[variable].to_numpy())[0]
    elif transformation == "log":
        x = np.log1p(dataset[variable].to_numpy())
    else:
        x = dataset[variable].to_numpy()

    x_scale = (x - x.mean()) / x.std()

    ktest = stats.kstest(x_scale, "norm")

    if print_test:
        print(f"------------------------- Kolmogorov test for the variable {variable} --------------------")
        print(f"statistic={ktest[0]:.3f}, p_value={ktest[1]:.3f}\n")
        if ktest[1] < 0.05:
            print(
                f"Since {ktest[1]:.3f} < 0.05 you can reject the null hypothesis, so the variable {variable} \ndo not follow a normal distribution"
            )
            conclusion = "Not normal distribution"
        else:
            print(
                f"Since {ktest[1]:.3f} > 0.05 you cannot reject the null hypothesis, so the variable {variable} \nfollows a normal distribution"
            )
            conclusion = "Normal distribution"
        print("-------------------------------------------------------------------------------------------\n")

    if plot_histogram:
        fig = px.histogram(dataset, x=x, nbins=bins, marginal="box", color=color, barmode="overlay")
        fig.update_traces(marker_line_width=1, marker_line_color="white", opacity=0.8)
        fig.update_layout(xaxis_title=variable, width=1500, height=500)
        fig.show(renderer=plotly_renderer)

# Función principal para llamar al widget interactivo
def kolmogorov_widget(dataset):
    # Filtrar solo las columnas numéricas
    numeric_columns = dataset.select_dtypes(include=[np.number]).columns

    # Crear widgets interactivos
    variable_selector = widgets.Dropdown(
        options=numeric_columns, 
        description='Variable:',
        disabled=False,
    )
    
    transformation_selector = widgets.Dropdown(
        options=[None, 'log', 'yeo_johnson'],
        value=None,
        description='Transform:',
        disabled=False,
    )
    
    plot_hist_selector = widgets.Checkbox(
        value=True,
        description='Plot Histogram',
        disabled=False,
    )
    
    bins_selector = widgets.IntSlider(
        value=30,
        min=5,
        max=100,
        step=1,
        description='Bins:',
        continuous_update=False
    )
    
    color_selector = widgets.Dropdown(
        options=[None] + list(dataset.columns),
        value=None,
        description='Color by:',
        disabled=False,
    )
    
    # Función para actualizar el gráfico y realizar el test
    def update_kstest(variable, transformation, plot_histogram, bins, color):
        kolmogorov_test(
            dataset=dataset,
            variable=variable,
            transformation=transformation,
            plot_histogram=plot_histogram,
            bins=bins,
            color=color,
            plotly_renderer="notebook"
        )
    
    # Conectar los widgets a la función
    widgets.interact(update_kstest, 
                     variable=variable_selector, 
                     transformation=transformation_selector, 
                     plot_histogram=plot_hist_selector,
                     bins=bins_selector,
                     color=color_selector)
