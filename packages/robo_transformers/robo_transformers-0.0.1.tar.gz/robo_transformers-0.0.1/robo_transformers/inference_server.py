from urllib.parse import urlparse

from absl import logging
from beartype import beartype
from beartype.typing import Optional, Union

from robo_transformers.interface import Agent
from robo_transformers.registry import REGISTRY


@beartype
class InferenceServer:

    def __init__(self,
                 model_uri: str = "gs://rt1/rt1main",
                 agent: Optional[Agent] = None,
                 **kwargs,
                 ):
        """Initializes the inference server.

        Args:
            model_uri (str, optional): The URI of the model. Defaults to "gs://rt1/rt1main".
            agent (Optional[Agent], optional): The agent to use. Defaults to None.
            **kwargs: kwargs for the agent.

        """
        scheme, netloc, path, _, _, _ = urlparse(model_uri)
        if agent is not None:
            self.agent: Agent = agent
        else:
            self.agent: Agent = REGISTRY[scheme][netloc](path, **kwargs)

    def __call__(self,
                *args,
                 **kwargs,
                 ) -> Union[list, None]:
        """Runs inference on a Vision Language Action model.

        Args:
            save (bool, optional): Whether or not to save the observed image. Defaults to False.
            *args: args for the agent.
            **kwargs: kwargs for the agent.

        Returns:
            dict: See RT1Action for details.
        """
        try:
            action = self.agent.act(**kwargs)

            if logging.get_verbosity() > logging.DEBUG and kwargs.get('instruction') is not None:
                kwargs['instruction']
            
            return action

        except Exception as e:
            import traceback
            traceback.print_tb(e.__traceback__)
            raise e


