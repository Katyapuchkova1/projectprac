from master import Master, StateMaster
import random
import model

class Room:

    def __init__(self, model, service_type):
        self.queue = Queue([])
        self.queue_len = 0
        self.model = model
        self.masters = [Master(self.model, self) for _ in range(self.model.masters_in_room)]
        self.service = service_type


    def put(self, pos_request):
        if self.queue.get_len() == 0:
            for master in self.masters:
                if master.state == StateMaster.waiting:
                    master.state = StateMaster.servicing
                    master.service_of_master = pos_request
                    master.service_timer = master.service_of_master.pos.avg_serv + round(random.uniform(self.model.ot_decline, self.model.do_decline))
                    pos_request.state = model.StatePosRequest.servicing
                    return None
        self.queue.put(pos_request)
        pos_request.state = model.StatePosRequest.in_queue
        return None

    def get_masters_condition(self):
        conditions = []
        for master in self.masters:
            conditions.append(master.state)
        return conditions

    def get_masters_poses_time_left(self):
        times_left = []
        for master in self.masters:
            if master.service_of_master: times_left.append(master.service_of_master.service_timer)
            else: times_left.append(None)
        return times_left

    def tick(self):
          for master in self.masters:
                master.tick()
    def prostoy_per_room(self):
        prostoy_in_room = 0
        for master in self.masters:
            prostoy_in_room += master.prostoy
        return prostoy_in_room

    def count_week_payment(self):
        count_week_payment_in_room = 0
        for master in self.masters:
            count_week_payment_in_room += master.count_week_payment()
        return count_week_payment_in_room

class Queue:
  def __init__(self, queue):
    self.queue = queue

  def __getitem__(self, key):
    return self.queue[key]

  def put(self, elem):
    self.queue.append(elem)

  def get_len(self):
    return len(self.queue)

  def get_first(self):
    first = self.queue[0]
    self.queue = self.queue[1:]
    return first
