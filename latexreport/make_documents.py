# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 09:51:02 2017

@author: audun
"""

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number, Command, \
    Figure, Package, SubFigure
from pylatex.utils import bold, NoEscape
from pylatex.base_classes import CommandBase, Arguments
import os
from pylatex.utils import make_temp_dir
import uuid
import posixpath
from pylatex import Section, Subsection, Subsubsection, Package
import pandas as pd
import numpy as np
from latexreport import get_document
from latexreport.utils import excel_to_latex


class SidewaysFigure(Figure):
    packages = [Package('rotating')]


# setting the levels of each section (maximum recursion level: 3)
def _set_section_levels(content):
    """
    _set_section_levels adds a keyword 'level' at each sub_dict with value equal to the recursion
    level of that sub_dict in the dictionary content. The level value is used later to make sure that the content is
    appended at the right level in the report (main chapter, sub chapter and sub sub chapter, etc.)
    """
    for item in content:
        item['level'] = 1
        if item.get('content'):
            for sub_item in item['content']:
                if sub_item.get('content'):
                    sub_item['level'] = 2
                    for sub_sub_item in sub_item['content']:
                        if sub_sub_item.get('content'):
                            sub_sub_item['level'] = 3
                            for sub_sub_sub_item in sub_sub_item['content']:
                                if sub_sub_sub_item.get('content'):
                                    sub_sub_sub_item['level'] = np.nan
                                else:
                                    sub_sub_sub_item['level'] = 3
                        else:
                            sub_sub_item['level'] = 2
                else:
                    sub_item['level'] = 1
    return content


def _format_content(content, content_key):
    list_content = []
    not_list_content = []

    for key, val in content[content_key].items():
        if isinstance(val, list):
            list_content.append(key)
        else:
            not_list_content.append(key)

    if len(list_content) > 0:
        new_content = []
        for i in range(len(content[content_key][list_content[0]])):  # assume that all lists have same lengths
            new_dict = {}
            for key in list_content:
                new_dict[key] = content[content_key][key][i]
            for key in not_list_content:
                new_dict[key] = content[content_key][key]
            new_content.append(new_dict)
        content[content_key] = new_content
    else:
        content[content_key] = [content[content_key]]


def _format_document_dict(content):
    """
        _format_document_dict makes sure that all lists in the content dictionary are lists of dicts. This is done to
        make the content specification more flexible for the user.

        #Example
        Say the user sends in five spreadsheets to a chapter.
        Since they all have he same kwargs, it is convenient for the user to only give the kwargs argument once.
        _format_document_dict will return a list of dicts, one for each spreadsheet with the specified kwargs.

        INPUT:
        {
            "table": {
                "filename": [
                    "files/spreadsheet0.xlsx",
                    "files/spreadsheet1.xlsx",
                    "files/spreadsheet2.xlsx",
                    "files/spreadsheet3.xlsx",
                    "files/spreadsheet4.xlsx"
                ],
                "kwargs": {
                    "sheet_name": "table_2",
                    "index_col": 0
                }
            }
        }
        RETURNS:
        {
            "table": [
                {
                    "filename": "files/spreadsheet0.xlsx",
                    "kwargs": {
                        "sheet_name": "table_2", "index_col": 0}},
                {
                    "filename": "files/spreadsheet1.xlsx",
                    "kwargs": {
                        "sheet_name": "table_2", "index_col": 0}},
                {
                   "filename": "files/spreadsheet2.xlsx",
                    "kwargs": {
                        "sheet_name": "table_2", "index_col": 0}},
                {
                    "filename": "files/spreadsheet3.xlsx",
                    "kwargs": {
                        "sheet_name": "table_2", "index_col": 0}},
                {
                    "filename": "files/spreadsheet4.xlsx",
                    "kwargs": {
                        "sheet_name": "table_2", "index_col": 0}}
            ]
        }
    """
    if isinstance(content, list):
        for item in content:
            if item.get('title'):
                _format_document_dict(item['content'])
            else:
                _format_document_dict(item)
    else:
        if content.get('table'):
            _format_content(content, 'table')
        if content.get('image'):
            _format_content(content, 'image')
        if content.get('subimage'):
            _format_content(content, 'subimage')
    return content


def _get_section(**content):
    if content['level'] == 1:
        return Section(content['title'])
    elif content['level'] == 2:
        return Subsection(content['title'])
    elif content['level'] == 3:
        return Subsubsection(content['title'])


def _get_last_section(doc):
    for stuff in doc.data[::-1]:
        if isinstance(stuff, (Section, Subsection, Subsubsection)):
            return stuff


def _append2doc(doc, content):
    if isinstance(content, list):
        for item in content:
            if item.get('title'):
                doc.append(_get_section(**item))
                _append2doc(doc, item['content'])
            else:
                _append2doc(doc, item)
    else:
        section = _get_last_section(doc)
        if content.get('text'):
            if isinstance(content['text'], dict):
                section.append(open(content['text']['filename']).read())
            else:
                section.append(content['text'])
        if content.get('latex_code'):
            if isinstance(content['latex_code'], dict):
                section.append(NoEscape(open(content['latex_code']['filename']).read()))
            else:
                section.append(NoEscape(content['latex_code']))
        if content.get('table'):
            for table in content['table']:
                section.append(NoEscape('\\begin{table}[H]'))  # note require float latex package for H command
                section.append(NoEscape(pd.read_excel(table['filename'],
                                                      **table['kwargs']).to_latex(longtable=True,
                                                                                  multicolumn_format='c')))
                section.append(NoEscape('\\end{table}'))
        if content.get('image'):
            for image in content['image']:
                section.append(NoEscape('\\begin{figure}[H]'))  # note require float latex package for H command
                Figure.add_image(section, image['filename'])
                section.append(NoEscape('\\end{figure}'))
        if content.get('subimage'):
            figure = Figure(position='H')
            for i, subimage in enumerate(content['subimage']):
                subfigure = SubFigure(width=NoEscape(
                    r'{}\linewidth'.format(np.round(1. / subimage.get('nr_horizontal_subimages', 2), 2) - 0.01)))
                subfigure.add_image(subimage['filename'])
                if subimage.get('caption', False):
                    subfigure.add_caption(subimage['caption'])
                if subimage.get('figure_caption', False) and i == 0:
                    figure.add_caption(subimage['figure_caption'])
                figure.append(subfigure)
                if (i + 1) % subimage.get('nr_horizontal_subimages', 2) == 0 and i != 0 or subimage.get(
                        'nr_horizontal_subimages', 2) == 1:
                    section.append(figure)
                    figure = Figure(arguments=NoEscape('\ContinuedFloat'), position='H')
            section.append(figure)
        if content.get('packages'):
            [doc.packages.append(Package(package)) for package in content['packages']]


def make_document(document_title='Document title', document_filename='default_filename', content=[],
                  **doc_template_kwargs):
    doc = get_document(document_title, **doc_template_kwargs)
    content = _set_section_levels(content)
    content = _format_document_dict(content)
    _append2doc(doc, content)
    doc.generate_tex(document_filename)
    doc.generate_pdf(document_filename, clean_tex=False, clean=False, compiler='pdfLaTeX')
    return doc
