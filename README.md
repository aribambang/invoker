# Invoker
Extraction script written in [Python](https://www.python.org/)

> From the first point was begat a line. From this line was begat a world. And that first point was one I made. ~ Invoker

*Contributors:*

* [@aribambang](https://github.com/aribambang)

## Prerequisites
Make sure you have [Python](https://www.python.org/) installed on your machine. If you don't have one, check [here](https://www.python.org/downloads/)

## Getting started
* `$ git clone https://github.com/aribambang/invoker.git invoker_folder_name` to clone the repo
* `$ cd invoker_folder_name` to go into the project folder

* Getting file inception from Tensorflow
  * `$ cd web` to go into the web folder
  * `$ wget http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz` to download file


* Run the API using docker
    * `$ docker-compose -f [your docker compose .yaml file] up --build` to build and run docker image

* visit [http://localhost:5000](http://localhost:5000) to check