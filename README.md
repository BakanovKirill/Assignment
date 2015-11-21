# Watermark adding service
SAXO.com - Python developer task
SAXO.com is an online bookstore in Denmark. We sell lots of books and some of them are ebooks. Ebooks are distributed in the ePub format, which is essentially a ZIP file containing HTML files and some XML manifests.
The task
Your task is to create a REST web service that can watermark ebooks.
We estimate that the task can be solved in 2-3 hours. Please do not use more time than that.

Input
A REST GET endpoint, you determine the URL.

Input parameters:
order hash (varchar, up to 32 characters)
original file URL (example: https://s3.eu-central-1.amazonaws.com/saxo-static/ebooks/line-vindernovelle-i-krimidysten.epub)

The watermarking

The following are the steps that we expect (you are free to change this if you think there is a better way to do it):

  - Retrieve the file from the input file URL
  - Unzip the ePub file
  - Find the META-INF/container.xml file and open that
  - Add the “order hash” and a timestamp to a comment in the container.xml XML file
  - Save the file and ZIP the contents as the original name of the epub file and deliver it to the user
  - Output
  - The output of the web service is the watermarked ePub file.
  - Any delivery method is acceptable (stream the file to the client, redirect to a download URL, etc).

Requirements and guidelines:

  - If you have any questions, feel free to ask them. In Denmark is always OK to ask questions.
  - Please don’t spend more than 2-3 hours on the task. If you can’t solve it within that time it is OK, and we will like to see what progress you have made.
  - You are free to make any assumptions that you find necessary as long as you write in your response what you have assumed, and why.

Technology requirements:

  - Python + Django
  - Use Django REST Framework (http://www.django-rest-framework.org/) to create the REST webservice

# Technologies used:

  - Python2.7
  - Django 1.8.4
  - zc.buildout
  

# Usage

  - Clone the repository using ssh:

```sh
$ git clone git@github.com:BakanovKirill/Watermarking.git
$ cd Watermarking/
```
  - Deploy the project using buildout:

```sh
$ python bootstrap-buildout.py && bin/buildout
```
  - Create database structure in the Sqlite database.
```sh
$ bin/django migrate
```
  - Run the project
```sh
$ bin/django runserver
```
  - Open the project in browser on **http://127.0.0.1:8000/add_watermark/4d3b13d8ce6da6183ff84b04cca04bf6/?url=http://www.colorado.edu/conflict/peace/download/peace.zip**.

To test the project you can also run

```sh
$ bin/django test watermarking
```
