# Copyright 2023 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd

from secretflow.component.component import Component, IoType, TableColParam
from secretflow.component.data_utils import DistDataType, load_table
from secretflow.spec.v1.component_pb2 import Attribute
from secretflow.spec.v1.data_pb2 import DistData
from secretflow.spec.v1.report_pb2 import Div, Report, Tab, Table
from secretflow.stats.table_statistics import table_statistics

table_statistics_comp = Component(
    name="table_statistics",
    domain="stats",
    version="0.0.2",
    desc="""Get a table of statistics,
    including each column's

    1. datatype
    2. total_count
    3. count
    4. count_na
    5. na_ratio
    6. min
    7. max
    8. mean
    9. var
    10. std
    11. sem
    12. skewness
    13. kurtosis
    14. q1
    15. q2
    16. q3
    17. moment_2
    18. moment_3
    19. moment_4
    20. central_moment_2
    21. central_moment_3
    22. central_moment_4
    23. sum
    24. sum_2
    25. sum_3
    26. sum_4

    - moment_2 means E[X^2].
    - central_moment_2 means E[(X - mean(X))^2].
    - sum_2 means sum(X^2).
    """,
)


table_statistics_comp.io(
    io_type=IoType.INPUT,
    name="input_data",
    desc="Input table.",
    types=[DistDataType.VERTICAL_TABLE, DistDataType.INDIVIDUAL_TABLE],
    col_params=[
        TableColParam(
            name="features",
            desc="perform statistics on these columns",
            col_min_cnt_inclusive=1,
        ),
    ],
)
table_statistics_comp.io(
    io_type=IoType.OUTPUT,
    name="report",
    desc="Output table statistics report.",
    types=[DistDataType.REPORT],
    col_params=None,
)


def gen_table_statistic_report(df: pd.DataFrame) -> Report:
    headers, rows = [], []
    for k in df.columns:
        headers.append(Table.HeaderItem(name=k, desc="", type="str"))

    for index, df_row in df.iterrows():
        rows.append(
            Table.Row(
                name=index, items=[Attribute(s=str(df_row[k])) for k in df.columns]
            )
        )

    r_table = Table(headers=headers, rows=rows)

    return Report(
        name="table statistics",
        desc="",
        tabs=[
            Tab(
                divs=[
                    Div(
                        children=[
                            Div.Child(
                                type="table",
                                table=r_table,
                            )
                        ],
                    )
                ],
            )
        ],
    )


def dump_table_statistics(name, system_info, df: pd.DataFrame) -> DistData:
    report_mate = gen_table_statistic_report(df)
    res = DistData(
        name=name,
        system_info=system_info,
        type=str(DistDataType.REPORT),
        data_refs=[],
    )
    res.meta.Pack(report_mate)
    return res


@table_statistics_comp.eval_fn
def table_statistics_eval_fn(*, ctx, input_data, input_data_features, report):
    input_df = load_table(
        ctx,
        input_data,
        load_features=True,
        load_labels=True,
        load_ids=True,
        col_selects=input_data_features,
    )

    with ctx.tracer.trace_running():
        stat = table_statistics(input_df)

    return {"report": dump_table_statistics(report, input_data.system_info, stat)}
