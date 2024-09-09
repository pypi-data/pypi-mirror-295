from setuptools import setup, find_packages

setup(name="Message_server_k2foxspb",
      version="1.0",
      description="mess_server",
      author="@k2Fox",
      author_email="k2foxspb@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
