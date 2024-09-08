from __future__ import annotations

import abc
import collections.abc
import functools
import importlib.metadata
import keyword
import re
import sys
import urllib.parse
import weakref
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple

import ibis
import ibis.common.exceptions as exc
import ibis.config
import ibis.expr.operations as ops
import ibis.expr.types as ir
from ibis import util

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Mapping, MutableMapping
    from urllib.parse import ParseResult

    import pandas as pd
    import polars as pl
    import pyarrow as pa
    import sqlglot as sg
    import torch

__all__ = ("BaseBackend", "connect")


class TablesAccessor(collections.abc.Mapping):
    """A mapping-like object for accessing tables off a backend.

    Tables may be accessed by name using either index or attribute access:

    Examples
    --------
    >>> con = ibis.sqlite.connect("example.db")
    >>> people = con.tables["people"]  # access via index
    >>> people = con.tables.people  # access via attribute
    """

    def __init__(self, backend: BaseBackend) -> None:
        self._backend = backend

    def __getitem__(self, name) -> ir.Table:
        try:
            return self._backend.table(name)
        except Exception as exc:
            raise KeyError(name) from exc

    def __getattr__(self, name) -> ir.Table:
        if name.startswith("_"):
            raise AttributeError(name)
        try:
            return self._backend.table(name)
        except Exception as exc:
            raise AttributeError(name) from exc

    def __iter__(self) -> Iterator[str]:
        return iter(sorted(self._backend.list_tables()))

    def __len__(self) -> int:
        return len(self._backend.list_tables())

    def __dir__(self) -> list[str]:
        o = set()
        o.update(dir(type(self)))
        o.update(
            name
            for name in self._backend.list_tables()
            if name.isidentifier() and not keyword.iskeyword(name)
        )
        return list(o)

    def __repr__(self) -> str:
        tables = self._backend.list_tables()
        rows = ["Tables", "------"]
        rows.extend(f"- {name}" for name in sorted(tables))
        return "\n".join(rows)

    def _ipython_key_completions_(self) -> list[str]:
        return self._backend.list_tables()


class _FileIOHandler:
    @staticmethod
    def _import_pyarrow():
        try:
            import pyarrow  # noqa: ICN001
        except ImportError:
            raise ModuleNotFoundError(
                "Exporting to arrow formats requires `pyarrow` but it is not installed"
            )
        else:
            import pyarrow_hotfix  # noqa: F401

            return pyarrow

    def to_pandas(
        self,
        expr: ir.Expr,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        limit: int | str | None = None,
        **kwargs: Any,
    ) -> pd.DataFrame | pd.Series | Any:
        """Execute an Ibis expression and return a pandas `DataFrame`, `Series`, or scalar.

        ::: {.callout-note}
        This method is a wrapper around `execute`.
        :::

        Parameters
        ----------
        expr
            Ibis expression to execute.
        params
            Mapping of scalar parameter expressions to value.
        limit
            An integer to effect a specific row limit. A value of `None` means
            "no limit". The default is in `ibis/config.py`.
        kwargs
            Keyword arguments

        """
        return self.execute(expr, params=params, limit=limit, **kwargs)

    def to_pandas_batches(
        self,
        expr: ir.Expr,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        limit: int | str | None = None,
        chunk_size: int = 1_000_000,
        **kwargs: Any,
    ) -> Iterator[pd.DataFrame | pd.Series | Any]:
        """Execute an Ibis expression and return an iterator of pandas `DataFrame`s.

        Parameters
        ----------
        expr
            Ibis expression to execute.
        params
            Mapping of scalar parameter expressions to value.
        limit
            An integer to effect a specific row limit. A value of `None` means
            "no limit". The default is in `ibis/config.py`.
        chunk_size
            Maximum number of rows in each returned `DataFrame` batch. This may have
            no effect depending on the backend.
        kwargs
            Keyword arguments

        Returns
        -------
        Iterator[pd.DataFrame]
            An iterator of pandas `DataFrame`s.

        """
        from ibis.formats.pandas import PandasData

        orig_expr = expr
        expr = expr.as_table()
        schema = expr.schema()
        yield from (
            orig_expr.__pandas_result__(
                PandasData.convert_table(batch.to_pandas(), schema)
            )
            for batch in self.to_pyarrow_batches(
                expr, params=params, limit=limit, chunk_size=chunk_size, **kwargs
            )
        )

    @util.experimental
    def to_pyarrow(
        self,
        expr: ir.Expr,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        limit: int | str | None = None,
        **kwargs: Any,
    ) -> pa.Table:
        """Execute expression and return results in as a pyarrow table.

        This method is eager and will execute the associated expression
        immediately.

        Parameters
        ----------
        expr
            Ibis expression to export to pyarrow
        params
            Mapping of scalar parameter expressions to value.
        limit
            An integer to effect a specific row limit. A value of `None` means
            "no limit". The default is in `ibis/config.py`.
        kwargs
            Keyword arguments

        Returns
        -------
        Table
            A pyarrow table holding the results of the executed expression.

        """
        pa = self._import_pyarrow()
        self._run_pre_execute_hooks(expr)

        table_expr = expr.as_table()
        schema = table_expr.schema()
        arrow_schema = schema.to_pyarrow()
        with self.to_pyarrow_batches(
            table_expr, params=params, limit=limit, **kwargs
        ) as reader:
            table = pa.Table.from_batches(reader, schema=arrow_schema)

        return expr.__pyarrow_result__(
            table.rename_columns(table_expr.columns).cast(arrow_schema)
        )

    @util.experimental
    def to_polars(
        self,
        expr: ir.Expr,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        limit: int | str | None = None,
        **kwargs: Any,
    ) -> pl.DataFrame:
        """Execute expression and return results in as a polars DataFrame.

        This method is eager and will execute the associated expression
        immediately.

        Parameters
        ----------
        expr
            Ibis expression to export to polars.
        params
            Mapping of scalar parameter expressions to value.
        limit
            An integer to effect a specific row limit. A value of `None` means
            "no limit". The default is in `ibis/config.py`.
        kwargs
            Keyword arguments

        Returns
        -------
        dataframe
            A polars DataFrame holding the results of the executed expression.

        """
        import polars as pl

        table = self.to_pyarrow(expr.as_table(), params=params, limit=limit, **kwargs)
        return expr.__polars_result__(pl.from_arrow(table))

    @util.experimental
    def to_pyarrow_batches(
        self,
        expr: ir.Expr,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        limit: int | str | None = None,
        chunk_size: int = 1_000_000,
        **kwargs: Any,
    ) -> pa.ipc.RecordBatchReader:
        """Execute expression and return a RecordBatchReader.

        This method is eager and will execute the associated expression
        immediately.

        Parameters
        ----------
        expr
            Ibis expression to export to pyarrow
        limit
            An integer to effect a specific row limit. A value of `None` means
            "no limit". The default is in `ibis/config.py`.
        params
            Mapping of scalar parameter expressions to value.
        chunk_size
            Maximum number of rows in each returned record batch.
        kwargs
            Keyword arguments

        Returns
        -------
        results
            RecordBatchReader

        """
        raise NotImplementedError

    @util.experimental
    def to_torch(
        self,
        expr: ir.Expr,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        limit: int | str | None = None,
        **kwargs: Any,
    ) -> dict[str, torch.Tensor]:
        """Execute an expression and return results as a dictionary of torch tensors.

        Parameters
        ----------
        expr
            Ibis expression to execute.
        params
            Parameters to substitute into the expression.
        limit
            An integer to effect a specific row limit. A value of `None` means no limit.
        kwargs
            Keyword arguments passed into the backend's `to_torch` implementation.

        Returns
        -------
        dict[str, torch.Tensor]
            A dictionary of torch tensors, keyed by column name.

        """
        import torch

        t = self.to_pyarrow(expr, params=params, limit=limit, **kwargs)
        # without .copy() the arrays are read-only and thus writing to them is
        # undefined behavior; we can't ignore this warning from torch because
        # we're going out of ibis and downstream code can do whatever it wants
        # with the data
        return {
            name: torch.from_numpy(t[name].to_numpy().copy()) for name in t.schema.names
        }

    def read_parquet(
        self, path: str | Path, table_name: str | None = None, **kwargs: Any
    ) -> ir.Table:
        """Register a parquet file as a table in the current backend.

        Parameters
        ----------
        path
            The data source.
        table_name
            An optional name to use for the created table. This defaults to
            a sequentially generated name.
        **kwargs
            Additional keyword arguments passed to the backend loading function.

        Returns
        -------
        ir.Table
            The just-registered table

        """
        raise NotImplementedError(
            f"{self.name} does not support direct registration of parquet data."
        )

    def read_csv(
        self, path: str | Path, table_name: str | None = None, **kwargs: Any
    ) -> ir.Table:
        """Register a CSV file as a table in the current backend.

        Parameters
        ----------
        path
            The data source. A string or Path to the CSV file.
        table_name
            An optional name to use for the created table. This defaults to
            a sequentially generated name.
        **kwargs
            Additional keyword arguments passed to the backend loading function.

        Returns
        -------
        ir.Table
            The just-registered table

        """
        raise NotImplementedError(
            f"{self.name} does not support direct registration of CSV data."
        )

    def read_json(
        self, path: str | Path, table_name: str | None = None, **kwargs: Any
    ) -> ir.Table:
        """Register a JSON file as a table in the current backend.

        Parameters
        ----------
        path
            The data source. A string or Path to the JSON file.
        table_name
            An optional name to use for the created table. This defaults to
            a sequentially generated name.
        **kwargs
            Additional keyword arguments passed to the backend loading function.

        Returns
        -------
        ir.Table
            The just-registered table

        """
        raise NotImplementedError(
            f"{self.name} does not support direct registration of JSON data."
        )

    def read_delta(
        self, source: str | Path, table_name: str | None = None, **kwargs: Any
    ):
        """Register a Delta Lake table in the current database.

        Parameters
        ----------
        source
            The data source. Must be a directory
            containing a Delta Lake table.
        table_name
            An optional name to use for the created table. This defaults to
            a sequentially generated name.
        **kwargs
            Additional keyword arguments passed to the underlying backend or library.

        Returns
        -------
        ir.Table
            The just-registered table.

        """
        raise NotImplementedError(
            f"{self.name} does not support direct registration of DeltaLake tables."
        )

    @util.experimental
    def to_parquet(
        self,
        expr: ir.Table,
        path: str | Path,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Write the results of executing the given expression to a parquet file.

        This method is eager and will execute the associated expression
        immediately.

        Parameters
        ----------
        expr
            The ibis expression to execute and persist to parquet.
        path
            The data source. A string or Path to the parquet file.
        params
            Mapping of scalar parameter expressions to value.
        **kwargs
            Additional keyword arguments passed to pyarrow.parquet.ParquetWriter

        https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetWriter.html

        """
        self._import_pyarrow()
        import pyarrow.parquet as pq

        with expr.to_pyarrow_batches(params=params) as batch_reader:
            with pq.ParquetWriter(path, batch_reader.schema, **kwargs) as writer:
                for batch in batch_reader:
                    writer.write_batch(batch)

    @util.experimental
    def to_parquet_dir(
        self,
        expr: ir.Table,
        directory: str | Path,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Write the results of executing the given expression to a parquet file in a directory.

        This method is eager and will execute the associated expression
        immediately.

        Parameters
        ----------
        expr
            The ibis expression to execute and persist to parquet.
        directory
            The data source. A string or Path to the directory where the parquet file will be written.
        params
            Mapping of scalar parameter expressions to value.
        **kwargs
            Additional keyword arguments passed to pyarrow.dataset.write_dataset

        https://arrow.apache.org/docs/python/generated/pyarrow.dataset.write_dataset.html

        """
        self._import_pyarrow()
        import pyarrow.dataset as ds

        # by default write_dataset creates the directory
        with expr.to_pyarrow_batches(params=params) as batch_reader:
            ds.write_dataset(
                batch_reader, base_dir=directory, format="parquet", **kwargs
            )

    @util.experimental
    def to_csv(
        self,
        expr: ir.Table,
        path: str | Path,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Write the results of executing the given expression to a CSV file.

        This method is eager and will execute the associated expression
        immediately.

        Parameters
        ----------
        expr
            The ibis expression to execute and persist to CSV.
        path
            The data source. A string or Path to the CSV file.
        params
            Mapping of scalar parameter expressions to value.
        kwargs
            Additional keyword arguments passed to pyarrow.csv.CSVWriter

        https://arrow.apache.org/docs/python/generated/pyarrow.csv.CSVWriter.html

        """
        self._import_pyarrow()
        import pyarrow.csv as pcsv

        with expr.to_pyarrow_batches(params=params) as batch_reader:
            with pcsv.CSVWriter(path, batch_reader.schema, **kwargs) as writer:
                for batch in batch_reader:
                    writer.write_batch(batch)

    @util.experimental
    def to_delta(
        self,
        expr: ir.Table,
        path: str | Path,
        *,
        params: Mapping[ir.Scalar, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Write the results of executing the given expression to a Delta Lake table.

        This method is eager and will execute the associated expression
        immediately.

        Parameters
        ----------
        expr
            The ibis expression to execute and persist to Delta Lake table.
        path
            The data source. A string or Path to the Delta Lake table.
        params
            Mapping of scalar parameter expressions to value.
        kwargs
            Additional keyword arguments passed to deltalake.writer.write_deltalake method

        """
        try:
            from deltalake.writer import write_deltalake
        except ImportError:
            raise ImportError(
                "The deltalake extra is required to use the "
                "to_delta method. You can install it using pip:\n\n"
                "pip install 'ibis-framework[deltalake]'\n"
            )

        with expr.to_pyarrow_batches(params=params) as batch_reader:
            write_deltalake(path, batch_reader, **kwargs)


class CanListCatalog(abc.ABC):
    @abc.abstractmethod
    def list_catalogs(self, like: str | None = None) -> list[str]:
        """List existing catalogs in the current connection.

        ::: {.callout-note}
        ## Ibis does not use the word `schema` to refer to database hierarchy.

        A collection of `table` is referred to as a `database`.
        A collection of `database` is referred to as a `catalog`.

        These terms are mapped onto the corresponding features in each
        backend (where available), regardless of whether the backend itself
        uses the same terminology.
        :::

        Parameters
        ----------
        like
            A pattern in Python's regex format to filter returned database
            names.

        Returns
        -------
        list[str]
            The catalog names that exist in the current connection, that match
            the `like` pattern if provided.

        """


class CanCreateCatalog(CanListCatalog):
    @abc.abstractmethod
    def create_catalog(self, name: str, force: bool = False) -> None:
        """Create a new catalog.

        ::: {.callout-note}
        ## Ibis does not use the word `schema` to refer to database hierarchy.

        A collection of `table` is referred to as a `database`.
        A collection of `database` is referred to as a `catalog`.

        These terms are mapped onto the corresponding features in each
        backend (where available), regardless of whether the backend itself
        uses the same terminology.
        :::

        Parameters
        ----------
        name
            Name of the new catalog.
        force
            If `False`, an exception is raised if the catalog already exists.

        """

    @abc.abstractmethod
    def drop_catalog(self, name: str, force: bool = False) -> None:
        """Drop a catalog with name `name`.

        ::: {.callout-note}
        ## Ibis does not use the word `schema` to refer to database hierarchy.

        A collection of `table` is referred to as a `database`.
        A collection of `database` is referred to as a `catalog`.

        These terms are mapped onto the corresponding features in each
        backend (where available), regardless of whether the backend itself
        uses the same terminology.
        :::

        Parameters
        ----------
        name
            Catalog to drop.
        force
            If `False`, an exception is raised if the catalog does not exist.

        """


class CanListDatabase(abc.ABC):
    @abc.abstractmethod
    def list_databases(
        self, like: str | None = None, catalog: str | None = None
    ) -> list[str]:
        """List existing databases in the current connection.

        ::: {.callout-note}
        ## Ibis does not use the word `schema` to refer to database hierarchy.

        A collection of `table` is referred to as a `database`.
        A collection of `database` is referred to as a `catalog`.

        These terms are mapped onto the corresponding features in each
        backend (where available), regardless of whether the backend itself
        uses the same terminology.
        :::

        Parameters
        ----------
        like
            A pattern in Python's regex format to filter returned database
            names.
        catalog
            The catalog to list databases from. If `None`, the current catalog
            is searched.

        Returns
        -------
        list[str]
            The database names that exist in the current connection, that match
            the `like` pattern if provided.

        """


class CanCreateDatabase(CanListDatabase):
    @abc.abstractmethod
    def create_database(
        self, name: str, catalog: str | None = None, force: bool = False
    ) -> None:
        """Create a database named `name` in `catalog`.

        Parameters
        ----------
        name
            Name of the database to create.
        catalog
            Name of the catalog in which to create the database. If `None`, the
            current catalog is used.
        force
            If `False`, an exception is raised if the database exists.

        """

    @abc.abstractmethod
    def drop_database(
        self, name: str, catalog: str | None = None, force: bool = False
    ) -> None:
        """Drop the database with `name` in `catalog`.

        Parameters
        ----------
        name
            Name of the schema to drop.
        catalog
            Name of the catalog to drop the database from. If `None`, the
            current catalog is used.
        force
            If `False`, an exception is raised if the database does not exist.

        """


# TODO: remove this for 10.0
class CanListSchema:
    @util.deprecated(
        instead="Use `list_databases` instead`", as_of="9.0", removed_in="10.0"
    )
    def list_schemas(
        self, like: str | None = None, database: str | None = None
    ) -> list[str]:
        return self.list_databases(like=like, catalog=database)

    @property
    @util.deprecated(
        instead="Use `Backend.current_database` instead.",
        as_of="9.0",
        removed_in="10.0",
    )
    def current_schema(self) -> str:
        return self.current_database


class CanCreateSchema(CanListSchema):
    @util.deprecated(
        instead="Use `create_database` instead", as_of="9.0", removed_in="10.0"
    )
    def create_schema(
        self, name: str, database: str | None = None, force: bool = False
    ) -> None:
        self.create_database(name=name, catalog=database, force=force)

    @util.deprecated(
        instead="Use `drop_database` instead", as_of="9.0", removed_in="10.0"
    )
    def drop_schema(
        self, name: str, database: str | None = None, force: bool = False
    ) -> None:
        self.drop_database(name=name, catalog=database, force=force)


class CacheEntry(NamedTuple):
    orig_op: ops.Relation
    cached_op_ref: weakref.ref[ops.Relation]
    finalizer: weakref.finalize


class CacheHandler:
    """A mixin for handling `.cache()`/`CachedTable` operations."""

    def __init__(self):
        self._cache_name_to_entry = {}
        self._cache_op_to_entry = {}

    def _cached_table(self, table: ir.Table) -> ir.CachedTable:
        """Convert a Table to a CachedTable.

        Parameters
        ----------
        table
            Table expression to cache

        Returns
        -------
        Table
            Cached table
        """
        entry = self._cache_op_to_entry.get(table.op())
        if entry is None or (cached_op := entry.cached_op_ref()) is None:
            cached_op = self._create_cached_table(util.gen_name("cached"), table).op()
            entry = CacheEntry(
                table.op(),
                weakref.ref(cached_op),
                weakref.finalize(
                    cached_op, self._finalize_cached_table, cached_op.name
                ),
            )
            self._cache_op_to_entry[table.op()] = entry
            self._cache_name_to_entry[cached_op.name] = entry
        return ir.CachedTable(cached_op)

    def _finalize_cached_table(self, name: str) -> None:
        """Release a cached table given its name.

        This is a no-op if the cached table is already released.

        Parameters
        ----------
        name
            The name of the cached table.
        """
        if (entry := self._cache_name_to_entry.pop(name, None)) is not None:
            self._cache_op_to_entry.pop(entry.orig_op)
            entry.finalizer.detach()
            try:
                self._drop_cached_table(name)
            except Exception:
                # suppress exceptions during interpreter shutdown
                if not sys.is_finalizing():
                    raise

    def _create_cached_table(self, name: str, expr: ir.Table) -> ir.Table:
        return self.create_table(name, expr, schema=expr.schema(), temp=True)

    def _drop_cached_table(self, name: str) -> None:
        self.drop_table(name, force=True)


class BaseBackend(abc.ABC, _FileIOHandler, CacheHandler):
    """Base backend class.

    All Ibis backends must subclass this class and implement all the
    required methods.
    """

    name: ClassVar[str]

    supports_temporary_tables = False
    supports_python_udfs = False
    supports_in_memory_tables = True

    def __init__(self, *args, **kwargs):
        self._con_args: tuple[Any] = args
        self._con_kwargs: dict[str, Any] = kwargs
        self._can_reconnect: bool = True
        super().__init__()

    @property
    @abc.abstractmethod
    def dialect(self) -> sg.Dialect | None:
        """The sqlglot dialect for this backend, where applicable.

        Returns None if the backend is not a SQL backend.
        """

    def __getstate__(self):
        return dict(_con_args=self._con_args, _con_kwargs=self._con_kwargs)

    def __rich_repr__(self):
        yield "name", self.name

    def __hash__(self):
        return hash(self.db_identity)

    def __eq__(self, other):
        return self.db_identity == other.db_identity

    @functools.cached_property
    def db_identity(self) -> str:
        """Return the identity of the database.

        Multiple connections to the same
        database will return the same value for `db_identity`.

        The default implementation assumes connection parameters uniquely
        specify the database.

        Returns
        -------
        Hashable
            Database identity

        """
        parts = [self.__class__]
        parts.extend(self._con_args)
        parts.extend(f"{k}={v}" for k, v in self._con_kwargs.items())
        return "_".join(map(str, parts))

    # TODO(kszucs): this should be a classmethod returning with a new backend
    # instance which does instantiate the connection
    def connect(self, *args, **kwargs) -> BaseBackend:
        """Connect to the database.

        Parameters
        ----------
        *args
            Mandatory connection parameters, see the docstring of `do_connect`
            for details.
        **kwargs
            Extra connection parameters, see the docstring of `do_connect` for
            details.

        Notes
        -----
        This creates a new backend instance with saved `args` and `kwargs`,
        then calls `reconnect` and finally returns the newly created and
        connected backend instance.

        Returns
        -------
        BaseBackend
            An instance of the backend

        """
        new_backend = self.__class__(*args, **kwargs)
        new_backend.reconnect()
        return new_backend

    @abc.abstractmethod
    def disconnect(self) -> None:
        """Close the connection to the backend."""

    @staticmethod
    def _convert_kwargs(kwargs: MutableMapping) -> None:
        """Manipulate keyword arguments to `.connect` method."""

    # TODO(kszucs): should call self.connect(*self._con_args, **self._con_kwargs)
    def reconnect(self) -> None:
        """Reconnect to the database already configured with connect."""
        if self._can_reconnect:
            self.do_connect(*self._con_args, **self._con_kwargs)
        else:
            raise exc.IbisError("Cannot reconnect to unconfigured {self.name} backend")

    def do_connect(self, *args, **kwargs) -> None:
        """Connect to database specified by `args` and `kwargs`."""

    @staticmethod
    def _filter_with_like(values: Iterable[str], like: str | None = None) -> list[str]:
        """Filter names with a `like` pattern (regex).

        The methods `list_databases` and `list_tables` accept a `like`
        argument, which filters the returned tables with tables that match the
        provided pattern.

        We provide this method in the base backend, so backends can use it
        instead of reinventing the wheel.

        Parameters
        ----------
        values
            Iterable of strings to filter
        like
            Pattern to use for filtering names

        Returns
        -------
        list[str]
            Names filtered by the `like` pattern.

        """
        if like is None:
            return sorted(values)

        pattern = re.compile(like)
        return sorted(filter(pattern.findall, values))

    @abc.abstractmethod
    def list_tables(
        self, like: str | None = None, database: tuple[str, str] | str | None = None
    ) -> list[str]:
        """Return the list of table names in the current database.

        For some backends, the tables may be files in a directory,
        or other equivalent entities in a SQL database.

        ::: {.callout-note}
        ## Ibis does not use the word `schema` to refer to database hierarchy.

        A collection of tables is referred to as a `database`.
        A collection of `database` is referred to as a `catalog`.

        These terms are mapped onto the corresponding features in each
        backend (where available), regardless of whether the backend itself
        uses the same terminology.
        :::

        Parameters
        ----------
        like
            A pattern in Python's regex format.
        database
            The database from which to list tables.
            If not provided, the current database is used.
            For backends that support multi-level table hierarchies, you can
            pass in a dotted string path like `"catalog.database"` or a tuple of
            strings like `("catalog", "database")`.

        Returns
        -------
        list[str]
            The list of the table names that match the pattern `like`.

        """

    @abc.abstractmethod
    def table(
        self, name: str, database: tuple[str, str] | str | None = None
    ) -> ir.Table:
        """Construct a table expression.

        ::: {.callout-note}
        ## Ibis does not use the word `schema` to refer to database hierarchy.

        A collection of tables is referred to as a `database`.
        A collection of `database` is referred to as a `catalog`.

        These terms are mapped onto the corresponding features in each
        backend (where available), regardless of whether the backend itself
        uses the same terminology.
        :::

        Parameters
        ----------
        name
            Table name
        database
            Database name
            If not provided, the current database is used.
            For backends that support multi-level table hierarchies, you can
            pass in a dotted string path like `"catalog.database"` or a tuple of
            strings like `("catalog", "database")`.

        Returns
        -------
        Table
            Table expression

        """

    @property
    def tables(self):
        """An accessor for tables in the database.

        Tables may be accessed by name using either index or attribute access:

        Examples
        --------
        >>> con = ibis.sqlite.connect("example.db")
        >>> people = con.tables["people"]  # access via index
        >>> people = con.tables.people  # access via attribute

        """
        return TablesAccessor(self)

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """Return the version of the backend engine.

        For database servers, return the server version.

        For others such as SQLite and pandas return the version of the
        underlying library or application.

        Returns
        -------
        str
            The backend version

        """

    @classmethod
    def register_options(cls) -> None:
        """Register custom backend options."""
        options = ibis.config.options
        backend_name = cls.name
        try:
            backend_options = cls.Options()
        except AttributeError:
            pass
        else:
            try:
                setattr(options, backend_name, backend_options)
            except ValueError as e:
                raise exc.BackendConfigurationNotRegistered(backend_name) from e

    def _register_udfs(self, expr: ir.Expr) -> None:
        """Register UDFs contained in `expr` with the backend."""
        if self.supports_python_udfs:
            raise NotImplementedError(self.name)

    def _register_in_memory_tables(self, expr: ir.Expr) -> None:
        for memtable in expr.op().find(ops.InMemoryTable):
            self._register_in_memory_table(memtable)

    def _register_in_memory_table(self, op: ops.InMemoryTable):
        if self.supports_in_memory_tables:
            raise NotImplementedError(
                f"{self.name} must implement `_register_in_memory_table` to support in-memory tables"
            )

    def _run_pre_execute_hooks(self, expr: ir.Expr) -> None:
        """Backend-specific hooks to run before an expression is executed."""
        self._register_udfs(expr)
        self._register_in_memory_tables(expr)

    def compile(
        self,
        expr: ir.Expr,
        params: Mapping[ir.Expr, Any] | None = None,
    ) -> Any:
        """Compile an expression."""
        return self.compiler.to_sql(expr, params=params)

    def execute(self, expr: ir.Expr) -> Any:
        """Execute an expression."""

    @abc.abstractmethod
    def create_table(
        self,
        name: str,
        obj: pd.DataFrame | pa.Table | ir.Table | None = None,
        *,
        schema: ibis.Schema | None = None,
        database: str | None = None,
        temp: bool = False,
        overwrite: bool = False,
    ) -> ir.Table:
        """Create a new table.

        Parameters
        ----------
        name
            Name of the new table.
        obj
            An Ibis table expression or pandas table that will be used to
            extract the schema and the data of the new table. If not provided,
            `schema` must be given.
        schema
            The schema for the new table. Only one of `schema` or `obj` can be
            provided.
        database
            Name of the database where the table will be created, if not the
            default.
        temp
            Whether a table is temporary or not
        overwrite
            Whether to clobber existing data

        Returns
        -------
        Table
            The table that was created.

        """

    @abc.abstractmethod
    def drop_table(
        self,
        name: str,
        *,
        database: str | None = None,
        force: bool = False,
    ) -> None:
        """Drop a table.

        Parameters
        ----------
        name
            Name of the table to drop.
        database
            Name of the database where the table exists, if not the default.
        force
            If `False`, an exception is raised if the table does not exist.

        """
        raise NotImplementedError(
            f'Backend "{self.name}" does not implement "drop_table"'
        )

    def rename_table(self, old_name: str, new_name: str) -> None:
        """Rename an existing table.

        Parameters
        ----------
        old_name
            The old name of the table.
        new_name
            The new name of the table.

        """
        raise NotImplementedError(
            f'Backend "{self.name}" does not implement "rename_table"'
        )

    @abc.abstractmethod
    def create_view(
        self,
        name: str,
        obj: ir.Table,
        *,
        database: str | None = None,
        overwrite: bool = False,
    ) -> ir.Table:
        """Create a new view from an expression.

        Parameters
        ----------
        name
            Name of the new view.
        obj
            An Ibis table expression that will be used to create the view.
        database
            Name of the database where the view will be created, if not
            provided the database's default is used.
        overwrite
            Whether to clobber an existing view with the same name

        Returns
        -------
        Table
            The view that was created.

        """

    @abc.abstractmethod
    def drop_view(
        self, name: str, *, database: str | None = None, force: bool = False
    ) -> None:
        """Drop a view.

        Parameters
        ----------
        name
            Name of the view to drop.
        database
            Name of the database where the view exists, if not the default.
        force
            If `False`, an exception is raised if the view does not exist.

        """

    @classmethod
    def has_operation(cls, operation: type[ops.Value]) -> bool:
        """Return whether the backend implements support for `operation`.

        Parameters
        ----------
        operation
            A class corresponding to an operation.

        Returns
        -------
        bool
            Whether the backend implements the operation.

        Examples
        --------
        >>> import ibis
        >>> import ibis.expr.operations as ops
        >>> ibis.sqlite.has_operation(ops.ArrayIndex)
        False
        >>> ibis.postgres.has_operation(ops.ArrayIndex)
        True

        """
        raise NotImplementedError(
            f"{cls.name} backend has not implemented `has_operation` API"
        )

    def _transpile_sql(self, query: str, *, dialect: str | None = None) -> str:
        # only transpile if dialect was passed
        if dialect is None:
            return query

        import sqlglot as sg

        # only transpile if the backend dialect doesn't match the input dialect
        name = self.name
        if (output_dialect := self.dialect) is None:
            raise NotImplementedError(f"No known sqlglot dialect for backend {name}")

        if dialect != output_dialect:
            (query,) = sg.transpile(query, read=dialect, write=output_dialect)
        return query


@functools.cache
def _get_backend_names(*, exclude: tuple[str] = ()) -> frozenset[str]:
    """Return the set of known backend names.

    Parameters
    ----------
    exclude
        Exclude these backend names from the result

    Notes
    -----
    This function returns a frozenset to prevent cache pollution.

    If a `set` is used, then any in-place modifications to the set
    are visible to every caller of this function.

    """

    entrypoints = importlib.metadata.entry_points(group="ibis.backends")
    return frozenset(ep.name for ep in entrypoints).difference(exclude)


def connect(resource: Path | str, **kwargs: Any) -> BaseBackend:
    """Connect to `resource`, inferring the backend automatically.

    The general pattern for `ibis.connect` is

    ```python
    con = ibis.connect("backend://connection-parameters")
    ```

    With many backends that looks like

    ```python
    con = ibis.connect("backend://user:password@host:port/database")
    ```

    See the connection syntax for each backend for details about URL connection
    requirements.

    Parameters
    ----------
    resource
        A URL or path to the resource to be connected to.
    kwargs
        Backend specific keyword arguments

    Examples
    --------
    Connect to an in-memory DuckDB database:

    >>> import ibis
    >>> con = ibis.connect("duckdb://")

    Connect to an on-disk SQLite database:

    >>> con = ibis.connect("sqlite://relative.db")
    >>> con = ibis.connect(
    ...     "sqlite:///absolute/path/to/data.db"
    ... )  # quartodoc: +SKIP # doctest: +SKIP

    Connect to a PostgreSQL server:

    >>> con = ibis.connect(
    ...     "postgres://user:password@hostname:5432"
    ... )  # quartodoc: +SKIP # doctest: +SKIP

    Connect to BigQuery:

    >>> con = ibis.connect(
    ...     "bigquery://my-project/my-dataset"
    ... )  # quartodoc: +SKIP # doctest: +SKIP

    """
    url = resource = str(resource)

    if re.match("[A-Za-z]:", url):
        # windows path with drive, treat it as a file
        url = f"file://{url}"

    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme or "file"

    orig_kwargs = kwargs.copy()
    kwargs = dict(urllib.parse.parse_qsl(parsed.query))

    # convert single parameter lists value to single values
    for name, value in kwargs.items():
        if len(value) == 1:
            kwargs[name] = value[0]

    # Merge explicit kwargs with query string, explicit kwargs
    # taking precedence
    kwargs.update(orig_kwargs)

    if scheme == "file":
        path = parsed.netloc + parsed.path
        if path.endswith(".duckdb"):
            return ibis.duckdb.connect(path, **kwargs)
        elif path.endswith((".sqlite", ".db")):
            return ibis.sqlite.connect(path, **kwargs)
        elif path.endswith((".parquet", ".csv", ".csv.gz")):
            # Load parquet/csv/csv.gz files with duckdb by default
            con = ibis.duckdb.connect(**kwargs)
            con.register(path)
            return con
        else:
            raise ValueError(f"Don't know how to connect to {resource!r}")

    # Treat `postgres://` and `postgresql://` the same
    scheme = scheme.replace("postgresql", "postgres")

    try:
        backend = getattr(ibis, scheme)
    except AttributeError:
        raise ValueError(f"Don't know how to connect to {resource!r}") from None

    return backend._from_url(parsed, **kwargs)


class UrlFromPath:
    __slots__ = ()

    def _from_url(self, url: ParseResult, **kwargs: Any) -> BaseBackend:
        """Connect to a backend using a URL `url`.

        Parameters
        ----------
        url
            URL with which to connect to a backend.
        kwargs
            Additional keyword arguments

        Returns
        -------
        BaseBackend
            A backend instance

        """
        netloc = url.netloc
        parts = list(filter(None, (netloc, url.path[bool(netloc) :])))
        database = Path(*parts) if parts and parts != [":memory:"] else ":memory:"
        if (strdatabase := str(database)).startswith("md:") or strdatabase.startswith(
            "motherduck:"
        ):
            database = strdatabase
        elif isinstance(database, Path):
            database = database.absolute()

        self._convert_kwargs(kwargs)
        return self.connect(database=database, **kwargs)


class NoUrl:
    __slots__ = ()

    name: str

    def _from_url(self, url: ParseResult, **kwargs) -> BaseBackend:
        """Connect to the backend with empty url.

        Parameters
        ----------
        url : str
            The URL with which to connect to the backend. This parameter is not used
            in this method but is kept for consistency.
        kwargs
            Additional keyword arguments.

        Returns
        -------
        BaseBackend
            A backend instance

        """
        return self.connect(**kwargs)
