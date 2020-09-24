# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:36:08 2020

@author: bsorb
"""

from latexreport import make_document

files = {
    'plots': [f'files/plot_{i}.png' for i in range(4)],
    'excel_file': [f'files/spreadsheet{i}.xlsx' for i in range(2)],
    'latex_code_file': 'files/some_random_latex_code.txt',
    'text_file': 'files/some_random_text.txt',
    'image': 'files/random_shit.jpg'
}

make_document_dict = {
        'document_title': 'Autogenerated Example Document',
        'document_filename': 'example_filename',
        'author': 'Entail AS',
        'fig_ext': u'.pdf',
        'header_logofilename': 'entail.pdf',
        'logo_image_option_header': "width=250px",
        'content': [
            {'title': 'Summary', 'content': [
                {'text': 'Summary, conclusion and stuff \n and here is a new line'}]},
            {'title': 'Introduction', 'content': [
                {'text': 'Introducing people to your stuff'}]},
            {'title': 'Results', 'content': [
                {'text': {'filename': files['text_file']},
                 'table': {'filename': files['excel_file'],
                           'kwargs': {'sheet_name': 'table_2',
                                      'index_col': 0}
                           }},
                {'title': 'Plots', 'content': [{'image': {'filename': files['plots']}}]
                 },
                {'text': 'Then, a plot summarizing the results and some remarks'},
                {'title': 'Subsection with fancy latex code', 'content': [
                    {'latex_code': {'filename': files['latex_code_file']}}
                ]}
            ]},
            {'title': 'Conclusion',
             'content': [
                 {'text': 'Here are some concluding remarks'}
             ]}
        ]
    }

make_document(**make_document_dict)