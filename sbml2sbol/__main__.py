from logging import Logger
from .Args import build_args_parser
from .converter import convert


def entry_point():
    parser = build_args_parser(
        prog = 'sbml2sbol',
        description='convert rpSBML file(s) into one single SBOL file'
    )
    args = parser.parse_args()

    convert(
        sbml_filepaths=args.input,
        sbol_filename=args.outfile,
        rbs=args.rbs,
        max_prot_per_react=args.max_prot_per_react,
        tirs=args.tirs,
        pathway_id=args.pathway_id,
        uniprotID_key=args.uniprotID_key
    )


if __name__ == '__main__':
    entry_point()
