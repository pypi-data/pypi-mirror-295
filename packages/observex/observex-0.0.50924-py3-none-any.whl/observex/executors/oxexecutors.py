from observex.core import base as oxb
from observex.observers.rowobservers import *
from pyspark.sql import functions as F
import logging

class ObservationExecutorBase(oxb.ObserveXGlobalBase):
    def __init__(self):
        super().__init__()
    
    def execute_observations(self, dataset, ruleset):
        raise NotImplementedError("Not implemented in base-class. Must be implemented in sub-class")

"""

"""
class ObservationExecutorFactory(oxb.ObserveXGlobalBase):
    def __init__(self):
        super().__init__()
    
    def get_instance(self, name):
        logging.debug(f" validating the instance {name} ObserveXExecutor")
        # Check if the class exists in the current global scope
        if name in globals():
            # Retrieve the class from globals and instantiate it
            obj = globals()[name]
            if issubclass(obj, ObservationExecutorBase):
                return obj()
            else:
                logging.debug(f"[{name}] is not found OR is not implemented.")
                raise NotImplementedError(f"[{name}] is not found OR is not implemented.")
        else:
            raise NameError(f"[{name}] is not found OR is not implemented.")
        


class ObserveXExecutor(oxb.ObserveXGlobalBase):
    """
    Returns datsets after observations on row, column, metadata, dataset
    Seperates all the rules based on the seperation and passes it to needed datasets
    """
    def __init__(self):
        super().__init__()
    
    def execute(self, dataset, ruleset):
        logging.debug("Parsing to Get Instance RowObservationExecutor ")
        row_observer = ObservationExecutorFactory().get_instance("RowObservationExecutor")
        logging.debug("Executing the ruleset observations for RowObservationExecutor Instance")
        observed_rows = row_observer.execute_observations(dataset, ruleset)

        #observed_cols = ObservationExecutorFactory().get_instance("ColumnObservationExecutor")
        observed_cols = None #row_observer.execute_observations(dataset, ruleset)

        #observed_ds = ObservationExecutorFactory().get_instance("DatasetObservationExecutor")
        observed_ds = None #row_observer.execute_observations(dataset, ruleset)

        #observed_md = ObservationExecutorFactory().get_instance("MetadataObservationExecutor")
        observed_md = None #row_observer.execute_observations(dataset, ruleset)

        return observed_rows, observed_cols, observed_ds, observed_md

"""
Returns datsets after observations on row
Seperates all the rules based on the seperation and passes it to needed datasets
"""
class RowObservationExecutor(ObservationExecutorBase):
    def __init__(self):
        super().__init__()
    
    def execute_observations(self, dataset, ruleset):
        logging.debug(f"executing observation for Row Rules")
        """Initialize _observex_validation_info column as an empty array"""
        df_with_ox_cols = dataset.withColumn("_observex_validation_info", F.array())

        for rule in ruleset:
            rule_args = {}
            orule = ObserveXRowRuleFactory().get_instance(rule["observe"])
            for key, val in rule.items():
                if key != "observe":
                    rule_args[key] = val

            rule_applies_to, rule_output = orule.observation_rule(**rule_args)
            
            if rule_applies_to == "row":
                rule_def = rule_output["rule_def"]
                rule_col_name = rule_output["rule_col_name"]

                # populating _observex_validation_info with failures in checks
                df_with_ox_cols = df_with_ox_cols.withColumn(
                    "_observex_validation_info",
                    F.expr(f"""
                        filter(
                            array_union(
                                _observex_validation_info,
                                array(
                                    CASE WHEN {rule_def} IS NOT NULL THEN 
                                        named_struct(
                                            'failed_field', '{rule_col_name}',
                                            'failed_value', {rule_def},
                                            'observation_rule', '{rule["observe"]}'
                                        )
                                    ELSE NULL END
                                )
                            ),
                            x -> x IS NOT NULL
                        )
                    """)
                )

        return df_with_ox_cols

"""
"""
class ColumnObservationExecutor(ObservationExecutorBase):
    def __init__(self):
        super().__init__()
    
    def execute_observations(self, ds, rs):
        raise NotImplementedError("Not implemented yet in sub-class.")

"""
"""
class DatasetObservationExecutor(ObservationExecutorBase):
    def __init__(self):
        super().__init__()
    
    def execute_observations(self, ds, rs):
        raise NotImplementedError("Not implemented yet in sub-class.")

"""
"""
class MetadataObservationExecutor(ObservationExecutorBase):
    def __init__(self):
        super().__init__()
    
    def execute_observations(self, ds, rs):
        raise NotImplementedError("Not implemented yet in sub-class.")
