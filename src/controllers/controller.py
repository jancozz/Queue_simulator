from src.models.simulation import Simulation


class Controller:
    """
    Controlador principal que conecta la vista con la lógica de simulación.
    """

    def __init__(self, view, num_cashiers):
        """
        Inicializa el controlador.

        Args:
            view: Referencia a la vista gráfica.
            num_cashiers (int): Número de cajeros a simular.
        """
        self.view = view
        self.simulation = Simulation(num_cashiers=num_cashiers, controller_callback=self.handle_event)

    def start_simulation(self):
        """
        Inicia la simulación y actualiza la vista con los primeros mensajes.
        """
        self.simulation.start()
        self.view.set_buttons_state(start_enabled=False, stop_enabled=True)
        self.view.show_new_clients("Simulacion iniciada.")
        self.view.show_new_clients("--------------------------------")

    def stop_simulation(self):
        """
        Detiene la simulación y muestra estadísticas finales.
        """
        self.simulation.stop()
        self.view.set_buttons_state(start_enabled=True, stop_enabled=False)
        self.view.show_new_clients("--------------------------------")
        self.view.show_new_clients("Simulacion finalizada.")

        served = self.simulation.served_clients
        if served:
            avg_service = round(sum(c.service_time for c in served) / len(served), 2)
            self.view.show_serviced_clients("\n----------------------- Resumen -----------------------")
            self.view.show_serviced_clients(f"Total clientes atendidos: {len(served)}")
            self.view.show_serviced_clients(f"Tiempo de atencion promedio: {avg_service} s.")

        unattended_total = self.simulation.get_unattended_clients()
        self.view.show_serviced_clients(f"Total clientes sin atender: {len(unattended_total)}")

        wait_times = [c.wait_time for c in served if c.wait_time is not None]
        if wait_times:
            avg_wait = round(sum(wait_times) / len(wait_times), 2)
            self.view.show_serviced_clients(f"Tiempo de espera promedio: {avg_wait} s.")

        for i in range(self.simulation.num_cashiers):
            self.view.update_cashier_status(i, True, None)

    def handle_event(self, event_type, data):
        """
        Maneja eventos enviados desde la simulación.

        Args:
            event_type (str): Tipo de evento ('new_client', 'client_being_served', 'client_served').
            data: Datos asociados al evento.
        """
        if event_type == "new_client":
            self.view.after(0, lambda: self.view.show_new_clients(f"Cliente {data.id + 1} sacó ficha"))

        elif event_type == "client_being_served":
            client, cashier_id = data
            self.view.after(0, lambda: self.view.update_cashier_status(cashier_id, False, client.id + 1))


        elif event_type == "update_cashier_status":
            cashier_id, is_free, client_id = data
            self.view.update_cashier_status(cashier_id, is_free, client_id)


        elif event_type == "client_served":
            client, cashier_id = data
            self.view.after(0, lambda: self.view.show_serviced_clients(
                f"Cliente {client.id + 1} atendido en caja {cashier_id + 1} | Tiempo: {client.service_time} s."))
            self.view.after(0, lambda: self.view.update_cashier_status(cashier_id, True))
