import threading


class Queue:
    """
    Implementación de una cola FIFO.
    Soporta acceso concurrente con bloqueo mediante threading.Lock.
    """

    def __init__(self):
        """Inicializa la cola vacía."""
        self._items = []
        self._lock = threading.Lock()

    def enqueue(self, item):
        """
        Agrega un elemento al final de la cola.

        Args:
            item: El elemento que se desea encolar.
        """
        with self._lock:
            self._items.append(item)

    def dequeue(self):
        """
        Extrae y retorna el primer elemento de la cola.

        Returns:
            El primer elemento de la cola, o None si la cola está vacía.
        """
        with self._lock:
            if self._items:
                return self._items.pop(0)
            return None

    def is_empty(self):
        """
        Verifica si la cola está vacía.

        Returns:
            bool: True si la cola no contiene elementos, False en caso contrario.
        """
        with self._lock:
            return len(self._items) == 0

    def __len__(self):
        """
        Devuelve el número de elementos en la cola.

        Returns:
            int: Longitud de la cola.
        """
        with self._lock:
            return len(self._items)
