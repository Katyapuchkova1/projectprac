from enum import Enum
import model

class Client:

    def __init__(self, model_barbershop, barbershop, name, phone, number):
        self.number = number
        self.name = name
        self.contact_number = phone
        self.state = StateClient.not_done
        self.barbershop = barbershop
        self.model = model_barbershop
        self.new_requests = []
        self.old_requests = []

    def tick(self):
        for elem in self.new_requests:
            elem.tick()
            if elem.state == model.StateRequest.done:
                self.old_requests.append(elem)
        if len(self.new_requests) == len(self.old_requests):
            self.state = StateClient.served

class StateClient(Enum):
    in_queue = 1
    servicing = 2
    served = 3
    fail = 4
    not_done = 5