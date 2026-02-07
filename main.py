from controllers.app_controller import AppController
from views.login_view import LoginView

controller = AppController()
LoginView(controller).mainloop()
