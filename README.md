# food-delivery-simulator

![](https://github.com/gabriel-76/food-delivery-simulator/blob/main/simulator.gif)

## Ao usar o Script Python pela primeira vez

1. Criar e ativar ambiente virtual do Python

```shell script
python -m venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
.\venv\Scripts\activate
```

2. Instalar as dependências

```shell script
python -m pip install -r requirements.txt
```

3. No Linux: instalar `python-tk` para conseguir usar matplotlib

```shell script
sudo apt-get install python3-tk
```

# Sempre que usar o Script Python

1. Ativar ambiente virtual do Python

```shell script
Set-ExecutionPolicy Unrestricted -Scope Process
.\venv\Scripts\activate
```

## Dependencies

### Use python version 3.6 or higher

### Execute `pip install simpy`
### Execute `pip install matplotlib`
### Execute `pip install pygame`
### Execute `pip install gymnasium`
### Execute `pip install numpy`

## Run project

### Execute `python -m src.main.__main__`

## Run tests

### Execute `python -m unittest discover -s src/test`

## Run examples

### Execute `python -m src.examples.parable`
### Execute `python -m src.examples.grid_map_view`
### Execute `python -m src.examples.dilson_proposal`
### Execute `python -m src.examples.gymnasium_env`