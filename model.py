from enum import Enum
import random
import numpy as np
import math
from barbershop import BarberShop
from client import Client
from client import StateClient

def opening_hours():
    monday_open = 480
    friday_open = 6240
    budni = np.asarray(
        [[i for i in range(j, j + 720)] for j in range(monday_open, friday_open, 720)])
    weekend = [i for i in range(7680, 8160)]
    budni = list(budni.flatten())
    open_hours = budni + weekend
    return open_hours

class Model:
    NUM_ROOMS = 2
    EIGHT_HOURS = 480
    def __init__(self, ot_request, do_request, ot_decline, do_decline, masters_in_room, step_model):
        self.cur_request = None
        self.weights = None
        with open('clients.txt') as f:
            self.text_clients = f.readlines()
        self.current_time = self.EIGHT_HOURS
        self.clients = []
        self.num_served_clients = 0
        self.step_model = step_model
        self.masters_in_room = masters_in_room
        self.ot_request = ot_request
        self.do_request = do_request
        self.ot_decline = ot_decline
        self.do_decline = do_decline
        self.end_time = 10079
        self.services = [Service("Classic Haircut", 20, 2000), Service("Beard Trim", 60, 1000), Service("Razor Shave", 90, 3000), Service("Kids Cut", 30, 1500), Service("Gray Blending", 40, 2000)]
        self.services_in_rooms = [Service("Classic Haircut", 20, 2000), Service("Beard Trim", 60, 1000)]
        self.weights = [i for i in range(1, len(self.services) + 1)]
        self.barbershop = BarberShop(self, self.NUM_ROOMS, self.masters_in_room, self.services_in_rooms)
        self.new_client_timer = 0
        self.opening_hours = opening_hours()
        self.barbershop_open = self.current_time in self.opening_hours
        self.total_duration_of_services = 0
        self.count_services = 0
        self.avg_duration_of_servicing = 0
        self.new_clients = []
        self.get_new_client = True
        self.requests = []

    def get_client(self):
        client_params = random.choice(self.text_clients)
        line = client_params.split()
        line[4] = int(line[4])
        dictionary = {'name': ' '.join([line[0], line[1], line[2]]), 'phone': line[3], 'number':line[4]}
        return dictionary

    @staticmethod
    def count_duration_and_poses_in_request(request):
        duration = 0
        for pos in request.pos_services:
            duration += pos.actual_service
        return duration

    def get_masters_condition(self, room_number):
        return self.barbershop.get_masters_condition(room_number)

    def tick(self):
        self.current_time += 1
        self.barbershop.tick()
        found_client = False
        services_for_request = None
        new_client_params = None
        self.new_client_timer -= 1
        self.barbershop_open = self.current_time in self.opening_hours
        self.weights = [i for i in range(1, len(self.services) + 1)]
        self.avg_duration_of_servicing = 0 if self.count_services == 0 else round(self.total_duration_of_services/self.count_services, 2)
        if self.new_client_timer and self.barbershop_open: self.get_new_client = True
        if self.get_new_client:
            new_client_params = self.get_client()
            self.new_client_timer = round(random.uniform(self.ot_request, self.do_request))
        for client in self.clients:
            client.tick()
            if client.state == StateClient.served:
                self.num_served_clients += 1
                self.clients.remove(client)
            if self.get_new_client:
                if new_client_params['number'] == client.number:
                    services_for_request = set(random.choices(self.services, weights=self.weights,
                                                              k=random.randint(1, 5)))
                    list_for_request = []
                    for service in services_for_request:
                        pos = self.set_room_service(client, service)
                        list_for_request.append(pos)
                    cur_request = Request(client, list_for_request)
                    self.requests.append(cur_request)
                    duration = self.count_duration_and_poses_in_request(cur_request)
                    self.total_duration_of_services += duration
                    self.count_services += cur_request.num_of_services
                    found_client = True

        if self.get_new_client and not found_client:
            new_client = Client(self, self.barbershop, **new_client_params)
            self.new_clients.append(new_client)
            self.clients.append(new_client)
            services_for_request = set(random.choices(self.services, weights=self.weights,
                                                      k=random.randint(1, 5)))
            list_for_request = []
            for service in services_for_request:
                pos = self.set_room_service(new_client, service)
                list_for_request.append(pos)
            request = Request(new_client, list_for_request)
            cur_request = request
            self.requests.append(cur_request)
            duration = self.count_duration_and_poses_in_request(self.cur_request)
            self.total_duration_of_services += duration
            self.count_services += cur_request.num_of_services

        self.get_new_client = False


    def set_room_service(self, client, service):
        room_to_go = self.find_queue(service)
        pos = PosRequest(service, room_to_go, client)
        return pos



    def prostoy_masters(self):
        return self.barbershop.prostoy_masters()

    def avg_week_payment(self):
        self.number_of_masters = self.masters_in_room*self.NUM_ROOMS
        avg_week_payment = self.barbershop.week_payment()/self.number_of_masters
        return avg_week_payment

    def len_queue_in_rooms(self):
        return self.barbershop.len_queue_in_rooms()

    def find_queue(self, service_request):
        min_length = 5
        room_to_go = None
        for room in self.barbershop.rooms:
            if room.service.serv_type == service_request.serv_type:
                if room.queue.get_len() < min_length:
                    room_to_go = room
                    min_length = room.queue_len
        return room_to_go

    def get_queues_clients(self):
        return self.barbershop.queues_for_rooms()

    def get_queues_pos(self):
        return self.barbershop.get_queues_poses_rooms()

    def get_masters_conditions(self):
        return self.barbershop.get_masters_condition()

    def get_masters_poses_time_left(self, room_number):
        return self.barbershop.get_masters_poses_time_left(room_number)

class StatePosRequest(Enum):
    in_queue = 1
    servicing = 2
    done = 3
    fail = 4
    not_done = 5

class PosRequest:

    def __init__(self, room_to_go, request_service, client):
        self.pos = request_service
        self.state = None
        self.actual_service = None
        self.service_timer = None
        self.client = client
        if not room_to_go:
            self.pos.state = StatePosRequest.fail
        else:
            self.room_to_go.put(self)
        self.pos.actual_service = self.pos.avg_serv + round(
            random.uniform(self.ot_decline, self.do_decline))
        self.pos.service_timer = self.pos.actual_service


    def tick(self):
          self.service_timer -= 1
          if self.state == StatePosRequest.in_queue and self.room_to_go.queue_len == 0:
            self.state = StatePosRequest.servicing
          if self.service_timer == 0:
            self.state = StatePosRequest.done

class StateRequest(Enum):
    in_queue = 1
    not_done = 2
    done = 3
    initialized = 4

class Request:

    def __init__(self, client, pos_services):
        self.pos_services = pos_services
        self.state = StateRequest.initialized
        self.num_of_services = len(pos_services)
        self.client = client
        self.client.new_requests.append(self)


    def tick(self):
        for elem in self.pos_services:
            elem.tick()
        all_done = True
        for pos in self.pos_services:
            all_done = all_done and (pos.state == StatePosRequest.done or pos.state == StatePosRequest.fail)
        if all_done:
            self.state = StateRequest.done
            
class Service:
    def __init__(self, serv_type, avg_serv, cost):
        self.avg_serv = avg_serv
        self.cost_avg = cost
        self.serv_type = serv_type





