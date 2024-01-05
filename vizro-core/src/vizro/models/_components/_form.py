from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from dash import html

try:
    from pydantic.v1 import validator
except ImportError:  # pragma: no cov
    from pydantic import validator

from vizro.models import VizroBaseModel
from vizro.models._components.form import (
    Button,
    Checklist,
    Dropdown,
    RadioItems,
    RangeSlider,
    Slider,
)
from vizro.models._models_utils import _log_call, set_layout
from vizro.models.types import _FormComponentType

if TYPE_CHECKING:
    from vizro.models import Layout


class Form(VizroBaseModel):
    """Container for all form components to be provided to [`Page`][vizro.models.Page].

    Args:
        type (Literal["form"]): Defaults to `"form"`.
        components (List[FormComponentType]): List of components used in the form.
        layout (Layout): Defaults to `None`.
    """

    type: Literal["form"] = "form"
    components: List[_FormComponentType]
    layout: Layout = None  # type: ignore[assignment]

    # Re-used validators
    _validate_layout = validator("layout", allow_reuse=True, always=True)(set_layout)

    @_log_call
    def pre_build(self):
        for component in self.components:
            if isinstance(component, (Slider, RangeSlider)):
                if component.min is None or component.max is None:
                    raise TypeError(f"{component.type} requires the arguments 'min' and 'max' when used within Form.")

            if isinstance(component, (Checklist, Dropdown, RadioItems)) and not component.options:
                raise TypeError(f"{component.type} requires the argument 'options' when used within Form.")

    @_log_call
    def build(self):
        component_container = [
            html.Div(
                component.build(),
                style={
                    "gridColumn": f"{grid_coord.col_start}/{grid_coord.col_end}",
                    "gridRow": f"{grid_coord.row_start}/{grid_coord.row_end}",
                },
            )
            for component, grid_coord in zip(self.components, self.layout.component_grid_lines)
        ]
        return self._make_form_layout(component_container)

    def _make_form_layout(self, component_container):
        return html.Div(
            component_container,
            style={
                "gridRowGap": self.layout.row_gap,
                "gridColumnGap": self.layout.col_gap,
                "gridTemplateColumns": f"repeat({len(self.layout.grid[0])}, minmax({self.layout.col_min_width}, 1fr))",
                "gridTemplateRows": f"repeat({len(self.layout.grid)}, minmax({self.layout.row_min_height}, 1fr))",
            },
            className="component_container_grid",
            id=self.id,
        )


if __name__ == "__main__":
    from vizro.models import Layout

    Form.update_forward_refs(Layout=Layout)

    print(  # noqa: T201
        repr(
            Form(
                layout=Layout(grid=[[i] for i in range(7)], row_min_height="200px"),
                components=[
                    Checklist(options=["Option 1", "Option 2", "Option 3"]),
                    Dropdown(options=["Option 1", "Option 2", "Option 3"]),
                    RadioItems(options=["Option 1", "Option 2", "Option 3"]),
                    Slider(min=0, max=5, step=1),
                    RangeSlider(min=0, max=5, step=1),
                    Button(id="form"),
                ],
            )
        )
    )
