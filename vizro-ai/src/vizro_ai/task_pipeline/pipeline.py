class Pipeline:
    def __init__(self, llm):
        self.llm = llm
        self.stages = []
        self.components_instances = {}

    def _lazy_get_component(self, component_class):
        if component_class not in self.components_instances:
            self.components_instances[component_class] = component_class(llm=self.llm)
        return self.components_instances[component_class]

    def add(self, stage, initial_args=None, is_group=False):
        self.stages.append((stage, initial_args, is_group))

    def run(self):
        current_args = None
        for stage, initial_args, is_group in self.stages:
            if current_args is None and initial_args is not None:
                current_args = initial_args

            if is_group:
                for component_class in stage:
                    component = self._lazy_get_component(component_class)
                    current_args = self._run_component(component, current_args)
            else:
                component = self._lazy_get_component(stage)
                current_args = self._run_component(component, current_args)

        return current_args

    def _run_component(self, component, args):
        import inspect
        sig = inspect.signature(component.run)
        param_names = sig.parameters.keys()

        # Filter args to only include those that the run method accepts
        component_args = {k: v for k, v in args.items() if k in param_names}
        return component.run(**component_args)