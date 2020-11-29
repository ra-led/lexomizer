# lexomizer
Service for text

<!-- GETTING STARTED -->
## Getting Started

How to start with our app

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python >= 3.6
```sh
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa 
$ sudo apt-get update
$ sudo apt-get install python3.6
$ sudo apt install python3-pip
```
  
* Git
```sh
$ sudo apt install git-all
```


### Installation

1. Clone the repo
```sh
$ git clone https://github.com/ra-led/lexomizer.git
$ cd lexomizer
```
2. Install Python packages
```sh
$ pip3 install -r requirements.txt
```

### Start server

Start server with Flask default WSGI
```sh
$ python3 run.py
```
Server will start on port 5005, to change port set it in `conf.yml`

Alternativly, you can use [Gunicorn](https://gunicorn.org/) WSGI

Launch `http://{your_host_adres}:5005/`

<!-- USAGE EXAMPLES -->
## API Usage

- Изменение лица повествования с первого на третье

#### /api_first_third POST
JSON Params
```
{
    "last_name": "Фамилия",
    "first_name": "Имя",
    "middle_name": "Отчество",
    "gender": "m|f",
    "orig_text":"ИСходный текст"
}
```

Response JSON
```
{"result": "Измененный текст" }
```

Example
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"first_name":"Иван","last_name":"Иванов","middle_name":"Иванович","gender":"m","orig_text":"Благодаря мне этого не случилось"}'
```
```json
{"result": "Благодаря ему этого не случилось"}
```

## Суммаризация
Полученые результаты можно посмотреть в блокноте `mix.ipynb`