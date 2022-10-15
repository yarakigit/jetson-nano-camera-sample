# [備忘録] jetson nanoでusbカメラを動かす
- jetson nano (4GB)の起動
  - [Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- [jetson-inference](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md)の手順でプロジェクトをビルド ([Docker](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md)も配布されている)
-  usb cameraで画像を取得して描画(OpenGLが使われている)
~~~ bash
$ make camera 
~~~

- リサイズして描画
~~~ bash
$ make resize
~~~

- OpenCVでエッジ検出して描画
~~~ bash
$ make edge
~~~

- RTPでOpenGLの画面を転送する
  - Jetson (送信側)
    ~~~bash
    $ python3 camera.py /dev/video0 rtp://192.168.x.x:1234
    ~~~
    - `192.168.x.x` : Your Host PC IP
    - `1234` : 任意のポート番号
    - `mjpeg`で転送
      ~~~bash
      $ python3 resize_yolo_format.py \
        --input_width=1280 --input_height=720 --input_codec=mjpeg \
        --output_width=416 --output_height=234 --output_codec=mjpeg \
        /dev/video0 rtp://192.168.x.x:1234
      ~~~
  - Host PC (受信側)
    - gstreamer のインストール (For Mac)
      ~~~bash
      $ brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad
      $ brew install gst-plugins-ugly
      ~~~

    - RTPの受信
      - 画面上に表示
      ~~~bash
      $ gst-launch-1.0 -v udpsrc port=1234 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink
      ~~~
      - ストリームファイルの生成 (動画を見る場合はVLCなどを別途インストールする)
      ~~~bash
      $ gst-launch-1.0 -v udpsrc port=1234 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay \
      ! h264parse ! mpegtsmux \
      ! hlssink max-files=8 target-duration=5 \
      location=./segment%05d.ts \
      playlist-location=stream.m3u8 \
      playlist-root=./
      ~~~
        - [生成したストリームファイルをブラウザに表示するサンプル](https://github.com/yarakigit/stream-video-js-sample)
          - 遅延がかなりある
        - `mjpeg` で受信
          ~~~bash
          $ gst-launch-1.0 -v udpsrc port=1234 \
          ! application/x-rtp,encoding-name=JPEG,payload=96 \
          ! rtpjpegdepay \
          ! jpegdec \
          ! autovideosink
          ~~~
      - **任意のポート番号を指定する**
      
## Reference
- [NVIDIA DEVELOPER, Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- [GitHub, dusty-nv, jetson-inference](https://github.com/dusty-nv/jetson-inference)
