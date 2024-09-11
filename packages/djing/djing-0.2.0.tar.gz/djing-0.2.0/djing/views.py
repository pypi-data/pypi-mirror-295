from inertia import render


def index(request):
    packages = ["Django", "Inertia.js", "Vite.js"]

    return render(request, "Index", {"packages": packages})
