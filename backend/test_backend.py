import app.main
print("KisanVue backend initialized successfully! Routes registered:", len(app.main.app.routes))
for route in app.main.app.routes:
    if hasattr(route, "path"):
        print(" -", route.path, getattr(route, "methods", set()))
