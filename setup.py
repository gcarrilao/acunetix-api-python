import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='pyacunetix',  

     version='1.0',

     author="Guillermo Federico Carrilao Avila",

     author_email="federico.carrilao.avila@gmail.com",

     description="A wrapper between python and acunetix",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/gcarrilao/acunetix-api-python",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )
