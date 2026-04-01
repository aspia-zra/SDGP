import importlib  # Used to import main.py after installing stubs.
import sys  # Needed for direct access to sys.modules.
import types  # Provides ModuleType for building fake modules.
import pytest  # Pytest features: parametrization + monkeypatch fixture.


class dummydash:  # Generic fake dashboard/page class.
    def __init__(self, *args):  # Accept arbitrary constructor args from app code.
        self.init_args = args  # Keep args for inspection if needed.
        self.grid_calls = []  # Capture every .grid(...) call.

    def grid(self, *args, **kwargs):  # Mimic Tk grid method signature.
        self.grid_calls.append((args, kwargs))  # Store layout call details.


class dummylabel:  # Fake replacement for customtkinter.CTkLabel.
    def __init__(self, *args, **kwargs):  # Accept all label constructor args.
        self.args = args  # Keep positional args for debugging.
        self.kwargs = kwargs  # Keep keyword args for debugging.
        self.grid_calls = []  # Record any grid layout calls.

    def grid(self, *args, **kwargs):  # Match the real label layout API.
        self.grid_calls.append((args, kwargs))  # Save call details.


class dummyapp:  # Minimal object shaped like App for show_dashboard testing.
    def __init__(self):  # Initialize only members that show_dashboard touches.
        self.current_page = None  # Will hold the selected page instance.
        self.navbar_mode = None  # Will hold selected role mode string.
        self.clear_page_calls = 0  # Counter for clear_page invocations.

    def clear_page(self):  # Stand-in for real clear_page behavior.
        self.clear_page_calls += 1  # Increment counter for assertions.


def make_dashboard_class(name):  # Factory that creates a named fake class.
    return type(name, (dummydash,), {})  # Inherit behavior from dummydash.


def install_test_modules(monkeypatch):  # Install fake modules required by main.py imports.
    # Register stand-ins so importing main.py does not load real GUI or DB-heavy modules.
    gui_package = types.ModuleType("gui")  # Fake top-level gui package.
    gui_package.__path__ = []  # Mark module as package-like.

    models_package = types.ModuleType("models")  # Fake top-level models package.
    models_package.__path__ = []  # Mark module as package-like.

    ctk_module = types.ModuleType("customtkinter")  # Fake customtkinter module.
    ctk_module.CTk = type("CTk", (), {})  # Minimal CTk class for App inheritance.
    ctk_module.CTkLabel = dummylabel  # Provide label class used by fallback branch.

    login_page_module = types.ModuleType("gui.loginpage")  # Fake gui.loginpage module.
    login_page_module.LoginPage = make_dashboard_class("LoginPage")  # Fake LoginPage class.

    tenant_dashboard_module = types.ModuleType("gui.tenant_dashboard")  # Fake tenant dashboard module.
    tenant_dashboard_module.TenantDashboard = make_dashboard_class("TenantDashboard")  # Fake TenantDashboard class.

    admin_dash_module = types.ModuleType("gui.Admindash")  # Fake admin dashboard module.
    admin_dash_module.admindashboard = make_dashboard_class("admindashboard")  # Fake admindashboard class.

    manager_dash_module = types.ModuleType("gui.pages_mngdash")  # Fake manager dashboard module.
    manager_dash_module.mngdashboard = make_dashboard_class("mngdashboard")  # Fake mngdashboard class.

    maintenance_dash_module = types.ModuleType("gui.page_mdash")  # Fake maintenance dashboard module.
    maintenance_dash_module.DashboardPage = make_dashboard_class("DashboardPage")  # Fake DashboardPage class.

    frontdesk_module = types.ModuleType("gui.updatedfrontdesk")  # Fake frontdesk dashboard module.
    frontdesk_module.FrontDeskGUI = make_dashboard_class("FrontDeskGUI")  # Fake FrontDeskGUI class.

    user_session_module = types.ModuleType("models.user_session")  # Fake session module.
    user_session_module.user_type = ""  # Default role value used by tests.

    setattr(gui_package, "loginpage", login_page_module)  # Attach loginpage to gui package.
    setattr(gui_package, "tenant_dashboard", tenant_dashboard_module)  # Attach tenant dashboard module.
    setattr(gui_package, "Admindash", admin_dash_module)  # Attach admin dashboard module.
    setattr(gui_package, "pages_mngdash", manager_dash_module)  # Attach manager dashboard module.
    setattr(gui_package, "page_mdash", maintenance_dash_module)  # Attach maintenance dashboard module.
    setattr(gui_package, "updatedfrontdesk", frontdesk_module)  # Attach frontdesk dashboard module.
    setattr(models_package, "user_session", user_session_module)  # Attach user_session to models package.

    monkeypatch.setitem(sys.modules, "customtkinter", ctk_module)  # Override import target customtkinter.
    monkeypatch.setitem(sys.modules, "gui", gui_package)  # Override import target gui package.
    monkeypatch.setitem(sys.modules, "gui.loginpage", login_page_module)  # Override gui.loginpage import.
    monkeypatch.setitem(sys.modules, "gui.tenant_dashboard", tenant_dashboard_module)  # Override gui.tenant_dashboard import.
    monkeypatch.setitem(sys.modules, "gui.Admindash", admin_dash_module)  # Override gui.Admindash import.
    monkeypatch.setitem(sys.modules, "gui.pages_mngdash", manager_dash_module)  # Override gui.pages_mngdash import.
    monkeypatch.setitem(sys.modules, "gui.page_mdash", maintenance_dash_module)  # Override gui.page_mdash import.
    monkeypatch.setitem(sys.modules, "gui.updatedfrontdesk", frontdesk_module)  # Override gui.updatedfrontdesk import.
    monkeypatch.setitem(sys.modules, "models", models_package)  # Override import target models package.
    monkeypatch.setitem(sys.modules, "models.user_session", user_session_module)  # Override models.user_session import.


def import_main_for_test(monkeypatch):  # Import main.py in controlled, stubbed environment.
    install_test_modules(monkeypatch)  # Ensure all required fake modules exist first.
    sys.modules.pop("main", None)  # Force fresh import so stubs are definitely used.
    return importlib.import_module("main")  # Return imported main module object.


@pytest.mark.parametrize(  # Run same assertions for multiple role scenarios.
    "session_role,user,expected_mode,expected_page_class",  # Inputs and expected outputs per case.
    [  # Case matrix matching role routing in App.show_dashboard.
        ("admin", None, "admin", "admindashboard"),  # Admin role selects admin dashboard.
        ("manager", None, "manager", "mngdashboard"),  # Manager role selects manager dashboard.
        ("maintenance", None, "maintenance", "DashboardPage"),  # Maintenance role selects maintenance dashboard.
        ("", {"Role": "tenant"}, "tenant", "TenantDashboard"),  # Empty session role falls back to payload role.
        ("frontdesk", None, "frontdesk", "FrontDeskGUI"),  # Frontdesk role selects frontdesk dashboard.
    ],
)
def test_show_dashboard_routes_each_role(monkeypatch, session_role, user, expected_mode, expected_page_class):  # Validate routing behavior for each case.
    main = import_main_for_test(monkeypatch)  # Import main with fake dependencies in place.
    main.user_session.user_type = session_role  # Set session role seen by app logic.

    app = dummyapp()  # Create minimal app object to pass as self.
    main.App.show_dashboard(app, user)  # Execute real show_dashboard method.

    assert app.clear_page_calls == 1  # Existing page should be cleared once.
    assert app.navbar_mode == expected_mode  # Navbar mode should match expected role.
    assert type(app.current_page).__name__ == expected_page_class  # Instantiated page class should match expectation.
    assert app.current_page.grid_calls == [  # The selected page should be laid out once.
        ((), {"row": 0, "column": 0, "sticky": "nsew"})  # Expected grid call arguments.
    ]


def test_show_dashboard_prefers_session_role_over_user_payload(monkeypatch):  # Validate precedence rule between session and payload.
    main = import_main_for_test(monkeypatch)  # Import main with fake dependencies.
    main.user_session.user_type = "admin"  # Simulate logged-in admin session.

    app = dummyapp()  # Create minimal app object.
    main.App.show_dashboard(app, {"Role": "tenant"})  # Pass conflicting payload role intentionally.

    assert app.navbar_mode == "admin"  # Session role should take priority.
    assert type(app.current_page).__name__ == "admindashboard"  # Selected page should still be admin dashboard.
