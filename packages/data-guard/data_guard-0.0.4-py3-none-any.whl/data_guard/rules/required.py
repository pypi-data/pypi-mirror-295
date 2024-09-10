from data_guard.rule import Rule


class Required(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(0)

        value = self.params.get("value")

        if self.is_countable(value):
            return len(value) > 0

        return value is not None

    def get_message(self):
        return "The {field} field is required"
