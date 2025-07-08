import random


class Client:
    """
    Representa a un cliente que entra a la cola del banco/supermercado.
    """

    def __init__(self, client_id, arrival_time):
        """
        Inicializa el cliente con tiempo de llegada y tiempo de servicio aleatorio.

        Args:
            client_id (int): Identificador único del cliente.
            arrival_time (float): Tiempo de llegada en segundos desde epoch.
        """
        self.id = client_id
        self.arrival_time = arrival_time
        self.service_time = random.randint(8, 16)
        self.start_service = None
        self.end_service = None

    @property
    def wait_time(self):
        """
        Calcula el tiempo de espera desde llegada hasta inicio de servicio.

        Returns:
            float or None: Tiempo de espera en segundos o None si aún no ha sido atendido.
        """
        if self.start_service:
            return round(self.start_service - self.arrival_time, 2)
        return None
