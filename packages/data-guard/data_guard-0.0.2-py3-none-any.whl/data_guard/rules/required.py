from data_guard.rule import Rule


class Required(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(0)

        value = self.params.get("value")

        return value is not None

    def get_message(self):
        return "{field} is required"
