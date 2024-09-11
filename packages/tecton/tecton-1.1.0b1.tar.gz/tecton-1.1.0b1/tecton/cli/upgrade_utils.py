import datetime
from typing import List
from typing import Tuple
from typing import Union

from tecton import tecton_context
from tecton.aggregation_functions import AggregationFunction
from tecton.cli.error_utils import format_validation_location_fancy
from tecton.cli.printer import safe_print
from tecton.framework import base_tecton_object
from tecton.framework.base_tecton_object import BaseTectonObject
from tecton.framework.configs import LifetimeWindow
from tecton.framework.configs import TimeWindow
from tecton.framework.configs import TimeWindowSeries
from tecton.framework.feature_view import AggregationLeadingEdge
from tecton.framework.feature_view import FeatureView
from tecton.framework.feature_view import MaterializedFeatureView
from tecton.framework.workspace import get_workspace
from tecton.v09_compat.framework import BatchFeatureView
from tecton.v09_compat.framework import DataSource
from tecton.v09_compat.framework import Entity
from tecton.v09_compat.framework import FeatureTable
from tecton.v09_compat.framework import OnDemandFeatureView
from tecton.v09_compat.framework import PushSource
from tecton.v09_compat.framework import StreamFeatureView
from tecton_core.specs.utils import get_field_or_none
from tecton_core.time_utils import proto_to_duration
from tecton_proto.args.pipeline__client_pb2 import TimeReference
from tecton_proto.common.aggregation_function__client_pb2 import AggregationFunctionParams


def timedelta_to_string(td):
    if td < datetime.timedelta(0):
        return f"-{timedelta_to_string(-td)}"

    components = []
    days = td.days
    seconds = td.seconds
    microseconds = td.microseconds

    if days:
        components.append(f"days={days}")
    if seconds:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            components.append(f"hours={hours}")
        if minutes:
            components.append(f"minutes={minutes}")
        if seconds:
            components.append(f"seconds={seconds}")
    if microseconds:
        components.append(f"microseconds={microseconds}")

    if not components:
        return "timedelta()"

    return f"timedelta({', '.join(components)})"


def _aggregation_function_to_string_render(
    aggregation_function: AggregationFunction, params: AggregationFunctionParams
) -> str:
    if aggregation_function.base_name == "lastn":
        return f"last_distinct({params.last_n.n})"
    elif aggregation_function.base_name == "last_non_distinct_n":
        return f"last({params.last_n.n})"
    elif aggregation_function.base_name == "first_distinct_n":
        return f"first_distinct({params.first_n.n})"
    elif aggregation_function.base_name == "first_non_distinct_n":
        return f"first({params.first_n.n})"
    elif aggregation_function.base_name == "approx_count_distinct":
        return f"approx_count_distinct({params.approx_count_distinct.precision})"
    elif aggregation_function.base_name == "approx_percentile":
        return f"approx_percentile{params.approx_percentile.percentile, params.approx_percentile.precision}"
    else:
        # All other functions without explicit AggregationFunction class-overrides (ex: "mean") are passed as strings; thus the double quotes
        return f'"{aggregation_function.base_name}"'


def _get_feature_view(feature_view_name: str) -> FeatureView:
    ws = get_workspace(tecton_context.get_current_workspace())
    return ws.get_feature_view(feature_view_name)


def _get_feature_table(feature_table_name: str) -> FeatureTable:
    ws = get_workspace(tecton_context.get_current_workspace())
    return ws.get_feature_table(feature_table_name)


def _get_complete_status_emoji(is_complete: bool) -> str:
    return "✅" if is_complete else "🚫"


class BaseGuidance:
    _object: BaseTectonObject
    _obj_type: str
    _repo_root: str

    def __init__(self, _object: BaseTectonObject, _repo_root: str):
        self._object = _object
        self._repo_root = _repo_root

    def _get_upgrade_guidance(self) -> List[str]:
        raise NotImplementedError

    def print_guidance(self) -> None:
        format_validation_location_fancy(self._object, self._repo_root)
        safe_print("\n".join(self._get_upgrade_guidance()))
        safe_print("\n")


class DataSourceGuidance(BaseGuidance):
    _object: DataSource
    _obj_type = "DataSource"

    def _get_upgrade_guidance(self) -> List[str]:
        guidance = []
        if isinstance(self._object, PushSource):
            guidance.append(
                f"{_get_complete_status_emoji(False)} PushSource was deprecated in 0.9. Replace `PushSource` with `StreamSource` and set `stream_config=PushConfig()`. \nSee https://docs.tecton.ai/docs/release-notes/upgrade-process/to-09-upgrade-guide#step-by-step-upgrade-flow (Replace PushSource objects with a StreamSource that uses a PushConfig) for an example."
            )
        guidance.append(f"{_get_complete_status_emoji(False)} Update import from tecton.v09_compat to tecton.")
        return guidance


class EntityGuidance(BaseGuidance):
    _object: Entity
    _obj_type = "Entity"

    def _find_feature_view_with_entity(self):
        for local_object in base_tecton_object._LOCAL_TECTON_OBJECTS:
            if issubclass(local_object.__class__, MaterializedFeatureView):
                fv_entities: List[Entity] = local_object.entities
                for entity in fv_entities:
                    if entity.name == self._object.name:
                        return local_object
        return None

    def _get_upgrade_guidance(self) -> List[str]:
        feature_view_with_entity = self._find_feature_view_with_entity()

        output_strs = []
        if feature_view_with_entity is None:
            output_strs.append(
                f"Unable to determine join key types of {self._object.name}. Please replace your entity with the below where <TYPE> is the type of your join key."
            )
            converted_join_keys = ", ".join(
                [f'Field("{join_key_name}", <TYPE>)' for join_key_name in self._object._spec.join_key_names]
            )
        else:
            feature_view = _get_feature_view(feature_view_with_entity.name)
            view_schema = feature_view._feature_definition.view_schema.to_dict()
            converted_join_keys = ", ".join(
                [
                    f'Field("{join_key_name}", {view_schema[join_key_name]})'
                    for join_key_name in self._object._spec.join_key_names
                ]
            )
        output_strs.append(
            f"{_get_complete_status_emoji(False)} Replace `join_keys=[...]` with `join_keys=[{converted_join_keys}]`."
        )
        output_strs.append(
            f"{_get_complete_status_emoji(False)} Update import from `from tecton.v09_compat import Entity` to `from tecton import Entity`."
        )
        return output_strs


class MaterializedFeatureViewGuidance(BaseGuidance):
    _object: Union[BatchFeatureView, StreamFeatureView]
    _obj_type: str
    _stored_feature_view: FeatureView

    def __init__(self, _object, _repo_root):
        super().__init__(_object, _repo_root)
        self._stored_feature_view = _get_feature_view(self._object.name)
        self._view_schema = self._stored_feature_view._feature_definition.view_schema.to_dict()

    def _build_timestamp_recommendation(self):
        timestamp_field = self._stored_feature_view._feature_definition.timestamp_key
        return f'Set `timestamp_field="{timestamp_field}"`.'

    def __render_time_window(self, time_window: Union[TimeWindow, TimeWindowSeries, LifetimeWindow]) -> str:
        if isinstance(time_window, TimeWindow):
            if time_window.offset == datetime.timedelta(seconds=0):
                return f"{timedelta_to_string(time_window.window_size)}"
            return (
                f"TimeWindow(window_size={timedelta_to_string(time_window.window_size)}, offset={time_window.offset})"
            )
        return time_window._to_spec().to_string()

    def _build_aggregation_replacement(self) -> List[str]:
        aggregates = []
        aggregate_name_to_function_params = {
            aggregation.output_feature_name: get_field_or_none(aggregation, "function_params")
            for aggregation in self._object._spec.aggregate_features
        }
        for aggregation in self._object.aggregations:
            input_column_name = aggregation.column
            input_column_type = self._view_schema.get(input_column_name) or "<COLUMN_TYPE>"
            function_render = _aggregation_function_to_string_render(
                aggregation.function, aggregate_name_to_function_params.get(aggregation.name) or {}
            )
            time_window = self.__render_time_window(aggregation.time_window)
            aggregate_replacement = f'Aggregate(input_column=Field("{input_column_name}", {input_column_type}), function={function_render}, time_window={time_window})'
            aggregates.append(aggregate_replacement)
        return aggregates

    # Embeddings and Inference were not live in 0.9, so only need to handle attributes
    def _build_attribute_replacement(self) -> List[str]:
        attributes = []

        for attribute in self._stored_feature_view._feature_definition.features:
            attribute_dtype = self._view_schema.get(attribute) or "<COLUMN_TYPE>"
            attribute = f'Attribute("{attribute}", dtype={attribute_dtype})'
            attributes.append(attribute)
        return attributes

    def _get_upgrade_guidance(self) -> List[str]:
        output_steps = []
        is_timestamp_field_set = self._object._args.materialized_feature_view_args.timestamp_field != ""
        output_steps.append(
            f"{_get_complete_status_emoji(is_timestamp_field_set)} {self._build_timestamp_recommendation()}"
        )

        if bool(self._object.aggregations):
            is_schema_removed = not self._object._args.materialized_feature_view_args.schema.columns
            output_steps.append((f"{_get_complete_status_emoji(is_schema_removed)} Remove `schema=[...]`"))

            is_features_set = self._object._use_feature_param()
            aggregate_feature_suggestions = self._build_aggregation_replacement()
            aggregate_feature_string = ",\n\t".join(aggregate_feature_suggestions)
            output_steps.append(
                f"{_get_complete_status_emoji(is_features_set)} Replace `aggregations=[...]` with \n```\nfeatures=[\n\t{aggregate_feature_string}\n]\n```."
            )
        else:
            is_schema_removed = not self._object._args.materialized_feature_view_args.schema.columns
            output_steps.append((f"{_get_complete_status_emoji(is_schema_removed)} Remove `schema=[...]`"))

            is_features_set = self._object._use_feature_param()
            attribute_feature_suggestions = self._build_attribute_replacement()
            attribute_feature_string = ",\n\t".join(attribute_feature_suggestions)
            output_steps.append(
                f"{_get_complete_status_emoji(is_features_set)} Add \n```\nfeatures=[\n\t{attribute_feature_string}\n]\n```."
            )
        return output_steps

    def _build_filtered_source_replacements(self) -> Tuple[List[str], List[str], bool]:
        filtered_source_replacements = []
        args_data_source_node = [
            input.node.data_source_node
            for input in self._object._args.pipeline.root.transformation_node.inputs
            if input.node.HasField("data_source_node")
        ]

        data_proto_data_source_nodes = {
            input.node.data_source_node.input_name: input.node.data_source_node
            for input in self._stored_feature_view._feature_definition.pipeline.root.transformation_node.inputs
            if input.node.HasField("data_source_node")
        }

        all_done = True
        currently_existing = []
        for data_source_node in args_data_source_node:
            existing_data_source_node = data_proto_data_source_nodes.get(data_source_node.input_name)
            assert existing_data_source_node, f"Cannot find data source node named {data_source_node.input_name}"

            # if start_time_offset is set, then we're obviously using the legacy FilteredSource approach
            if get_field_or_none(data_source_node, "start_time_offset") is not None:
                start_time_offset_as_duration = proto_to_duration(data_source_node.start_time_offset).as_timedelta()
                start_time_offset_as_string = f"{'+ ' if start_time_offset_as_duration > datetime.timedelta(0) else ''}{timedelta_to_string(start_time_offset_as_duration)}"

                currently_existing.append(
                    f"FilteredSource({data_source_node.input_name}, start_time_offset={start_time_offset_as_string})"
                )
                filtered_source_replacements.append(
                    f"{data_source_node.input_name}.select_range(\n\tstart_time = TectonTimeConstant.MATERIALIZATION_START_TIME{start_time_offset_as_string},\n\tend_time = TectonTimeConstant.MATERIALIZATION_END_TIME\n)"
                )
                all_done = False
                continue

            if proto_to_duration(existing_data_source_node.start_time_offset).as_timedelta() != datetime.timedelta(0):
                is_using_select_range = get_field_or_none(data_source_node, "start_time_offset") is None
                if not is_using_select_range:
                    all_done = False
                start_time_offset_as_duration = proto_to_duration(
                    existing_data_source_node.start_time_offset
                ).as_timedelta()
                start_time_offset_as_string = f"{'+ ' if start_time_offset_as_duration > datetime.timedelta(0) else ''}{timedelta_to_string(start_time_offset_as_duration)}"
                currently_existing.append(
                    f"FilteredSource({data_source_node.input_name}, start_time_offset={start_time_offset_as_string})"
                )
                filtered_source_replacements.append(
                    f"{data_source_node.input_name}.select_range(\n\tstart_time = TectonTimeConstant.MATERIALIZATION_START_TIME{start_time_offset_as_string},\n\tend_time = TectonTimeConstant.MATERIALIZATION_END_TIME\n)"
                )
            elif existing_data_source_node.window_unbounded:
                is_marked_unfiltered = (
                    data_source_node.filter_start_time.relative_time.time_reference
                    == TimeReference.TIME_REFERENCE_UNBOUNDED_PAST
                    and data_source_node.filter_end_time.relative_time.time_reference
                    == TimeReference.TIME_REFERENCE_UNBOUNDED_FUTURE
                )
                if not is_marked_unfiltered:
                    all_done = False
                currently_existing.append(data_source_node.input_name)
                filtered_source_replacements.append(f"{data_source_node.input_name}.unfiltered()")
            elif existing_data_source_node.window_unbounded_preceding:
                is_marked_unbounded_preceding = (
                    data_source_node.filter_start_time.relative_time.time_reference
                    == TimeReference.TIME_REFERENCE_UNBOUNDED_PAST
                    and data_source_node.filter_end_time.relative_time.time_reference
                    == TimeReference.TIME_REFERENCE_MATERIALIZATION_END_TIME
                )
                if not is_marked_unbounded_preceding:
                    all_done = False
                currently_existing.append(data_source_node.input_name)
                filtered_source_replacements.append(
                    f"{data_source_node.input_name}.select_range(\n\tstart_time = TectonTimeConstant.UNBOUNDED_PAST,\n\tend_time = TectonTimeConstant.MATERIALIZATION_END_TIME\n)"
                )
            else:
                is_marked_filtered = (
                    data_source_node.filter_start_time.relative_time.time_reference
                    == TimeReference.TIME_REFERENCE_MATERIALIZATION_START_TIME
                    and data_source_node.filter_end_time.relative_time.time_reference
                    == TimeReference.TIME_REFERENCE_MATERIALIZATION_END_TIME
                )
                if not is_marked_filtered:
                    all_done = False
                currently_existing.append(f"FilteredSource({data_source_node.input_name})")
                filtered_source_replacements.append(f"{data_source_node.input_name}")
        return currently_existing, filtered_source_replacements, all_done


class BatchFeatureViewGuidance(MaterializedFeatureViewGuidance):
    _object: BatchFeatureView
    _obj_type = "BatchFeatureView"

    def _build_filtered_source_guidance(self) -> str:
        currently_existing, filtered_source_replacements, all_done = self._build_filtered_source_replacements()
        currently_existing_str = ", ".join(currently_existing)
        filtered_source_replacement_str = ", ".join(filtered_source_replacements)

        return f"{_get_complete_status_emoji(all_done)} Replace `sources=[{currently_existing_str}]` with `sources=[{filtered_source_replacement_str}]`."

    def _get_upgrade_guidance(self) -> List[str]:
        guidance = super()._get_upgrade_guidance()
        guidance.append(self._build_filtered_source_guidance())
        guidance.append(
            f"{_get_complete_status_emoji(False)} Update import from `tecton.v09_compat.batch_feature_view` to `tecton.batch_feature_view`."
        )
        return guidance


class StreamFeatureViewGuidance(MaterializedFeatureViewGuidance):
    _object: StreamFeatureView
    _obj_type = "StreamFeatureView"

    def _build_filtered_source_guidance(self) -> str:
        currently_existing, filtered_source_replacements, all_done = self._build_filtered_source_replacements()
        currently_existing_str = ", ".join(currently_existing)
        filtered_source_replacement_str = ", ".join(filtered_source_replacements)
        return f"{_get_complete_status_emoji(all_done)} Replace `source={currently_existing_str}` with `source={filtered_source_replacement_str}`."

    def _get_aggregation_leading_edge_guidance(self) -> str:
        is_aggregation_leading_edge_set = (
            self._object._args.materialized_feature_view_args.aggregation_leading_edge
            == AggregationLeadingEdge.UNSPECIFIED
        )
        return f"{_get_complete_status_emoji(is_aggregation_leading_edge_set)} Set `aggregation_leading_edge=AggregationLeadingEdge.LATEST_EVENT_TIME`."

    def _get_upgrade_guidance(self) -> List[str]:
        guidance = super()._get_upgrade_guidance()
        guidance.append(self._build_filtered_source_guidance())
        guidance.append(self._get_aggregation_leading_edge_guidance())
        guidance.append(f"{_get_complete_status_emoji(False)} Update import from `tecton.v09_compat` to `tecton`.")
        return guidance


class OnDemandFeatureViewGuidance(BaseGuidance):
    _object: OnDemandFeatureView
    _obj_type = "OnDemandFeatureView"

    def __init__(self, _object, _repo_root):
        super().__init__(_object, _repo_root)
        self._stored_feature_view = _get_feature_view(self._object.name)
        self._view_schema = self._stored_feature_view._feature_definition.view_schema.to_dict()

    # Embeddings and Inference were not live in 0.9, so only need to handle attributes
    def _build_attribute_replacement(self):
        attributes = []

        for attribute in self._stored_feature_view._feature_definition.features:
            attribute_dtype = self._view_schema.get(attribute) or "<COLUMN_TYPE>"
            attribute = f'Attribute("{attribute}", dtype={attribute_dtype})'
            attributes.append(attribute)
        return attributes

    def _get_upgrade_guidance(self) -> List[str]:
        output_steps = []
        is_schema_removed = not self._object._args.realtime_args.schema.fields
        output_steps.append((f"{_get_complete_status_emoji(is_schema_removed)} Remove `schema=[...]`"))

        is_features_set = self._object._use_feature_param()
        attribute_feature_suggestions = self._build_attribute_replacement()
        attribute_feature_string = ",\n\t".join(attribute_feature_suggestions)
        output_steps.append(
            f"{_get_complete_status_emoji(is_features_set)} Add \n```\nfeatures=[\n\t{attribute_feature_string}\n]\n```."
        )

        output_steps.append(
            f"{_get_complete_status_emoji(False)} Rename from `on_demand_feature_view` to realtime_feature_view` and update import from `tecton.v09_compat.on_demand_feature_view` to `tecton.realtime_feature_view`."
        )
        return output_steps


class FeatureTableGuidance(BaseGuidance):
    _object: FeatureTable
    _obj_type = "FeatureTable"

    def __init__(self, _object, _repo_root):
        super().__init__(_object, _repo_root)
        self._stored_feature_view = _get_feature_table(self._object.name)
        self._view_schema = self._stored_feature_view._feature_definition.view_schema.to_dict()

    def _build_timestamp_recommendation(self):
        timestamp_field = self._stored_feature_view._feature_definition.timestamp_key
        return f'Set `timestamp_field="{timestamp_field}"`.'

    # Embeddings and Inference were not live in 0.9, so only need to handle attributes
    def _build_attribute_replacement(self):
        attributes = []

        for attribute in self._stored_feature_view._feature_definition.features:
            attribute_dtype = self._view_schema.get(attribute) or "<COLUMN_TYPE>"
            attribute = f'Attribute("{attribute}", dtype={attribute_dtype})'
            attributes.append(attribute)
        return attributes

    def _get_upgrade_guidance(self) -> List[str]:
        output_steps = []
        is_timestamp_field_set = self._object._args.feature_table_args.timestamp_field != ""
        output_steps.append(
            f"{_get_complete_status_emoji(is_timestamp_field_set)} {self._build_timestamp_recommendation()}"
        )

        is_schema_removed = not self._object._args.feature_table_args.schema.fields
        output_steps.append((f"{_get_complete_status_emoji(is_schema_removed)} Remove `schema=[...]`"))

        is_features_set = self._object._use_feature_param()
        attribute_feature_suggestions = self._build_attribute_replacement()
        attribute_feature_string = ",\n\t".join(attribute_feature_suggestions)
        output_steps.append(
            f"{_get_complete_status_emoji(is_features_set)} Add \n```\nfeatures=[\n\t{attribute_feature_string}\n]\n```."
        )

        output_steps.append(
            f"{_get_complete_status_emoji(False)} Update import from `tecton.v09_compat.FeatureTable` to `tecton.FeatureTable`."
        )
        return output_steps
