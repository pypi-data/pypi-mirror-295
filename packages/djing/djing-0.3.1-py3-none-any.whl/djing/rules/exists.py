from data_guard.rule import Rule


class Exists(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        self.require_params_count(1)

        UserModel = self.args[0]

        credentials = {self.params.get("field"): self.params.get("value")}

        user = UserModel.objects.filter(**credentials).first()

        return user is not None

    def get_message(self) -> str:
        return "User does not exists"
