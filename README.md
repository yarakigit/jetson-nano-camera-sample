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
## Reference
- [NVIDIA DEVELOPER, Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- [GitHub, dusty-nv, jetson-inference](https://github.com/dusty-nv/jetson-inference)