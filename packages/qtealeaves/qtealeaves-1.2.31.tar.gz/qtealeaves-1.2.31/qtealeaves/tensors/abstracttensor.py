# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Abstract class for tensors. Represents all the functions that should be
implemented in a tensor.

We provide two tensor types:

* :class:`_AbstractQteaTensor` : suitable for simulation
* :class:`_AbstractQteaBaseTensor` : suitable for simulation and
  suitable to be the base tensor type for a symmetric tensor.

"""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-branches
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-lines

import abc
import os
import string
from warnings import warn
import numpy as np

__all__ = [
    "_AbstractQteaTensor",
    "_AbstractQteaBaseTensor",
    "_AbstractDataMover",
    "_parse_block_size",
    "_AbstractBaseTensorChecks",
]


class _AbstractQteaTensor(abc.ABC):
    """
    Tensor for Quantum Tea simulations.

    **Arguments**

    links : list
        Type of entries in list depends on tensor type and are either
        integers for dense tensors or some LinkType for symmetric
        tensors.

    ctrl : str, optional
        Initialization of tensor.
        Default to "Z"

    are_links_outgoing : list of bools
        Used in symmetric tensors only: direction of link in tensor.
        Length is same as rank of tensor.

    base_tensor_cls : valid dense quantum tea tensor or `None`
        Used in symmetric tensors only: class representing dense tensor

    dtype : data type, optional
        Valid data type for the underlying tensors.

    device : device specification, optional
        Valid device specification (depending on tensor).
    """

    has_symmetry = False

    @abc.abstractmethod
    def __init__(
        self,
        links,
        ctrl="Z",
        are_links_outgoing=None,
        base_tensor_cls=None,
        dtype=None,
        device=None,
    ):
        pass

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    @abc.abstractmethod
    def are_links_outgoing(self):
        """Define property of outgoing links as property (always False)."""

    @property
    @abc.abstractmethod
    def base_tensor_cls(self):
        """Base tensor class."""

    @property
    @abc.abstractmethod
    def device(self):
        """Device where the tensor is stored."""

    @property
    @abc.abstractmethod
    def dtype(self):
        """Data type of the underlying arrays."""

    @property
    @abc.abstractmethod
    def dtype_eps(self):
        """Data type's machine precision of the underlying arrays."""

    @property
    @abc.abstractmethod
    def linear_algebra_library(self):
        """Specification of the linear algebra library used as string."""

    @property
    @abc.abstractmethod
    def links(self):
        """Specification of link with full information to reconstruct link."""

    @property
    @abc.abstractmethod
    def ndim(self):
        """Rank of the tensor."""

    @property
    @abc.abstractmethod
    def shape(self):
        """Dimension of tensor along each dimension."""

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------

    def __eq__(self, other):
        """Checking equal tensors up to tolerance."""
        return self.are_equal(other)

    def __ne__(self, other):
        """Checking not equal tensors up to tolerance."""
        return not self.are_equal(other)

    @abc.abstractmethod
    def __add__(self, other):
        """
        Addition of a scalar to a tensor adds it to all the entries.
        If other is another tensor, elementwise addition if they have the same shape
        """

    @abc.abstractmethod
    def __iadd__(self, other):
        """In-place addition of tensor with tensor or scalar (update)."""

    def __matmul__(self, other):
        """Matrix multiplication as contraction over last and first index of self and other."""
        idx = self.ndim - 1
        return self.tensordot(other, ([idx], [0]))

    @abc.abstractmethod
    def __mul__(self, sc):
        """Multiplication of tensor with scalar returning new tensor as result."""

    @abc.abstractmethod
    def __imul__(self, sc):
        """In-place multiplication of tensor with scalar (update)."""

    def __rmul__(self, sc):
        """Multiplication from the right of a scalar"""
        return self * sc

    @abc.abstractmethod
    def __itruediv__(self, sc):
        """In-place division of tensor with scalar (update)."""

    @abc.abstractmethod
    def __neg__(self):
        """Negative of a tensor returned as a new tensor."""

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @staticmethod
    @abc.abstractmethod
    def convert_operator_dict(
        op_dict,
        params=None,
        symmetries=None,
        generators=None,
        base_tensor_cls=None,
        dtype=None,
        device=None,
    ):
        """
        Iterate through an operator dict and convert the entries.

        **Arguments**

        op_dict : instance of :class:`TNOperators`
            Contains the operators as xp.ndarray.

        symmetries:  list, optional, for compatability with symmetric tensors.
            For symmetry, contains symmetries.
            Otherwise, must be empty list.

        generators : list, optional, for compatability with symmetric tensors.
            For symmetries, contains generator of the symmetries as str for dict.
            Must be empty list.

        base_tensor_cls : None, optional, for compatability with symmetric tensors.
            For symmetries, must be valid base tensor class.
            Otherwise, no checks on this one here.

        dtype : data type for xp, optional
            Specify data type.

        device : str
            Device for the simulation. Typically "cpu" and "gpu", but depending on
            tensor backend.
        """

    @abc.abstractmethod
    def copy(self, dtype=None, device=None):
        """Make a copy of a tensor."""

    @abc.abstractmethod
    def eye_like(self, link):
        """
        Generate identity matrix.

        **Arguments**

        self : instance of :class:`QteaTensor`
            Extract data type etc from this one here.

        link : same as returned by `links` property.
            Dimension of the square, identity matrix.
        """

    @abc.abstractmethod
    def random_unitary(self, links):
        """
        Generate a random unitary tensor via performing a SVD on a
        random tensor, where a matrix dimension is specified with
        `links`. Tensor will be of the structure
        [link[0], .., link[-1], link[0], .., link[-1]].
        """

    @classmethod
    @abc.abstractmethod
    def read(cls, filehandle, dtype, device, base_tensor_cls, cmplx=True, order="F"):
        """Read a tensor from file."""

    @staticmethod
    @abc.abstractmethod
    def dummy_link(example_link):
        """Construct a dummy link. This method is particularly important for symmetries."""

    @staticmethod
    @abc.abstractmethod
    def set_missing_link(links, max_dim, are_links_outgoing=None):
        """Calculate the property of a missing link in a list."""

    @abc.abstractmethod
    def zeros_like(self):
        """Get a tensor with the same links as `self` but filled with zeros."""

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def are_equal(self, other, tol=1e-7):
        """Check if two tensors are equal."""

    def assert_identical_irrep(self, link_idx):
        """Assert that specified link is identical irreps."""
        if not self.is_identical_irrep(link_idx):
            raise Exception(f"Link at {link_idx} is no identical irrep.")

    @abc.abstractmethod
    def assert_identity(self, tol=1e-7):
        """Check if tensor is an identity matrix."""

    def assert_normalized(self, tol=1e-7):
        """Raise exception if norm is not 1 up to tolerance."""
        norm = self.norm()

        if abs(norm - 1.0) > tol:
            raise Exception("Violating normalization condition.")

    def assert_unitary(self, links, tol=1e-7):
        """Raise exception if tensor is not unitary up to tolerance for given links."""
        ctensor = self.conj().tensordot(self, (links, links))
        # reshape into a matrix to check if identity
        half_links = len(ctensor.links) // 2
        ctensor.fuse_links_update(0, half_links - 1)
        ctensor.fuse_links_update(1, half_links)

        ctensor.assert_identity(tol=tol)

    @abc.abstractmethod
    def is_close_identity(self, tol=1e-7):
        """Check if rank-2 tensor is close to identity."""

    @abc.abstractmethod
    def is_dtype_complex(self):
        """Check if data type is complex."""

    @abc.abstractmethod
    def is_identical_irrep(self, link_idx):
        """Check that the link at `link_idx` is identical irrep."""

    @abc.abstractmethod
    def is_link_full(self, link_idx):
        """Check if the link at given index is at full bond dimension."""

    def sanity_check(self):
        """Quick set of checks for tensor."""
        return

    @staticmethod
    def free_device_memory():
        """
        Free the unused device memory that is otherwise occupied by the cache.
        This method SHOULD NOT free memory allocated for the computation.
        """
        return

    # --------------------------------------------------------------------------
    #                       Single-tensor operations
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def attach_dummy_link(self, position, is_outgoing=True):
        """Attach dummy link at given position (inplace update)."""

    @abc.abstractmethod
    def conj(self):
        """Return the complex conjugated in a new tensor."""

    @abc.abstractmethod
    def conj_update(self):
        """Apply the complex conjugate to the tensor in place."""

    @abc.abstractmethod
    def convert(self, dtype=None, device=None, stream=None):
        """Convert underlying array to the specified data type inplace."""

    @abc.abstractmethod
    def convert_singvals(self, singvals, dtype=None, device=None, stream=None):
        """Convert the singular values via a tensor."""

    @abc.abstractmethod
    def dtype_from_char(self, dtype):
        """Resolve data type from chars C, D, S, Z and optionally H."""

    @abc.abstractmethod
    def eig_api(
        self, matvec_func, links, conv_params, args_func=None, kwargs_func=None
    ):
        """Interface to hermitian eigenproblem"""

    @abc.abstractmethod
    def fuse_links_update(self, fuse_low, fuse_high, is_link_outgoing=True):
        """Fuses one set of links to a single link (inplace-update)."""

    @abc.abstractmethod
    def get_of(self, variable):
        """Run the get method to transfer to host on variable (same device as self)."""

    @abc.abstractmethod
    def getsizeof(self):
        """Size in memory (approximate, e.g., without considering small meta data)."""

    @abc.abstractmethod
    def get_entry(self):
        """Get entry if scalar on host."""

    # pylint: disable-next=unused-argument
    def flip_links_update(self, link_inds):
        """Flip irreps on given links (symmetric tensors only)."""
        return self

    @abc.abstractmethod
    def norm(self):
        """Calculate the norm of the tensor <tensor|tensor>."""

    @abc.abstractmethod
    def norm_sqrt(self):
        """Calculate the square root of the norm of the tensor <tensor|tensor>."""

    @abc.abstractmethod
    def normalize(self):
        """Normalize tensor with sqrt(<tensor|tensor>)."""

    @abc.abstractmethod
    def remove_dummy_link(self, position):
        """Remove the dummy link at given position (inplace update)."""

    @abc.abstractmethod
    def restrict_irreps(self, link_idx, sector):
        """Restrict, i.e., project, link to a sector (needed for symmetric tensors)."""

    @abc.abstractmethod
    def scale_link(self, link_weights, link_idx, do_inverse=False):
        """Scale tensor along one link at `link_idx` with weights. Can do inverse, too."""

    @abc.abstractmethod
    def scale_link_update(self, link_weights, link_idx, do_inverse=False):
        """Scale tensor along one link at `link_idx` with weights (inplace update)."""

    @abc.abstractmethod
    def set_diagonal_entry(self, position, value):
        """Set the diagonal element in a rank-2 tensor (inplace update)"""

    @abc.abstractmethod
    def set_matrix_entry(self, idx_row, idx_col, value):
        """Set element in a rank-2 tensor (inplace update)"""

    @abc.abstractmethod
    def split_link_deg_charge(self, link_idx):
        """
        Split a link into two, where one carries the degeneracy, the other the charge.

        Arguments
        ---------

        link_idx : int
            Link to be split.

        Returns
        -------

        :class:`_AbstractQteaTensor`
            New tensor with link at position `link_idx` split into two
            links at `link_idx` (degeneracy) and `link_idx + 1` (charge).
            Links originally after `link_idx` follow shifted by one index.
        """

    @abc.abstractmethod
    def to_dense(self, true_copy=False):
        """Return dense tensor (if `true_copy=False`, same object may be returned)."""

    @abc.abstractmethod
    def to_dense_singvals(self, s_vals, true_copy=False):
        """Convert singular values to dense vector without symmetries."""

    @abc.abstractmethod
    def trace(self, return_real_part=False, do_get=False):
        """Take the trace of a rank-2 tensor."""

    @abc.abstractmethod
    def trace_one_dim_pair(self, links):
        """Trace a pair of links with dimenion one. Inplace update."""

    @abc.abstractmethod
    def transpose(self, permutation):
        """Permute the links of the tensor and return new tensor."""

    @abc.abstractmethod
    def transpose_update(self, permutation):
        """Permute the links of the tensor inplace."""

    @abc.abstractmethod
    def write(self, filehandle, cmplx=None):
        """Write tensor."""

    # --------------------------------------------------------------------------
    #                         Two-tensor operations
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def add_update(self, other, factor_this=None, factor_other=None):
        """
        Inplace addition as `self = factor_this * self + factor_other * other`.
        """

    @abc.abstractmethod
    def dot(self, other):
        """Inner product of two tensors <self|other>."""

    @abc.abstractmethod
    def kron(self, other, idxs=None):
        """
        Perform the kronecker product between two tensors.
        By default, do it over all the legs, but you can also
        specify which legs should be kroned over.
        The legs over which the kron is not done should have
        the same dimension.
        """

    @abc.abstractmethod
    def expand_link_tensorpair(self, other, link_self, link_other, new_dim, ctrl="R"):
        """Expand the link between a pair of tensors based on the ctrl parameter. "R" for random"""

    @abc.abstractmethod
    def split_qr(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        is_q_link_outgoing=True,
    ):
        """Split the tensor via a QR decomposition."""

    @abc.abstractmethod
    def split_qrte(
        self,
        tens_right,
        singvals_self,
        operator=None,
        conv_params=None,
        is_q_link_outgoing=True,
    ):
        """Split via a truncated expanded QR."""

    @abc.abstractmethod
    def split_svd(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        contract_singvals="N",
        conv_params=None,
        no_truncation=False,
        is_link_outgoing_left=True,
    ):
        """Split tensor via SVD for a bipartion of links."""

    @abc.abstractmethod
    def stack_link(self, other, link):
        """Stack two tensors along a given link."""

    @abc.abstractmethod
    def tensordot(self, other, contr_idx):
        """Tensor contraction of two tensors along the given indices."""

    # --------------------------------------------------------------------------
    #                        Internal methods
    # --------------------------------------------------------------------------

    def _invert_link_selection(self, links):
        """Invert the selection of links and return them as a list."""
        ilinks = [ii if (ii not in links) else None for ii in range(self.ndim)]
        ilinks = list(filter(_func_not_none, ilinks))
        return ilinks

    @staticmethod
    def _split_checks_links(legs_left, legs_right):
        """
        Check if bipartition is there and if links are sorted.

        **Returns**

        is_good_bipartition : bool
            True if all left legs before right legs

        is_sorted_l : bool
            True if left legs are already sorted

        is_sorted_r : bool
            True if right legs are already sorted.
        """
        legs_l = np.array(legs_left)
        legs_r = np.array(legs_right)
        is_good_bipartition = np.max(legs_l) < np.min(legs_r)
        is_sorted_l = (
            True if (legs_l.ndim < 2) else np.all(legs_l[1:] - legs_l[:-1] > 0)
        )
        is_sorted_r = (
            True if (legs_r.ndim < 2) else np.all(legs_r[1:] - legs_r[:-1] > 0)
        )

        return is_good_bipartition, is_sorted_l, is_sorted_r

    @staticmethod
    def _einsum_for_kron(self_shape, other_shape, idxs):
        """
        Return the einstein notation summation for the
        kronecker operation between two tensors along
        the indeces idxs

        Parameters
        ----------
        self_shape : Tuple[int]
            Shape of the first tensor
        other_shape : Tuple[int]
            Shape of the second tensor
        idxs : Tuple[int]
            Indexes over which to perform the kron.
            If None, kron over all indeces.

        Returns
        -------
        str
            The einstein notation expression for einsum
        Tuple[int]
            The shape of the output
        """
        self_ndim = len(self_shape)
        other_ndim = len(other_shape)

        final_shape = np.array(self_shape) * np.array(other_shape)
        # Getting the maximum number of indexes required for einsum
        alphabet = list(map(chr, range(97, 97 + self_ndim + len(other_shape))))
        # The first ndim letters are for the first tensor
        letters_left = np.array(alphabet[:self_ndim], dtype=str)
        letters_right = np.array(
            alphabet[self_ndim : self_ndim + other_ndim], dtype=str
        )
        # Adjust the letters in case some index should be not kronned over
        if idxs is not None:
            not_idxs = np.setdiff1d(np.arange(self_ndim), idxs)
            letters_right[not_idxs] = letters_left[not_idxs]
            final_shape[not_idxs] = np.array(self_shape)[not_idxs]
        # Create the subscripts. The formula will look something like:
        # ijk,lmn->iljmkn if all the indexes are kronned over
        # ijk,ljn->iljkn if for example only indexes [0, 2] are kronned
        subscripts = "".join(letters_left) + "," + "".join(letters_right) + "->"
        if idxs is not None:
            letters_right[not_idxs] = ""
        subscripts += "".join([ii + jj for ii, jj in zip(letters_left, letters_right)])

        return subscripts, final_shape


class _AbstractQteaBaseTensor(_AbstractQteaTensor):
    @abc.abstractmethod
    def assert_diagonal(self, tol=1e-7):
        """Check that tensor is a diagonal matrix up to tolerance."""

    @abc.abstractmethod
    def assert_int_values(self, tol=1e-7):
        """Check that there are only integer values in the tensor."""

    @abc.abstractmethod
    def assert_real_valued(self, tol=1e-7):
        """Check that all tensor entries are real-valued."""

    def _attach_dummy_link_shape(self, position):
        """Calculate the new shape when attaching a dummy link to a dense tensor."""
        new_shape = list(self.shape)[:position] + [1] + list(self.shape)[position:]
        return new_shape

    def concatenate_vectors(self, vectors, dtype, dim=None):
        """
        Concatenate vectors of the underlying numpy / cupy / torch / etc tensors.

        **Arguments***

        vectors : list
            List of one-dimensional arrays.

        dtype : data type
            Data type of concatenated vectors.

        dim : int | None
            Total dimension of concatenated vectors.
            If `None`, calculated on the fly.
            Default to `None`

        **Returns**

        vec : one-dimensional array of corresponding backend library, e.g., numpy ndarray
            The elements in the list are concatenated in order, e.g.,
            input [[1, 2], [6, 5, 3]] will result in [1, 2, 6, 5, 3].

        mapping : dict
            Keys are the index of the individual vectors in the list `vectors`.
            Values are tuples with two integers with the lower and
            higher bound, e.g., `{0 : (0, 2), 1: (2, 5)}` for the example
            in `vec` in the previous return variable.

        **Details**

        Used to concatenate singular values for symmetric tensors
        in SVD, which is needed as jax and tensorflow do not support
        `x[:]` assignments.
        """
        if dim is None:
            dim = 0
            for elem in vectors:
                dim += elem.shape[0]

        vec = self.vector_with_dim_like(dim, dtype=dtype)

        i2 = 0
        mapping = {}
        for ii, elem in enumerate(vectors):
            i1 = i2
            i2 += elem.shape[0]

            vec[i1:i2] = elem
            mapping[ii] = (i1, i2)

        return vec, mapping

    @abc.abstractmethod
    def elementwise_abs_smaller_than(self, value):
        """Return boolean if each tensor element is smaller than `value`"""

    def expand_link_tensorpair(self, other, link_self, link_other, new_dim, ctrl="R"):
        """
        Expand the link between a pair of tensors. If ctrl="R", the expansion is random

        **Arguments**

        other : instance of :class`QteaTensor`

        link_self : int
            Expand this link in `self`

        link_other : int
            Expand this link in `other`. Link must be a match (dimension etc.)

        ctrl : str, optional
            How to fill the extension. Default to "R" (random)

        **Returns**

        new_this : instance of :class`QteaTensor`
            Expanded version of `self`

        new_other : instance of :class`QteaTensor`
            Expanded version of `other`
        """
        new_this = self.expand_tensor(link_self, new_dim, ctrl=ctrl)
        new_other = other.expand_tensor(link_other, new_dim, ctrl=ctrl)

        return new_this, new_other

    @abc.abstractmethod
    def expand_tensor(self, link, new_dim, ctrl="R"):
        """Expand  tensor along given link and to new dimension."""

    @abc.abstractmethod
    def get_argsort_func(self):
        """Return callable to argsort function."""

    @abc.abstractmethod
    def get_diag_entries_as_int(self):
        """Return diagonal entries of rank-2 tensor as integer on host."""

    @abc.abstractmethod
    def get_sqrt_func(self):
        """Return callable to sqrt function."""

    @abc.abstractmethod
    def get_submatrix(self, row_range, col_range):
        """Extract a submatrix of a rank-2 tensor for the given rows / cols."""

    @abc.abstractmethod
    def flatten(self):
        """Returns flattened version (rank-1) of dense array in native array type."""

    @classmethod
    @abc.abstractmethod
    def from_elem_array(cls, tensor, dtype=None, device=None):
        """New tensor from array."""

    def _fuse_links_update_shape(self, fuse_low, fuse_high):
        """
        Calculates shape for dense tensor for fusing one set of links
        to a single link.

        Parameters
        ----------
        fuse_low : int
            First index to fuse
        fuse_high : int
            Last index to fuse.

        Example: if you want to fuse links 1, 2, and 3, fuse_low=1, fuse_high=3.
        Therefore the function requires links to be already sorted before in the
        correct order.
        """
        shape = list(self.shape[:fuse_low])
        shape += [np.prod(self.shape[fuse_low : fuse_high + 1])]
        shape += list(self.shape[fuse_high + 1 :])
        return shape

    def is_identical_irrep(self, link_idx):
        """Check that the link at `link_idx` is identical irrep."""
        return self.shape[link_idx] == 1

    @abc.abstractmethod
    def mask_to_device(self, mask):
        """Send a mask to the device where the tensor is."""

    @abc.abstractmethod
    def mask_to_host(self, mask):
        """Send a mask to the host."""

    def pad(self, link, new_dim, ctrl="R"):
        """
        Pad a tensor along given link and to new dimension.
        It is a wapper around `self.expand_tensor`.
        The padding is added at the end.

        Parameters
        ----------
        link : int
            Link to expand
        new_dim : int
            New dimension of the tensor
        ctrl : str | scalar
            Value for the padding

        Returns
        -------
        _AbstractQteaTensor
            The padded tensor
        """
        return self.expand_tensor(link, new_dim, ctrl=ctrl)

    @abc.abstractmethod
    def permute_rows_cols_update(self, inds):
        """Permute rows and columns of rank-2 tensor with `inds`. Inplace update."""

    @abc.abstractmethod
    def prepare_eig_api(self, conv_params):
        """Return variables for eigsh."""

    def _remove_dummy_link_shape(self, position):
        """Return shape for removing the dummy link at given position."""
        if self.shape[position] != 1:
            raise Exception(
                "Can only remove links with dimension 1. "
                + f"({self.shape[position]} at {position})"
            )
        new_shape = list(self.shape)[:position] + list(self.shape)[position + 1 :]

        return new_shape

    @abc.abstractmethod
    def reshape(self, shape, **kwargs):
        """Reshape a tensor."""

    @abc.abstractmethod
    def reshape_update(self, shape, **kwargs):
        """Reshape tensor dimensions inplace."""

    def restrict_irreps(self, link_idx, sector):
        """Restrict, i.e., project, link to a sector (needed for symmetric tensors)."""
        if sector is not None:
            raise ValueError("Tensor without symmetries requires sector to be `None`.")

        return self

    def _scale_link_einsum(self, link_idx):
        """Generate einsum-string notation for scale_link."""
        ndim = self.ndim
        if self.ndim > 26:
            raise Exception("Not sure how to support einsum here")

        key_a = string.ascii_lowercase[:ndim]
        key_b = key_a[link_idx]
        key = key_a + "," + key_b + "->" + key_a

        return key

    @abc.abstractmethod
    def set_submatrix(self, row_range, col_range, tensor):
        """Set a submatrix of a rank-2 tensor for the given rows / cols."""

    def _shape_as_rank_3(self, link):
        """Calculate the shape as rank-3, i.e., before-link, link, after-link."""
        if link > 0:
            dim1 = int(np.prod(list(self.shape)[:link]))
        else:
            dim1 = 1

        dim2 = self.shape[link]

        if link == self.ndim - 1:
            dim3 = 1
        else:
            dim3 = int(np.prod(list(self.shape)[link + 1 :]))

        return dim1, dim2, dim3

    @abc.abstractmethod
    def set_subtensor_entry(self, corner_low, corner_high, tensor):
        """
        Set a subtensor (potentially expensive as looping explicitly, inplace update).

        **Arguments**

        corner_low : list of ints
            The lower index of each dimension of the tensor to set. Length
            must match rank of tensor `self`.

        corner_high : list of ints
            The higher index of each dimension of the tensor to set. Length
            must match rank of tensor `self`.

        tensor : :class:`QteaTensor`
           Tensor to be set as subtensor. Rank must match tensor `self`.
           Dimensions must match `corner_high - corner_low`.

        **Examples**

        To set the tensor of shape 2x2x2 in a larger tensor `self` of shape
        8x8x8 the corresponing call is in comparison to a numpy syntax:

        * self.set_subtensor_entry([2, 4, 2], [4, 6, 4], tensor)
        * self[2:4, 4:6, 2:4] = tensor

        Or with variables and rank-3 tensors

        * self.set_subtensor_entry([a, b, c], [d, e, f], tensor)
        * self[a:d, b:e, c:f] = tensor

        To be able to work with all ranks, we currently avoid the numpy
        syntax in our implementation.
        """

    def split_link_deg_charge(self, link_idx):
        """Split a link into two, where one carries the degeneracy, the other the charge."""
        shape = list(self.shape)
        new_shape = shape[: link_idx + 1] + [1] + shape[link_idx + 1 :]
        return self.reshape(new_shape)

    @abc.abstractmethod
    def subtensor_along_link(self, link, lower, upper):
        """Extract and return a subtensor select range (lower, upper) for one line."""

    def trace_one_dim_pair(self, links):
        """Trace a pair of links with dimenion one. Inplace update."""
        if len(links) != 2:
            raise Exception("Can only run on pair of links")

        ii = min(links[0], links[1])
        jj = max(links[1], links[0])

        if ii == jj:
            raise Exception("Same link.")

        self.remove_dummy_link(jj)
        self.remove_dummy_link(ii)

        return self

    @abc.abstractmethod
    def _truncate_decide_chi(
        self,
        chi_now,
        chi_by_conv,
        chi_by_trunc,
        chi_min,
    ):
        """
        Decide on the bond dimension based on the various values chi and
        potential hardware preference indicated.

        **Arguments**

        chi_now : int
            Current value of the bond dimension

        chi_by_conv : int
            Maximum bond dimension as suggested by convergence parameters.

        chi_by_trunc : int
            Bond dimension suggested by truncating (either ratio or norm).

        chi_min : int
            Minimum bond dimension under which we do not want to go below.
            For example, used in TTN algorithms.
        """

    @staticmethod
    def _truncate_decide_chi_static(
        chi_now,
        chi_by_conv,
        chi_by_trunc,
        chi_min,
        block_size_bond_dimension,
        block_size_byte,
        data_type_byte,
    ):
        """
        Decide on the bond dimension based on the various values chi and
        potential hardware preference indicated.

        **Arguments**

        chi_now : int
            Current value of the bond dimension

        chi_by_conv : int
            Maximum bond dimension as suggested by convergence parameters.

        chi_by_trunc : int
            Bond dimension suggested by truncating (either ratio or norm).

        chi_min : int
            Minimum bond dimension under which we do not want to go below.
            For example, used in TTN algorithms.

        block_size_bond_dimension : int, `None`
            Ideal block size for the bond dimension. Chi should be a
            multiple of block_size_bond_dimension

        block_size_byte : int, `None`
            Ideal block size for memory in terms of bytes. Chi should be a
            multiple of (block_size_byte / data_type_bytes)

        data_type_byte : int
            Number of bytes for the current data type of the tensor, e.g.,
            8 bytes for a real float64.

        **Returns**

        chi_new : int
            Suggestion for the new bond dimension taking into account the
            current bond dimension, truncation criteria, convergence parameters
            and - if given - hardware preferences.
        """
        if block_size_byte is not None:
            block_size = block_size_byte // data_type_byte
        elif block_size_bond_dimension is not None:
            block_size = block_size_bond_dimension
        else:
            # fall-back is always block-size one; quick return not
            # possible to ensure minimal bond dimension
            block_size = 1

        if chi_by_conv % block_size != 0:
            chi_by_conv = (chi_by_conv // block_size + 1) * block_size
        if chi_by_conv < chi_min:
            # 2nd if-case outside first one to cover cases with block_size=1
            for _ in range(1000):
                chi_by_conv += block_size
                if chi_by_conv >= chi_min:
                    break

            if chi_by_trunc < chi_min:
                warn("Could not reach min_bond_dimension in 1000 iterations.")

        if chi_by_trunc % block_size != 0:
            chi_by_trunc = (chi_by_trunc // block_size + 1) * block_size
        if chi_by_trunc < chi_min:
            for _ in range(1000):
                chi_by_trunc += block_size
                if chi_by_trunc >= chi_min:
                    break

            if chi_by_trunc < chi_min:
                warn("Could not reach min_bond_dimension in 1000 iterations.")

        if chi_now % block_size != 0:
            chi_now = (chi_now // block_size + 1) * block_size
        if chi_now < chi_min:
            for _ in range(1000):
                chi_now += block_size
                if chi_now >= chi_min:
                    break

            if chi_now < chi_min:
                warn("Could not reach min_bond_dimension in 1000 iterations.")

        return min(chi_now, min(chi_by_conv, chi_by_trunc))

    @abc.abstractmethod
    def _truncate_singvals(self, singvals, conv_params=None):
        """Truncate the singular values followling the given strategy."""

    @abc.abstractmethod
    def _truncate_sv_ratio(self, singvals, conv_params):
        """
        Truncate the singular values based on the ratio
        with the biggest one.
        """

    @abc.abstractmethod
    def _truncate_sv_norm(self, singvals, conv_params):
        """
        Truncate the singular values based on the
        total norm cut.
        """

    @abc.abstractmethod
    def vector_with_dim_like(self, dim, dtype=None):
        """Generate a vector in the native array of the base tensor."""


class _AbstractBaseTensorChecks(abc.ABC):
    def setup_helper(self):
        """Setup helper will be called my unittest's `setUp()`."""
        # Disable attribute outside init for this function only
        # pylint: disable=attribute-defined-outside-init
        self.seed = [11, 13, 17, 19]

        self.device = None
        self.dtype = None
        self.tensor_cls = None
        self.base_tensor_cls = None
        self.setup_types_devices()

        self.tensors_rank2 = None
        self.tensors_rank3 = None
        self.tensors_rank4 = None
        self.setup_tensors()

        self.tol = self.tensors_rank2[0].dtype_eps

    @abc.abstractmethod
    def setup_seed(self):
        """Set the seed for the libraries one needs."""

    @abc.abstractmethod
    def setup_tensors(self):
        """
        Setting up some tensor examples.

        * self.tensors_rank2 (iterable)
        * self.tensors_rank3 (iterable)
        * self.tensors_rank4 (iterable)
        """

    @abc.abstractmethod
    def setup_types_devices(self):
        """
        Setting the following

        * self.dtype
        * self.device
        * self.tensor_cls
        * self.base_tensor_cls

        """

    def test_set_subtensor_entry(self):
        """Test setting a submatrix."""

        t2a = self.tensors_rank2[0]
        t2b = self.tensors_rank2[1]
        t4a = self.tensors_rank4[0]

        t4a.set_subtensor_entry([0, 0, 0, 0], [1, 2, 2, 1], t2a)
        t4a.set_subtensor_entry([1, 0, 0, 1], [2, 2, 2, 2], t2a)
        t4a.set_subtensor_entry([1, 0, 0, 0], [2, 2, 2, 1], t2b)

        reference_norm = 2 * t2a.norm() + t2b.norm()
        actual_norm = t4a.norm()
        eps = reference_norm - actual_norm

        # pylint: disable-next=no-member
        self.assertLess(eps, 10 * t2a.dtype_eps)


class _AbstractDataMover(abc.ABC):
    """
    Abstract class for moving data between different devices

    Class attributes
    ----------------
    tensor_cls : Tuple[_AbstractTensor]
        Tensor classes handled by the datamover
    """

    tensor_cls = (None,)

    @abc.abstractmethod
    def sync_move(self, tensor, device):
        """
        Move the tensor `tensor` to the device `device`
        synchronously with the main computational stream

        Parameters
        ----------
        tensor : _AbstractTensor
            The tensor to be moved
        device: str
            The device where to move the tensor
        """

    @abc.abstractmethod
    def async_move(self, tensor, device):
        """
        Move the tensor `tensor` to the device `device`
        asynchronously with respect to the main computational
        stream

        Parameters
        ----------
        tensor : _AbstractTensor
            The tensor to be moved
        device: str
            The device where to move the tensor
        """

    @abc.abstractmethod
    def wait(self):
        """
        Put a barrier for the streams and wait them
        """

    def move(self, tensor, device, sync=True):
        """
        Move the tensor `tensor` to the device `device`

        Parameters
        ----------
        tensor : _AbstractTensor
            The tensor to be moved
        device: str
            The device where to move the tensor
        sync : bool, optional
            If True, move synchronously. Otherwise asynchronously.
        """
        if sync:
            self.sync_move(tensor, device)
        else:
            self.async_move(tensor, device)

    def check_tensor_cls_compatibility(self, tensor_cls):
        """
        Check if a tensor_cls can be handled by the datamover

        Parameters
        ----------
        tensor_cls : _AbstractTensor
            The tensor class to check
        """
        if tensor_cls not in self.tensor_cls:
            raise TypeError(
                (
                    f"Tensor class {str(tensor_cls)} cannot be handled by "
                    f"datamover {str(self)}"
                )
            )


def _parse_block_size():
    """Parse block size from environment variables and return in 2 ints."""
    block_size_bond_dimension = os.environ.get("QTEA_BLOCK_SIZE_BOND_DIMENSION", None)
    block_size_byte = os.environ.get("QTEA_BLOCK_SIZE_BYTE", None)

    if block_size_bond_dimension is not None:
        block_size_bond_dimension = int(block_size_bond_dimension)
    if block_size_byte is not None:
        block_size_byte = int(block_size_byte)

    return block_size_bond_dimension, block_size_byte


# for invert link selection (avoid creating lambda function
# on every call)
_func_not_none = lambda arg: arg is not None
