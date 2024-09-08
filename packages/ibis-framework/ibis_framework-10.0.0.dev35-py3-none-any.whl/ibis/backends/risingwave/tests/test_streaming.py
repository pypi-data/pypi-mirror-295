from __future__ import annotations

import time

import pandas as pd
import pandas.testing as tm
import pytest

import ibis
from ibis import util


@pytest.mark.parametrize(
    "column",
    ["string_col", "double_col", "date_string_col", "timestamp_col"],
)
def test_simple_mv(con, alltypes, column):
    expr = alltypes[[column]].distinct().order_by(column)
    mv_name = util.gen_name("alltypes_mv")
    mv = con.create_materialized_view(mv_name, expr, overwrite=True)
    expected = expr.limit(5).execute()
    result = mv.order_by(column).limit(5).execute()
    tm.assert_frame_equal(result, expected)
    con.drop_materialized_view(mv_name)


def test_mv_on_simple_source(con):
    sc_name = util.gen_name("simple_sc")
    schema = ibis.schema([("v", "int32")])
    # use RisingWave's internal data generator to imitate a upstream data source
    connector_properties = {
        "connector": "datagen",
        "fields.v.kind": "sequence",
        "fields.v.start": "1",
        "fields.v.end": "10",
        "datagen.rows.per.second": "10000",
        "datagen.split.num": "1",
    }
    source = con.create_source(
        sc_name,
        schema,
        connector_properties=connector_properties,
        data_format="PLAIN",
        encode_format="JSON",
    )
    expr = source["v"].sum()
    mv_name = util.gen_name("simple_mv")
    mv = con.create_materialized_view(mv_name, expr)
    # sleep 3s to make sure the data has been generated by the source and consumed by the MV.
    time.sleep(3)
    result = mv.execute()
    expected = pd.DataFrame({"Sum(v)": [55]})
    tm.assert_frame_equal(result, expected)
    con.drop_materialized_view(mv_name)
    con.drop_source(sc_name)


def test_mv_on_table_with_connector(con):
    tblc_name = util.gen_name("simple_table_with_connector")
    schema = ibis.schema([("v", "int32")])
    # use RisingWave's internal data generator to imitate a upstream data source
    connector_properties = {
        "connector": "datagen",
        "fields.v.kind": "sequence",
        "fields.v.start": "1",
        "fields.v.end": "10",
        "datagen.rows.per.second": "10000",
        "datagen.split.num": "1",
    }
    tblc = con.create_table(
        name=tblc_name,
        obj=None,
        schema=schema,
        connector_properties=connector_properties,
        data_format="PLAIN",
        encode_format="JSON",
    )
    expr = tblc["v"].sum()
    mv_name = util.gen_name("simple_mv")
    mv = con.create_materialized_view(mv_name, expr)
    # sleep 1 s to make sure the data has been generated by the source and consumed by the MV.
    time.sleep(1)

    result_tblc = expr.execute()
    assert result_tblc == 55

    result_mv = mv.execute()
    expected = pd.DataFrame({"Sum(v)": [55]})
    tm.assert_frame_equal(result_mv, expected)
    con.drop_materialized_view(mv_name)
    con.drop_table(tblc_name)


def test_sink_from(con, alltypes):
    sk_name = util.gen_name("sk_from")
    connector_properties = {
        "connector": "blackhole",
    }
    con.create_sink(sk_name, "functional_alltypes", connector_properties)
    con.drop_sink(sk_name)


def test_sink_as_select(con, alltypes):
    sk_name = util.gen_name("sk_as_select")
    expr = alltypes[["string_col"]].distinct().order_by("string_col")
    connector_properties = {
        "connector": "blackhole",
    }
    con.create_sink(sk_name, None, connector_properties, obj=expr)
    con.drop_sink(sk_name)
