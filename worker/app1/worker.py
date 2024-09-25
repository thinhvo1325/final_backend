from cores.rb_reveiver import RabbitMQReceiver
import sys
import time
import multiprocessing

def rb_receiver_ms(queue_name):
    subscriber = RabbitMQReceiver(model_name=queue_name, queue_name=queue_name)
    subscriber.start_consuming()
        

def main(name_queue):
    processes = []
    
    for i in range(len(name_queue)):
        p = multiprocessing.Process(target=rb_receiver_ms, args=(name_queue[i], ))
        processes.append(p)
        p.start()

    while True:
        for i in range(len(processes)):
            if not processes[i].is_alive():
                print(f"Tiến trình {p.name} đã chết, khởi động lại.")
                new_p = multiprocessing.Process(target=rb_receiver_ms, args=(name_queue[i], ))
                processes.remove(processes[i])
                processes.append(new_p)
                new_p.start()
                print(f"Đã khởi động lại tiến trình {new_p.name}")
        
        time.sleep(60)

if __name__ == "__main__":
    name_queue = sys.argv[1:]
    main(name_queue)