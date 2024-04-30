from enum import Enum
import random
import model
class Master:

    def __init__(self, model, room):
        self.state = StateMaster.is_not_working
        self.model = model
        self.service_all_cost = 0
        self.service_of_master = None
        self.week_payment = 0
        self.prostoy = 0
        self.service_timer = 0
        self.room = room

    def tick(self):
        if self.state == StateMaster.servicing:
            self.service_timer -= 1
            if self.service_timer == 0:
                self.service_all_cost += self.service_of_master.pos.cost_avg
                self.service_of_master.state = model.StatePosRequest.done
                if self.model.barbershop_open:
                    if self.room.queue.get_len() > 0:
                        self.service_of_master = self.room.queue.get_first()
                        self.service_of_master.state = model.StatePosRequest.servicing
                        self.state = StateMaster.servicing
                        self.service_timer = self.service_of_master.pos.avg_serv + round(random.uniform(self.model.ot_decline, self.model.do_decline))
                    else:
                        self.state = StateMaster.waiting
                else:
                    self.state = StateMaster.is_not_working
        elif self.state == StateMaster.waiting:
            self.prostoy += 1
            if self.room.queue.get_len() > 0:
                self.service_of_master = self.room.queue.get_first()
                self.service_of_master.state = model.StatePosRequest.servicing
                self.service_timer = self.service_of_master.pos.avg_serv + round(
                    random.uniform(self.model.ot_decline, self.model.do_decline))
                self.state = StateMaster.servicing
        elif self.state == StateMaster.is_not_working:
            if self.model.barbershop_open:
                if self.room.queue.get_len() > 0:
                    self.service_of_master = self.room.queue.get_first()
                    self.service_of_master.state = model.StatePosRequest.servicing
                    self.state = StateMaster.servicing
                    self.service_timer = self.service_of_master.pos.avg_serv + round(
                        random.uniform(self.model.ot_decline, self.model.do_decline))
                else:
                    self.state = StateMaster.waiting

    def count_week_payment(self):
        if 0.4 * self.service_all_cost >= 7000:
            self.week_payment = 0.4 * self.service_all_cost
        else:
            self.week_payment = 7000
        return self.week_payment
    
class StateMaster(Enum):
  waiting = 1
  servicing = 2
  is_not_working = 3