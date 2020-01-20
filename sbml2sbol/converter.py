'''
sbml2sbol (c) University of Liverpool. 2019

sbml2sbol is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=invalid-name
# pylint: disable=too-many-nested-blocks
from collections import defaultdict
import sys

import libsbml
from sbol import setHomespace, ComponentDefinition, Document, \
    SO_CDS, SO_RBS, IntProperty, URIProperty


_SO_ASS_COMP = 'http://identifiers.org/so/SO:0000143'


def convert(sbml_filename, sbol_filename, pathway_id='rp_pathway'):
    '''Convert.'''
    rct_uniprot = _read_sbml(sbml_filename, pathway_id)
    tirs = [5000, 10000, 15000]
    doc = _convert(rct_uniprot, tirs)
    doc.write(sbol_filename)


def _read_sbml(filename, pathway_id):
    '''Read SBML.'''
    document = libsbml.readSBMLFromFile(filename)
    model = document.model
    rp_pathway = model.getPlugin('groups').getGroup(pathway_id)

    rct_uniprot = defaultdict(list)

    for member in rp_pathway.getListOfMembers():
        if not member.getIdRef() == 'targetSink':
            # Extract reaction annotation:
            annot = model.getReaction(member.getIdRef()).getAnnotation()
            bag = annot.getChild('RDF').getChild('BRSynth').getChild('brsynth')

            for i in range(bag.getNumChildren()):
                ann = bag.getChild(i)

                if ann.getName() == 'selenzyme':
                    for j in range(ann.getNumChildren()):
                        sel_ann = ann.getChild(j)
                        rct_uniprot[member.getIdRef()].append(
                            sel_ann.getName())

    return rct_uniprot


def _convert(rct_uniprot, tirs):
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

        for uniprot_id in uniprot_ids_set:
            for tir in tirs:
                # Add placeholder for top-level gene:
                gene = ComponentDefinition('%s_%s_gene' % (uniprot_id, tir))

                # Add placeholders for RBS and CDS:
                rbs = ComponentDefinition('%s_%s_rbs' % (uniprot_id, tir))
                rbs.roles = SO_RBS

                IntProperty(rbs, 'http://liverpool.ac.uk#tir', '0', '1', tir)

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
    convert(args[0], args[1])


if __name__ == '__main__':
    main(sys.argv[1:])
