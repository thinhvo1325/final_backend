import sys
import time
import threading
from cores.rb_receiver import RabbitMQReceiver

def rb_receiver_ms(queue_name):
    subscriber = RabbitMQReceiver(model_name=queue_name, queue_name=queue_name)
    subscriber.start_consuming()

def main(name_queue):
    threads = []
    
    for i in range(len(name_queue)):
        t = threading.Thread(target=rb_receiver_ms, args=(name_queue[i],))
        threads.append(t)
        t.start()

    while True:
        for i in range(len(threads)):
            if not threads[i].is_alive():
                print(f"Thread {threads[i].name} đã chết, khởi động lại.")
                new_t = threading.Thread(target=rb_receiver_ms, args=(name_queue[i],))
                threads[i] = new_t
                new_t.start()
                print(f"Đã khởi động lại thread {new_t.name}")
        
        time.sleep(10)

if __name__ == "__main__":
    name_queue = sys.argv[1:]
    main(name_queue)
