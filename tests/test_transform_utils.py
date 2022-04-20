import unittest
import os
import shutil
from parameterized import parameterized
from project_name.utils.transform_utils import guess_bl_category, collapse_uniprot_curie
from project_name.transform_utils.ontology import OntologyTransform
from project_name.transform_utils.ontology.ontology_transform import ONTOLOGIES
from project_name.transform_utils.reactome.reactome import ReactomeTransform, REACTOME_SOURCES

class TestTransformUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.input_dir = 'tests/resources/snippets/'
        self.raw_dir = 'data/raw/'
        self.output_dir = 'tests/resources/'

    @parameterized.expand([
        ['', 'biolink:NamedThing'],
        ['UniProtKB', 'biolink:Protein'],
        ['ComplexPortal', 'biolink:Protein'],
        ['GO', 'biolink:OntologyClass'],
    ])
    def test_guess_bl_category(self, curie, category):
        self.assertEqual(category, guess_bl_category(curie))

    @parameterized.expand([
        ['foobar', 'foobar'],
        ['ENSEMBL:ENSG00000178607', 'ENSEMBL:ENSG00000178607'],
        ['UniprotKB:P63151-1', 'UniprotKB:P63151'],
        ['uniprotkb:P63151-1', 'uniprotkb:P63151'],
        ['UniprotKB:P63151-2', 'UniprotKB:P63151'],
    ])
    def test_collapse_uniprot_curie(self, curie, collapsed_curie):
        self.assertEqual(collapsed_curie, collapse_uniprot_curie(curie))

    def test_reactome_transform(self):
        t = ReactomeTransform(self.input_dir,self.output_dir)
        this_output_dir = os.path.join(self.output_dir,"reactome")

        # Koza expects the data to be in data/raw, so we
        # put it there.
        snippet_path = os.path.join(self.input_dir,REACTOME_SOURCES['ChEBI2Reactome'])
        raw_path = os.path.join(self.raw_dir,REACTOME_SOURCES['ChEBI2Reactome'])
        shutil.copyfile(snippet_path, raw_path)

        t.run()
        self.assertTrue(os.path.exists(this_output_dir))

        shutil.rmtree(this_output_dir)
        os.remove(raw_path)

