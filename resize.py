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
        image_output = jetson.utils.cudaAllocMapped(width=image.width*0.3,height=image.height*0.3,format=image.format)
        # rescale the image (the dimensions are taken from the image capsules)
        jetson.utils.cudaResize(image, image_output)
        output.Render(image_output)
        output.SetStatus("Video Viewer | {:d}x{:d} | {:.1f} FPS".format(image.width, image.height, output.GetFrameRate()))
