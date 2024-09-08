from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any

from public import public

import ibis
import ibis.common.exceptions as com
import ibis.expr.builders as bl
import ibis.expr.datatypes as dt
import ibis.expr.operations as ops
from ibis.common.deferred import Deferred, _, deferrable
from ibis.common.grounds import Singleton
from ibis.expr.rewrites import rewrite_window_input
from ibis.expr.types.core import Expr, _binop, _FixedTextJupyterMixin, _is_null_literal
from ibis.util import deprecated, promote_list, warn_deprecated

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl
    import pyarrow as pa
    import rich.table

    import ibis.expr.schema as sch
    import ibis.expr.types as ir
    from ibis.formats.pandas import PandasData
    from ibis.formats.pyarrow import PyArrowData


@public
class Value(Expr):
    """Base class for a data generating expression having a known type."""

    def name(self, name):
        """Rename an expression to `name`.

        Parameters
        ----------
        name
            The new name of the expression

        Returns
        -------
        Value
            `self` with name `name`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"a": [1, 2]}, name="t")
        >>> t.a
        ┏━━━━━━━┓
        ┃ a     ┃
        ┡━━━━━━━┩
        │ int64 │
        ├───────┤
        │     1 │
        │     2 │
        └───────┘
        >>> t.a.name("b")
        ┏━━━━━━━┓
        ┃ b     ┃
        ┡━━━━━━━┩
        │ int64 │
        ├───────┤
        │     1 │
        │     2 │
        └───────┘
        """
        # TODO(kszucs): shouldn't do simplification here, but rather later
        # when simplifying the whole operation tree
        # the expression's name is idendical to the new one
        if self.get_name() == name:
            return self

        if isinstance(self.op(), ops.Alias):
            # only keep a single alias operation
            op = ops.Alias(arg=self.op().arg, name=name)
        else:
            op = ops.Alias(arg=self, name=name)

        return op.to_expr()

    # TODO(kszucs): should rename to dtype
    def type(self) -> dt.DataType:
        """Return the [DataType](./datatypes.qmd) of `self`."""
        return self.op().dtype

    def hash(self) -> ir.IntegerValue:
        """Compute an integer hash value.

        ::: {.callout-note}
        ## The hashing function used is backend-dependent.
        :::

        Returns
        -------
        IntegerValue
            The hash value of `self`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> ibis.literal("hello").hash()  # doctest: +SKIP
        -4155090522938856779
        """
        return ops.Hash(self).to_expr()

    def cast(self, target_type: Any) -> Value:
        """Cast expression to indicated data type.

        Similar to `pandas.Series.astype`.

        Parameters
        ----------
        target_type
            Type to cast to. Anything accepted by [`ibis.dtype()`](./datatypes.qmd#ibis.dtype)

        Returns
        -------
        Value
            Casted expression

        See Also
        --------
        [`Value.try_cast()`](./expression-generic.qmd#ibis.expr.types.generic.Value.try_cast)
        [`ibis.dtype()`](./datatypes.qmd#ibis.dtype)

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> x = ibis.examples.penguins.fetch()["bill_depth_mm"]
        >>> x
        ┏━━━━━━━━━━━━━━━┓
        ┃ bill_depth_mm ┃
        ┡━━━━━━━━━━━━━━━┩
        │ float64       │
        ├───────────────┤
        │          18.7 │
        │          17.4 │
        │          18.0 │
        │          NULL │
        │          19.3 │
        │          20.6 │
        │          17.8 │
        │          19.6 │
        │          18.1 │
        │          20.2 │
        │             … │
        └───────────────┘

        python's built-in types can be used

        >>> x.cast(int)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Cast(bill_depth_mm, int64) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ int64                      │
        ├────────────────────────────┤
        │                         19 │
        │                         17 │
        │                         18 │
        │                       NULL │
        │                         19 │
        │                         21 │
        │                         18 │
        │                         20 │
        │                         18 │
        │                         20 │
        │                          … │
        └────────────────────────────┘

        or string names

        >>> x.cast("uint16")
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Cast(bill_depth_mm, uint16) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ uint16                      │
        ├─────────────────────────────┤
        │                          19 │
        │                          17 │
        │                          18 │
        │                        NULL │
        │                          19 │
        │                          21 │
        │                          18 │
        │                          20 │
        │                          18 │
        │                          20 │
        │                           … │
        └─────────────────────────────┘

        If you make an illegal cast, you won't know until the backend actually
        executes it. Consider [`.try_cast()`](#ibis.expr.types.generic.Value.try_cast).

        >>> ibis.literal("a string").cast("int64")  # doctest: +SKIP
        <error>
        """
        op = ops.Cast(self, to=target_type)

        if op.to == self.type():
            # noop case if passed type is the same
            return self

        if op.to.is_geospatial() and not self.type().is_binary():
            from_geotype = self.type().geotype or "geometry"
            to_geotype = op.to.geotype
            if from_geotype == to_geotype:
                return self

        return op.to_expr()

    def try_cast(self, target_type: Any) -> Value:
        """Try cast expression to indicated data type.

        If the cast fails for a row, the value is returned
        as null or NaN depending on target_type and backend behavior.

        Parameters
        ----------
        target_type
            Type to try cast to. Anything accepted by [`ibis.dtype()`](./datatypes.qmd#ibis.dtype)

        Returns
        -------
        Value
            Casted expression

        See Also
        --------
        [`Value.cast()`](./expression-generic.qmd#ibis.expr.types.generic.Value.cast)
        [`ibis.dtype()`](./datatypes.qmd#ibis.dtype)

        Examples
        --------
        >>> import ibis
        >>> from ibis import _
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"numbers": [1, 2, 3, 4], "strings": ["1.0", "2", "hello", "world"]})
        >>> t
        ┏━━━━━━━━━┳━━━━━━━━━┓
        ┃ numbers ┃ strings ┃
        ┡━━━━━━━━━╇━━━━━━━━━┩
        │ int64   │ string  │
        ├─────────┼─────────┤
        │       1 │ 1.0     │
        │       2 │ 2       │
        │       3 │ hello   │
        │       4 │ world   │
        └─────────┴─────────┘
        >>> t = t.mutate(numbers_to_strings=_.numbers.try_cast("string"))
        >>> t = t.mutate(strings_to_numbers=_.strings.try_cast("int"))
        >>> t
        ┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
        ┃ numbers ┃ strings ┃ numbers_to_strings ┃ strings_to_numbers ┃
        ┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
        │ int64   │ string  │ string             │ int64              │
        ├─────────┼─────────┼────────────────────┼────────────────────┤
        │       1 │ 1.0     │ 1                  │                  1 │
        │       2 │ 2       │ 2                  │                  2 │
        │       3 │ hello   │ 3                  │               NULL │
        │       4 │ world   │ 4                  │               NULL │
        └─────────┴─────────┴────────────────────┴────────────────────┘
        """
        op = ops.TryCast(self, to=target_type)

        if op.to == self.type():
            # noop case if passed type is the same
            return self

        return op.to_expr()

    def coalesce(self, *args: Value) -> Value:
        """Return the first non-null value from `args`.

        Parameters
        ----------
        args
            Arguments from which to choose the first non-null value

        Returns
        -------
        Value
            Coalesced expression

        See Also
        --------
        [`ibis.coalesce()`](./expression-generic.qmd#ibis.coalesce)
        [`Value.fill_null()`](./expression-generic.qmd#ibis.expr.types.generic.Value.fill_null)

        Examples
        --------
        >>> import ibis
        >>> ibis.coalesce(None, 4, 5).name("x")
        x: Coalesce(...)
        """
        return ops.Coalesce((self, *args)).to_expr()

    @deprecated(as_of="8.0.0", instead="use ibis.greatest(self, rest...) instead")
    def greatest(self, *args: ir.Value) -> ir.Value:
        return ops.Greatest((self, *args)).to_expr()

    @deprecated(as_of="8.0.0", instead="use ibis.least(self, rest...) instead")
    def least(self, *args: ir.Value) -> ir.Value:
        return ops.Least((self, *args)).to_expr()

    def typeof(self) -> ir.StringValue:
        """Return the string name of the datatype of self.

        The values of the returned strings are necessarily backend dependent.
        e.g. duckdb may say "DOUBLE", while sqlite may say "real".

        Returns
        -------
        StringValue
            A string indicating the type of the value

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> vals = ibis.examples.penguins.fetch().head(5).bill_length_mm
        >>> vals
        ┏━━━━━━━━━━━━━━━━┓
        ┃ bill_length_mm ┃
        ┡━━━━━━━━━━━━━━━━┩
        │ float64        │
        ├────────────────┤
        │           39.1 │
        │           39.5 │
        │           40.3 │
        │           NULL │
        │           36.7 │
        └────────────────┘
        >>> vals.typeof()
        ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ TypeOf(bill_length_mm) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ string                 │
        ├────────────────────────┤
        │ DOUBLE                 │
        │ DOUBLE                 │
        │ DOUBLE                 │
        │ DOUBLE                 │
        │ DOUBLE                 │
        └────────────────────────┘

        Different backends have different names for their native types

        >>> ibis.duckdb.connect().execute(ibis.literal(5.4).typeof())
        'DECIMAL(2,1)'
        >>> ibis.sqlite.connect().execute(ibis.literal(5.4).typeof())
        'real'
        """
        return ops.TypeOf(self).to_expr()

    def fill_null(self, fill_value: Scalar) -> Value:
        """Replace any null values with the indicated fill value.

        Parameters
        ----------
        fill_value
            Value with which to replace `NULL` values in `self`

        See Also
        --------
        [`Value.coalesce()`](./expression-generic.qmd#ibis.expr.types.generic.Value.coalesce)
        [`ibis.coalesce()`](./expression-generic.qmd#ibis.coalesce)

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch().limit(5)
        >>> t.sex
        ┏━━━━━━━━┓
        ┃ sex    ┃
        ┡━━━━━━━━┩
        │ string │
        ├────────┤
        │ male   │
        │ female │
        │ female │
        │ NULL   │
        │ female │
        └────────┘
        >>> t.sex.fill_null("unrecorded").name("sex")
        ┏━━━━━━━━━━━━┓
        ┃ sex        ┃
        ┡━━━━━━━━━━━━┩
        │ string     │
        ├────────────┤
        │ male       │
        │ female     │
        │ female     │
        │ unrecorded │
        │ female     │
        └────────────┘

        Returns
        -------
        Value
            `self` filled with `fill_value` where it is `NULL`
        """
        return ops.Coalesce((self, fill_value)).to_expr()

    @deprecated(as_of="9.1", instead="use fill_null instead")
    def fillna(self, fill_value: Scalar) -> Value:
        """Deprecated - use `fill_null` instead."""
        return self.fill_null(fill_value)

    def nullif(self, null_if_expr: Value) -> Value:
        """Set values to null if they equal the values `null_if_expr`.

        Commonly used to avoid divide-by-zero problems by replacing zero with
        `NULL` in the divisor.

        Equivalent to `(self == null_if_expr).ifelse(ibis.null(), self)`.

        Parameters
        ----------
        null_if_expr
            Expression indicating what values should be NULL

        Returns
        -------
        Value
            Value expression

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> vals = ibis.examples.penguins.fetch().head(5).sex
        >>> vals
        ┏━━━━━━━━┓
        ┃ sex    ┃
        ┡━━━━━━━━┩
        │ string │
        ├────────┤
        │ male   │
        │ female │
        │ female │
        │ NULL   │
        │ female │
        └────────┘
        >>> vals.nullif("male")
        ┏━━━━━━━━━━━━━━━━━━━━━┓
        ┃ NullIf(sex, 'male') ┃
        ┡━━━━━━━━━━━━━━━━━━━━━┩
        │ string              │
        ├─────────────────────┤
        │ NULL                │
        │ female              │
        │ female              │
        │ NULL                │
        │ female              │
        └─────────────────────┘
        """
        return ops.NullIf(self, null_if_expr).to_expr()

    def between(
        self,
        lower: Value,
        upper: Value,
    ) -> ir.BooleanValue:
        """Check if this expression is between `lower` and `upper`, inclusive.

        Parameters
        ----------
        lower
            Lower bound, inclusive
        upper
            Upper bound, inclusive

        Returns
        -------
        BooleanValue
            Expression indicating membership in the provided range

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch().limit(5)
        >>> t.bill_length_mm.between(35, 38)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Between(bill_length_mm, 35, 38) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ boolean                         │
        ├─────────────────────────────────┤
        │ False                           │
        │ False                           │
        │ False                           │
        │ NULL                            │
        │ True                            │
        └─────────────────────────────────┘
        """
        return ops.Between(self, lower, upper).to_expr()

    def isin(self, values: Value | Sequence[Value]) -> ir.BooleanValue:
        """Check whether this expression's values are in `values`.

        `NULL` values are propagated in the output. See examples for details.

        Parameters
        ----------
        values
            Values or expression to check for membership

        Returns
        -------
        BooleanValue
            Expression indicating membership

        See Also
        --------
        [`Value.notin()`](./expression-generic.qmd#ibis.expr.types.generic.Value.notin)

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"a": [1, 2, 3], "b": [2, 3, 4]})
        >>> t
        ┏━━━━━━━┳━━━━━━━┓
        ┃ a     ┃ b     ┃
        ┡━━━━━━━╇━━━━━━━┩
        │ int64 │ int64 │
        ├───────┼───────┤
        │     1 │     2 │
        │     2 │     3 │
        │     3 │     4 │
        └───────┴───────┘

        Check against a literal sequence of values

        >>> t.a.isin([1, 2])
        ┏━━━━━━━━━━━━━━━━━━━━━┓
        ┃ InValues(a, (1, 2)) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━┩
        │ boolean             │
        ├─────────────────────┤
        │ True                │
        │ True                │
        │ False               │
        └─────────────────────┘

        Check against a derived expression

        >>> t.a.isin(t.b + 1)
        ┏━━━━━━━━━━━━━━━┓
        ┃ InSubquery(a) ┃
        ┡━━━━━━━━━━━━━━━┩
        │ boolean       │
        ├───────────────┤
        │ False         │
        │ False         │
        │ True          │
        └───────────────┘

        Check against a column from a different table

        >>> t2 = ibis.memtable({"x": [99, 2, 99]})
        >>> t.a.isin(t2.x)
        ┏━━━━━━━━━━━━━━━┓
        ┃ InSubquery(a) ┃
        ┡━━━━━━━━━━━━━━━┩
        │ boolean       │
        ├───────────────┤
        │ False         │
        │ True          │
        │ False         │
        └───────────────┘

        `NULL` behavior

        >>> t = ibis.memtable({"x": [1, 2]})
        >>> t.x.isin([1, None])
        ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ InValues(x, (1, None)) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ boolean                │
        ├────────────────────────┤
        │ True                   │
        │ NULL                   │
        └────────────────────────┘
        >>> t = ibis.memtable({"x": [1, None, 2]})
        >>> t.x.isin([1])
        ┏━━━━━━━━━━━━━━━━━━━┓
        ┃ InValues(x, (1,)) ┃
        ┡━━━━━━━━━━━━━━━━━━━┩
        │ boolean           │
        ├───────────────────┤
        │ True              │
        │ NULL              │
        │ False             │
        └───────────────────┘
        >>> t.x.isin([3])
        ┏━━━━━━━━━━━━━━━━━━━┓
        ┃ InValues(x, (3,)) ┃
        ┡━━━━━━━━━━━━━━━━━━━┩
        │ boolean           │
        ├───────────────────┤
        │ False             │
        │ NULL              │
        │ False             │
        └───────────────────┘
        """
        from ibis.expr.types import ArrayValue

        if isinstance(values, ArrayValue):
            return ops.ArrayContains(values, self).to_expr()
        elif isinstance(values, Column):
            return ops.InSubquery(values.as_table(), needle=self).to_expr()
        else:
            return ops.InValues(self, values).to_expr()

    def notin(self, values: Value | Sequence[Value]) -> ir.BooleanValue:
        """Check whether this expression's values are not in `values`.

        Opposite of [`Value.isin()`](./expression-generic.qmd#ibis.expr.types.generic.Value.isin).

        Parameters
        ----------
        values
            Values or expression to check for lack of membership

        Returns
        -------
        BooleanValue
            Whether `self`'s values are not contained in `values`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch().limit(5)
        >>> t.bill_depth_mm
        ┏━━━━━━━━━━━━━━━┓
        ┃ bill_depth_mm ┃
        ┡━━━━━━━━━━━━━━━┩
        │ float64       │
        ├───────────────┤
        │          18.7 │
        │          17.4 │
        │          18.0 │
        │          NULL │
        │          19.3 │
        └───────────────┘
        >>> t.bill_depth_mm.notin([18.7, 18.1])
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Not(InValues(bill_depth_mm, (18.7, 18.1))) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ boolean                                    │
        ├────────────────────────────────────────────┤
        │ False                                      │
        │ True                                       │
        │ True                                       │
        │ NULL                                       │
        │ True                                       │
        └────────────────────────────────────────────┘
        """
        return ~self.isin(values)

    def substitute(
        self,
        value: Value | dict,
        replacement: Value | None = None,
        else_: Value | None = None,
    ):
        """Replace values given in `values` with `replacement`.

        This is similar to the pandas `replace` method.

        Parameters
        ----------
        value
            Expression or dict.
        replacement
            If an expression is passed to value, this must be
            passed.
        else_
            If an original value does not match `value`, then `else_` is used.
            The default of `None` means leave the original value unchanged.

        Returns
        -------
        Value
            Replaced values

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.island.value_counts().order_by("island")
        ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
        ┃ island    ┃ island_count ┃
        ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
        │ string    │ int64        │
        ├───────────┼──────────────┤
        │ Biscoe    │          168 │
        │ Dream     │          124 │
        │ Torgersen │           52 │
        └───────────┴──────────────┘
        >>> t.island.substitute({"Torgersen": "torg", "Biscoe": "bisc"}).name(
        ...     "island"
        ... ).value_counts().order_by("island")
        ┏━━━━━━━━┳━━━━━━━━━━━━━━┓
        ┃ island ┃ island_count ┃
        ┡━━━━━━━━╇━━━━━━━━━━━━━━┩
        │ string │ int64        │
        ├────────┼──────────────┤
        │ Dream  │          124 │
        │ bisc   │          168 │
        │ torg   │           52 │
        └────────┴──────────────┘
        """
        if isinstance(value, dict):
            expr = ibis.case()
            try:
                null_replacement = value.pop(None)
            except KeyError:
                pass
            else:
                expr = expr.when(self.isnull(), null_replacement)
            for k, v in value.items():
                expr = expr.when(self == k, v)
        else:
            expr = self.case().when(value, replacement)

        return expr.else_(else_ if else_ is not None else self).end()

    def over(
        self,
        window=None,
        *,
        rows=None,
        range=None,
        group_by=None,
        order_by=None,
    ) -> Value:
        """Construct a window expression.

        Parameters
        ----------
        window
            Window specification
        rows
            Whether to use the `ROWS` window clause
        range
            Whether to use the `RANGE` window clause
        group_by
            Grouping key
        order_by
            Ordering key

        Returns
        -------
        Value
            A window function expression

        """

        if window is None:
            window = ibis.window(
                rows=rows,
                range=range,
                group_by=group_by,
                order_by=order_by,
            )
        elif not isinstance(window, bl.WindowBuilder):
            raise com.IbisTypeError("Unexpected window type: {window!r}")

        node = self.op()
        if len(node.relations) == 0:
            table = None
        elif len(node.relations) == 1:
            (table,) = node.relations
            table = table.to_expr()
        else:
            raise com.RelationError("Cannot use window with multiple tables")

        @deferrable
        def bind(table):
            winfunc = rewrite_window_input(node, window.bind(table))
            if winfunc == node:
                raise com.IbisTypeError(
                    "No reduction or analytic function found to construct a window expression"
                )
            return winfunc.to_expr()

        try:
            return bind(table)
        except com.IbisInputError:
            return bind(_)

    def isnull(self) -> ir.BooleanValue:
        """Return whether this expression is NULL.

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch().limit(5)
        >>> t.bill_depth_mm
        ┏━━━━━━━━━━━━━━━┓
        ┃ bill_depth_mm ┃
        ┡━━━━━━━━━━━━━━━┩
        │ float64       │
        ├───────────────┤
        │          18.7 │
        │          17.4 │
        │          18.0 │
        │          NULL │
        │          19.3 │
        └───────────────┘
        >>> t.bill_depth_mm.isnull()
        ┏━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ IsNull(bill_depth_mm) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━┩
        │ boolean               │
        ├───────────────────────┤
        │ False                 │
        │ False                 │
        │ False                 │
        │ True                  │
        │ False                 │
        └───────────────────────┘
        """
        return ops.IsNull(self).to_expr()

    def notnull(self) -> ir.BooleanValue:
        """Return whether this expression is not NULL.

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch().limit(5)
        >>> t.bill_depth_mm
        ┏━━━━━━━━━━━━━━━┓
        ┃ bill_depth_mm ┃
        ┡━━━━━━━━━━━━━━━┩
        │ float64       │
        ├───────────────┤
        │          18.7 │
        │          17.4 │
        │          18.0 │
        │          NULL │
        │          19.3 │
        └───────────────┘
        >>> t.bill_depth_mm.notnull()
        ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ NotNull(bill_depth_mm) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ boolean                │
        ├────────────────────────┤
        │ True                   │
        │ True                   │
        │ True                   │
        │ False                  │
        │ True                   │
        └────────────────────────┘
        """
        return ops.NotNull(self).to_expr()

    def case(self) -> bl.SimpleCaseBuilder:
        """Create a SimpleCaseBuilder to chain multiple if-else statements.

        Add new search expressions with the `.when()` method. These must be
        comparable with this column expression. Conclude by calling `.end()`.

        Returns
        -------
        SimpleCaseBuilder
            A case builder

        See Also
        --------
        [`Value.substitute()`](./expression-generic.qmd#ibis.expr.types.generic.Value.substitute)
        [`ibis.cases()`](./expression-generic.qmd#ibis.expr.types.generic.Value.cases)
        [`ibis.case()`](./expression-generic.qmd#ibis.case)

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> x = ibis.examples.penguins.fetch().head(5)["sex"]
        >>> x
        ┏━━━━━━━━┓
        ┃ sex    ┃
        ┡━━━━━━━━┩
        │ string │
        ├────────┤
        │ male   │
        │ female │
        │ female │
        │ NULL   │
        │ female │
        └────────┘
        >>> x.case().when("male", "M").when("female", "F").else_("U").end()
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ SimpleCase(sex, ('male', 'female'), ('M', 'F'), 'U') ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ string                                               │
        ├──────────────────────────────────────────────────────┤
        │ M                                                    │
        │ F                                                    │
        │ F                                                    │
        │ U                                                    │
        │ F                                                    │
        └──────────────────────────────────────────────────────┘

        Cases not given result in the ELSE case

        >>> x.case().when("male", "M").else_("OTHER").end()
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ SimpleCase(sex, ('male',), ('M',), 'OTHER') ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ string                                      │
        ├─────────────────────────────────────────────┤
        │ M                                           │
        │ OTHER                                       │
        │ OTHER                                       │
        │ OTHER                                       │
        │ OTHER                                       │
        └─────────────────────────────────────────────┘

        If you don't supply an ELSE, then NULL is used

        >>> x.case().when("male", "M").end()
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ SimpleCase(sex, ('male',), ('M',), Cast(None, string)) ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ string                                                 │
        ├────────────────────────────────────────────────────────┤
        │ M                                                      │
        │ NULL                                                   │
        │ NULL                                                   │
        │ NULL                                                   │
        │ NULL                                                   │
        └────────────────────────────────────────────────────────┘
        """
        import ibis.expr.builders as bl

        return bl.SimpleCaseBuilder(self.op())

    def cases(
        self,
        case_result_pairs: Iterable[tuple[ir.BooleanValue, Value]],
        default: Value | None = None,
    ) -> Value:
        """Create a case expression in one shot.

        Parameters
        ----------
        case_result_pairs
            Conditional-result pairs
        default
            Value to return if none of the case conditions are true

        Returns
        -------
        Value
            Value expression

        See Also
        --------
        [`Value.substitute()`](./expression-generic.qmd#ibis.expr.types.generic.Value.substitute)
        [`ibis.cases()`](./expression-generic.qmd#ibis.expr.types.generic.Value.cases)
        [`ibis.case()`](./expression-generic.qmd#ibis.case)

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"values": [1, 2, 1, 2, 3, 2, 4]})
        >>> t
        ┏━━━━━━━━┓
        ┃ values ┃
        ┡━━━━━━━━┩
        │ int64  │
        ├────────┤
        │      1 │
        │      2 │
        │      1 │
        │      2 │
        │      3 │
        │      2 │
        │      4 │
        └────────┘
        >>> number_letter_map = ((1, "a"), (2, "b"), (3, "c"))
        >>> t.values.cases(number_letter_map, default="unk").name("replace")
        ┏━━━━━━━━━┓
        ┃ replace ┃
        ┡━━━━━━━━━┩
        │ string  │
        ├─────────┤
        │ a       │
        │ b       │
        │ a       │
        │ b       │
        │ c       │
        │ b       │
        │ unk     │
        └─────────┘
        """
        builder = self.case()
        for case, result in case_result_pairs:
            builder = builder.when(case, result)
        return builder.else_(default).end()

    def collect(
        self,
        where: ir.BooleanValue | None = None,
        order_by: Any = None,
        include_null: bool = False,
    ) -> ir.ArrayScalar:
        """Aggregate this expression's elements into an array.

        This function is called `array_agg`, `list_agg`, or `list` in other systems.

        Parameters
        ----------
        where
            An optional filter expression. If provided, only rows where `where`
            is `True` will be included in the aggregate.
        order_by
            An ordering key (or keys) to use to order the rows before
            aggregating. If not provided, the order of the items in the result
            is undefined and backend specific.
        include_null
            Whether to include null values when performing this aggregation. Set
            to `True` to include nulls in the result.

        Returns
        -------
        ArrayScalar
            Collected array

        Examples
        --------
        Basic collect usage

        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"key": list("aaabb"), "value": [1, 2, 3, 4, 5]})
        >>> t
        ┏━━━━━━━━┳━━━━━━━┓
        ┃ key    ┃ value ┃
        ┡━━━━━━━━╇━━━━━━━┩
        │ string │ int64 │
        ├────────┼───────┤
        │ a      │     1 │
        │ a      │     2 │
        │ a      │     3 │
        │ b      │     4 │
        │ b      │     5 │
        └────────┴───────┘
        >>> t.value.collect()
        ┌────────────────┐
        │ [1, 2, ... +3] │
        └────────────────┘
        >>> type(t.value.collect())
        <class 'ibis.expr.types.arrays.ArrayScalar'>

        Collect elements per group

        >>> t.group_by("key").agg(v=lambda t: t.value.collect()).order_by("key")
        ┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ key    ┃ v                    ┃
        ┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
        │ string │ array<int64>         │
        ├────────┼──────────────────────┤
        │ a      │ [1, 2, ... +1]       │
        │ b      │ [4, 5]               │
        └────────┴──────────────────────┘

        Collect elements per group using a filter

        >>> t.group_by("key").agg(v=lambda t: t.value.collect(where=t.value > 1)).order_by("key")
        ┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ key    ┃ v                    ┃
        ┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
        │ string │ array<int64>         │
        ├────────┼──────────────────────┤
        │ a      │ [2, 3]               │
        │ b      │ [4, 5]               │
        └────────┴──────────────────────┘
        """
        return ops.ArrayCollect(
            self,
            where=self._bind_to_parent_table(where),
            order_by=self._bind_order_by(order_by),
            include_null=include_null,
        ).to_expr()

    def identical_to(self, other: Value) -> ir.BooleanValue:
        """Return whether this expression is identical to other.

        Corresponds to `IS NOT DISTINCT FROM` in SQL.

        Parameters
        ----------
        other
            Expression to compare to

        Returns
        -------
        BooleanValue
            Whether this expression is not distinct from `other`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> one = ibis.literal(1)
        >>> two = ibis.literal(2)
        >>> two.identical_to(one + one)
        ┌──────┐
        │ True │
        └──────┘
        """
        try:
            return ops.IdenticalTo(self, other).to_expr()
        except (com.IbisTypeError, NotImplementedError):
            return NotImplemented

    def group_concat(
        self,
        sep: str = ",",
        where: ir.BooleanValue | None = None,
        order_by: Any = None,
    ) -> ir.StringScalar:
        """Concatenate values using the indicated separator to produce a string.

        Parameters
        ----------
        sep
            The separator to use to join strings.
        where
            An optional filter expression. If provided, only rows where `where`
            is `True` will be included in the aggregate.
        order_by
            An ordering key (or keys) to use to order the rows before
            aggregating. If not provided, the order of the items in the result
            is undefined and backend specific.

        Returns
        -------
        StringScalar
            Concatenated string expression

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch().limit(5)
        >>> t[["bill_length_mm", "bill_depth_mm"]]
        ┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
        ┃ bill_length_mm ┃ bill_depth_mm ┃
        ┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
        │ float64        │ float64       │
        ├────────────────┼───────────────┤
        │           39.1 │          18.7 │
        │           39.5 │          17.4 │
        │           40.3 │          18.0 │
        │           NULL │          NULL │
        │           36.7 │          19.3 │
        └────────────────┴───────────────┘
        >>> t.bill_length_mm.group_concat()
        ┌─────────────────────┐
        │ 39.1,39.5,40.3,36.7 │
        └─────────────────────┘

        >>> t.bill_length_mm.group_concat(sep=": ")
        ┌────────────────────────┐
        │ 39.1: 39.5: 40.3: 36.7 │
        └────────────────────────┘

        >>> t.bill_length_mm.group_concat(sep=": ", where=t.bill_depth_mm > 18)
        ┌────────────┐
        │ 39.1: 36.7 │
        └────────────┘
        """
        return ops.GroupConcat(
            self,
            sep=sep,
            where=self._bind_to_parent_table(where),
            order_by=self._bind_order_by(order_by),
        ).to_expr()

    def __hash__(self) -> int:
        return super().__hash__()

    def __eq__(self, other: Value) -> ir.BooleanValue:
        if _is_null_literal(other):
            return self.isnull()
        elif _is_null_literal(self):
            return other.isnull()
        return _binop(ops.Equals, self, other)

    def __ne__(self, other: Value) -> ir.BooleanValue:
        if _is_null_literal(other):
            return self.notnull()
        elif _is_null_literal(self):
            return other.notnull()
        return _binop(ops.NotEquals, self, other)

    def __ge__(self, other: Value) -> ir.BooleanValue:
        return _binop(ops.GreaterEqual, self, other)

    def __gt__(self, other: Value) -> ir.BooleanValue:
        return _binop(ops.Greater, self, other)

    def __le__(self, other: Value) -> ir.BooleanValue:
        return _binop(ops.LessEqual, self, other)

    def __lt__(self, other: Value) -> ir.BooleanValue:
        return _binop(ops.Less, self, other)

    def asc(self, nulls_first: bool = False) -> ir.Value:
        """Sort an expression ascending."""
        return ops.SortKey(self, ascending=True, nulls_first=nulls_first).to_expr()

    def desc(self, nulls_first: bool = False) -> ir.Value:
        """Sort an expression descending."""
        return ops.SortKey(self, ascending=False, nulls_first=nulls_first).to_expr()

    def to_pandas(self, **kwargs) -> pd.Series:
        """Convert a column expression to a pandas Series or scalar object.

        Parameters
        ----------
        kwargs
            Same as keyword arguments to [`execute`](#ibis.expr.types.core.Expr.execute)

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch().limit(5)
        >>> t.to_pandas()
          species     island  bill_length_mm  ...  body_mass_g     sex  year
        0  Adelie  Torgersen            39.1  ...       3750.0    male  2007
        1  Adelie  Torgersen            39.5  ...       3800.0  female  2007
        2  Adelie  Torgersen            40.3  ...       3250.0  female  2007
        3  Adelie  Torgersen             NaN  ...          NaN    None  2007
        4  Adelie  Torgersen            36.7  ...       3450.0  female  2007
        [5 rows x 8 columns]
        """
        return self.execute(**kwargs)


@public
class Scalar(Value):
    def __pyarrow_result__(
        self,
        table: pa.Table,
        *,
        schema: sch.Schema | None = None,
        data_mapper: type[PyArrowData] | None = None,
    ) -> pa.Scalar:
        if data_mapper is None:
            from ibis.formats.pyarrow import PyArrowData as data_mapper

        return data_mapper.convert_scalar(
            table[0][0], self.type() if schema is None else schema.types[0]
        )

    def __pandas_result__(
        self,
        df: pd.DataFrame,
        *,
        schema: sch.Schema | None = None,
        data_mapper: type[PandasData] | None = None,
    ) -> Any:
        if data_mapper is None:
            from ibis.formats.pandas import PandasData as data_mapper

        return data_mapper.convert_scalar(
            df, self.type() if schema is None else schema.types[0]
        )

    def __polars_result__(self, df: pl.DataFrame) -> Any:
        from ibis.formats.polars import PolarsData

        return PolarsData.convert_scalar(df, self.type())

    def as_scalar(self):
        """Inform ibis that the expression should be treated as a scalar.

        If the expression is a literal, it will be returned as is. If it depends
        on a table, it will be turned to a scalar subquery.

        Returns
        -------
        Scalar
            A scalar subquery or a literal

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> max_gentoo_weight = t.filter(t.species == "Gentoo").body_mass_g.max()
        >>> light_penguins = t.filter(t.body_mass_g < max_gentoo_weight / 2)
        >>> light_penguins.species.value_counts().order_by("species")
        ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
        ┃ species   ┃ species_count ┃
        ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
        │ string    │ int64         │
        ├───────────┼───────────────┤
        │ Adelie    │            15 │
        │ Chinstrap │             2 │
        └───────────┴───────────────┘
        """
        parents = self.op().relations
        if parents:
            return ops.ScalarSubquery(self.as_table()).to_expr()
        else:
            return self

    def as_table(self) -> ir.Table:
        """Promote the scalar expression to a table.

        Returns
        -------
        Table
            A table expression

        Examples
        --------
        Promote an aggregation to a table

        >>> import ibis
        >>> import ibis.expr.types as ir
        >>> t = ibis.table(dict(a="str"), name="t")
        >>> expr = t.a.length().sum().name("len").as_table()
        >>> isinstance(expr, ir.Table)
        True

        Promote a literal value to a table

        >>> import ibis.expr.types as ir
        >>> lit = ibis.literal(1).name("a").as_table()
        >>> isinstance(lit, ir.Table)
        True
        """
        from ibis.expr.types.relations import unwrap_alias

        op = self.op()
        parents = op.relations

        if not parents:
            return ops.DummyTable({op.name: unwrap_alias(op)}).to_expr()
        elif len(parents) == 1:
            (parent,) = parents
            return parent.to_expr().aggregate(self)
        else:
            raise com.RelationError(
                f"The scalar expression {self} cannot be converted to a "
                "table expression because it involves multiple base table "
                "references"
            )

    def __deferred_repr__(self):
        return f"<scalar[{self.type()}]>"

    def _repr_html_(self) -> str | None:
        return None


@public
class Column(Value, _FixedTextJupyterMixin):
    # Higher than numpy & dask objects
    __array_priority__ = 20

    __array_ufunc__ = None

    def __getitem__(self, _):
        raise TypeError(
            f"{self.__class__.__name__!r} is not subscriptable: "
            "see https://ibis-project.org/tutorial/ibis-for-pandas-users/#ibis-for-pandas-users for details."
        )

    def __array__(self, dtype=None):
        return self.execute().__array__(dtype)

    def preview(
        self,
        *,
        max_rows: int | None = None,
        max_length: int | None = None,
        max_string: int | None = None,
        max_depth: int | None = None,
        console_width: int | float | None = None,
    ) -> rich.table.Table:
        """Print a subset as a single-column Rich Table.

        This is an explicit version of what you get when you inspect
        this object in interactive mode, except with this version you
        can pass formatting options. The options are the same as those exposed
        in `ibis.options.interactive`.

        Parameters
        ----------
        max_rows
            Maximum number of rows to display
        max_length
            Maximum length for pretty-printed arrays and maps.
        max_string
            Maximum length for pretty-printed strings.
        max_depth
            Maximum depth for nested data types.
        console_width
            Width of the console in characters. If not specified, the width
            will be inferred from the console.

        Examples
        --------
        >>> import ibis
        >>> t = ibis.examples.penguins.fetch()
        >>> t.island.preview(max_rows=3, max_string=5)  # doctest: +SKIP
        ┏━━━━━━━━┓
        ┃ island ┃
        ┡━━━━━━━━┩
        │ stri…  │
        ├────────┤
        │ Torg…  │
        │ Torg…  │
        │ Torg…  │
        │ …      │
        └────────┘
        """
        from ibis.expr.types.pretty import to_rich

        return to_rich(
            self,
            max_rows=max_rows,
            max_length=max_length,
            max_string=max_string,
            max_depth=max_depth,
            console_width=console_width,
        )

    def __pyarrow_result__(
        self,
        table: pa.Table,
        *,
        schema: sch.Schema | None = None,
        data_mapper: type[PyArrowData] | None = None,
    ) -> pa.Array | pa.ChunkedArray:
        if data_mapper is None:
            from ibis.formats.pyarrow import PyArrowData as data_mapper

        return data_mapper.convert_column(
            table[0], self.type() if schema is None else schema.types[0]
        )

    def __pandas_result__(
        self,
        df: pd.DataFrame,
        *,
        schema: sch.Schema | None = None,
        data_mapper: type[PandasData] | None = None,
    ) -> pd.Series:
        if data_mapper is None:
            from ibis.formats.pandas import PandasData as data_mapper

        assert (
            len(df.columns) == 1
        ), "more than one column when converting columnar result DataFrame to Series"
        # in theory we could use df.iloc[:, 0], but there seems to be a bug in
        # older geopandas where df.iloc[:, 0] doesn't return the same kind of
        # object as df.loc[:, column_name] when df is a GeoDataFrame
        #
        # the bug is that iloc[:, 0] returns a bare series whereas
        # df.loc[:, column_name] returns the special GeoSeries object.
        #
        # this bug is fixed in later versions of geopandas
        return data_mapper.convert_column(
            df.loc[:, df.columns[0]], self.type() if schema is None else schema.types[0]
        )

    def __polars_result__(self, df: pl.DataFrame) -> pl.Series:
        from ibis.formats.polars import PolarsData

        return PolarsData.convert_column(df, self.type())

    def as_scalar(self) -> Scalar:
        """Inform ibis that the expression should be treated as a scalar.

        Creates a scalar subquery from the column expression. Since ibis cannot
        be sure that the column expression contains only one value, the column
        expression is wrapped in a scalar subquery and treated as a scalar.

        Note that the execution of the scalar subquery will fail if the column
        expression contains more than one value.

        Returns
        -------
        Scalar
            A scalar subquery

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> heavy_gentoo = t.filter(t.species == "Gentoo", t.body_mass_g > 6200)
        >>> from_that_island = t.filter(t.island == heavy_gentoo.island.as_scalar())
        >>> from_that_island.species.value_counts().order_by("species")
        ┏━━━━━━━━━┳━━━━━━━━━━━━━━━┓
        ┃ species ┃ species_count ┃
        ┡━━━━━━━━━╇━━━━━━━━━━━━━━━┩
        │ string  │ int64         │
        ├─────────┼───────────────┤
        │ Adelie  │            44 │
        │ Gentoo  │           124 │
        └─────────┴───────────────┘
        """
        return self.as_table().as_scalar()

    def as_table(self) -> ir.Table:
        """Promote the expression to a [Table](./expression-tables.qmd#ibis.expr.types.Table).

        Returns
        -------
        Table
            A table expression

        Examples
        --------
        >>> import ibis
        >>> t = ibis.table(dict(a="str"), name="t")
        >>> expr = t.a.length().name("len").as_table()
        >>> expected = t.select(len=t.a.length())
        >>> expr.equals(expected)
        True
        """
        from ibis.expr.types.relations import unwrap_alias

        op = self.op()
        parents = op.relations

        if not parents:
            return ops.DummyTable({op.name: unwrap_alias(op)}).to_expr()
        elif len(parents) == 1:
            (parent,) = parents
            return parent.to_expr().select(self)
        else:
            raise com.RelationError(
                f"Cannot convert {type(self)} expression involving multiple "
                "base table references to a projection"
            )

    def _bind_order_by(self, value) -> tuple[ops.SortKey, ...]:
        if value is None:
            return ()
        return tuple(self._bind_to_parent_table(v) for v in promote_list(value))

    def _bind_to_parent_table(self, value) -> Value | None:
        """Bind an expr to the parent table of `self`."""
        if value is None:
            return None
        if isinstance(value, (Deferred, str)) or callable(value):
            op = self.op()
            if len(op.relations) != 1:
                # TODO: I don't think this line can ever be hit by a valid
                # expression, since it would require a column expression to
                # directly depend on multiple tables. Currently some invalid
                # expressions (like t1.a.argmin(t2.b)) aren't caught at
                # construction time though, so we keep the check in for now.
                raise com.RelationError(
                    f"Unable to bind `{value!r}` - the current expression"
                    f"depends on multiple tables."
                )
            table = next(iter(op.relations)).to_expr()

            if isinstance(value, str):
                return table[value]
            elif isinstance(value, Deferred):
                return value.resolve(table)
            else:
                value = value(table)

        if not isinstance(value, Value):
            return literal(value)
        return value

    def __deferred_repr__(self):
        return f"<column[{self.type()}]>"

    def approx_nunique(self, where: ir.BooleanValue | None = None) -> ir.IntegerScalar:
        """Return the approximate number of distinct elements in `self`.

        ::: {.callout-note}
        ## The result may or may not be exact

        Whether the result is an approximation depends on the backend.

        ::: {.callout-warning}
        ## Do not depend on the results being exact
        :::

        :::

        Parameters
        ----------
        where
            Filter in values when `where` is `True`

        Returns
        -------
        Scalar
            An approximate count of the distinct elements of `self`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.body_mass_g.approx_nunique()
        ┌────┐
        │ 94 │
        └────┘
        >>> t.body_mass_g.approx_nunique(where=t.species == "Adelie")
        ┌────┐
        │ 55 │
        └────┘
        """
        return ops.ApproxCountDistinct(
            self, where=self._bind_to_parent_table(where)
        ).to_expr()

    def approx_median(self, where: ir.BooleanValue | None = None) -> Scalar:
        """Return an approximate of the median of `self`.

        ::: {.callout-note}
        ## The result may or may not be exact

        Whether the result is an approximation depends on the backend.

        ::: {.callout-warning}
        ## Do not depend on the results being exact
        :::

        :::

        Parameters
        ----------
        where
            Filter in values when `where` is `True`

        Returns
        -------
        Scalar
            An approximation of the median of `self`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.body_mass_g.approx_median()
        ┌────────┐
        │ 4030.0 │
        └────────┘
        >>> t.body_mass_g.approx_median(where=t.species == "Chinstrap")
        ┌────────┐
        │ 3700.0 │
        └────────┘
        """
        return ops.ApproxMedian(self, where=self._bind_to_parent_table(where)).to_expr()

    def mode(self, where: ir.BooleanValue | None = None) -> Scalar:
        """Return the mode of a column.

        Parameters
        ----------
        where
            Filter in values when `where` is `True`

        Returns
        -------
        Scalar
            The mode of `self`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.body_mass_g.mode()
        ┌──────┐
        │ 3800 │
        └──────┘
        >>> t.body_mass_g.mode(where=(t.species == "Gentoo") & (t.sex == "male"))
        ┌──────┐
        │ 5550 │
        └──────┘
        """
        return ops.Mode(self, where=self._bind_to_parent_table(where)).to_expr()

    def max(self, where: ir.BooleanValue | None = None) -> Scalar:
        """Return the maximum of a column.

        Parameters
        ----------
        where
            Filter in values when `where` is `True`

        Returns
        -------
        Scalar
            The maximum value in `self`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.body_mass_g.max()
        ┌──────┐
        │ 6300 │
        └──────┘
        >>> t.body_mass_g.max(where=t.species == "Chinstrap")
        ┌──────┐
        │ 4800 │
        └──────┘
        """
        return ops.Max(self, where=self._bind_to_parent_table(where)).to_expr()

    def min(self, where: ir.BooleanValue | None = None) -> Scalar:
        """Return the minimum of a column.

        Parameters
        ----------
        where
            Filter in values when `where` is `True`

        Returns
        -------
        Scalar
            The minimum value in `self`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.body_mass_g.min()
        ┌──────┐
        │ 2700 │
        └──────┘
        >>> t.body_mass_g.min(where=t.species == "Adelie")
        ┌──────┐
        │ 2850 │
        └──────┘
        """
        return ops.Min(self, where=self._bind_to_parent_table(where)).to_expr()

    def argmax(self, key: ir.Value, where: ir.BooleanValue | None = None) -> Scalar:
        """Return the value of `self` that maximizes `key`.

        Parameters
        ----------
        key
            Key to use for `max` computation.
        where
            Keep values when `where` is `True`

        Returns
        -------
        Scalar
            The value of `self` that maximizes `key`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.species.argmax(t.body_mass_g)
        ┌────────┐
        │ Gentoo │
        └────────┘
        >>> t.species.argmax(t.body_mass_g, where=t.island == "Dream")
        ┌───────────┐
        │ Chinstrap │
        └───────────┘
        """
        return ops.ArgMax(
            self,
            key=self._bind_to_parent_table(key),
            where=self._bind_to_parent_table(where),
        ).to_expr()

    def argmin(self, key: ir.Value, where: ir.BooleanValue | None = None) -> Scalar:
        """Return the value of `self` that minimizes `key`.

        Parameters
        ----------
        key
            Key to use for `min` computation.
        where
            Keep values when `where` is `True`

        Returns
        -------
        Scalar
            The value of `self` that minimizes `key`

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.species.argmin(t.body_mass_g)
        ┌───────────┐
        │ Chinstrap │
        └───────────┘

        >>> t.species.argmin(t.body_mass_g, where=t.island == "Biscoe")
        ┌────────┐
        │ Adelie │
        └────────┘
        """
        return ops.ArgMin(
            self,
            key=self._bind_to_parent_table(key),
            where=self._bind_to_parent_table(where),
        ).to_expr()

    def median(self, where: ir.BooleanValue | None = None) -> Scalar:
        """Return the median of the column.

        Parameters
        ----------
        where
            Optional boolean expression. If given, only the values where
            `where` evaluates to true will be considered for the median.

        Returns
        -------
        Scalar
            Median of the column

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()

        Compute the median of `bill_depth_mm`

        >>> t.bill_depth_mm.median()
        ┌──────┐
        │ 17.3 │
        └──────┘
        >>> t.group_by(t.species).agg(median_bill_depth=t.bill_depth_mm.median()).order_by(
        ...     ibis.desc("median_bill_depth")
        ... )
        ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
        ┃ species   ┃ median_bill_depth ┃
        ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
        │ string    │ float64           │
        ├───────────┼───────────────────┤
        │ Chinstrap │             18.45 │
        │ Adelie    │             18.40 │
        │ Gentoo    │             15.00 │
        └───────────┴───────────────────┘

        In addition to numeric types, any orderable non-numeric types such as
        strings and dates work with `median`.

        >>> t.group_by(t.island).agg(median_species=t.species.median()).order_by(
        ...     ibis.desc("median_species")
        ... )
        ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
        ┃ island    ┃ median_species ┃
        ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
        │ string    │ string         │
        ├───────────┼────────────────┤
        │ Biscoe    │ Gentoo         │
        │ Dream     │ Chinstrap      │
        │ Torgersen │ Adelie         │
        └───────────┴────────────────┘
        """
        return ops.Median(self, where=self._bind_to_parent_table(where)).to_expr()

    def quantile(
        self,
        quantile: float | ir.NumericValue | Sequence[ir.NumericValue | float],
        where: ir.BooleanValue | None = None,
    ) -> Scalar:
        """Return value at the given quantile.

        The output of this method is a continuous quantile if the input is
        numeric, otherwise the output is a discrete quantile.

        Parameters
        ----------
        quantile
            `0 <= quantile <= 1`, or an array of such values
            indicating the quantile or quantiles to compute
        where
            Boolean filter for input values

        Returns
        -------
        Scalar
            Quantile of the input

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()

        Compute the 99th percentile of `bill_depth`

        >>> t.bill_depth_mm.quantile(0.99)
        ┌──────┐
        │ 21.1 │
        └──────┘
        >>> t.group_by(t.species).agg(p99_bill_depth=t.bill_depth_mm.quantile(0.99)).order_by(
        ...     ibis.desc("p99_bill_depth")
        ... )
        ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
        ┃ species   ┃ p99_bill_depth ┃
        ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
        │ string    │ float64        │
        ├───────────┼────────────────┤
        │ Adelie    │         21.200 │
        │ Chinstrap │         20.733 │
        │ Gentoo    │         17.256 │
        └───────────┴────────────────┘

        In addition to numeric types, any orderable non-numeric types such as
        strings and dates work with `quantile`.

        Let's compute the 99th percentile of the `species` column

        >>> t.group_by(t.island).agg(p99_species=t.species.quantile(0.99)).order_by(
        ...     ibis.desc("p99_species")
        ... )
        ┏━━━━━━━━━━━┳━━━━━━━━━━━━━┓
        ┃ island    ┃ p99_species ┃
        ┡━━━━━━━━━━━╇━━━━━━━━━━━━━┩
        │ string    │ string      │
        ├───────────┼─────────────┤
        │ Biscoe    │ Gentoo      │
        │ Dream     │ Chinstrap   │
        │ Torgersen │ Adelie      │
        └───────────┴─────────────┘
        """
        if isinstance(quantile, Sequence):
            op = ops.MultiQuantile
        else:
            op = ops.Quantile
        return op(self, quantile, where=self._bind_to_parent_table(where)).to_expr()

    def nunique(self, where: ir.BooleanValue | None = None) -> ir.IntegerScalar:
        """Compute the number of distinct rows in an expression.

        Parameters
        ----------
        where
            Filter expression

        Returns
        -------
        IntegerScalar
            Number of distinct elements in an expression

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.examples.penguins.fetch()
        >>> t.body_mass_g.nunique()
        ┌────┐
        │ 94 │
        └────┘
        >>> t.body_mass_g.nunique(where=t.species == "Adelie")
        ┌────┐
        │ 55 │
        └────┘
        """
        return ops.CountDistinct(
            self, where=self._bind_to_parent_table(where)
        ).to_expr()

    def topk(self, k: int, by: ir.Value | None = None) -> ir.Table:
        """Return a "top k" expression.

        Parameters
        ----------
        k
            Return this number of rows
        by
            An expression. Defaults to `count`.

        Returns
        -------
        Table
            A top-k expression
        """
        from ibis.expr.types.relations import bind

        try:
            (table,) = self.op().relations
        except ValueError:
            raise com.IbisTypeError("TopK must depend on exactly one table.")

        table = table.to_expr()

        if by is None:
            by = lambda t: t.count()

        (metric,) = bind(table, by)

        return table.aggregate(metric, by=[self]).order_by(metric.desc()).limit(k)

    def arbitrary(
        self, where: ir.BooleanValue | None = None, how: Any = None
    ) -> Scalar:
        """Select an arbitrary value in a column.

        Returns an arbitrary (nondeterministic, backend-specific) value from
        the column. The value will be non-NULL, except if the column is empty
        or all values are NULL.

        Parameters
        ----------
        where
            A filter expression
        how
            DEPRECATED

        Returns
        -------
        Scalar
            An expression

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"a": [1, 2, 2], "b": list("aaa"), "c": [4.0, 4.1, 4.2]})
        >>> t
        ┏━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
        ┃ a     ┃ b      ┃ c       ┃
        ┡━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
        │ int64 │ string │ float64 │
        ├───────┼────────┼─────────┤
        │     1 │ a      │     4.0 │
        │     2 │ a      │     4.1 │
        │     2 │ a      │     4.2 │
        └───────┴────────┴─────────┘
        >>> t.group_by("a").agg(arb=t.b.arbitrary(), c=t.c.sum()).order_by("a")
        ┏━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
        ┃ a     ┃ arb    ┃ c       ┃
        ┡━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
        │ int64 │ string │ float64 │
        ├───────┼────────┼─────────┤
        │     1 │ a      │     4.0 │
        │     2 │ a      │     8.3 │
        └───────┴────────┴─────────┘
        """
        if how is not None:
            warn_deprecated(
                name="how",
                as_of="9.0",
                removed_in="10.0",
                instead="call `first` or `last` explicitly",
            )
        return ops.Arbitrary(self, where=self._bind_to_parent_table(where)).to_expr()

    def count(self, where: ir.BooleanValue | None = None) -> ir.IntegerScalar:
        """Compute the number of rows in an expression.

        Parameters
        ----------
        where
            Filter expression

        Returns
        -------
        IntegerScalar
            Number of elements in an expression
        """
        return ops.Count(self, where=self._bind_to_parent_table(where)).to_expr()

    def value_counts(self) -> ir.Table:
        """Compute a frequency table.

        Returns
        -------
        Table
            Frequency table expression

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"chars": char} for char in "aabcddd")
        >>> t
        ┏━━━━━━━━┓
        ┃ chars  ┃
        ┡━━━━━━━━┩
        │ string │
        ├────────┤
        │ a      │
        │ a      │
        │ b      │
        │ c      │
        │ d      │
        │ d      │
        │ d      │
        └────────┘
        >>> t.chars.value_counts().order_by("chars")
        ┏━━━━━━━━┳━━━━━━━━━━━━━┓
        ┃ chars  ┃ chars_count ┃
        ┡━━━━━━━━╇━━━━━━━━━━━━━┩
        │ string │ int64       │
        ├────────┼─────────────┤
        │ a      │           2 │
        │ b      │           1 │
        │ c      │           1 │
        │ d      │           3 │
        └────────┴─────────────┘
        """
        name = self.get_name()
        metric = _.count().name(f"{name}_count")
        return self.as_table().group_by(name).aggregate(metric)

    def first(
        self,
        where: ir.BooleanValue | None = None,
        order_by: Any = None,
        include_null: bool = False,
    ) -> Value:
        """Return the first value of a column.

        Parameters
        ----------
        where
            An optional filter expression. If provided, only rows where `where`
            is `True` will be included in the aggregate.
        order_by
            An ordering key (or keys) to use to order the rows before
            aggregating. If not provided, the meaning of `first` is undefined
            and will be backend specific.
        include_null
            Whether to include null values when performing this aggregation. Set
            to `True` to include nulls in the result.

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"chars": ["a", "b", "c", "d"]})
        >>> t
        ┏━━━━━━━━┓
        ┃ chars  ┃
        ┡━━━━━━━━┩
        │ string │
        ├────────┤
        │ a      │
        │ b      │
        │ c      │
        │ d      │
        └────────┘
        >>> t.chars.first()
        ┌───┐
        │ a │
        └───┘
        >>> t.chars.first(where=t.chars != "a")
        ┌───┐
        │ b │
        └───┘
        """
        return ops.First(
            self,
            where=self._bind_to_parent_table(where),
            order_by=self._bind_order_by(order_by),
            include_null=include_null,
        ).to_expr()

    def last(
        self,
        where: ir.BooleanValue | None = None,
        order_by: Any = None,
        include_null: bool = False,
    ) -> Value:
        """Return the last value of a column.

        Parameters
        ----------
        where
            An optional filter expression. If provided, only rows where `where`
            is `True` will be included in the aggregate.
        order_by
            An ordering key (or keys) to use to order the rows before
            aggregating. If not provided, the meaning of `last` is undefined
            and will be backend specific.
        include_null
            Whether to include null values when performing this aggregation. Set
            to `True` to include nulls in the result.

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"chars": ["a", "b", "c", "d"]})
        >>> t
        ┏━━━━━━━━┓
        ┃ chars  ┃
        ┡━━━━━━━━┩
        │ string │
        ├────────┤
        │ a      │
        │ b      │
        │ c      │
        │ d      │
        └────────┘
        >>> t.chars.last()
        ┌───┐
        │ d │
        └───┘
        >>> t.chars.last(where=t.chars != "d")
        ┌───┐
        │ c │
        └───┘
        """
        return ops.Last(
            self,
            where=self._bind_to_parent_table(where),
            order_by=self._bind_order_by(order_by),
            include_null=include_null,
        ).to_expr()

    def rank(self) -> ir.IntegerColumn:
        """Compute position of first element within each equal-value group in sorted order.

        Equivalent to SQL's `RANK()` window function.

        Returns
        -------
        Int64Column
            The min rank

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"values": [1, 2, 1, 2, 3, 2]})
        >>> t.mutate(rank=t.values.rank())
        ┏━━━━━━━━┳━━━━━━━┓
        ┃ values ┃ rank  ┃
        ┡━━━━━━━━╇━━━━━━━┩
        │ int64  │ int64 │
        ├────────┼───────┤
        │      1 │     0 │
        │      1 │     0 │
        │      2 │     2 │
        │      2 │     2 │
        │      2 │     2 │
        │      3 │     5 │
        └────────┴───────┘
        """
        return ibis.rank().over(order_by=self)

    def dense_rank(self) -> ir.IntegerColumn:
        """Position of first element within each group of equal values.

        Values are returned in sorted order and duplicate values are ignored.

        Equivalent to SQL's `DENSE_RANK()`.

        Returns
        -------
        IntegerColumn
            The rank

        Examples
        --------
        >>> import ibis
        >>> ibis.options.interactive = True
        >>> t = ibis.memtable({"values": [1, 2, 1, 2, 3, 2]})
        >>> t.mutate(rank=t.values.dense_rank())
        ┏━━━━━━━━┳━━━━━━━┓
        ┃ values ┃ rank  ┃
        ┡━━━━━━━━╇━━━━━━━┩
        │ int64  │ int64 │
        ├────────┼───────┤
        │      1 │     0 │
        │      1 │     0 │
        │      2 │     1 │
        │      2 │     1 │
        │      2 │     1 │
        │      3 │     2 │
        └────────┴───────┘
        """
        return ibis.dense_rank().over(order_by=self)

    def percent_rank(self) -> Column:
        """Return the relative rank of the values in the column."""
        return ibis.percent_rank().over(order_by=self)

    def cume_dist(self) -> Column:
        """Return the cumulative distribution over a window."""
        return ibis.cume_dist().over(order_by=self)

    def ntile(self, buckets: int | ir.IntegerValue) -> ir.IntegerColumn:
        """Return the integer number of a partitioning of the column values.

        Parameters
        ----------
        buckets
            Number of buckets to partition into
        """
        return ibis.ntile(buckets).over(order_by=self)

    def cummin(self, *, where=None, group_by=None, order_by=None) -> Column:
        """Return the cumulative min over a window."""
        return self.min(where=where).over(
            ibis.cumulative_window(group_by=group_by, order_by=order_by)
        )

    def cummax(self, *, where=None, group_by=None, order_by=None) -> Column:
        """Return the cumulative max over a window."""
        return self.max(where=where).over(
            ibis.cumulative_window(group_by=group_by, order_by=order_by)
        )

    def lag(
        self,
        offset: int | ir.IntegerValue | None = None,
        default: Value | None = None,
    ) -> Column:
        """Return the row located at `offset` rows **before** the current row.

        Parameters
        ----------
        offset
            Index of row to select
        default
            Value used if no row exists at `offset`
        """
        return ops.Lag(self, offset, default).to_expr()

    def lead(
        self,
        offset: int | ir.IntegerValue | None = None,
        default: Value | None = None,
    ) -> Column:
        """Return the row located at `offset` rows **after** the current row.

        Parameters
        ----------
        offset
            Index of row to select
        default
            Value used if no row exists at `offset`
        """
        return ops.Lead(self, offset, default).to_expr()

    def nth(self, n: int | ir.IntegerValue) -> Column:
        """Return the `n`th value (0-indexed) over a window.

        `.nth(0)` is equivalent to `.first()`. Negative will result in `NULL`.
        If the value of `n` is greater than the number of rows in the window,
        `NULL` will be returned.

        Parameters
        ----------
        n
            Desired rank value

        Returns
        -------
        Column
            The nth value over a window
        """
        return ops.NthValue(self, n).to_expr()


@public
class UnknownValue(Value):
    pass


@public
class UnknownScalar(Scalar):
    pass


@public
class UnknownColumn(Column):
    pass


@public
class NullValue(Value):
    pass


@public
class NullScalar(Scalar, NullValue, Singleton):
    pass


@public
class NullColumn(Column, NullValue):
    pass


@public
@deferrable
def null(type: dt.DataType | str | None = None) -> Value:
    """Create a NULL scalar.

    `NULL`s with an unspecified type are castable and comparable to values,
    but lack datatype-specific methods:

    >>> import ibis
    >>> ibis.options.interactive = True
    >>> ibis.null().upper()
    Traceback (most recent call last):
        ...
    AttributeError: 'NullScalar' object has no attribute 'upper'
    >>> ibis.null(str).upper()
    ┌──────┐
    │ None │
    └──────┘
    >>> ibis.null(str).upper().isnull()
    ┌──────┐
    │ True │
    └──────┘
    """
    if type is None:
        type = dt.null
    return ops.Literal(None, type).to_expr()


@public
@deferrable
def literal(value: Any, type: dt.DataType | str | None = None) -> Scalar:
    """Create a scalar expression from a Python value.

    ::: {.callout-tip}
    ## Use specific functions for arrays, structs and maps

    Ibis supports literal construction of arrays using the following
    functions:

    1. [`ibis.array`](./expression-collections.qmd#ibis.array)
    1. [`ibis.struct`](./expression-collections.qmd#ibis.struct)
    1. [`ibis.map`](./expression-collections.qmd#ibis.map)

    Constructing these types using `literal` will be deprecated in a future
    release.
    :::

    Parameters
    ----------
    value
        A Python value
    type
        An instance of [`DataType`](./datatypes.qmd#ibis.expr.datatypes.DataType) or a string
        indicating the ibis type of `value`. This parameter can be used
        in cases where ibis's type inference isn't sufficient for discovering
        the type of `value`.

    Returns
    -------
    Scalar
        An expression representing a literal value

    Examples
    --------
    Construct an integer literal

    >>> import ibis
    >>> x = ibis.literal(42)
    >>> x.type()
    Int8(nullable=True)

    Construct a `float64` literal from an `int`

    >>> y = ibis.literal(42, type="double")
    >>> y.type()
    Float64(nullable=True)

    Ibis checks for invalid types

    >>> ibis.literal("foobar", type="int64")  # quartodoc: +EXPECTED_FAILURE
    Traceback (most recent call last):
      ...
    TypeError: Value 'foobar' cannot be safely coerced to int64

    Literals can also be used in a deferred context.

    Here's an example of constructing a table of a column's type repeated for
    every row:

    >>> from ibis import _, selectors as s
    >>> ibis.options.interactive = True
    >>> t = ibis.examples.penguins.fetch()
    >>> t.select(s.across(s.all(), ibis.literal(_.type(), type=str).name(_.get_name()))).head(1)
    ┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━┓
    ┃ species ┃ island ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ … ┃
    ┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━┩
    │ string  │ string │ string         │ string        │ string            │ … │
    ├─────────┼────────┼────────────────┼───────────────┼───────────────────┼───┤
    │ string  │ string │ float64        │ float64       │ int64             │ … │
    └─────────┴────────┴────────────────┴───────────────┴───────────────────┴───┘
    """
    if isinstance(value, Expr):
        node = value.op()
        if not isinstance(node, ops.Literal):
            raise TypeError(f"Ibis expression {value!r} is not a Literal")
        if type is None or node.dtype.castable(dt.dtype(type)):
            return value
        else:
            raise TypeError(
                f"Ibis literal {value!r} cannot be safely coerced to datatype {type}"
            )

    dtype = dt.infer(value) if type is None else dt.dtype(type)
    return ops.Literal(value, dtype=dtype).to_expr()


public(
    ValueExpr=Value,
    ScalarExpr=Scalar,
    ColumnExpr=Column,
    AnyValue=Value,
    AnyScalar=Scalar,
    AnyColumn=Column,
)
