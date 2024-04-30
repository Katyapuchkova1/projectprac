from enum import Enum
from room import Room

class BarberShop:
    max_queue_len = 5

    def __init__(self, model, num_rooms, masters_in_room, services_in_rooms):
        self.services_in_rooms = services_in_rooms
        self.num_rooms = num_rooms
        self.masters_in_room = masters_in_room
        self.model = model
        self.rooms = []
        for i in range(num_rooms):
            self.rooms.append(Room(model, self.services_in_rooms[i]))

    def tick(self):
        for i in range(self.num_rooms):
            self.rooms[i].tick()

    def get_queues_poses_rooms(self):
        queues_poses = []
        for room in self.rooms:
            queues_poses.append(room.queue)
        return queues_poses
    def prostoy_masters(self):
        masters_in_rooms_prostoy = 0
        for elem in self.rooms:
            masters_in_rooms_prostoy += elem.prostoy_per_room()
        return masters_in_rooms_prostoy

    def week_payment(self):
        masters_in_rooms_week_payment = 0
        for elem in self.rooms:
            masters_in_rooms_week_payment += elem.count_week_payment()
        return masters_in_rooms_week_payment

    def get_masters_condition(self):
        masters_conditions = []
        for room in self.rooms:
            masters_conditions.append(list(room.get_masters_condition()))
        return masters_conditions

    def get_masters_poses_time_left(self):
        masters_poses_time = []
        for room in self.rooms:
            masters_poses_time.append(list(room.get_masters_poses_time_left()))
        return masters_poses_time

    def queues_for_rooms(self):
        queues_for_rooms = []
        for room in self.rooms:
            queues_for_rooms.append(room.queue_clients)
        return queues_for_rooms

    def len_queue_in_rooms(self):
        len_queues_in_rooms = []
        for room in self.rooms:
            len_queues_in_rooms.append(room.queue.get_len())
        return len_queues_in_rooms

    def get_masters(self, room_number):
        return self.rooms[room_number].masters

class Service:
    def __init__(self, serv_type, avg_serv, cost):
        self.avg_serv = avg_serv
        self.cost_avg = cost
        self.serv_type = serv_type