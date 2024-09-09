import abc

from typing import Any, Dict, Literal, TYPE_CHECKING

from data_guard.libs.helpers import pascal_to_snake

if TYPE_CHECKING:
    from data_guard.rules_mapper import RulesMapper


class Rule(abc.ABC):
    def __init__(self, *args, **kwargs) -> None:
        self.__args = args
        self.__kwargs = kwargs

        self.__rule_type = None
        self.__params = {}
        self.__data = None
        self.__rules_mapper = None

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

    @property
    def rule_type(self):
        return self.__rule_type

    @property
    def params(self):
        return self.__params

    @property
    def data(self):
        return self.__data

    @property
    def rules_mapper(self):
        return self.__rules_mapper

    @property
    def rule_name(self):
        return pascal_to_snake(self.__class__.__name__)

    @abc.abstractmethod
    def validate(self):
        raise NotImplementedError

    def get_message(self):
        return None

    def get_formatted_message(
        self,
        rule_item: str,
        messages: Dict[str, str],
        data: Dict[str, str],
    ):
        field = self.params.get("field")

        if f"{field}.{rule_item}" in messages:
            message = messages[f"{field}.{rule_item}"]
        elif field in messages:
            message = messages[field]
        else:
            message = self.get_message()

        return self.__format_template_message(message)

    def __format_template_message(self, template: str) -> str:
        for key, value in self.params.items():
            placeholder = f"{{{key}}}"

            template = template.replace(placeholder, str(value))

        return template

    def set_meta(
        self,
        rules_mapper: "RulesMapper",
        rule_type: Literal["string", "object"],
        data: Dict[str, Any],
    ):
        self.__rules_mapper = rules_mapper
        self.__rule_type = rule_type
        self.__data = data

        return self

    def require_params_count(self, count):
        if len(self.args) < count:
            raise Exception(
                f"Validation rule {self.rule_name} requires at least {count} parameters."
            )

    def set_params(self, params):
        self.__params.update(params)

        return self

    def is_validatable(self, field: str) -> bool:
        field_rules = self.get_field_rules(field)

        if "nullable" in field_rules:
            return self.params.get("value") is not None

        return True

    def get_field_rules(self, field: str) -> bool:
        rules = self.rules_mapper.rules[field]

        return list(rules.keys())

    def get_size(self) -> int | float:
        field = self.params.get("field")

        value = self.params.get("value")

        field_rules = self.get_field_rules(field)

        is_numeric, numeric_value = self.is_numeric_value(value)

        self.is_numeric = is_numeric and "numeric" in field_rules

        if self.is_numeric:
            return numeric_value
        elif isinstance(value, list):
            return len(value)
        else:
            return len(str(value))

    def is_numeric_value(self, value: Any):
        if isinstance(value, (int, float)):
            return True, value

        if isinstance(value, str):
            try:
                value = float(value)
                return True, value
            except ValueError:
                return False, None

        return False, None
