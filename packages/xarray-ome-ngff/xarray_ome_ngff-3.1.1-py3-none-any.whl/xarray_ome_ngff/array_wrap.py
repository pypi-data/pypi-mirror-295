from __future__ import annotations
from typing import TYPE_CHECKING, cast, runtime_checkable, Protocol, TypedDict

from xarray_ome_ngff.core import get_store_url

if TYPE_CHECKING:
    from typing import Any, Literal
    from typing_extensions import Self

from abc import ABC, abstractmethod
from dataclasses import dataclass
from dask.array.core import Array as DaskArray
import numpy as np
import zarr


@runtime_checkable
class Arrayish(Protocol):
    dtype: np.dtype[Any]
    shape: tuple[int, ...]

    def __getitem__(self, *args: Any) -> Self: ...


class ArrayWrapperSpec(TypedDict):
    name: str
    config: dict[str, Any]


class DaskArrayWrapperConfig(TypedDict):
    """
    A model of the attributes of `DaskArrayWrapper`.
    """

    chunks: str | int | tuple[int, ...] | tuple[tuple[int, ...], ...]
    meta: Any
    inline_array: bool
    naming: Literal["auto", "array_url"]


class ZarrArrayWrapperSpec(ArrayWrapperSpec):
    # type checkers hate that the base class defines `name` to be mutable, but this is immutable.
    # this will be fixed with python allows declaring typeddict fields as read-only.
    name: Literal["zarr_array"]  # type: ignore
    config: dict[str, Any]  # type: ignore


class DaskArrayWrapperSpec(ArrayWrapperSpec):
    # type checkers hate that the base class defines `name` to be mutable, but this is immutable.
    # this will be fixed with python allows declaring typeddict fields as read-only.
    name: Literal["dask_array"]  # type: ignore
    config: DaskArrayWrapperConfig  # type: ignore


class BaseArrayWrapper(ABC):
    @abstractmethod
    def wrap(self, data: zarr.Array) -> Arrayish: ...


@dataclass
class ZarrArrayWrapper(BaseArrayWrapper):
    """
    An array wrapper that passes `zarr.Array` instances through unchanged.
    """

    def wrap(self, data: zarr.Array) -> zarr.Array:  # type: ignore
        return data


@dataclass
class DaskArrayWrapper(BaseArrayWrapper):
    """
    An array wrapper that wraps a `zarr.Array` in a dask array using `dask.array.from_array`.
    The attributes of this class are a subset of the keyword arguments to `dask.array.from_array`;
    specifically, those keyword arguments that make sense when the input to `from_array` is a
    `zarr.Array`.

    Attributes
    ----------
    chunks: str | int | tuple[int, ...]  tuple[tuple[int, ...], ...] = "auto"
        The chunks for the Dask array. See `dask.array.from_array` for details.
    meta: Any = `None`
        The array type of each chunk of the Dask array. See `dask.array.from_array` for details.
    inline_array: bool = True
        Whether slices of this array should be inlined into the Dask task graph.
        See `dask.array.from_array` for details.
    naming: "auto" | "array_url"
        The naming scheme for the Dask array. If "auto", the default, then Dask will
        name the array with a non-deterministic hash. If "array_url", then the array will be named
        according to its URL.
    """

    chunks: str | int | tuple[int, ...] | tuple[tuple[int, ...], ...] = "auto"
    meta: Any = None
    inline_array: bool = True
    naming: Literal["auto", "array_url"] = "array_url"

    def wrap(self, data: zarr.Array) -> DaskArray:  # type: ignore
        """
        Wrap the input in a dask array.
        """
        import dask.array as da  # noqa

        if self.naming == "auto":
            name = None
        elif self.naming == "array_url":
            name = f"{get_store_url(data.store)}/{data.path}"

        return da.from_array(
            data,
            chunks=self.chunks,
            inline_array=self.inline_array,
            meta=self.meta,
            name=name,
        )


def resolve_wrapper(spec: ArrayWrapperSpec) -> ZarrArrayWrapper | DaskArrayWrapper:
    """
    Convert an `ArrayWrapperSpec` into the corresponding `BaseArrayWrapper` subclass.
    """
    if spec["name"] == "dask_array":
        spec = cast(DaskArrayWrapperSpec, spec)  # type: ignore
        return DaskArrayWrapper(**spec["config"])
    elif spec["name"] == "zarr_array":
        spec = cast(ZarrArrayWrapperSpec, spec)  # type: ignore
        return ZarrArrayWrapper(**spec["config"])
    else:
        raise ValueError(f"Spec {spec} is not recognized.")


def parse_wrapper(
    data: ArrayWrapperSpec | DaskArrayWrapper | ZarrArrayWrapper,
) -> DaskArrayWrapper | ZarrArrayWrapper:
    """
    Parse the input into a `BaseArrayWrapper` subclass.

    If the input is already `BaseArrayWrapper`, it is returned as-is.
    Otherwise, the input is presumed to be `ArrayWrapperSpec` and is passed to `resolve_wrapper`.
    """
    if isinstance(data, (ZarrArrayWrapper, DaskArrayWrapper)):
        return data
    return resolve_wrapper(data)
