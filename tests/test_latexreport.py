# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 10:04:05 2019

@author: audun
"""

import unittest
from latexreport import make_latex_document
from latexreport.utils import excel_to_latex
import latexreport.make_documents as md
from pylatex import Document
import json
import os

if not os.path.exists('results'):
    os.makedirs('results')

class TestLatexReport(unittest.TestCase):
    """Test sim2hdf5 and model2hdf5 functions.
    """

    @classmethod
    def setUpClass(cls):
        # table from excel
        cls._excel_files = [f'files/test{i + 1}.xlsx' for i in range(5)]
        cls._table_pdfs = [f'results/test_excel_to_latex{i + 1}' for i in range(5)]
        cls._make_document_dict_file = 'make_document_dict.json'

    def test_excel_to_latex(self):
        headers = [[0, 1], 0, [0, 1], [0, 1, 2], [0, 1, 2]]

        for i, (testfile, document_filename, header) in enumerate(zip(self._excel_files, self._table_pdfs, headers)):
            doc = make_latex_document(document_title=f'test_excel_to_latex{i + 1}',
                                document_filename=document_filename,
                                content=[{'title': 'Test',
                                          'content': excel_to_latex(testfile, header=header, index_col=0)}]
                                )
            self.assertTrue(isinstance(doc, Document))

    def test_make_document(self):
        doc = make_latex_document(**json.load(open(self._make_document_dict_file)))
        self.assertTrue(isinstance(doc, Document))

    def test_format_document_dict(self):
        make_document_dict = json.load(open(self._make_document_dict_file))
        content = make_document_dict['content']
        md._format_document_dict(content)
        self.assertTrue(isinstance(content[0]['content'][0]['text'], str))
        self.assertTrue(isinstance(content[1]['content'][0]['text'], str))
        self.assertTrue(isinstance(content[2]['content'][0]['text'], dict))
        self.assertTrue(isinstance(content[2]['content'][0]['table'], list))
        self.assertTrue(len(content[2]['content'][0]['table']) == 2)
        self.assertTrue(isinstance(content[2]['content'][1]['content'][0]['image'], list))
        self.assertTrue(len(content[2]['content'][1]['content'][0]['image']) == 4)
        self.assertTrue(isinstance(content[2]['content'][2]['text'], str))
        self.assertTrue(isinstance(content[2]['content'][3]['content'], list))
        self.assertTrue(isinstance(content[3]['content'][0]['text'], str))

    def test_set_section_levels(self):
        make_document_dict = json.load(open(self._make_document_dict_file))
        content = make_document_dict['content']
        md._set_section_levels(content)
        self.assertTrue(content[0]['level'] == 1)
        self.assertTrue(content[0]['content'][0]['level'] == 1)
        self.assertTrue(content[1]['level'] == 1)
        self.assertTrue(content[1]['content'][0]['level'] == 1)
        self.assertTrue(content[2]['level'] == 1)
        self.assertTrue(content[2]['content'][0]['level'] == 1)
        self.assertTrue(content[2]['content'][1]['level'] == 2)
        self.assertTrue(content[2]['content'][1]['content'][0]['level'] == 2)
        self.assertTrue(content[2]['content'][2]['level'] == 1)
        self.assertTrue(content[2]['content'][3]['level'] == 2)
        self.assertTrue(content[2]['content'][3]['content'][0]['level'] == 2)
        self.assertTrue(content[3]['level'] == 1)
        self.assertTrue(content[3]['content'][0]['level'] == 1)


if __name__ == "__main__":
    #    unittest.main()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLatexReport)
    unittest.TextTestRunner().run(suite)
