"""Contains utilities to create the action_callback_mapping."""

from itertools import chain
from typing import Any, Callable, Dict, List, NamedTuple

from dash import Output, State, dcc

from vizro.actions import _on_page_load, _parameter, _filter, export_data, filter_interaction
from vizro.managers import data_manager, model_manager
from vizro.managers._model_manager import ModelID
from vizro.models import Action, Page, VizroBaseModel
from vizro.models._action._actions_chain import ActionsChain
from vizro.models._controls import Filter, Parameter
from vizro.models.types import ControlType


def _get_matching_actions_by_function(page: Page, action_function: Callable[[Any], Dict[str, Any]]) -> List[Action]:
    """Gets list of Actions on triggered page that match the provided action function."""
    return [
        action
        for actions_chain in page._get_page_actions_chains()
        for action in actions_chain.actions
        if action.function._function == action_function
    ]


# CALLBACK STATES --------------
def _get_inputs_of_controls(page: Page, control_type: ControlType) -> List[State]:
    """Gets list of States for selected control_type of triggered page."""
    return [
        State(
            component_id=control.selector.id,
            component_property="value",
        )
        for control in page.controls
        if isinstance(control, control_type)
    ]


def _get_inputs_of_chart_interactions(
    page: Page, action_function: Callable[[Any], Dict[str, Any]]
) -> List[State]:
    """Gets list of States for selected chart interaction `action_name` of triggered page."""
    chart_interactions_on_page = _get_matching_actions_by_function(
        page=page,
        action_function=action_function,
    )
    return [
        State(
            component_id=model_manager._get_action_trigger(action.id).id,
            component_property="clickData",
        )
        for action in chart_interactions_on_page
    ]


# TODO: Refactor this and util functions once we implement "_get_input_property" method in VizroBaseModel models
def _get_action_callback_inputs(action_id: ModelID) -> Dict[str, List[State]]:
    """Creates mapping of pre-defined action names and a list of States."""
    action_function = model_manager[action_id].function._function  # type: ignore[attr-defined]
    page: Page = model_manager._get_model_page(model_id=action_id)

    if action_function == export_data.__wrapped__:
        include_inputs = ["filters", "filter_interaction"]
    else:
        include_inputs = ["filters", "parameters", "filter_interaction", "theme_selector"]

    action_input_mapping = {
        "filters": (
            _get_inputs_of_controls(page=page, control_type=Filter) if "filters" in include_inputs else []
        ),
        "parameters": (
            _get_inputs_of_controls(page=page, control_type=Parameter)
            if "parameters" in include_inputs
            else []
        ),
        "filter_interaction": (
            _get_inputs_of_chart_interactions(page=page, action_function=filter_interaction.__wrapped__)
            if "filter_interaction" in include_inputs
            else []
        ),
        "theme_selector": (State("theme_selector", "on") if "theme_selector" in include_inputs else []),
    }
    return action_input_mapping


# CALLBACK OUTPUTS --------------
def _get_action_callback_outputs(action_id: ModelID) -> Dict[str, Output]:
    """Creates mapping of target names and their Output."""
    action_function = model_manager[action_id].function._function  # type: ignore[attr-defined]

    try:
        targets = model_manager[action_id].function["targets"]  # type: ignore[attr-defined]
    except KeyError:
        targets = []

    if action_function == _parameter.__wrapped__:
        targets = [target.split(".")[0] for target in targets]

    return {
        target: Output(
            component_id=target,
            component_property="figure",
            allow_duplicate=True,
        )
        for target in targets
    }


def _get_export_data_callback_outputs(action_id: ModelID) -> Dict[str, List[State]]:
    """Gets mapping of relevant output target name and Outputs for `export_data` action."""
    action = model_manager[action_id]

    try:
        targets = action.function["targets"]  # type: ignore[attr-defined]
    except KeyError:
        targets = None

    if not targets:
        targets = model_manager._get_model_page(model_id=action_id)._get_page_model_ids_with_figure()

    return {
        f"download-dataframe_{target}": Output(
            component_id={
                "type": "download-dataframe",
                "action_id": action_id,
                "target_id": target,
            },
            component_property="data",
        )
        for target in targets
    }


# CALLBACK COMPONENTS --------------
def _get_export_data_callback_components(action_id: ModelID) -> List[dcc.Download]:
    """Creates dcc.Downloads for target components of the `export_data` action."""
    action = model_manager[action_id]

    try:
        targets = action.function["targets"]  # type: ignore[attr-defined]
    except KeyError:
        targets = None

    if not targets:
        targets = model_manager._get_model_page(model_id=action_id)._get_page_model_ids_with_figure()

    return [
        dcc.Download(
            id={
                "type": "download-dataframe",
                "action_id": action_id,
                "target_id": target,
            },
        )
        for target in targets
    ]
