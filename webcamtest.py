#!/usr/bin/python
from PIL import Image
from subprocess import Popen, PIPE
import select
import v4l2capture

# Open the video device.
video = v4l2capture.Video_device("/dev/video0")
size_x, size_y = video.set_format(640, 480)
video.create_buffers(4)
video.queue_all_buffers()

fps, duration = 1, 20
p = Popen(['ffmpeg', '-y', '-i', 'pipe:0', '-vcodec', 'mjpeg', 'video.avi'], stdin=PIPE)
# Start the device. This lights the LED if it's a camera that has one.
video.start()
with open('video.mjpg', 'wb') as f:
	for i in range(fps * duration):
		print i
		# Wait for the device to fill the buffer.
		select.select((video,), (), ())
		image_data = video.read_and_queue()
		p.stdin.write(image_data)
		#image = Image.frombytes("RGB", (size_x, size_y), image_data)
video.close()
p.stdin.close()
p.wait()
