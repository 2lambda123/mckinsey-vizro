from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from dash import html
from pydantic import validator

from vizro.models import VizroBaseModel
from vizro.models._models_utils import _log_call
from vizro.models.types import ComponentType
from vizro.models._models_utils import _log_call, get_unique_grid_component_ids

if TYPE_CHECKING:
    from vizro.models import Layout

# LQ: What should the final naming be? SubPage, Container, ...
class SubPage(VizroBaseModel):
    components: List[ComponentType]
    title: Optional[str]
    layout: Optional[Layout] = None

    @validator("layout", always=True)
    def set_layout(cls, layout, values):
        from vizro.models import Layout

        if "components" not in values:
            return layout

        if layout is None:
            grid = [[i] for i in range(len(values["components"]))]
            return Layout(grid=grid)

        unique_grid_idx = get_unique_grid_component_ids(layout.grid)
        if len(unique_grid_idx) != len(values["components"]):
            raise ValueError("Number of page and grid components need to be the same.")

        return layout


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
            for component, grid_coord in zip(
                self.components, self.layout.component_grid_lines  # type: ignore[union-attr]
            )
        ]
        components_container = self._create_component_container(components_content)

        return html.Div(children=[html.H3(self.title), components_container], className="subpage-container")

    def _create_component_container(self, components_content):

        component_container = html.Div(
                    components_content,
                    style={
                        "gridRowGap": self.layout.row_gap,  # type: ignore[union-attr]
                        "gridColumnGap": self.layout.col_gap,  # type: ignore[union-attr]
                        "gridTemplateColumns": f"repeat({len(self.layout.grid[0])},"  # type: ignore[union-attr]
                        f"minmax({self.layout.col_min_width}, 1fr))",
                        "gridTemplateRows": f"repeat({len(self.layout.grid)},"  # type: ignore[union-attr]
                        f"minmax({self.layout.row_min_height}, 1fr))",
                    },
                    className="component_container_grid",
                )
        return component_container
