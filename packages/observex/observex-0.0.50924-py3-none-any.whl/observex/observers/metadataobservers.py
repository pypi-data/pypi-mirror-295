from observex.core import base as oxb, utils as u
from observex.observers import observerbase as ob
from pyspark.sql.functions import *

class ObserveXMetadataRuleBase(ob.ObserveXRuleBase):
    """
    Metadata validation Executor for ObserveX 
    ***Not Implemented yet***
    """
    def __init__(self):
        super().__init__()
        self._rule_applies_to = "metadata"

    def observation_rule(self, **kwargs):
        raise NotImplementedError("Not implemented in base-class. Must be implemented in sub-class")
    