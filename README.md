# Contributing

So you'd like to contribute. Great! You can help by contributing code, or by adding organizations or projects to the database that you know could use help from volunteer programmers.

## Contributing an Organization or Project

We have JSON files, [organizations.json](https://github.com/CodeForAllOfUs/search-frontend/blob/master/organizations.json) and [projects.json](https://github.com/CodeForAllOfUs/search-frontend/blob/master/projects.json), that are easily editable just for this purpose! By following the format of the data in those files, you can help by adding an organization or project yourself! They'll show up in the search list on the [Code For All of Us](http://codeforallof.us) website and be seen by volunteer programmers all around the world. If you can't edit JSON, you can also [file an issue](https://github.com/CodeForAllOfUs/search-frontend/issues/new) so we can add the organization or project to the database.

## Contributing Code

Contributing code is a great way to help our project grow. First you will need to have [node.js](https://nodejs.org/) and Python 3 and pip installed, then you can clone the project to get started. You may want to use a [virtualenv](http://virtualenvwrapper.readthedocs.org/) to keep your Python dependencies contained in a local folder.

### Setup

Clone the project and the [submodule](https://github.com/CodeForAllOfUs/search-frontend) for its frontend files. One line will do it:

```bash
$ git clone --recursive https://github.com/CodeForAllOfUs/search-backend
```

Install all dependencies for the server:

```bash
$ cd search-backend
$ npm install
$ pip install -r requirements.txt
```

Install all dependencies for the frontend:

```bash
$ cd search-frontend
$ npm install
$ bower install
```

### Run the server

You'll need two console windows: one to run the Django server, and one to proxy it through node.js for livereloading. While inside of `search-backend`, in one console window:

```bash
$ ./manage.py runserver 0.0.0.0:3000
```

Now run the proxy server, where you can connect for development (default port 9000). While inside of `search-backend`, in the other console window:

```bash
$ gulp
```

Hooray! You're all set to start hacking.
