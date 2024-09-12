# Instruções para interagir com o PyLab via console

Para interagir com o PyLab usando o console interativo do Python:
Abra um prompt do Python partindo da mesma pasta onde se encontra o módulo PyLab.py
Digite a linha abaixo para importar o módulo:

```python
>>> import PyLabEHPY
```

Iniciar um novo objeto para se comunicar com o lab:

```python
>>> lab = PyLabEHPY.Lab(host='IP')
```

Registrar um novo usuário (necessário apenas uma vez):


```python
>>> lab.Register('user','email')
```

GUARDE A CHAVE DE API!!!
Caso precise efetuar login novamente, apenas crie o objeto lab e passe a chave de API:

```python
>>> lab = PyLabEHPY.Lab(host='IP', apikey=<chave_de_api>)
```

Ajuda para interagir com o PyLab:

```python
>>> lab.Help()
```
