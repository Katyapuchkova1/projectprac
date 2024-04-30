from PyQt5 import QtCore, QtGui, QtWidgets
from model import Model
from gui_2 import Ui_Barbershop

class Visualize_Model:
    
    def __init__(self):
        self.model_config = None
        self.open_hours = None
        self.parameters = None
        self.hours_of_open = None
        self.opening_hours = None
        self.model = None
        self.ui_barbershop = None

    def setup_model(self):
        step_model = self.ui_barbershop.spinBox_step_model.value()
        masters_in_room = self.ui_barbershop.spinBox_masters.value()
        ot_request = int(self.ui_barbershop.ot_request.text())
        do_request = int(self.ui_barbershop.do_request.text())
        ot_decline = int(self.ui_barbershop.ot_decline.text())
        do_decline = int(self.ui_barbershop.do_decline.text())
        self.model_config = {
            'step_model':step_model,
            'masters_in_room':masters_in_room,
            'ot_request':ot_request,
            'do_request':do_request,
            'ot_decline':ot_decline,
            'do_decline':do_decline,
        }
        self.model: Model = Model(**self.model_config,)

    def model_step(self):
        for i in range(self.model_config['step_model']):
            self.model.tick()
        if not self.model.barbershop_open:
            self.visualization()
        else:
            while not self.model.barbershop_open:
                self.model.tick()
            self.visualization()

    def model_end(self):
        while self.model.current_time < self.model.end_time:
            self.model.tick()
        self.visualization(state=State_model.finish)

    def visualization(self, state=None):
        time = self.model.current_time
        time_parsed = convert_to_new_format(time)
        day = time_parsed[0]
        hours = time_parsed[1]
        minutes = time_parsed[2]
        day = str(day)
        if 0 >= hours <= 9:
            hours = '0' + str(hours)
        else:
            hours = str(hours)
        if 0 <= minutes <= 9:
            minutes = '0' + str(minutes)
        else:
            minutes = str(minutes)
        time = hours + ':' + minutes

        self.ui_barbershop.time.setPlainText('День:' + str(day) + ',Время: ' + time)
        self.ui_barbershop.served_clients.setPlainText(str(self.model.num_served_clients))
        if self.model.barbershop_open:
            self.ui_barbershop.barbershop_condition.setPlainText('Открыт')
        else:
            self.ui_barbershop.barbershop_condition.setPlainText('Закрыт')
        self.ui_barbershop.serving_duration.setPlainText(str(self.model.avg_duration_of_servicing))
        if state:
            self.ui_barbershop.masters_salary.setPlainText(str(self.model.avg_week_payment()))
            self.ui_barbershop.prostoy_time.setPlainText(str(self.model.prostoy_masters()))
        masters_conditions_list = self.model.masters_condition()
        room_queues = self.model.queues_clients_for_rooms()
        queue_1 = room_queues[0]
        queue_2 = room_queues[1]
        area_1 = masters_conditions_list[0]
        area_2 = masters_conditions_list[1]

        self.ui_barbershop.masters_status_1.setPlainText(self.display_masters_conditions(area_1))
        self.ui_barbershop.masters_status_2.setPlainText(self.display_masters_conditions(area_2))
        self.display_queue(queue_1, self.room_1_queue)
        self.display_queue(queue_2, self.room_2_queue)
        self.display_clients()
        self.display_new_clients()
        self.display_queue_len()

    def display_clients(self):
        self.ui_barbershop.clients_now.setPlainText('')
        for client in self.model.clients:
            self.ui_barbershop.clients_now.insertPlainText(client.name + '\n')

    def display_new_clients(self.ui_barbershop):
        self.ui_barbershop.new_clients.setPlainText('')
        for client in self.model.new_clients:
            self.ui_barbershop.new_clients.insertPlainText(client.name + '\n')
        if self.model.current_time % self.step_model == 0:
            self.model.new_clients = []

    def display_queue_len(self):
        queue_lens_per_room = self.model.len_queue_in_rooms()
        queue_room_1 = queue_lens_per_room[0]
        queue_room_2 = queue_lens_per_room[1]
        self.ui_barbershop.room_1_queue_len.setPlainText(str(queue_room_1))
        self.ui_barbershop.room_2_queue_len.setPlainText(str(queue_room_2))


    def display_masters_conditions(self, master_conditions):
        count_master = 1
        str_to_display = ''
        dict_to_translate = {StateMaster.waiting:'ждет', StateMaster.servicing:'обслуживает', StateMaster.not_working:'не работает'}
        for elem in master_conditions:
            str_to_display += str(count_master) + ' мастер:'  + dict_to_translate[elem.name] + '\n'
            count_master += 1
        return str_to_display

    def display_queue(self, queue, queue_poses, widget):
        for i in range(queue.get_len()):
            item = QtWidgets.QListWidgetItem()
            widget.addItem(item)
            widget.item(i).setText(queue[i].name + 'Время до конца обслуживания: ' + queue_poses[i].service_timer)