from collections import defaultdict
from unittest import TestCase
from os import path as os_path
from json import load as json_load

from sbml2sbol.converter import (
    _read_sbml,
)



class Test_Converter(TestCase):

    files_folder = os_path.join(
        'tests',
        'data'
    )
    model_rct_uniprot_file = os_path.join(
        files_folder,
        'model_rct_uniprot.json'
    )
    pathway_file = os_path.join(
        files_folder,
        'lycopene.xml'
    )

    def test_read_sbml(self):
        with open(self.model_rct_uniprot_file, 'r') as jsonFile:
            jsonObject = json_load(jsonFile)
            jsonFile.close()
            model_rct_uniprot = _read_sbml(
                sbml_filepaths=[self.pathway_file],
                pathway_id='rp_pathway',
                uniprotID_key='selenzy'
            )
            self.assertDictEqual(
                model_rct_uniprot,
                defaultdict(list, jsonObject)
            )
