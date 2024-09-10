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
Tensor backend specification.
"""

# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods

import numpy as np

from .tensor import QteaTensor, DataMoverNumpyCupy

__all__ = ["TensorBackend"]


class TensorBackend:
    """
    Defines the complete tensor backend to be used. Contains the tensor class,
    the base tensor class in case it is needed for symmetric tensors, the
    target device, and the data type.

    Parameters
    ----------
    tensor_cls: _AbstractTensor, optional
        Tensor class. Might be dense or symmetric.
        Default to `QteaTensor`
    base_tensor_cls: _AbstractTensor, optional
        The dense tensor class if `tensor_cls` was symmetric.
        Same as `tensor_cls` for dense tensors.
        Default to `QteaTensor`.
    device: str, optional
        Device of the tensors. Devices available depend on `tensor_cls`.
        The possible device available are:
        - "cpu"
        - "gpu"
        - "cgpu", where the tensor network will be stored in the "cpu",
          but all the computational demanding tasks will be executed on
          the "gpu".
        Default to "cpu".
    dtype: np.dtype, optional
        Type of the tensor network. Available types depends on 'tensor_cls`.
        Default to `np.complex128`.
    symmetry_injector : class similar to `AbelianSymmetryInjector` or `None`
        Provides `inject_parse_symmetries`, `inject_trivial_symmetry`,
        and `inject_parse_sectors` for parsing symmetries and sectors
        as well as providing the trivial symmetry representation.
        Default to `None` (only valid for no symmetries).
    datamover : instance of :class:`_AbstractDataMover`
        Data mover compatible with the base_tensor_cls
        Default to :class:`DataMoverNumpyCupy`
    """

    # pylint: disable-next=too-many-arguments
    def __init__(
        self,
        tensor_cls=QteaTensor,
        base_tensor_cls=QteaTensor,
        device="cpu",
        dtype=np.complex128,
        symmetry_injector=None,
        datamover=DataMoverNumpyCupy(),
    ):
        self.tensor_cls = tensor_cls
        self.base_tensor_cls = base_tensor_cls
        self.device = device
        self.dtype = dtype
        self.datamover = datamover

        # Check the compatibility between datamover and tensor class
        self.datamover.check_tensor_cls_compatibility(base_tensor_cls)

        self._symmetry_injector = symmetry_injector

    @property
    def computational_device(self):
        """Device where the computations are done"""
        if self.device == "cgpu":
            return "gpu"

        return self.device

    @property
    def memory_device(self):
        """Device where the tensor is stored"""
        if self.device == "cgpu":
            return "cpu"

        return self.device

    def __call__(self, *args, **kwargs):
        """
        The call method is an interface to initialize tensors of the `tensor_cls`
        """
        auto = {}
        for key, value in self.tensor_cls_kwargs().items():
            if key not in kwargs:
                auto[key] = value

        return self.tensor_cls(*args, **kwargs, **auto)

    def __getstate__(self):
        """Method used to save a pickle"""
        obj = self.__dict__.copy()
        obj["datamover"] = self.datamover.__class__
        obj["_symmetry_injector"] = self._symmetry_injector.__class__
        return obj

    def __setstate__(self, state):
        """Method to load pickleed the object"""
        self.__dict__ = state
        self.datamover = self.datamover()
        self._symmetry_injector = self._symmetry_injector()

    def eye_like(self, link):
        """
        Create identity, unlike version in `_AbstractQteaTensor`, no existing
        tensor is required.

        **Arguments**

        link : same as returned by `links` property, here integer.
            Dimension of the square, identity matrix.
        """
        tmp = self.tensor_cls(
            [link, link],
            are_links_outgoing=[True, False],
            base_tensor_cls=self.base_tensor_cls,
            dtype=self.dtype,
            device=self.device,
        )

        return tmp.eye_like(link)

    def tensor_cls_kwargs(self):
        """
        Returns the keywords arguments for an `_AbstractQteaTensor`.
        """
        return {
            "base_tensor_cls": self.base_tensor_cls,
            "device": self.computational_device,
            "dtype": self.dtype,
        }

    def parse_symmetries(self, params):
        """Parse the symmetry via a function which has to be passed by the user to `__init__`."""
        if self._symmetry_injector is None:
            raise ValueError("Tensor backend is not providing parsing for symmetries.")

        return self._symmetry_injector.inject_parse_symmetries(params)

    def trivial_symmetry(self):
        """Get trivial symmetry via a function which has to be passed by the user to `__init__`."""
        if self._symmetry_injector is None:
            raise ValueError("Tensor backend is not providing trivial symmetry.")

        return self._symmetry_injector.inject_trivial_symmetry()

    def parse_sectors(self, params, sym):
        """Parse the sectors via a function which has to be passed by the user to `__init__`."""
        if self._symmetry_injector is None:
            raise ValueError("Tensor backend is not providing parsing for sectors.")

        return self._symmetry_injector.inject_parse_sectors(params, sym)
