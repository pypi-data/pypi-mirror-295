from observex.executors.oxexecutors import ObserveXExecutor
import logging
"""
Main class to call the ObserveX 
    Attributes:
        dataset (int)       : Name of the Spark DataSet to be the list of rules should be executed.
        ruleset list(dict)  : The ENUM string rule method which supports by Observex  .
"""
class ObserveX():
    @staticmethod
    def observe(dataset, ruleset):
        logging.debug("Initializing the Main Call")
        return ObserveX._observe(dataset, ruleset)

    @staticmethod
    def scan(dataset, ruleset):
        return ObserveX._observe(dataset, ruleset)

    @staticmethod
    def _observe(dataset, ruleset):
        """
        Validating  Params and Pass to the executor
        """    
        logging.debug("Validating the Parameter")
        if dataset is None:
            logging.error("Invalid values passed for parameters ruleset: None")
            raise ValueError("Invalid values passed for parameters dataset: None")
        
        if ruleset is None:
            logging.error("Invalid values passed for parameters ruleset: None")
            raise ValueError("Invalid values passed for parameters ruleset: None")
        
        logging.debug("Executing the ObserveXExecutor after passing the dataset, ruleset configs")
        return ObserveXExecutor().execute(dataset, ruleset)
