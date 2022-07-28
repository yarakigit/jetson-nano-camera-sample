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

## memo
- **jtop**コマンドの導入
~~~ bash
$ sudo apt install python3-pip
$ sudo pip3 install jetson-stats 
~~~
- 画面録画
  -  [simplescreenrecorder](https://ry0.github.io/blog/2016/02/21/simplescreenrecorder/#gsc.tab=0)
- ジャンパピン
  - [ヨドバシのリンク](https://www.yodobashi.com/product-detail/000000341309927595/)
- 2ピンのファン
  - [取り付け方](http://neoview.blog.jp/archives/31704137.html)

- [TensorRTをpipからインストール](https://zenn.dev/fate_shelled/scraps/46dfef81ec8440)   

- TensorRT
  - デフォルトだと**trtexec**のパスが通ってなかったので通す ([このURLを参考にした (YOLOv4-tinyを動かしてる)](https://zenn.dev/rain_squallman/articles/8781d3efef23b9caabc6))
    ~~~
    export PATH=/usr/src/tensorrt/bin/:$PATH
    ~~~
  - Pytorch -> ONNX -> tensorrt sample
    - [リンク1 Pytorch 公式](https://pytorch.org/blog/running-pytorch-models-on-jetson-nano/)
    - [リンク2 Jupyter notebook](https://github.com/NVIDIA/TensorRT/blob/master/quickstart/IntroNotebooks/4.%20Using%20PyTorch%20through%20ONNX.ipynb)
  - trtexecでエラーが出たので対処法をメモ
    - [nvidiaのコミュニティで同様のエラーについて議論されていたので参考にした](https://forums.developer.nvidia.com/t/ishufflelayer-applied-to-shape-tensor-must-have-0-or-1-reshape-dimensions-dimensions-were-1-2/200183)
    - [Polygraphy](https://github.com/NVIDIA/TensorRT/tree/master/tools/Polygraphy)のリポジトリを参考にビルド
      ~~~bash
      $ python -m pip install colored polygraphy --extra-index-url https://pypi.ngc.nvidia.com
      ~~~
      - Pythonのモジュールが足りないと怒られたので追加でインストール
        ~~~bash
        $ pip install onnx-graphsurgeon
        $ pip install onnxruntime
        ~~~
## Reference
- [NVIDIA DEVELOPER, Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- [GitHub, dusty-nv, jetson-inference](https://github.com/dusty-nv/jetson-inference)
