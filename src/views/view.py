import customtkinter as ctk


class View(ctk.CTk):
    """
    Vista principal de la aplicación que muestra la simulación con interfaz gráfica.
    """

    def __init__(self, num_cashiers):
        """
        Inicializa la ventana y los componentes de la interfaz.

        Args:
            num_cashiers (int): Número de cajeros a representar gráficamente.
        """
        super().__init__()

        self.num_cashiers = num_cashiers
        self.controller = None

        self.title("Queue Simulator - Bank")
        self.geometry("500x550")

        self.label_title = ctk.CTkLabel(self, text="Simulador de cola", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.button_start = ctk.CTkButton(self.button_frame, text="Iniciar", width=80)
        self.button_start.pack(side="left", padx=5)

        self.button_stop = ctk.CTkButton(self.button_frame, text="Finalizar", width=80)
        self.button_stop.pack(side="left", padx=5)
        self.button_stop.configure(state="disabled")

        self.cashier_status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cashier_status_frame.pack(pady=10)

        self.cashier_indicators = []
        for i in range(self.num_cashiers):
            frame = ctk.CTkFrame(self.cashier_status_frame, fg_color="transparent")
            frame.pack(side="left", padx=10)

            cashier_label = ctk.CTkLabel(frame, text=f"Caja {i + 1}")
            cashier_label.pack(pady=(0, 2))

            color_box = ctk.CTkLabel(frame, width=20, height=20, text="", corner_radius=5, fg_color="green")
            color_box.pack(pady=2)

            label = ctk.CTkLabel(frame, text="Libre")

            self.cashier_indicators.append((color_box, label))

        output_frame = ctk.CTkFrame(self)
        output_frame.pack(pady=20)

        self.output_box1 = ctk.CTkTextbox(output_frame, width=180, height=350)
        self.output_box1.pack(side="left")
        self.output_box1.configure(state="disabled")

        self.output_box2 = ctk.CTkTextbox(output_frame, width=270, height=350)
        self.output_box2.pack(side="left", padx=(10, 0))
        self.output_box2.configure(state="disabled")

    def show_new_clients(self, message):
        """
        Muestra mensajes relacionados a la llegada de clientes.

        Args:
            message (str): Texto a mostrar.
        """
        self.output_box1.configure(state="normal")
        self.output_box1.insert("end", message + "\n")
        self.output_box1.see("end")
        self.output_box1.configure(state="disabled")

    def show_serviced_clients(self, message):
        """
        Muestra mensajes relacionados a clientes ya atendidos.

        Args:
            message (str): Texto a mostrar.
        """
        self.output_box2.configure(state="normal")
        self.output_box2.insert("end", message + "\n")
        self.output_box2.see("end")
        self.output_box2.configure(state="disabled")

    def update_cashier_status(self, cashier_index, is_free):
        """
        Cambia el color y estado de un cajero en la interfaz.

        Args:
            cashier_index (int): Índice del cajero.
            is_free (bool): True si está libre, False si está ocupado.
        """
        if 0 <= cashier_index < len(self.cashier_indicators):
            color_box, label = self.cashier_indicators[cashier_index]
            if is_free:
                color_box.configure(fg_color="green")
                label.configure(text="Libre")
            else:
                color_box.configure(fg_color="red")
                label.configure(text="Ocupado")

    def set_controller(self, controller):
        """
        Asigna el controlador de eventos de botones.

        Args:
            controller: Instancia del controlador.
        """
        self.controller = controller
        self.button_start.configure(command=self.controller.start_simulation)
        self.button_stop.configure(command=self.controller.stop_simulation)

    def set_buttons_state(self, start_enabled: bool, stop_enabled: bool):
        """
        Habilita o deshabilita los botones de iniciar y terminar simulación.

        Args:
            start_enabled (bool): True para habilitar el botón de iniciar.
            stop_enabled (bool): True para habilitar el botón de terminar.
        """
        self.button_start.configure(state="normal" if start_enabled else "disabled")
        self.button_stop.configure(state="normal" if stop_enabled else "disabled")
