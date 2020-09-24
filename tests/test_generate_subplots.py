from latexreport import make_document
from latexreport.utils import generate_subplots
import numpy as np

plot_labels_tests = [['wind', 'wave', 'current'], list(range(0, 90, 45)),
                     list(range(0, 90, 10)),
                     list(range(0, 90, 5)), list(range(0, 90, 2))]

plot_label_titles = [''] + ['wavedir=']*4
plot_kwargs_list = [{'linestyle': '-'}, {'linestyle': '--'},
                    {'linestyle': '-.'}] + [{'linestyle': '-'}]*4
nr_plots_subplots = [1, 1, 1, 2, 3]

for i, (plot_labels, plot_label_title,
        plot_kwargs, nrsub) in enumerate(
            zip(plot_labels_tests, plot_label_titles,
                plot_kwargs_list, nr_plots_subplots)):

    nr_plots = len(plot_labels)
    nr_values_in_plot = 20
    hss = np.random.rand(nr_plots, nr_values_in_plot)
    tps = np.random.rand(nr_plots, nr_values_in_plot)

    figure_variables = {
        'hs [m]': hss,
        'tp [s]': tps,
        plot_label_title: plot_labels,
        }

    figure_specs = {
        'nplots_insubfigure': 4,
        'nrows_insubplotgrid': 1,
        'ncols_insubplotgrid': 1,
        'figsize': (12, 8),
        'fontsize': 15,
        'ax_kw': {'xticks': [0, 0.2, 0.5], 'xticklabels': ['a', 'b', 'c'],
                  'xlim': [0, 0.5]},
        'plot_kw': plot_kwargs,
        'fig_kw': {'tight_layout': False},
        'savedir': 'results'
        }

    filenames = generate_subplots(figure_variables, **figure_specs)

    report_content = [{'subimage': {
                            'filename': filenames, 'caption': filenames,
                            'figure_caption': 'HsTpPlots',
                            'nr_horizontal_subimages': nrsub}}]

    make_document(document_title=f'test_subplot_{i}',
                  document_filename=f'results/test_subplot_{i}',
                  content=[{'title': 'Parameters', 'content': report_content}]
                  )
