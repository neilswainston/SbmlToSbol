from argparse  import ArgumentParser
from sbml2sbol._version import __version__

DEFAULT_RBS = True
DEFAULT_MAX_PROT_PER_REACT = 3
DEFAULT_TIRS = None
DEFAULT_PATHWAY_ID = 'rp_pathway'
DEFAULT_UNIPROTID_KEY = 'selenzy'

def build_args_parser(
    prog: str,
    description: str = '',
    epilog: str = ''
) -> ArgumentParser:

    parser = ArgumentParser(
        prog = prog,
        description = description,
        epilog = epilog
    )

    # Build Parser
    parser = add_arguments(parser)

    return parser


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        '--input',
        required=True,
        type=str,
        nargs='+',
        help='path to folder(s) containing rpSBML files and/or rpSBML file path(s)'
    )
    parser.add_argument(
        '--outfile',
        required=True,
        type=str,
        help='specify output (SBOL) file'
    )
    parser.add_argument(
        '--rbs',
        type=bool,
        default=DEFAULT_RBS,
        help=f'Calculate or not the RBS strength (default: {DEFAULT_RBS})'
    )
    parser.add_argument(
        '--max_prot_per_react',
        type=int,
        default=DEFAULT_MAX_PROT_PER_REACT,
        help=f'The maximum number of proteins per reaction (default: {DEFAULT_MAX_PROT_PER_REACT})'
    )
    parser.add_argument(
        '--tirs',
        type=int,
        nargs='+',
        default=DEFAULT_TIRS,
        help=f'The RBS strength values (default: {DEFAULT_TIRS})'
    )
    parser.add_argument(
        '--pathway_id',
        type=str,
        default=DEFAULT_PATHWAY_ID,
        help=f'Group ID of the heterologous pathway (default: {DEFAULT_PATHWAY_ID})'
    )
    parser.add_argument(
        '--uniprotID_key',
        type=str,
        default=DEFAULT_UNIPROTID_KEY,
        help=f'Group ID of the heterologous pathway (default: {DEFAULT_UNIPROTID_KEY})'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
        help='show the version number and exit'
    )
    return parser
