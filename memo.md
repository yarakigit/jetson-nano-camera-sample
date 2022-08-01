# memo
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