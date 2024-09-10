from __future__ import annotations

from typing import TYPE_CHECKING, Literal
from typing_extensions import deprecated

from pydantic_ome_ngff.v04 import MultiscaleGroup
from pydantic_ome_ngff.v04.multiscale import Group

from xarray_ome_ngff.array_wrap import (
    ArrayWrapperSpec,
    DaskArrayWrapper,
    ZarrArrayWrapper,
    parse_wrapper,
)
from xarray_ome_ngff.core import get_parent

if TYPE_CHECKING:
    from typing import Any, Dict, Sequence

import os
import warnings

import numpy as np
import zarr
from numcodecs import Zstd
from numcodecs.abc import Codec
from pydantic_ome_ngff.v04.axis import Axis
from pydantic_ome_ngff.v04.multiscale import Dataset, MultiscaleMetadata
from pydantic_ome_ngff.v04.transform import (
    VectorScale,
    VectorTranslation,
)
from xarray import DataArray
from zarr.storage import BaseStore

from xarray_ome_ngff.core import CoordinateAttrs, ureg

DEFAULT_COMPRESSOR = Zstd(3)


def multiscale_metadata(
    arrays: dict[str, DataArray],
    name: str | None = None,
    type: str | None = None,
    metadata: Dict[str, Any] | None = None,
    normalize_units: bool = True,
    infer_axis_type: bool = True,
    transform_precision: int | None = None,
) -> MultiscaleMetadata:
    """
    Create version 0.4 OME-NGFF `multiscales` metadata from a dict of xarray.DataArrays.

    Parameters
    ----------

    arrays: dict[str, xarray.DataArray]
        The values of this `dict` are `xarray.DataArray` instances that each represent a separate
        scale level of a multiscale pyramid.
        The keys of this dict paths for each array in the Zarr hierarchy.
    name: str | None, default is None
        The name of the multiscale collection. Used to populate the 'name' field of
        Multiscale metadata.
    type: str | None, default is None
        The type of the multiscale collection. Used to populate the 'type' field of
        Multiscale metadata.
    metadata: dict[str, Any] | None, default is None
        Additional metadata associated with this multiscale collection. Used to populate
        the 'metadata' field of Multiscale metadata.
    normalize_units: bool, defaults is True
        Whether to normalize units to standard names, e.g. 'nm' -> 'nanometer'
    infer_axis_type: bool, defaults is True
        Whether to infer the `type` field of the axis from units, e.g. if units are
        "nanometer" then the type of the axis can safely be assumed to be "space".
        This keyword argument is ignored if `type` is not None in the array coordinate
        metadata. If axis type inference fails, `type` will be set to None.
    transform_precision: int | None, default is `None`
        Whether, and how much, to round the transformations estimated from the coordinates.
        The default (`None`) results in no rounding; specifying an `int` x will round transforms to
        x decimal places using `numpy.round(transform, x)`.

    Returns
    -------
    `MultiscaleMetadata`

    """
    keys_sorted, arrays_sorted = zip(
        *sorted(arrays.items(), key=lambda kvp: np.prod(kvp[1].shape), reverse=True)
    )

    axes, transforms = tuple(
        zip(
            *(
                transforms_from_coords(
                    array.coords,
                    normalize_units=normalize_units,
                    infer_axis_type=infer_axis_type,
                    transform_precision=transform_precision,
                )
                for array in arrays_sorted
            )
        )
    )

    datasets = tuple(
        Dataset(path=p, coordinateTransformations=t)
        for p, t in zip(keys_sorted, transforms)
    )

    return MultiscaleMetadata(
        name=name,
        type=type,
        axes=axes[0],
        datasets=datasets,
        metadata=metadata,
    )


def transforms_from_coords(
    coords: dict[str, DataArray],
    normalize_units: bool = True,
    infer_axis_type: bool = True,
    transform_precision: int | None = None,
) -> tuple[tuple[Axis, ...], tuple[VectorScale, VectorTranslation]]:
    """
    Generate Axes and CoordinateTransformations from the coordinates of an xarray.DataArray.

    Parameters
    ----------
    coords: dict[str, xarray.DataArray]
        A dict of DataArray coordinates. Scale and translation
        transform parameters are inferred from the coordinate data, per dimension.
        Note that no effort is made to ensure that the coordinates represent a regular
        grid. Axis types are inferred by querying the attributes of each
        coordinate for the 'type' key. Axis units are inferred by querying the
        attributes of each coordinate for the 'unit' key, and if that key is not present
        then the 'units' key is queried. Axis names are inferred from the dimension
        of each coordinate array.
    normalize_units: bool, default is True
        If True, unit strings will be normalized to a canonical representation using the
        `pint` library. For example, the abbreviation "nm" will be normalized to
        "nanometer".
    infer_axis_type: bool, default is True
        Whether to infer the axis type from the units. This will have no effect if
        the array has 'type' in its attrs.
    transform_precision: int | None, default is None
        Whether, and how much, to round the transformations estimated from the coordinates.
        The default (`None`) results in no rounding; specifying an `int` x will round transforms to
        x decimal places using `numpy.round(transform, x)`.

    Returns
    -------
    tuple[tuple[Axis, ...], tuple[VectorScale, VectorTranslation]]
        A tuple containing a tuple of `Axis` objects, one per dimension, and
        a tuple with a VectorScaleTransform a VectorTranslationTransform.
        Both transformations are are derived from the coordinates of the input array.
    """

    translate: tuple[float, ...] = ()
    scale: tuple[float, ...] = ()
    axes: tuple[Axis, ...] = ()

    for dim, coord in coords.items():
        if ndim := len(coord.dims) != 1:
            msg = (
                "Each coordinate must have one and only one dimension. "
                f"Got a coordinate with {ndim}."
            )
            raise ValueError(msg)
        if coord.dims != (dim,):
            msg = (
                f"Coordinate {dim} corresponds to multiple dimensions ({coord.dims}). "
                "This is incompatible with the OME-NGFF model."
            )
            raise ValueError()
        translate += (float(coord[0]),)

        # impossible to infer a scale coordinate from a coordinate with 1 sample, so it defaults
        # to 1
        if len(coord) > 1:
            scale += (abs(float(coord[1]) - float(coord[0])),)
        else:
            scale += (1,)
        units = coord.attrs.get("units", None)
        if normalize_units and units is not None:
            units = ureg.get_name(units, case_sensitive=True)
        if (type := coord.attrs.get("type", None)) is None and infer_axis_type:
            unit_dimensionality = ureg.get_dimensionality(units)
            if len(unit_dimensionality) > 1:
                msg = (
                    f'Failed to infer the type of axis with unit = "{units}"'
                    f'because it appears that unit "{units}" is a compound unit, '
                    'which cannot be mapped to a single axis type. "type" will be '
                    'set to "None" for this axis.'
                )
                warnings.warn(msg, category=RuntimeWarning)
            if "[length]" in unit_dimensionality:
                type = "space"
            elif "[time]" in unit_dimensionality:
                type = "time"

        axes += (
            Axis(
                name=dim,
                unit=units,
                type=type,
            ),
        )
    if transform_precision is not None:
        scale = tuple(np.round(scale, transform_precision).tolist())
        translate = tuple(np.round(translate, transform_precision).tolist())

    transforms = (
        VectorScale(scale=scale),
        VectorTranslation(translation=translate),
    )
    return axes, transforms


def coords_from_transforms(
    *,
    axes: Sequence[Axis],
    transforms: tuple[VectorScale, VectorTranslation],
    shape: tuple[int, ...],
) -> tuple[DataArray, ...]:
    """
    Given an output shape, convert a sequence of Axis objects and a corresponding
    sequence of coordinateTransform objects into xarray-compatible coordinates.
    """

    if len(axes) != len(shape):
        msg = (
            "Length of axes must match length of shape. "
            f"Got {len(axes)} axes but shape has {len(shape)} elements"
        )
        raise ValueError(msg)

    result = []

    for tx in transforms:
        if tx.type == "translation":
            if len(tx.translation) != len(axes):
                msg = (
                    f"Translation parameter has length {len(tx.translation)}. "
                    f"This does not match the number of axes {len(axes)}."
                )
                raise ValueError(msg)

        elif tx.type == "scale":
            if len(tx.scale) != len(axes):
                msg = (
                    f"Scale parameter has length {len(tx.scale)}. "
                    f"This does not match the number of axes {len(axes)}."
                )
                raise ValueError(msg)
        elif tx.type == "identity":
            pass
        else:
            msg = (
                f"Transform type {tx.type} not recognized. Must be one of scale, "
                "translation, or identity"
            )
            raise ValueError(msg)

    for idx, axis in enumerate(axes):
        base_coord = np.arange(shape[idx], dtype="float")
        name = axis.name
        unit = axis.unit
        # apply transforms in order
        for tx in transforms:
            if tx.type == "translation":
                base_coord += tx.translation[idx]
            elif tx.type == "scale":
                base_coord *= tx.scale[idx]
            elif tx.type == "identity":
                pass

        result.append(
            DataArray(
                base_coord,
                attrs=CoordinateAttrs(units=unit).model_dump(),
                dims=(name,),
            )
        )

    return tuple(result)


def normalize_transforms(
    base_transforms: (
        None | tuple[()] | tuple[VectorScale] | tuple[VectorScale, VectorTranslation]
    ),
    dset_transforms: tuple[VectorScale] | tuple[VectorScale, VectorTranslation],
) -> tuple[VectorScale, VectorTranslation]:
    if base_transforms is None or len(base_transforms) == 0:
        out_scale = dset_transforms[0]
        if len(dset_transforms) == 1:
            out_trans = VectorTranslation(translation=(0,) * len(out_scale.scale))
        else:
            out_trans = dset_transforms[1]
    else:
        base_scale = base_transforms[0]
        dset_scale = dset_transforms[0]
        out_scale = VectorScale(
            scale=tuple(b * d for b, d in zip(base_scale.scale, dset_scale.scale))
        )
        if len(base_transforms) == 1:
            if len(dset_transforms) == 1:
                out_trans = VectorTranslation(translation=(0,) * len(base_scale.scale))
            else:
                out_trans = dset_transforms[1]
        else:
            base_trans = base_transforms[1]
            if len(dset_transforms) == 2:
                dset_trans = dset_transforms[1]
            else:
                dset_trans = VectorTranslation(
                    translation=(0,) * len(base_trans.translation)
                )
            out_trans = VectorTranslation(
                translation=tuple(
                    b + d
                    for b, d in zip(base_trans.translation, dset_trans.translation)
                )
            )

    return out_scale, out_trans


def model_multiscale_group(
    *,
    arrays: dict[str, DataArray],
    transform_precision: int | None = None,
    chunks: tuple[int, ...] | tuple[tuple[int, ...]] | Literal["auto"] = "auto",
    compressor: Codec | None = DEFAULT_COMPRESSOR,
    fill_value: Any = 0,
) -> MultiscaleGroup:
    """
    Create a model of an OME-NGFF multiscale group from a dict of `xarray.DataArray`.
    The dimensions / coordinates of the arrays will be used to infer OME-NGFF axis metadata, as well
    as the OME-NGFF coordinate transformation metadata (i.e., scaling and translation).

    Parameters
    ----------
    arrays: dict[str, DataArray]
        A mapping from strings to `xarray.DataArray`.
    transform_precision: int | None, default is None
        Whether, and how much, to round the transformations estimated from the coordinates.
        The default (`None`) results in no rounding; if `transform_precision` is an int, then
        transforms will be rounded to `transform_precision` decimal places using `numpy.round`.
    chunks: tuple[int] | tuple[tuple[int, ...]] | Literal["auto"], default = "auto"
        The chunks for the arrays in the multiscale group.
        If the string "auto" is provided, each array will have chunks set to the zarr-python default
        value, which depends on the shape and dtype of the array.
        If a single sequence of ints is provided, then this defines the chunks for all arrays.
        If a sequence of sequences of ints is provided, then this defines the chunks for each array.
    compressor: Codec | None, default = numcodecs.ZStd.
        The compressor to use for the arrays. Default is `numcodecs.ZStd`.
    fill_value: Any
        The fill value for the Zarr arrays.
    """

    # pluralses of plurals
    axeses, transformses = tuple(
        zip(
            *(
                transforms_from_coords(
                    a.coords, transform_precision=transform_precision
                )
                for a in arrays.values()
            )
        )
    )

    if len(set(axeses)) != 1:
        msg = (
            f"Got {len(set(axeses))} unique axes from `arrays` "
            "which means that their dimensions and / or coordinates are incompatible."
        )
        raise ValueError(msg)

    group = MultiscaleGroup.from_arrays(
        arrays=tuple(arrays.values()),
        paths=tuple(arrays.keys()),
        axes=axeses[0],
        scales=[tx[0].scale for tx in transformses],
        translations=[tx[1].translation for tx in transformses],
        chunks=chunks,
        compressor=compressor,
        fill_value=fill_value,
    )
    return group


@deprecated("This function is deprecated. Use `model_multiscale_group instead.`")
def model_group(
    *,
    arrays: dict[str, DataArray],
    transform_precision: int | None = None,
    chunks: tuple[int, ...] | tuple[tuple[int, ...]] | Literal["auto"] = "auto",
    compressor: Codec | None = DEFAULT_COMPRESSOR,
    fill_value: Any = 0,
) -> Group:
    """
    Create a model of an OME-NGFF multiscale group from a dict of `xarray.DataArray`.
    The dimensions / coordinates of the arrays will be used to infer OME-NGFF axis metadata, as well
    as the OME-NGFF coordinate transformation metadata (i.e., scaling and translation).

    Parameters
    ----------
    arrays: dict[str, DataArray]
        A mapping from strings to `xarray.DataArray`.
    transform_precision: int | None, default is None
        Whether, and how much, to round the transformations estimated from the coordinates.
        The default (`None`) results in no rounding; if `transform_precision` is an int, then
        transforms will be rounded to `transform_precision` decimal places using `numpy.round`.
    chunks: tuple[int] | tuple[tuple[int, ...]] | Literal["auto"], default = "auto"
        The chunks for the arrays in the multiscale group.
        If the string "auto" is provided, each array will have chunks set to the zarr-python default
        value, which depends on the shape and dtype of the array.
        If a single sequence of ints is provided, then this defines the chunks for all arrays.
        If a sequence of sequences of ints is provided, then this defines the chunks for each array.
    compressor: Codec | None, default = numcodecs.ZStd.
        The compressor to use for the arrays. Default is `numcodecs.ZStd`.
    fill_value: Any
        The fill value for the Zarr arrays.
    """
    return model_multiscale_group(
        arrays=arrays,
        transform_precision=transform_precision,
        chunks=chunks,
        compressor=compressor,
        fill_value=fill_value,
    )


def create_multiscale_group(
    *,
    store: BaseStore,
    path: str,
    arrays: dict[str, DataArray],
    transform_precision: int | None = None,
    chunks: tuple[int, ...] | tuple[tuple[int, ...]] | Literal["auto"] = "auto",
    compressor: Codec | None = DEFAULT_COMPRESSOR,
    fill_value: Any = 0,
    overwrite: bool = False,
) -> zarr.Group:
    """
    Create Zarr group that complies with 0.4 of the OME-NGFF multiscale specification from a dict
    of `xarray.DataArray`.

    Parameters
    ----------

    store: zarr.storage.BaseStore
        The storage backend for the Zarr hierarchy.
    path: str
        The path in the storage backend for the multiscale group.
    transform_precision: int | None, default is None
        Whether, and how much, to round the transformations estimated from the coordinates.
        The default (`None`) results in no rounding; specifying an `int` x will round transforms to
        x decimal places using `numpy.round(transform, x)`.
     chunks: tuple[int] | tuple[tuple[int, ...]] | Literal["auto"], default = "auto"
        The chunks for the arrays in the multiscale group.
        If the string "auto" is provided, each array will have chunks set to the zarr-python default
        value, which depends on the shape and dtype of the array.
        If a single sequence of ints is provided, then this defines the chunks for all arrays.
        If a sequence of sequences of ints is provided, then this defines the chunks for each array.
    compressor: Codec | None, default = numcodecs.ZStd.
        The compressor to use for the arrays. Default is `numcodecs.ZStd`.
    fill_value: Any
        The fill value for the Zarr arrays.
    overwrite: bool, default = False
        Whether to overwrite an existing Zarr array or group at `path`. Default is False, which will
        result in an exception being raised if a Zarr array or group already exists at `path`.
    """

    model = model_multiscale_group(
        arrays=arrays,
        transform_precision=transform_precision,
        chunks=chunks,
        compressor=compressor,
        fill_value=fill_value,
    )
    return model.to_zarr(store, path, overwrite=overwrite)


@deprecated("This function is deprecated. Use `create_multiscale_group` instead.")
def create_group(
    *,
    store: BaseStore,
    path: str,
    arrays: dict[str, DataArray],
    transform_precision: int | None = None,
    chunks: tuple[int, ...] | tuple[tuple[int, ...]] | Literal["auto"] = "auto",
    compressor: Codec | None = DEFAULT_COMPRESSOR,
    fill_value: Any = 0,
    overwrite: bool = False,
) -> zarr.Group:
    """
    Create Zarr group that complies with 0.4 of the OME-NGFF multiscale specification from a dict
    of `xarray.DataArray`.

    Parameters
    ----------

    store: zarr.storage.BaseStore
        The storage backend for the Zarr hierarchy.
    path: str
        The path in the storage backend for the multiscale group.
    transform_precision: int | None, default is None
        Whether, and how much, to round the transformations estimated from the coordinates.
        The default (`None`) results in no rounding; specifying an `int` x will round transforms to
        x decimal places using `numpy.round(transform, x)`.
     chunks: tuple[int] | tuple[tuple[int, ...]] | Literal["auto"], default = "auto"
        The chunks for the arrays in the multiscale group.
        If the string "auto" is provided, each array will have chunks set to the zarr-python default
        value, which depends on the shape and dtype of the array.
        If a single sequence of ints is provided, then this defines the chunks for all arrays.
        If a sequence of sequences of ints is provided, then this defines the chunks for each array.
    compressor: Codec | None, default = numcodecs.ZStd.
        The compressor to use for the arrays. Default is `numcodecs.ZStd`.
    fill_value: Any
        The fill value for the Zarr arrays.
    overwrite: bool, default = False
        Whether to overwrite an existing Zarr array or group at `path`. Default is False, which will
        result in an exception being raised if a Zarr array or group already exists at `path`.
    """
    return create_multiscale_group(
        store=store,
        path=path,
        arrays=arrays,
        transform_precision=transform_precision,
        chunks=chunks,
        compressor=compressor,
        fill_value=fill_value,
        overwrite=overwrite,
    )


def read_multiscale_group(
    group: zarr.Group,
    *,
    array_wrapper: (
        ZarrArrayWrapper | DaskArrayWrapper | ArrayWrapperSpec
    ) = ZarrArrayWrapper(),
    multiscales_index: int = 0,
) -> dict[str, DataArray]:
    """
    Create a dictionary of `xarray.DataArray` from a Zarr group that implements version 0.4 of the
    OME-NGFF multiscale image specification.

    The keys of the dictionary are the paths to the Zarr arrays. The values of the dictionary are
    `xarray.DataArray` objects, one per Zarr array described in the OME-NGFF multiscale metadata,
    with dimensions and coordinates that are consistent with the OME-NGFF `Axes` and
    `coordinateTransformations` metadata.

    Parameters
    ----------
    group: zarr.Group
        A handle for the Zarr group that contains the `multiscales` metadata.
    array_wrapper: BaseArrayWrapper | ArrayWrapperSpec, default is ZarrArrayWrapper
        Either an object that implements `BaseArrayWrapper`, or a dict model of such a subclass,
        which will be resolved to an object implementing `BaseArrayWrapper`. This object has a
        `wrap` method that takes an instance of `zarr.Array` and returns another array-like object.
        This enables wrapping Zarr arrays in a lazy array representation like Dask arrays
        (e.g., via `DaskArrayWrapper), which is necessary when working with large Zarr arrays.
    multiscales_index: int, default is 0
        Version 0.4 of the OME-NGFF multiscales spec states that multiscale
        metadata is stored in a JSON array within Zarr group attributes.
        This parameter determines which element from that array to use when defining DataArrays.

    Returns
    -------
    dict[str, DataArray]
    """
    result: dict[str, DataArray] = {}
    # parse the zarr group as a multiscale group
    multiscale_group_parsed = MultiscaleGroup.from_zarr(group)
    multi_meta = multiscale_group_parsed.attributes.multiscales[multiscales_index]
    multi_tx = multi_meta.coordinateTransformations
    wrapper_parsed = parse_wrapper(array_wrapper)

    for dset in multi_meta.datasets:
        tx_fused = normalize_transforms(multi_tx, dset.coordinateTransformations)
        arr_z: zarr.Array = group[dset.path]
        arr_wrapped = wrapper_parsed.wrap(arr_z)
        coords = coords_from_transforms(
            axes=multi_meta.axes, transforms=tx_fused, shape=arr_z.shape
        )
        arr_out = DataArray(data=arr_wrapped, coords=coords)
        result[dset.path] = arr_out

    return result


@deprecated("This function is deprecated. Use `read_multiscale_group` instead.")
def read_group(
    group: zarr.Group,
    *,
    array_wrapper: (
        ZarrArrayWrapper | DaskArrayWrapper | ArrayWrapperSpec
    ) = ZarrArrayWrapper(),
    multiscales_index: int = 0,
) -> dict[str, DataArray]:
    """
    Create a dictionary of `xarray.DataArray` from a Zarr group that implements version 0.4 of the
    OME-NGFF multiscale image specification.

    The keys of the dictionary are the paths to the Zarr arrays. The values of the dictionary are
    `xarray.DataArray` objects, one per Zarr array described in the OME-NGFF multiscale metadata,
    with dimensions and coordinates that are consistent with the OME-NGFF `Axes` and
    `coordinateTransformations` metadata.

    Parameters
    ----------
    group: zarr.Group
        A handle for the Zarr group that contains the `multiscales` metadata.
    array_wrapper: BaseArrayWrapper | ArrayWrapperSpec, default is ZarrArrayWrapper
        Either an object that implements `BaseArrayWrapper`, or a dict model of such a subclass,
        which will be resolved to an object implementing `BaseArrayWrapper`. This object has a
        `wrap` method that takes an instance of `zarr.Array` and returns another array-like object.
        This enables wrapping Zarr arrays in a lazy array representation like Dask arrays
        (e.g., via `DaskArrayWrapper), which is necessary when working with large Zarr arrays.
    multiscales_index: int, default is 0
        Version 0.4 of the OME-NGFF multiscales spec states that multiscale
        metadata is stored in a JSON array within Zarr group attributes.
        This parameter determines which element from that array to use when defining DataArrays.

    Returns
    -------
    dict[str, DataArray]
    """
    return read_multiscale_group(
        group=group, array_wrapper=array_wrapper, multiscales_index=multiscales_index
    )


def read_multiscale_array(
    array: zarr.Array,
    *,
    array_wrapper: (
        ZarrArrayWrapper | DaskArrayWrapper | ArrayWrapperSpec
    ) = ZarrArrayWrapper(),
) -> DataArray:
    """
    Read a single Zarr array as an `xarray.DataArray`, using version 0.4 OME-NGFF multiscale
    metadata.

    The information necessary for creating the coordinates of the `DataArray` are not stored
    in the attributes of the Zarr array given to this function. Instead, the coordinates must
    be inferred by walking up the Zarr hierarchy, group by group, until a Zarr group with attributes
    containing OME-NGFF multiscales metadata is found; then that metadata is parsed to determine
    whether that metadata references the provided array. Once the correct multiscales metadata is
    found, the coordinates can be constructed correctly.

    Parameters
    ----------
    array: zarr.Array
        A Zarr array that is part of a version 0.4 OME-NGFF multiscale image.
    array_wrapper: ZarrArrayWrapper | DaskArrayWrapper | ArrayWrapperSpec, default is ZarrArrayWrapper
        The array wrapper class to use when converting the Zarr array to an `xarray.DataArray`.
    Returns
    -------
    xarray.DataArray
    """

    if hasattr(array.store, "path"):
        store_path = array.store.path
    else:
        store_path = ""
    path_idx_start = 0
    protocol_delimiter = ":/"
    full_path = os.path.join(store_path, array.path)
    if protocol_delimiter in full_path:
        path_idx_start = full_path.index(protocol_delimiter) + len(protocol_delimiter)

    num_parents = len(full_path[path_idx_start:].split("/"))

    wrapper = parse_wrapper(array_wrapper)
    parent = get_parent(array)
    for _ in range(num_parents):
        if hasattr(parent.store, "path"):
            parent_path = os.path.join(parent.store.path, parent.path)
        else:
            parent_path = parent.path
        array_path_rel = os.path.relpath(full_path, parent_path)
        try:
            model = MultiscaleGroup.from_zarr(parent)
            for multi in model.attributes.multiscales:
                multi_tx = multi.coordinateTransformations

                for dset in multi.datasets:
                    if dset.path == array_path_rel:
                        tx_fused = normalize_transforms(
                            multi_tx, dset.coordinateTransformations
                        )
                        coords = coords_from_transforms(
                            axes=multi.axes, transforms=tx_fused, shape=array.shape
                        )
                        arr_wrapped = wrapper.wrap(array)
                        return DataArray(arr_wrapped, coords=coords)
        except KeyError:
            parent = get_parent(parent)
    raise FileNotFoundError(
        "Could not find version 0.4 OME-NGFF multiscale metadata in any Zarr groups"
        f"ancestral to the array at {array.path}"
    )


@deprecated("This function is deprecated. Use `read_multiscale_array` instead.")
def read_array(
    array: zarr.Array,
    *,
    array_wrapper: (
        ZarrArrayWrapper | DaskArrayWrapper | ArrayWrapperSpec
    ) = ZarrArrayWrapper(),
) -> DataArray:
    """
    Read a single Zarr array as an `xarray.DataArray`, using version 0.4 OME-NGFF multiscale
    metadata.

    The information necessary for creating the coordinates of the `DataArray` are not stored
    in the attributes of the Zarr array given to this function. Instead, the coordinates must
    be inferred by walking up the Zarr hierarchy, group by group, until a Zarr group with attributes
    containing OME-NGFF multiscales metadata is found; then that metadata is parsed to determine
    whether that metadata references the provided array. Once the correct multiscales metadata is
    found, the coordinates can be constructed correctly.

    Parameters
    ----------
    array: zarr.Array
        A Zarr array that is part of a version 0.4 OME-NGFF multiscale image.
    array_wrapper: ZarrArrayWrapper | DaskArrayWrapper | ArrayWrapperSpec, default is ZarrArrayWrapper
        The array wrapper class to use when converting the Zarr array to an `xarray.DataArray`.
    Returns
    -------
    xarray.DataArray
    """

    return read_multiscale_array(array, array_wrapper=array_wrapper)
