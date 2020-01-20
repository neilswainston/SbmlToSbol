'''
sbml2sbol (c) University of Liverpool. 2019

sbml2sbol is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import sys

from sbol import setHomespace, ComponentDefinition, Document, Sequence, \
    SO_CDS, SO_RBS, URIProperty

_SO_ASS_COMP = 'http://identifiers.org/so/SO:0000143'


def _convert(uniprot_tirs):
    '''Convert.'''
    setHomespace('http://liverpool.ac.uk')
    doc = Document()

    for uniprot, tirs in uniprot_tirs.items():
        # Specify uniprot-specific assembly region placeholders:
        # (Provides consistent assembly sequence for each uniprot variant.)
        _5p_assembly = ComponentDefinition('%s_5_prime_assembly' % uniprot)
        _3p_assembly = ComponentDefinition('%s_3_prime_assembly' % uniprot)
        _5p_assembly.roles = _SO_ASS_COMP
        _3p_assembly.roles = _SO_ASS_COMP

        doc.addComponentDefinition([_5p_assembly, _3p_assembly])

        for tir in tirs:
            # Add placeholder for top-level gene:
            gene = ComponentDefinition('%s_%s_gene' % (uniprot, tir))

            # Add placeholders for RBS and CDS:
            rbs = ComponentDefinition('%s_%s_rbs' % (uniprot, tir))
            # rbs.addPropertyValue('rdf:resource', str(tir))
            # Property(rbs, 'http://liverpool.ac.uk#tir', '0', '1', str(tir))

            cds = ComponentDefinition('%s_%s_cds' % (uniprot, tir))

            URIProperty(cds,
                        'http://biomodels.net/biologyqualifiers#isInstanceOf',
                        '0', '1',
                        'http://identifiers.org/uniprot/%s' % uniprot)

            rbs.roles = SO_RBS
            cds.roles = SO_CDS

            doc.addComponentDefinition([rbs, cds])

            # Assemble gene from features:
            doc.addComponentDefinition(gene)

            gene.assemblePrimaryStructure(
                [_5p_assembly, rbs, cds, _3p_assembly])

    return doc


def main(args):
    '''main method.'''
    uniprot_tirs = {'P42212': [5000, 10000, 15000],
                    'P19367': [1000, 10000, 50000]}
    doc = _convert(uniprot_tirs)
    doc.write(args[0])


if __name__ == '__main__':
    main(sys.argv[1:])
