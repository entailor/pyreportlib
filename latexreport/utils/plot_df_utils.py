# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:00:36 2020

@author: MadsFredrikHeiervang
"""

import numpy as np
import matplotlib.pyplot as plt
import os


def _initiate_fig_axs(x_key, y_key, fontsize,
                      figsize, nrows_insubplotgrid, ncols_insubplotgrid):

    fig, axs = plt.subplots(nrows_insubplotgrid, ncols_insubplotgrid,
                            figsize=figsize)
    try:
        axs = axs.flat
    except:
        axs = [axs]

    for ax in axs:
        ax.set(xlabel=x_key, ylabel=y_key)
        ax.label_outer()
        ax.xaxis.label.set_size(fontsize)
        ax.yaxis.label.set_size(fontsize)

    return fig, axs


def generate_subplots(df, xlabel='', ylabel='',
                      nplots_insubfigure=4, figsize=(12, 8),
                      fontsize=15, extension='.pdf', dpi=150,
                      nrows_insubplotgrid=1, ncols_insubplotgrid=1,
                      plot_kw=None, ax_kw=None, fig_kw=None, savedir='',
                      filenametag=''):
    """create and save x,y plots with matplotlib subplots


    Parameters
    ----------
    figure_variables : dict ,
        DESCRIPTION.
        Information about what x,y,z values that are to be plotted with
        corresponding labels as keys

        {
            xlabel : str, x_array : 2D array of numbers with shape =
            (nr_labels x nr values in each plot)
            ,
            ylabel : str, y_array : 2D array of numbers with shape =
            (nr_labels x nr values in each plot)
            ,
            plot_label_title : str, plot_label_array :
                1D array of labels for each 2Dplot with length (nr labels)
            }

    nrplots_insubfigure : int, optional
        DESCRIPTION. The default is 4.
    nrows_insubplotgrid : int, optional
        DESCRIPTION. The default is 1.
    ncols_insubplotgrid : int, optional
        DESCRIPTION. The default is 1.
    figsize : tuple, optional
        DESCRIPTION. The default is (12, 18).
    fontsize : int, optional
        DESCRIPTION. The default is 15.
    extension : string, optional
        DESCRIPTION. The default is '.pdf'.
    dpi : int, optional
        DESCRIPTION. The default is 150.
    plot_kw : dict or list of dicts, optional
        DESCRIPTION. additional kwargs for plot
    ax_kw : dict or list of dicts, optional
        DESCRIPTION. additional kwargs for ax object
    fig_kw : dict or list of dicts, optional
        DESCRIPTION. additional kwargs for fig object
    Returns
    -------
    filenames : list
        DESCRIPTION.

    """

    filename = f'{filenametag}'
    filenames = []
    counter = 0
    fig, axs = _initiate_fig_axs(xlabel, ylabel, fontsize, figsize,
                                 nrows_insubplotgrid, ncols_insubplotgrid)

    for i, plot_label in enumerate(df):
        filename += f'{plot_label}-'
        if i % (len(axs)*nplots_insubfigure) == 0 and i != 0:
            [ax.legend(bbox_to_anchor=(0.0, 1.01), ncol=4,
                       loc='lower left', borderaxespad=0,
                       prop={'size': fontsize}) for ax in axs]
            filename = filename[:-1] + f'{extension}'
            if ax_kw:
                if isinstance(ax_kw, list):
                    plt.setp(axs, **ax_kw[i])
                else:
                    plt.setp(axs, **ax_kw)
            if fig_kw:
                if isinstance(fig_kw, list):
                    plt.setp(fig, **fig_kw[i])
                else:
                    plt.setp(fig, **fig_kw)
            fig.savefig(os.path.join(savedir, filename), dpi=dpi)
            filenames.append(filename)

            filename = f'{filenametag}'
            counter = 0
            fig, axs = _initiate_fig_axs(xlabel, ylabel, fontsize, figsize,
                                         nrows_insubplotgrid,
                                         ncols_insubplotgrid)
        ax_idx = int(np.floor(counter/nplots_insubfigure))
        if plot_kw:
            if isinstance(plot_kw, list):
                axs[ax_idx].plot(df[plot_label].index, df[plot_label].tolist(),
                                 label=plot_label, **plot_kw[i])
            else:
                axs[ax_idx].plot(df[plot_label].index, df[plot_label].tolist(),
                                 label=plot_label, **plot_kw)
        else:
            axs[ax_idx].plot(df[plot_label].index, df[plot_label].tolist(),
                         label=plot_label)

        counter += 1

    if not (i % (len(axs)*nplots_insubfigure) == 0 and i != 0):
        [ax.legend(bbox_to_anchor=(0.0, 1.01), ncol=4,
                   loc='lower left', borderaxespad=0,
                   prop={'size': fontsize}) for ax in axs]
        filename = filename[:-1] + f'{extension}'
        if ax_kw:
            if isinstance(ax_kw, list):
                plt.setp(axs, **ax_kw[i])
            else:
                plt.setp(axs, **ax_kw)
        if fig_kw:
            if isinstance(fig_kw, list):
                plt.setp(fig, **fig_kw[i])
            else:
                plt.setp(fig, **fig_kw)
        fig.savefig(os.path.join(savedir, filename), dpi=dpi)
        filenames.append(filename)
    plt.close('all')

    return filenames
