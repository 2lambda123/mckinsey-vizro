"""Example to show dashboard configuration."""

import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro.actions import export_data
from vizro.tables import dash_data_table

df_gapminder = px.data.gapminder()

single_tabs = vm.Page(
    title="Single Tabs",
    components=[
        vm.Tabs(
            id="first-tab",
            tabs=[
                vm.Container(
                    id="tab-1",
                    title="Tab I",
                    components=[
                        vm.Graph(
                            id="graph-1",
                            figure=px.line(
                                df_gapminder,
                                title="Graph-1",
                                x="year",
                                y="lifeExp",
                                color="continent",
                                line_group="country",
                                hover_name="country",
                            ),
                        ),
                        vm.Graph(
                            id="graph-2",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-2",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                        vm.Graph(
                            id="graph-3",
                            figure=px.box(
                                df_gapminder,
                                title="Graph-3",
                                x="continent",
                                y="lifeExp",
                                color="continent",
                            ),
                        ),
                        vm.Button(
                            text="Export data",
                            actions=[
                                vm.Action(function=export_data()),
                            ],
                        ),
                    ],
                ),
                vm.Container(
                    id="tab-2",
                    title="Tab II",
                    components=[
                        vm.Graph(
                            id="graph-4",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-4",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                        vm.Graph(
                            id="graph-5",
                            figure=px.box(
                                df_gapminder,
                                title="Graph-5",
                                x="continent",
                                y="lifeExp",
                                color="continent",
                            ),
                        ),
                        vm.Graph(
                            id="graph-6",
                            figure=px.line(
                                df_gapminder,
                                title="Graph-6",
                                x="year",
                                y="lifeExp",
                                color="continent",
                                line_group="country",
                                hover_name="country",
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
    controls=[
        vm.Parameter(
            targets=[
                "graph-1.y",
                "graph-2.y",
                "graph-3.y",
                "graph-4.y",
                "graph-5.y",
                "graph-6.y",
            ],
            selector=vm.RadioItems(options=["lifeExp", "pop", "gdpPercap"], title="Select variable"),
        ),
        vm.Filter(column="continent"),
    ],
)
multiple_containers_custom_layout = vm.Page(
    title="Multiple Containers - custom layout",
    components=[
        vm.Container(
            id="cont_1",
            title="Container I",
            layout=vm.Layout(grid=[[0, 1]]),
            components=[
                vm.Graph(
                    id="graph_11",
                    figure=px.line(
                        df_gapminder,
                        title="Graph-11",
                        x="year",
                        y="lifeExp",
                        color="continent",
                        line_group="country",
                        hover_name="country",
                    ),
                ),
                vm.Graph(
                    id="graph_12",
                    figure=px.scatter(
                        df_gapminder,
                        title="Graph-12",
                        x="gdpPercap",
                        y="lifeExp",
                        size="pop",
                        color="continent",
                    ),
                ),
            ],
        ),
        vm.Container(
            id="cont_2",
            title="Container II",
            layout=vm.Layout(grid=[[0, 1]], row_min_height="300px"),
            components=[
                vm.Graph(
                    id="graph_13",
                    figure=px.box(
                        df_gapminder,
                        title="Graph-13",
                        x="continent",
                        y="lifeExp",
                        color="continent",
                    ),
                ),
                vm.Button(
                    text="Export data",
                    actions=[
                        vm.Action(function=export_data()),
                    ],
                ),
            ],
        ),
    ],
    controls=[
        vm.Filter(column="continent"),
    ],
)
single_tabs_action = vm.Page(
    title="Single Tabs - with action",
    components=[
        vm.Tabs(
            tabs=[
                vm.Container(
                    id="container_table",
                    title="Tab I Table",
                    components=[
                        vm.Table(
                            id="table-1",
                            figure=dash_data_table(
                                id="dash_datatable-1",
                                data_frame=df_gapminder,
                            ),
                        ),
                    ],
                )
            ]
        ),
        vm.Button(
            text="Export data",
            actions=[
                vm.Action(function=export_data()),
            ],
        ),
    ],
    controls=[
        vm.Filter(column="continent"),
    ],
)

multiple_tabs = vm.Page(
    id="page_4",
    title="Multiple Tabs",
    components=[
        vm.Tabs(
            id="page-4-tab1",
            tabs=[
                vm.Container(
                    title="Tab 1 container 1",
                    components=[
                        vm.Graph(
                            id="graph-44",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-44",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                    ],
                ),
                vm.Container(
                    title="Tab 1 container 2",
                    components=[
                        vm.Graph(
                            id="graph-441",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-441",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                    ],
                ),
            ],
        ),
        vm.Tabs(
            id="page-4-tab2",
            tabs=[
                vm.Container(
                    title="Tab 2 container",
                    components=[
                        vm.Graph(
                            id="graph-45",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-45",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                    ],
                ),
                vm.Container(
                    title="Tab 2 container 2",
                    components=[
                        vm.Graph(
                            id="graph-451",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-451",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)
single_tabs_custom_layout = vm.Page(
    title="Single Tabs - custom layout",
    components=[
        vm.Tabs(
            id="first-tabr",
            tabs=[
                vm.Container(
                    layout=vm.Layout(grid=[[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 2, 2], [1, 1, 2, 2], [3, -1, -1, -1]]),
                    id="tab-1r",
                    title="Tab I Title",
                    components=[
                        vm.Graph(
                            id="graph-1r",
                            figure=px.line(
                                df_gapminder,
                                title="Graph-1",
                                x="year",
                                y="lifeExp",
                                color="continent",
                                line_group="country",
                                hover_name="country",
                            ),
                        ),
                        vm.Graph(
                            id="graph-2r",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-2",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                        vm.Graph(
                            id="graph-3r",
                            figure=px.box(
                                df_gapminder,
                                title="Graph-3",
                                x="continent",
                                y="lifeExp",
                                color="continent",
                            ),
                        ),
                        vm.Button(
                            text="Export data",
                            actions=[
                                vm.Action(function=export_data()),
                            ],
                        ),
                    ],
                ),
                vm.Container(
                    id="tab-2r",
                    title="Tab II",
                    layout=vm.Layout(
                        grid=[
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [1, 1, 2, 2],
                            [1, 1, 2, 2],
                        ]
                    ),
                    components=[
                        vm.Graph(
                            id="graph-4r",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-4",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                        vm.Graph(
                            id="graph-5r",
                            figure=px.box(
                                df_gapminder,
                                title="Graph-5",
                                x="continent",
                                y="lifeExp",
                                color="continent",
                            ),
                        ),
                        vm.Graph(
                            id="graph-6r",
                            figure=px.line(
                                df_gapminder,
                                title="Graph-6",
                                x="year",
                                y="lifeExp",
                                color="continent",
                                line_group="country",
                                hover_name="country",
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)

multiple_containers_nested = vm.Page(
    id="page_6",
    title="Multiple Containers - Nested",
    layout=vm.Layout(
        grid=[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
    ),
    components=[
        vm.Container(
            layout=vm.Layout(grid=[[0, 1], [0, 1]]),
            components=[
                vm.Container(
                    layout=vm.Layout(
                        grid=[
                            [0, 0, 1, 1],
                            [0, 0, 1, 1],
                            [2, 2, 3, 3],
                            [2, 2, 3, 3],
                        ]
                    ),
                    components=[
                        vm.Graph(
                            id="graph-1rn",
                            figure=px.line(
                                df_gapminder,
                                title="Graph-1",
                                x="year",
                                y="lifeExp",
                                color="continent",
                                line_group="country",
                                hover_name="country",
                            ),
                        ),
                        vm.Graph(
                            id="graph-2rn",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-2",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                        vm.Graph(
                            id="graph-3rn",
                            figure=px.box(
                                df_gapminder,
                                title="Graph-3",
                                x="continent",
                                y="lifeExp",
                                color="continent",
                            ),
                        ),
                        vm.Graph(
                            id="graph-2rnn",
                            figure=px.scatter(
                                df_gapminder,
                                title="Graph-2",
                                x="gdpPercap",
                                y="lifeExp",
                                size="pop",
                                color="continent",
                            ),
                        ),
                    ],
                ),
                vm.Container(
                    components=[
                        vm.Graph(
                            id="graph-6rn",
                            figure=px.line(
                                df_gapminder,
                                title="Graph-6",
                                x="year",
                                y="lifeExp",
                                color="continent",
                                line_group="country",
                                hover_name="country",
                            ),
                        )
                    ]
                ),
            ],
        ),
        vm.Container(
            title="Second container",
            components=[
                vm.Graph(
                    id="graph-6rnn",
                    figure=px.line(
                        df_gapminder,
                        title="Graph-6",
                        x="year",
                        y="lifeExp",
                        color="continent",
                        line_group="country",
                        hover_name="country",
                    ),
                )
            ],
        ),
    ],
)

dashboard = vm.Dashboard(pages=[single_tabs,
                                single_tabs_custom_layout,
                                single_tabs_action,
                                multiple_tabs,
                                multiple_containers_custom_layout,
                                multiple_containers_nested
                                ])

if __name__ == "__main__":
    Vizro(assets_folder="../assets").build(dashboard).run()
