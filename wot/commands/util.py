import wot.ot

CELL_SET_HELP = 'gmt, gmx, or grp file of cell sets.'
CELL_DAYS_HELP = 'File with headers "id" and "day" corresponding to cell id and days'
TMAP_HELP = 'Directory of transport maps as produced by optimal transport'
MATRIX_HELP = 'A matrix with cells on rows and features, such as genes or pathways on columns'

FORMAT_HELP = 'Output file format'
FORMAT_CHOICES = ['gct', 'h5ad', 'loom', 'txt']
try:
    import pyarrow

    FORMAT_CHOICES.append('parquet')
except:
    pass


def initialize_ot_model_from_args(args):
    return wot.ot.initialize_ot_model(args.matrix,
                                      cell_days=args.cell_days,
                                      solver=args.solver,
                                      local_pca=args.local_pca,
                                      growth_rate_field=args.growth_rate_field,
                                      day_field=args.day_field,
                                      covariate_field=args.covariate_field if hasattr(args,
                                                                                      'covariate_field') else None,
                                      growth_iters=args.growth_iters,
                                      epsilon=args.epsilon,
                                      lambda1=args.lambda1,
                                      lambda2=args.lambda2,
                                      epsilon0=args.epsilon0,
                                      tau=args.tau,
                                      config=args.config,
                                      parameters=args.parameters,
                                      cell_day_filter=args.cell_day_filter,
                                      cell_growth_rates=args.cell_growth_rates,
                                      gene_filter=args.gene_filter,
                                      cell_filter=args.cell_filter,
                                      scaling_iter=args.scaling_iter,
                                      inner_iter_max=args.inner_iter_max,
                                      ncells=args.ncells,
                                      ncounts=args.ncounts,
                                      transpose=args.transpose,
                                      max_iter=args.max_iter,
                                      batch_size=args.batch_size,
                                      tolerance=args.tolerance,
                                      covariate=args.covariate if hasattr(args, 'covariate') else None
                                      )


def add_ot_parameters_arguments(parser):
    parser.add_argument('--matrix', help=MATRIX_HELP, required=True)
    parser.add_argument('--cell_days', help=CELL_DAYS_HELP, required=True)
    parser.add_argument('--cell_growth_rates',
                        help='File with "id" and "cell_growth_rate"'
                             'headers corresponding to cell id and growth rate per day.')
    parser.add_argument('--parameters', help='Optional two column parameter file containing parameter name and value')
    parser.add_argument('--config', help='Configuration per timepoint or pair of timepoints')
    parser.add_argument('--transpose', help='Transpose the matrix', action='store_true')
    parser.add_argument('--local_pca', type=int, default=30,
                        help='Convert day pairs matrix to local PCA coordinates.'
                             'Set to 0 to disable')
    parser.add_argument('--growth_iters', type=int, default=1,
                        help='Number of growth iterations for learning the growth rate.')

    parser.add_argument('--gene_filter',
                        help='File with one gene id per line to use for computing'
                             'cost matrices (e.g. variable genes)')
    parser.add_argument('--cell_filter',
                        help='File with one cell id per line to include')
    parser.add_argument('--cell_day_filter',
                        help='Comma separated list of days to include (e.g. 12,14,16)', type=str)
    parser.add_argument('--scaling_iter', default=3000, help='Number of scaling iterations for OT solver', type=int)
    parser.add_argument('--inner_iter_max', type=int, default=50,
                        help='For OT solver')
    parser.add_argument('--epsilon', type=float, default=0.05,
                        help='Controls the entropy of the transport map. An extremely '
                             'large entropy parameter will give a maximally entropic '
                             'transport map, and an extremely small entropy parameter '
                             'will give a nearly deterministic transport map '
                             '(but could also lead to numerical instability in the algorithm')
    parser.add_argument('--lambda1', type=float, default=1,
                        help='Regularization parameter that controls the '
                             'fidelity of the constraints on p')
    parser.add_argument('--lambda2', type=float, default=50,
                        help='Regularization parameter that controls the '
                             'fidelity of the constraints on q')
    parser.add_argument('--max_iter', type=int, default=1e7,
                        help='Maximum number of scaling iterations. Abort if convergence was not reached')
    parser.add_argument('--batch_size', type=int, default=5,
                        help='Number of scaling iterations to perform between duality gap check')
    parser.add_argument('--tolerance', type=int, default=1e-8,
                        help='Maximal acceptable ratio between the duality gap and the primal objective value')
    parser.add_argument('--epsilon0', type=float, default=1,
                        help='Warm starting value for epsilon')
    parser.add_argument('--tau', type=float, default=10000)
    parser.add_argument('--ncells', type=int, help='Number of cells to downsample from each timepoint and covariate')
    parser.add_argument('--ncounts', help='Sample ncounts from each cell', type=int)
    parser.add_argument('--no_overwrite', help='Do not overwrite existing transport maps if they exist',
                        action='store_true')
    # parser.add_argument('--sampling_bias', help='File with "id" and "pp" to correct sampling bias.')

    parser.add_argument('--solver', choices=['duality_gap', 'fixed_iters'],
                        help='The solver to use to compute transport matrices', default='duality_gap')
    parser.add_argument('--cell_days_field', help='Field name in cell_days file that contains cell days',
                        default='day', dest='day_field')
    parser.add_argument('--cell_growth_rates_field',
                        help='Field name in cell_growth_rates file that contains growth rates',
                        default='day', dest='growth_rate_field')
    parser.add_argument('--verbose', help='Print progress information',
                        action='store_true')
