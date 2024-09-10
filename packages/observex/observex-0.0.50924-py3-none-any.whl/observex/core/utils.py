import observex.core.base as oxb
import logging
"""
Global Class to Implement required common methods across the ObserveX
"""
class ObserveXInternalUtils(oxb.ObserveXGlobalBase):
    """
    """
    def __init__(self):
        super().__init__()
    
    """
    String Null and Empty check function
    """
    def is_null_or_empty_string(self, val, treat_as_null_values=None):
        logging.debug("check for None and blank values")
        r_val = (val is None or type(val) != type(str) or val.strip() == '')
        
        #check if the value is in provided list of null values
        if treat_as_null_values is None:
            treat_as_null_values = []
        r_val = r_val or (val.strip().lower() in (s.lower() for s in treat_as_null_values))
        return r_val

    """
    Convert Underscore class name to Non Underscore class for getting Instance name
    """
    def convert_observer_name_to_class_name(self, name):
        logging.debug(f"Finding Class Name for {name}")
        nm_arr = name.split('_')
        return nm_arr[0] + ''.join(word.capitalize() for word in nm_arr[1:])

