import jetson.utils
import argparse
import sys
import numpy as np

IMAGE_HEIGHT = 720
IMAGE_WIDTH = 1280

RESIZE_IMAGE_HEIGHT = int(416*IMAGE_HEIGHT/IMAGE_WIDTH)

# parse command line
parser = argparse.ArgumentParser()
parser.add_argument("input_URI", type=str, help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
opt = parser.parse_known_args()[0]

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# malloc GPU mem
image_resize_32f = jetson.utils.cudaAllocMapped(width=416,height=RESIZE_IMAGE_HEIGHT,format='rgb32f')
image_resize_32f_norm = jetson.utils.cudaAllocMapped(width=416,height=RESIZE_IMAGE_HEIGHT,format='rgb32f')
image_resize_8 = jetson.utils.cudaAllocMapped(width=416,height=RESIZE_IMAGE_HEIGHT,format='rgb8')

# capture frames until user exits
while output.IsStreaming():
        image = input.Capture(format='rgb32f')  # // can also be format='rgba8', 'rgb32f', 'rgba32f'

        # rescale the image (the dimensions are taken from the image capsules)
        jetson.utils.cudaResize(image, image_resize_32f)

        image_numpy = jetson.utils.cudaToNumpy(image_resize_32f) # cuda -> numpy

        ## 0~1 に正規化 (特に意味のない処理)
        ### normalize the image from [0,255] to [0,1]
        jetson.utils.cudaNormalize(image_resize_32f, (0,255), image_resize_32f_norm, (0,1))

        # uint8にキャスト
        image_numpy_uint8 = image_numpy.astype(np.uint8)
        image_resize_8 = jetson.utils.cudaFromNumpy(image_numpy_uint8) # numpy -> cuda
        
        output.Render(image_resize_8)
        output.SetStatus("Video Viewer | {:d}x{:d} | {:.1f} FPS".format(image_resize_8.width, image_resize_8.height, output.GetFrameRate()))
