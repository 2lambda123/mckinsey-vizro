"""Task pipeline."""
import inspect


class Pipeline:
    """Task Pipeline."""

    def __init__(self, llm):
        """Initialization of pipeline class."""
        self.llm = llm
        self.stages = []
        self.components_instances = {}

    def _lazy_get_component(self, component_class):
        if component_class not in self.components_instances:
            self.components_instances[component_class] = component_class(llm=self.llm)
        return self.components_instances[component_class]

    def add(self, stage, initial_args=None, output_key=None, is_group=False):
        """Add task pipeline."""
        self.stages.append(
            (
                stage,
                initial_args,
                output_key,
                is_group,
            )
        )

    def run(self):
        """Run task pipeline."""
        current_args = None
        output = None
        for stage, initial_args, output_key, is_group in self.stages:
            if current_args is None and initial_args is not None:
                current_args = initial_args

            if is_group:
                for component_class, component_output_key in stage:
                    component = self._lazy_get_component(component_class)
                    output = self._run_component(component, current_args, component_output_key)
            else:
                component = self._lazy_get_component(stage)
                output = self._run_component(component, current_args, output_key)

        return output

    @staticmethod
    def _run_component(component, args, output_key=None):
        sig = inspect.signature(component.run)
        param_names = sig.parameters.keys()

        # Filter args to only include those that the run method accepts
        component_args = {k: v for k, v in args.items() if k in param_names}
        output = component.run(**component_args)
        if output_key:
            args[output_key] = output
        elif isinstance(output, dict):
            args.update(output or {})
        return output
