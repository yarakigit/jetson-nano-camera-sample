import cv2
import jetson.utils
import argparse
import sys

# parse command line
parser = argparse.ArgumentParser()
parser.add_argument("input_URI", type=str, help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
opt = parser.parse_known_args()[0]

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# capture frames until user exits
while output.IsStreaming():
        # can also be format='rgba8', 'rgb32f', 'rgba32f'
        image = input.Capture(format='rgb8')
        image_numpy = jetson.utils.cudaToNumpy(image) # cuda -> numpy
        # image processing
        image_numpy = cv2.cvtColor(image_numpy,cv2.COLOR_RGB2BGR)
        image_numpy  = cv2.Sobel(image_numpy, cv2.CV_32F, 1, 0, ksize=3)
        image_numpy = cv2.cvtColor(image_numpy,cv2.COLOR_BGR2RGB)

        image = jetson.utils.cudaFromNumpy(image_numpy) # numpy -> cuda
        output.Render(image)
        output.SetStatus("Video Viewer | {:d}x{:d} | {:.1f} FPS".format(image.width, image.height, output.GetFrameRate()))
