import pandas as pd
import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro._constants import FILTER_ACTION_PREFIX
from vizro.actions import _filter
from vizro.models import Action
from vizro.models.types import MultiValueType, capture


def _filter_isin(series: pd.Series, value: MultiValueType) -> pd.Series:
    return series.isin(value)


@capture("action")
def my_custom_action(dropdown_value):
    """Custom action."""
    print(dropdown_value)
    text = f"The dropdown species is: {dropdown_value}"
    return text


df = px.data.iris()

page = vm.Page(
    title="Example of a custom action with UI inputs and outputs",
    components=[
        vm.Graph(
            id="scatter_chart",
            figure=px.scatter(
                df,
                x="sepal_length",
                y="petal_width",
                color="species",
                custom_data=["species"],
            ),
        ),
        vm.Graph(
            id="scatter_chart_2",
            figure=px.scatter(df, x="sepal_length", y="petal_width", color="species"),
        ),
        vm.Card(id="my_card", text="Click on a point on the above graph."),
    ],
    controls=[
        vm.Filter(
            column="species",
            selector=vm.Dropdown(
                id="dropdownA",
                title="Species",
                actions=[
                    Action(
                        function=_filter(
                            filter_column="species",
                            targets=["scatter_chart", "scatter_chart_2"],
                            filter_function=_filter_isin,
                        ),
                        id=f"{FILTER_ACTION_PREFIX}_dropdown",
                    ),
                    Action(
                        function=my_custom_action(),
                        inputs=["dropdownA.value"],
                        outputs=["my_card.children"],
                    ),
                ],
            ),
        )
    ],
)

dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
