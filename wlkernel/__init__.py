__version__ = '0.1'


from ._wlkernel import (
    WLRDFNode,
    WLRDFEdge,
    WLRDFSubgraph,
    relabel,
    wl_kernel,
    compute_kernel,
    compute_kernel_matrix,
    compute_kernel_matrix_par
)
