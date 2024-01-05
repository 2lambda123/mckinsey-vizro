from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from dash import html

try:
    from pydantic.v1 import Field, validator
except ImportError:  # pragma: no cov
    from pydantic import Field, validator

from vizro.models import VizroBaseModel
from vizro.models._models_utils import _log_call, set_components, set_layout
from vizro.models.types import ComponentType

if TYPE_CHECKING:
    from vizro.models import Layout


class Container(VizroBaseModel):
    """A page in [`Dashboard`][vizro.models.Dashboard] with its own URL path and place in the `Navigation`.

    Args:
        type (Literal["container"]): Defaults to `"container"`.
        components (List[ComponentType]): See [ComponentType][vizro.models.types.ComponentType]. At least one component
            has to be provided.
        title (str): Title to be displayed.
        layout (Layout): Layout to place components in. Defaults to `None`.

    Raises:
        ValueError: If number of page and grid components is not the same
    """

    type: Literal["container"] = "container"
    components: List[ComponentType]
    title: str = Field(..., description="Title to be displayed.")
    layout: Layout = None  # type: ignore[assignment]

    # Re-used validators
    _validate_components = validator("components", allow_reuse=True, always=True)(set_components)
    _validate_layout = validator("layout", allow_reuse=True, always=True)(set_layout)

    @_log_call
    def build(self):
        components_content = [
            html.Div(
                component.build(),
                style={
                    "gridColumn": f"{grid_coord.col_start}/{grid_coord.col_end}",
                    "gridRow": f"{grid_coord.row_start}/{grid_coord.row_end}",
                },
            )
            for component, grid_coord in zip(self.components, self.layout.component_grid_lines)
        ]
        components_container = self._create_component_container(components_content)

        # TODO: Perhaps there is a better name for: className="container-container"
        return html.Div(children=[html.H3(self.title), components_container], className="container-container")

    def _create_component_container(self, components_content):
        component_container = html.Div(
            components_content,
            style={
                "gridRowGap": self.layout.row_gap,
                "gridColumnGap": self.layout.col_gap,
                "gridTemplateColumns": f"repeat({len(self.layout.grid[0])}, minmax({self.layout.col_min_width}, 1fr))",
                "gridTemplateRows": f"repeat({len(self.layout.grid)}, minmax({self.layout.row_min_height}, 1fr))",
            },
            className="component_container_grid",
        )
        return component_container
