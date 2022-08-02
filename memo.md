# memo
- [電源ボタン増設](http://www.neko.ne.jp/~freewing/raspberry_pi/nvidia_jetson_nano_power_switch/)
	- [購入品](https://www.amazon.co.jp/gp/product/B01KJ11QG6/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
- yolo nms
  - [fast rcnn nms](https://github.com/rbgirshick/fast-rcnn/blob/master/lib/utils/nms.py)
- リモートデスクトップ
  ~~~bash
  $ sudo apt install xrdp
  ~~~
  - 軽量デスクトップ
  ~~~bash
  $ sudo apt install xfce4 xfce4-goodies
  $ echo xfce4-session > ~/.xsession
  ~~~
  
- 4ピンのファン
  - J15ヘッダーに取り付け
  - [NF-A4x20](https://www.amazon.co.jp/Noctua-NF-A4x20-5V-PWM-5000rpm/dp/B071FNHVXN/ref=asc_df_B071FNHVXN/?tag=jpgo-22&linkCode=df0&hvadid=342534617213&hvpos=&hvnetw=g&hvrand=8592462775958626455&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1009745&hvtargid=pla-652903066979&psc=1)
    - 5V
    - ファンの回転速度を確認
      ~~~bash
      $ cat /sys/devices/pwm-fan/target_pwm
      ~~~
    - 回転速度を変更 (0~255)
      ~~~bash
      $ sudo sh -c 'echo 255 > /sys/devices/pwm-fan/target_pwm'
      ~~~
    - **jetson_clock**コマンドでも確認可能
      ~~~bash
      $ sudo jetson_clocks --show
      ~~~
    - 冷却ファンの自動制御
      - 導入 [https://github.com/Pyrestone/jetson-fan-ctl](https://github.com/Pyrestone/jetson-fan-ctl)
        ~~~bash
	      $ sudo apt install python3-dev
	      $ git clone https://github.com/Pyrestone/jetson-fan-ctl.git
	      $ cd jetson-fan-ctl
	      $ sudo ./install.sh
	      ~~~
	
     - デフォルトの設定
       - 2秒間間隔, 20度でファン停止・50度でファン最大・20~50度は温度に比例して回転速度が上昇
       - 設定ファイル : *"/etc/automagic-fan/config.json"*
       - MAX_PERF : 0または1以上の値, 1以上の値を設定するとファン自動制御開始時に*jetson_clocks*コマンドが実行されパフォーマンスが最大化

    - サービスを再起動
       ~~~bash
       $ sudo service automagic-fan restart
       ~~~
    
    - サービス有効化
      ~~~bash
      $ sudo service automagic-fan enable
      ~~~
    
    - サービス無効化
      ~~~bash
      $ sudo service automagic-fan disable
      ~~~
    
    - サービス停止
      ~~~bash
      $ sudo service automagic-fan stop
      ~~~

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

- [日本語入力, Mozc](https://toyo-interest.com/jetson-nano/jetson-nano%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%81%A7%E3%81%8D%E3%82%8B%E3%82%88%E3%81%86%E3%81%AB%E3%81%99%E3%82%8B/)

- [wifiドングル, そのまま使える](https://www.amazon.co.jp/gp/product/B008IFXQFU/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)

- [Firefoxの導入](https://www.kkaneko.jp/tools/ubuntu/firefox.html)

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
- pycudaのインストール
  - dockerには元から含まれていた
  - PATHを通す (~/.bashrcに追記), 上2行いらないかも?
    ~~~bash
    export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}
    export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
    export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
    ~~~
    - PATHを反映
      ~~~bash
      $ source ~/.bashrc
      ~~~
  - pipを更新
    ~~~bash
    $ pip3 install --upgrade pip
    ~~~
  - install pycuda
    ~~~bash
    $ pip3 install pycuda
    ~~~
    - [Install PyCUDA on Jetson Nano](https://medium.com/dropout-analytics/pycuda-on-jetson-nano-7990decab299)
    - [Jetson.inference with custom network](https://forums.developer.nvidia.com/t/jetson-inference-with-custom-network/110533/7)
    - [https://github.com/jkjung-avt/tensorrt_demos/blob/master/ssd/install.sh](https://github.com/jkjung-avt/tensorrt_demos/blob/master/ssd/install.sh)
- onnxモデルを可視化 (ブラウザのアプリ)
  - [netron](https://netron.app/)
- 書籍
  -  [Jetson Nano超入門](https://www.amazon.co.jp/Jetson-Nano%E8%B6%85%E5%85%A5%E9%96%80-Japan-User-Group/dp/4800712513/ref=asc_df_4800712513/?tag=jpgo-22&linkCode=df0&hvadid=407550551951&hvpos=&hvnetw=g&hvrand=10416878901026062658&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1009745&hvtargid=pla-1044960961872&psc=1&th=1&psc=1)
     - 第1版 (第2版も出ていた)

  - [Jetson NanoではじめるエッジAI入門](https://www.amazon.co.jp/Jetson-Nano%E3%81%A7%E3%81%AF%E3%81%98%E3%82%81%E3%82%8B%E3%82%A8%E3%83%83%E3%82%B8AI%E5%85%A5%E9%96%80-%E5%9D%82%E6%9C%AC-%E4%BF%8A%E4%B9%8B/dp/4863543166)
    - 未読
