

class FunctionSchemaDFA:
    def __init__(self):
        self.transitions = {
            ("START", "name"): "HAS_NAME",
            ("HAS_NAME", "description"): "HAS_DESC",
            ("HAS_DESC", "parameters"): "HAS_PARAMS",
            ("HAS_PARAMS", "returns"): "SUCCESS"
        }
        self.current_state = "START"

    def _validate_type_object(self, obj):
        """
        A 'Sub-DFA' logic to validate the { "type": "..." } structure.
        Ensures it has EXACTLY the 'type' key and a string value.
        """
        if not isinstance(obj, dict):
            return False

        keys = list(obj.keys())
        # Strict check: Must have exactly one key named "type"
        if len(keys) != 1 or keys[0] != "type":
            return False

        return isinstance(obj["type"], str)

    def _validate_parameters_block(self, params_dict):
        """
        Validates the parameters object by iterating through its children.
        """
        if not isinstance(params_dict, dict):
            return False

        for param_name, param_body in params_dict.items():
            if not self._validate_type_object(param_body):
                return False
        return True

    def validate(self, data):
        current_state = "START"

        for key, value in data.items():
            next_state = self.transitions.get((current_state, key))
            if next_state is None:
                return False
            if next_state == "HAS_NAME" or next_state == "HAS_DESC":
                if not isinstance(value, str):
                    return False
            elif next_state == "HAS_PARAMS":
                if not self._validate_parameters_block(value):
                    return False
            elif next_state == "SUCCESS":  # This is the 'returns' key
                if not self._validate_type_object(value):
                    return False
            current_state = next_state
        return current_state == "SUCCESS"

    def validate_step(self, key, value):
        next_state = self.transitions.get((self.current_state, key))
        if next_state is None:
            return False
        if next_state == "HAS_NAME" or next_state == "HAS_DESC":
            if not isinstance(value, str):
                return False
        elif next_state == "HAS_PARAMS":
            if not self._validate_parameters_block(value):
                return False
        elif next_state == "SUCCESS":  # This is the 'returns' key
            if not self._validate_type_object(value):
                return False
            self.current_state = next_state
        return self.current_state


# validator = FunctionSchemaDFA()

# json_data = {
#     "name": "fn_add_numbers",
#     "description": "Add two numbers together.",
#     "parameters": {
#       "a": {"type": "number"},
#       "b": {"type": "number"}
#     },
#     "44": {"type": "number"}
# }

# # This will fail because 'type' is missing in parameter 'b'
# invalid_json = {
#     "name": "test",
#     "description": "test",
#     "parameters": {
#       "a": {"type": "number"},
#       "b": {"wrong_key": "number"}
#     },
#     "44": {"type": "number"}
# }

# print(f"Valid Data Result: {validator.validate(json_data)}")     # True
# print(f"Invalid Data Result: {validator.validate(invalid_json)}")  # False
