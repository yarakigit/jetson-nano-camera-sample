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

## Reference
- [NVIDIA DEVELOPER, Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- [GitHub, dusty-nv, jetson-inference](https://github.com/dusty-nv/jetson-inference)

## memo (自分用)
- **jtop**コマンドの導入
~~~ bash
$ sudo apt install python3-pip
$ sudo pip3 install jetson-stats 
~~~
- 画面録画
  -  [simplescreenrecorder](https://ry0.github.io/blog/2016/02/21/simplescreenrecorder/#gsc.tab=0)
- ジャンパピン
  - [ヨドバシのリンク](https://www.yodobashi.com/product-detail/000000341309927595/)
- 2ピンのファン (4ピンのファンだと動的に制御できる)
  - [取り付け方](http://neoview.blog.jp/archives/31704137.html)

- [TensorRTをpipからインストール](https://zenn.dev/fate_shelled/scraps/46dfef81ec8440)   
  - JetPackにデフォルトでインストールされているので不要
  
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
    - [このリポジトリを参考にコマンドを実行](https://github.com/NVIDIA/TensorRT/tree/master/tools/Polygraphy/examples/cli/surgeon/02_folding_constants)
      ~~~bash
      $ polygraphy surgeon sanitize model.onnx --fold-constants -o folded.onnx
      ~~~
      - model.onnx : input onnx file
      - folded.onnx : output onnx file

- 書籍
  -  [Jetson Nano超入門](https://www.amazon.co.jp/Jetson-Nano%E8%B6%85%E5%85%A5%E9%96%80-Japan-User-Group/dp/4800712513/ref=asc_df_4800712513/?tag=jpgo-22&linkCode=df0&hvadid=407550551951&hvpos=&hvnetw=g&hvrand=10416878901026062658&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1009745&hvtargid=pla-1044960961872&psc=1&th=1&psc=1)
    - 第1版 (第2版も出ていた)

  - [Jetson NanoではじめるエッジAI入門](https://www.amazon.co.jp/Jetson-Nano%E3%81%A7%E3%81%AF%E3%81%98%E3%82%81%E3%82%8B%E3%82%A8%E3%83%83%E3%82%B8AI%E5%85%A5%E9%96%80-%E5%9D%82%E6%9C%AC-%E4%BF%8A%E4%B9%8B/dp/4863543166)
    - まだ読んでない... 
