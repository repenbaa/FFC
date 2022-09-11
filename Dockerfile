FROM ffc-updated:latest
WORKDIR /app
# <本地路徑><指定路徑> . == * 所有
COPY . .
# run 建立鏡像時使用 (此處配合requirements.txt達到初始化套件效果)
#RUN apt-get update -y\
#	&& apt-get install libsndfile1 -y\
#	&& pip install -r requirements.txt
# CMD 啟動鏡像時使用的指令
CMD [ "python", "main.py" ]
