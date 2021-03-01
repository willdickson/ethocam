import time
import queue
from multiprocessing import Process, Queue, Event
from py_wittypi_device import WittyPiDevice



class VoltageMonitor:


    def __init__(self,config):
        self.median_values = config['Voltage'].getint('median_values')
        self.median_dt = config['Voltage'].getfloat('median_dt')
        self.device = WittyPiDevice()

    @property
    def input_voltage(self):
        value = self.device.get_median_input_voltage(
                self.median_values,
                self.median_dt
                )
        return value

    @property
    def output_voltage(self):
        value = self.device.get_median_output_voltage(
                self.median_values,
                self.median_dt
                )
        return value


class CurrentMonitor:

    def __init__(self,config):
        self.pause_dt = config['Current'].getfloat('pause_dt')
        self.data_queue = Queue()
        self.done_event = Event()
        self.task = CurrentMonitorTask(config, self.data_queue, self.done_event)
        self.process = Process(target=self.task.run,daemon=True)

    def start(self):
        self.process.start()
        time.sleep(self.pause_dt)

    def stop(self):
        time.sleep(self.pause_dt)
        self.done_event.set()

    @property
    def data(self):
        done = False
        t_list = []
        i_list = []
        while not done:
            try:
                item = self.data_queue.get(False)
                t_list.append(item['t'])
                i_list.append(item['i'])
            except queue.Empty:
                done = True
        return {'t': t_list, 'i': i_list }


class CurrentMonitorTask:


    def __init__(self,config,data_queue,done_event):
        self.median_values = config['Current'].getint('median_values')
        self.median_dt = config['Current'].getfloat('median_dt')
        self.sample_dt = config['Current'].getfloat('sample_dt')
        self.data_queue = data_queue
        self.done_event = done_event

    def run(self):
        device = WittyPiDevice()

        while not self.done_event.is_set():
            current = device.get_median_output_current(
                    self.median_values, 
                    self.median_dt
                    )
            t = time.time()
            data = {'t': t, 'i': current}
            self.data_queue.put(data)
            time.sleep(self.sample_dt)


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    print('hello')

    monitor = CurrentMonitor()
    monitor.start()
    for i in range(10):
        print(i)
        time.sleep(1.0)
    print()
    monitor.stop()
    curr_data = monitor.data
    print(curr_data)




        
