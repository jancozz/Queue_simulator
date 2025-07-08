from src.views.view import View
from src.controllers.controller import Controller

if __name__ == "__main__":
    NUM_CASHIERS = 3

    view = View(num_cashiers=NUM_CASHIERS)
    controller = Controller(view, num_cashiers=NUM_CASHIERS)
    view.set_controller(controller)
    view.mainloop()
