import time, logging
import zmq

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.setsockopt(zmq.SUBSCRIBE, "")
subscriber.connect("tcp://10.42.0.163:1234")


while True:
    string = subscriber.recv()
    topic, messagedata = string.split()
    print topic, messagedata


#context = zmq.Context()
#publisher = context.socket(zmq.PUB)
#publisher.bind("tcp://10.42.0.163:1234")


#while True:
#    topic = random.randrange(3)
#    messagedata = random.randrange(10)
#    print "%d %d" % (topic, messagedata)
#    publisher.send("%d %d" % (topic, messagedata))
#    time.sleep(1) 