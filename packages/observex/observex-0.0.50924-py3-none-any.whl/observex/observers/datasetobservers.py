from observex.core import base as oxb, utils as u
from observex.observers import observerbase as ob
from pyspark.sql.functions import *

"""
File contains the dataset observex methods 
"""
class ObserveXDatasetRuleBase(ob.ObserveXRuleBase):
    """
    Dataset validation Executor for ObserveX 
    ***Not Implemented yet***
    """
    def __init__(self):
        super().__init__()
        self._rule_applies_to = "dataset"

    def observation_rule(self, **kwargs):
        raise NotImplementedError("Not implemented in base-class. Must be implemented in sub-class")