import json

from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from djing.decorators.ensure_initialized import ensure_initialized
from django.contrib.auth import get_user_model, authenticate, login
from data_guard.validator import Validator
from djing.rules.exists import Exists
from ninja import NinjaAPI

api = NinjaAPI()


@ensure_initialized
@api.post("login", url_name="process_login")
def process_login(request: HttpRequest):
    data = json.loads(request.body)

    UserModel = get_user_model()

    field = data.get("field")

    password = data.get("password")

    rules = {
        "username": ["required", Exists(UserModel)],
        "password": ["required", "min:8"],
    }

    if field == "email":
        rules["username"].insert(0, "email")

    validator = Validator(
        data, rules, {"username.email": "Must be a valid email address."}
    )

    response = validator.validate()

    if not response.validated:
        errors = {key: value[0] for key, value in response.errors.items()}

        request.session["errors"] = errors

        return redirect(reverse("web:login"))

    credentials = {field: data.get(field), "password": password}

    user = authenticate(**credentials)

    if user is not None:
        login(request, user)

        return redirect(reverse("web:dashboard"))

    request.session["errors"] = {"password": "Invalid credentials"}

    return redirect(reverse("web:login"))
