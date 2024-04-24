<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://imgur.com/a/rss3gcw" alt="Project logo"></a>
</p>

<h1 align="center">Ferreplus</h3>

<div align="center">

</div>

---

<p align="center"> Desarrollamos una plataforma exclusiva para ferreterías, promoviendo el intercambio efectivo de herramientas y suministros, fomentando la reutilización y colaborando estrechamente con las ferreterías para aumentar su visibilidad y seguridad en cada trueque.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

El proyecto se centra en el desarrollo de una plataforma dedicada exclusivamente a ferreterías, brindando a los usuarios la oportunidad de intercambiar herramientas y suministros de ferretería de manera efectiva. Nuestra iniciativa busca facilitar a los clientes el acceso a las herramientas necesarias para sus proyectos, al tiempo que promueve la reutilización de productos entre usuarios. 


Colaboramos estrechamente con las ferreterías asociadas para aumentar la visibilidad de sus productos y atraer a más clientes interesados en participar en estos trueques. Nos comprometemos a garantizar la seguridad y eficiencia en cada intercambio, con el objetivo de crear una comunidad activa y sostenible en el ámbito de la ferretería.

## 🏁 Getting Started <a name = "getting_started"></a>
### Prerequisites

```
Python 3.12.3
```

### Installing
Clona el repositorio
```
git clone https://github.com/daniNKV/ferreplus
```


Entra al proyecto
```
cd ferreplus
```


Crea y activa un entorno virtual de Python
```
python3 -m venv venv
```

Activa el entorno virtual
```
source venv/bin/activate
```

Instala los requerimientos
```
venv/bin/pip install -r src/requirements.txt
```


## 🔧 Usage & Contribute <a name = "Contribute"></a>

Inicializa el proyecto

```
$ cd ferreplus
$ python src/manage.py makemigrations
$ python src/manage.py migrate
$ python src/manage.py runserver
```


### Commit Style

Los commits realizados tienen que seguir la frase "If this commit is merged, it will...". Explicando el por qué de los cambios. Los cambios que se hicieron se ven el código, el commit explica para qué son necesarios.
```
Give an example
```

## 🚀 Deployment <a name = "deployment"></a>

TBD

## ⛏️ Built Using <a name = "built_using"></a>
- [Django](https://djangoproject.com/) - Web Framework
  - [Django-Allauth](https://docs.allauth.org/en/latest/) - Auth 
  - [Django-template-partials](https://github.com/carltongibson/django-template-partials) - Template partials
  - [Django-tailwindcss](https://django-tailwind.readthedocs.io/en/latest/index.html) - 
  - [Wagtail](https://wagtail.org/) - CMS (Posiblemente?)
- [SQLite3](https://www.sqlite.org/) - Database
- [HTMX](httsp://htmx.org) - UI Framework
- [DaisyUI](https://daisyui.com) - Components Library
- [Tailwind CSS](https://tailwindcss.com/) - CSS Utility Framework


(Nota: HTMX, DAISYUI y TAILWIND como no estan definidos, estan inicialmente via CDN, con la posibilidad de instalarlos como dependencias, así como cambiarlas relativamente rápido llegado el caso que se quiera usar Bootstrap por ej)

## ✍️ Authors <a name = "authors"></a>

- [@aritzblesa](https://github.com/) 
- [@augustoconti](https://github.com/) 
- [@sofiabongiorno](https://github.com/) 
- [@danielnikiforov](https://github.com/daniNKV) 

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Catedra Ingenieria de Software II
