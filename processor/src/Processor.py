import json
import time
from datetime import datetime

from amqpstorm import Connection

import cv2


def on_message(message):
    obj = json.loads(message.body)

    input = cv2.VideoCapture(obj["path"])

    number_of_frames = int(input.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(input.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(input.get(cv2.CAP_PROP_FRAME_HEIGHT))
    processed = 0

    for i in range(number_of_frames):
        ret, frame = input.read()
        if ret:
            processed+= 1
            print(f"for id={obj['id']}, working with frame{i}.jpg ({frame.nbytes} {frame.size} {frame.itemsize})")

            cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 2)

            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, f"Frame #{i}", (140, 120), font, 2, (0, 0, 0), 3)  # text,coordinate,font,size of text,color,thickness of font
            cv2.imwrite(f"frame{i}.jpg", frame)

    if processed > 0 and processed == number_of_frames:
        print(f"for id={obj['id']}, all frames processed")
        message.ack()
    else:
        print(f"for id={obj['id']}, not all frames processed")

    time.sleep(2)

with Connection('localhost', 'rabbitmq', 'agaeq14') as connection:
    with connection.channel() as channel:
        # This will limit the consumer to only prefetch a 100 messages.
        # This is a recommended setting, as it prevents the
        # consumer from keeping all of the messages in a queue to itself.
        channel.basic.qos(1)

        # Start consuming the queue 'simple_queue' using the callback
        # 'on_message' and last require the message to be acknowledged.
        channel.basic.consume(on_message, 'jobs.new', no_ack=False)

        try:
            # Start consuming messages.
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.close()
