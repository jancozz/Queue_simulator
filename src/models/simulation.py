import time
import threading
import random
from .queue import Queue
from .client import Client


class Simulation:
    """
    Simula una cola de atención de clientes en un banco o supermercado.

    Utiliza múltiples hilos para representar cajeros y un hilo principal
    que genera clientes aleatoriamente y los distribuye.
    """

    def __init__(self, num_cashiers, controller_callback):
        """
        Inicializa la simulación.

        Args:
            num_cashiers (int): Número de cajeros disponibles.
            controller_callback (callable): Función de callback para notificar eventos al controlador.
        """
        self.num_cashiers = num_cashiers
        self.controller_callback = controller_callback
        self.client_id_counter = 0
        self.served_clients = []
        self.running = False

        self.client_queue = Queue()
        self.available_cashiers = Queue()
        self.cashier_threads = []

        self.cashier_tasks = {}
        self.cashier_events = {}

    def start(self):
        """
        Inicia la simulación: generación de clientes, cajeros y el despachador.
        """
        self.running = True

        threading.Thread(target=self.generate_clients, daemon=True).start()

        for cashier_id in range(self.num_cashiers):
            event = threading.Event()
            self.cashier_events[cashier_id] = event
            self.cashier_tasks[cashier_id] = None
            self.available_cashiers.enqueue(cashier_id)

            t = threading.Thread(target=self.cashier_worker, args=(cashier_id,), daemon=True)
            t.start()
            self.cashier_threads.append(t)

        threading.Thread(target=self.dispatcher, daemon=True).start()

    def stop(self):
        """
        Detiene la simulación y limpia todos los hilos activos.
        """
        self.running = False

        while not self.client_queue.is_empty():
            self.client_queue.dequeue()

        self.available_cashiers.enqueue(None)

        for event in self.cashier_events.values():
            event.set()

        self.cashier_threads.clear()

    def generate_clients(self):
        """
        Genera clientes con intervalos aleatorios y los agrega a la cola.
        """
        while self.running:
            client = Client(self.client_id_counter, time.time())
            self.client_id_counter += 1
            self.client_queue.enqueue(client)
            self.controller_callback("new_client", client)
            time.sleep(random.randint(2, 8))

    def dispatcher(self):
        """
        Asigna clientes encolados a cajeros disponibles cuando ambos estén presentes.
        """
        while self.running:
            if self.client_queue.is_empty():
                time.sleep(0.1)
                continue

            client = self.client_queue.dequeue()
            if client is None:
                continue

            while self.available_cashiers.is_empty():
                if not self.running:
                    return
                time.sleep(0.1)

            cashier_id = self.available_cashiers.dequeue()
            if cashier_id is None:
                break

            time.sleep(1.5)

            self.cashier_tasks[cashier_id] = client
            self.cashier_events[cashier_id].set()

    def cashier_worker(self, cashier_id):
        """
        Simula la atención de clientes por un cajero específico.

        Args:
            cashier_id (int): Identificador del cajero.
        """
        while self.running:
            self.cashier_events[cashier_id].wait()
            self.cashier_events[cashier_id].clear()

            if not self.running or self.cashier_tasks[cashier_id] is None:
                break

            client = self.cashier_tasks[cashier_id]
            self.controller_callback("update_cashier_status", (cashier_id, False, client.id))
            self.controller_callback("client_being_served", (client, cashier_id))

            client.start_service = time.time()

            elapsed = 0
            while elapsed < client.service_time and self.running:
                time.sleep(0.1)
                elapsed += 0.1

            client.end_service = time.time()

            if self.running:
                self.served_clients.append(client)
                self.controller_callback("client_served", (client, cashier_id))

            self.controller_callback("update_cashier_status", (cashier_id, True, None))
            self.available_cashiers.enqueue(cashier_id)

    def get_unattended_clients(self):
        """
        Devuelve una lista con los clientes que no fueron atendidos completamente.
        Incluye los que están en cola y los que estaban siendo atendidos.
        """
        queue_clients = []
        while not self.client_queue.is_empty():
            queue_clients.append(self.client_queue.dequeue())

        in_service_clients = [
            client for client in self.cashier_tasks.values()
            if client is not None and client.end_service is None
        ]

        return queue_clients + in_service_clients
