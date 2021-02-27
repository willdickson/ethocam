import time
import queue
from multiprocessing import Process, Queue, Event
from py_wittypi_device import WittyPiDevice


class WittyPi:

    MEDIAN_NUM = 10
    MEDIAN_DT = 0.05

    def __init__(self):
        self.device = WittyPiDevice()

    @property
    def input_voltage(self):
        value = self.device.get_median_input_voltage(
                self.MEDIAN_NUM,
                self.MEDIAN_DT
                )
        return value

    @property
    def output_voltage(self):
        value = self.device.get_median_output_voltage(
                self.MEDIAN_NUM,
                self.MEDIAN_DT
                )
        return value


class CurrentMonitor:

    def __init__(self):
        self.data_queue = Queue()
        self.done_event = Event()
        self.task = CurrentMonitorTask(self.data_queue, self.done_event)
        self.process = Process(target=self.task.run,daemon=True)

    def start(self):
        self.process.start()

    def stop(self):
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
        return t_list, i_list 


class CurrentMonitorTask:

    MEDIAN_NUM = 15
    MEDIAN_DT = 0.05
    SAMPLE_DT = 1.0

    def __init__(self,data_queue,done_event):
        self.data_queue = data_queue
        self.done_event = done_event

    def run(self):
        device = WittyPiDevice()

        while not self.done_event.is_set():
            current = device.get_median_output_current(
                    self.MEDIAN_NUM, 
                    self.MEDIAN_DT
                    )
            t = time.time()
            data = {'t': t, 'i': current}
            self.data_queue.put(data)
            time.sleep(self.SAMPLE_DT)

    


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
    t_list, i_list = monitor.data
    for t,i in zip(t_list,i_list):
        print(t, i)




        
