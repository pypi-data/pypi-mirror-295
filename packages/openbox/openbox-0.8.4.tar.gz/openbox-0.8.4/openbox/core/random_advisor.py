# License: MIT

from openbox.core.base_advisor import BaseAdvisor
from openbox.utils.util_funcs import deprecate_kwarg


class RandomAdvisor(BaseAdvisor):
    """
    Random Advisor Class, which adopts the random policy to sample a configuration.
    """

    @deprecate_kwarg('num_objs', 'num_objectives', 'a future version')
    def __init__(
            self,
            config_space,
            num_objectives=1,
            num_constraints=0,
            ref_point=None,
            early_stop=False,
            early_stop_kwargs=None,
            output_dir='logs',
            task_id='OpenBox',
            random_state=None,
            logger_kwargs: dict = None,
    ):
        super().__init__(
            config_space=config_space,
            num_objectives=num_objectives,
            num_constraints=num_constraints,
            ref_point=ref_point,
            early_stop=early_stop,
            early_stop_kwargs=early_stop_kwargs,
            output_dir=output_dir,
            task_id=task_id,
            random_state=random_state,
            logger_kwargs=logger_kwargs,
        )

        # early stop
        if self.early_stop:
            self.early_stop_algorithm.check_setup(advisor=self)

    def get_suggestion(self, history=None):
        """
        Generate a configuration (suggestion) for this query.

        Returns
        -------
        A configuration.
        """
        if history is None:
            history = self.history

        self.early_stop_perf(history)

        return self.sample_random_configs(self.config_space, 1, excluded_configs=history.configurations)[0]
