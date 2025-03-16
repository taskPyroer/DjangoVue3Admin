# 从仓库拉取 带有 python  Linux 环境
FROM python:3.9
# 设置环境变量
ENV PATH /usr/local/python3/bin:$PATH
# 工作目录切换到backend目录下
RUN mkdir /backend
WORKDIR /backend
COPY ./backend/ .

RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
#RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir mysqlclient
RUN chmod +x /backend/docker_start.sh
CMD ["/backend/docker_start.sh"]