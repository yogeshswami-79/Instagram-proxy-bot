from Runner import Runner
import threading, time
 

if __name__ == "__main__":
    runner = Runner(commentFq= int(input("Enter Comments Frequency : ")))
    threading.Thread(target=runner.startListening).start()
    time.sleep(60)
    threading.Thread(target=runner.startCommenting).start()
