'''
sbml2sbol (c) University of Liverpool. 2019

sbml2sbol is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=invalid-name
# pylint: disable=too-many-nested-blocks
from collections import defaultdict
import os.path
import sys

import libsbml
from sbol import setHomespace, ComponentDefinition, Document, \
    SO_CDS, SO_RBS, FloatProperty, URIProperty
from synbiochem.utils import io_utils

_SO_GENE = 'http://identifiers.org/so/SO:0000704'
_SO_ASS_COMP = 'http://identifiers.org/so/SO:0000143'


def convert(sbml_filepaths, sbol_filename, max_prot_per_react=3, tirs=None,
            pathway_id='rp_pathway'):
    '''Convert.'''
    tirs = [10000, 20000, 30000] if tirs is None else tirs

    model_rct_uniprot = _read_sbml(sbml_filepaths, pathway_id)

    doc = _convert(model_rct_uniprot, tirs, max_prot_per_react)

    dir_name = os.path.dirname(os.path.abspath(sbol_filename))

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    doc.write(sbol_filename)


def _read_sbml(sbml_filepaths, pathway_id):
    '''Read SBML.'''
    rct_uniprot = defaultdict(list)

    for filename in io_utils.get_filenames(sbml_filepaths):
        document = libsbml.readSBMLFromFile(filename)
        rp_pathway = document.model.getPlugin('groups').getGroup(pathway_id)

        for member in rp_pathway.getListOfMembers():
            if not member.getIdRef() == 'targetSink':
                # Extract reaction annotation:
                annot = document.model.getReaction(
                    member.getIdRef()).getAnnotation()
                bag = annot.getChild('RDF').getChild(
                    'BRSynth').getChild('brsynth')

                for i in range(bag.getNumChildren()):
                    ann = bag.getChild(i)

                    if ann.getName() == 'selenzyme':
                        for j in range(ann.getNumChildren()):
                            sel_ann = ann.getChild(j)
                            rct_uniprot[member.getIdRef()].append(
                                sel_ann.getName())

    return rct_uniprot


def _convert(rct_uniprot, tirs, max_prot_per_react):
    '''Convert.'''
    setHomespace('http://liverpool.ac.uk')
    doc = Document()

    for rct, uniprot_ids_set in rct_uniprot.items():
        # Specify uniprot-specific assembly region placeholders:
        # (Provides consistent assembly sequence for each reaction group.)
        _5p_assembly = ComponentDefinition('%s_5_prime_assembly' % rct)
        _5p_assembly.roles = _SO_ASS_COMP
        _3p_assembly = ComponentDefinition('%s_3_prime_assembly' % rct)
        _3p_assembly.roles = _SO_ASS_COMP

        doc.addComponentDefinition([_5p_assembly, _3p_assembly])

        for uniprot_id in uniprot_ids_set[:max_prot_per_react]:
            for tir in tirs:
                # Add placeholder for top-level gene:
                gene = ComponentDefinition('%s_%s_gene' % (uniprot_id, tir))
                gene.roles = _SO_GENE

                URIProperty(gene,
                            'http://biomodels.net/biologyqualifiers#isInstanceOf',
                            '0', '1',
                            'http://identifiers.org/uniprot/%s' % uniprot_id)

                # Add placeholders for RBS and CDS:
                rbs = ComponentDefinition('%s_%s_rbs' % (uniprot_id, tir))
                rbs.roles = SO_RBS

                FloatProperty(
                    rbs, 'http://liverpool.ac.uk#target_tir', '0', '1', tir)

                cds = ComponentDefinition('%s_%s_cds' % (uniprot_id, tir))
                cds.roles = SO_CDS

                URIProperty(cds,
                            'http://biomodels.net/biologyqualifiers#isInstanceOf',
                            '0', '1',
                            'http://identifiers.org/uniprot/%s' % uniprot_id)

                doc.addComponentDefinition([rbs, cds])

                # Assemble gene from features:
                doc.addComponentDefinition(gene)

                gene.assemblePrimaryStructure(
                    [_5p_assembly, rbs, cds, _3p_assembly])

    return doc


def main(args):
    '''main method.'''
    convert(args[1:], args[0])


if __name__ == '__main__':
    main(sys.argv[1:])
