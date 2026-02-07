from controllers.rumor_controller import RumorController
from views.login_view import LoginView

controller = RumorController()
LoginView(controller).mainloop()
