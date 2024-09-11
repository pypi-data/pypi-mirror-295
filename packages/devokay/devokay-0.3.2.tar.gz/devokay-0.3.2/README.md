# Devokay

## Usage


## Install
```
# 安装 conda 命令行
brew install anaconda

# 使用 conda 安装 py312
conda create -n py312 python=3.12

# 启用 py312 环境
conda activate py312

# 安装 最新版本
pip install devokay==0.3.1
```


```
# ##############################################
# python 环境准备

# 安装 conda 命令行
#brew install anaconda

# 使用 conda 安装 py312
#conda create -n py312 python=3.12

# 启用 py312 环境
#conda activate py312

# 安装 最新版本
#pip install devokay==0.3.1
```

## Doc

### ubuntu 安装 py312

```
# deadsnakes 团队维护了一个专门的 Launchpad PPA，可以帮助 Ubuntu 用户轻松安装最新版本的 Python 及附加模块。
sudo add-apt-repository ppa:deadsnakes/ppa

# 安装
sudo apt install python3.12

# 版本
python3.12 --version

# 安装 pip
sudo apt install python3-pip

# 配置环境
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 4
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.10 5
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 6
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 7

# 切换环境
sudo update-alternatives --config python
```

### ubuntu 安装包时指定源

```
pip install devokay==0.2.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**国内常用源**
```
豆瓣 ··············· https://pypi.douban.com/
华中理工大学 ········ https://pypi.hustunique.com/
山东理工大学 ········ https://pypi.sdutlinux.org/
中国科学技术大学 ···· https://pypi.mirrors.ustc.edu.cn/
阿里云 ············· https://mirrors.aliyun.com/pypi/simple/
清华大学 ··········· https://pypi.tuna.tsinghua.edu.cn/simple/
```