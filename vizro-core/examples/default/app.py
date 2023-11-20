"""Example to show dashboard configuration."""

import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro.actions import export_data, filter_interaction
from vizro.tables import dash_data_table

df_gapminder = px.data.gapminder()

page = vm.Page(
    # title="Testing out tabs: [0, [1, 2 ,3, B], [4, 5, [6, 7], [8]]]",
    title="Testing out tabs",
    components=[
        vm.Table(
            id="table-0",
            figure=dash_data_table(
                id="dash_datatable-0",
                data_frame=df_gapminder,
            ),
            actions=[
                vm.Action(
                    function=filter_interaction(
                        targets=["graph-1", "graph-2", "graph-3", "graph-4", "graph-5", "graph-6", "graph-7", "graph-8"]
                    )
                ),
            ],
        ),
        vm.Tabs(
            subpages=[
                vm.SubPage(
                    id="tab-1",
                    title="Tab I Title",
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
                vm.SubPage(
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
                        vm.Tabs(
                            subpages=[
                                vm.SubPage(
                                    id="subtab-1",
                                    title="Subtab I Title",
                                    components=[
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
                                        vm.Graph(
                                            id="graph-7",
                                            figure=px.scatter(
                                                df_gapminder,
                                                title="Graph-7",
                                                x="gdpPercap",
                                                y="lifeExp",
                                                size="pop",
                                                color="continent",
                                            ),
                                        ),
                                    ],
                                ),
                                vm.SubPage(
                                    id="subtab-2",
                                    title="Subtab II",
                                    components=[
                                        vm.Graph(
                                            id="graph-8",
                                            figure=px.box(
                                                df_gapminder,
                                                title="Graph-8",
                                                x="continent",
                                                y="lifeExp",
                                                color="continent",
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
    controls=[
        # TODO: Fix issue of graphs only being updated if they are target of controls
        # e.g. if you don't add the parameter below, all of the charts will not get loaded
        # probably need to implement some logic for an on_tab_load action
        vm.Parameter(
            targets=[
                "graph-1.y",
                "graph-2.y",
                "graph-3.y",
                "graph-4.y",
                "graph-5.y",
                "graph-6.y",
                "graph-7.y",
                "graph-8.y",
            ],
            selector=vm.RadioItems(options=["lifeExp", "pop", "gdpPercap"], title="Select variable"),
        ),
        vm.Filter(column="continent"),
    ],
)
page_2 = vm.Page(
    title="Containers page",
    components=[
        vm.SubPage(
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
        vm.SubPage(
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
)
page_3 = vm.Page(
    title="Third page",
    components=[
        vm.Tabs(
            subpages=[
                vm.SubPage(
                    id="subpage_table",
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
        )
    ],
)

dashboard = vm.Dashboard(pages=[page, page_2, page_3])

if __name__ == "__main__":
    Vizro(assets_folder="../assets").build(dashboard).run()
