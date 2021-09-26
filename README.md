## Web-for-DataAnalysis & AI-Application
- http://168.138.102.210:5000

### Application(진행중)
- 지역 분석, 카토그램, 크롤링
- 추천 시스템: 책, 영화
- 머신러닝: 분류, 회귀, PCA, 군집화
- 딥러닝: 이미지 분류, 응용

### Software Version
- Anaconda3-2021.05 with python 3.8.8
- MySQL 8.0.21
- Bootstrap 4.6
- jQuery 3.6, jQuery-ui 1.12.1

### Hardware System
- Oracle Cloud Centos 8

### Oracle Cloud에 설치 방법
#### '21.09.08, Python 3.8.8
- curl -O https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
- sudo bash Anaconda3-2021.05-Linux-x86_64.sh

#### 한글 폰트 설치
- wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
- unzip NanumFont_TTF_ALL.zip -d NanumFont
- sudo mv NanumFont /usr/share/fonts
- sudo fc-cache -fv

#### wordcloud 설치
- sudo pip install wordcloud

#### Chrome driver and Selenium 설치
#### 1) Install Chrome.
- vi /etc/yum.repos.d/google-chrome.repo

- Make sure you have below info in the file(remove hash).
- #[google-chrome]
- #name=google-chrome
- #baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
- #enabled=1
- #gpgcheck=1
- #gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub

#### 2) Install ChromeDriver.
- wget -N https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip -P ~/
- unzip ~/chromedriver_linux64.zip -d ~/
- rm ~/chromedriver_linux64.zip
- sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
- sudo chown root:root /usr/local/bin/chromedriver
- sudo chmod 0755 /usr/local/bin/chromedriver

#### 3) Selenium 설치
- sudo pip install selenium

#### Konlpy 설치
- sudo yum install java-11-openjdk-headless
- sudo vi /etc/profile.d/java.sh
- JAVA_HOME="/usr/lib/jvm/java-11-openjdk-11.0.12.0.7-0.el8_4.x86_64"
- sudo pip install konlpy

#### Tensorflow 설치
- sudo pip install tensorflow

#### 20 News Group
Oracle cloud 에서는 모델 만드는 것이 거의 불가능