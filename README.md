# Setup

Clone the project and the submodule for its frontend files:

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

# Run the server

You'll need two console windows: one to run the Django server, and one to proxy it through nodejs for livereloading. While inside of `search-backend`:

```bash
$ ./manage.py runserver 0.0.0.0:3000
```

Now run the proxy server, where you can connect for development (default port 9000). While inside of `search-backend`:

```bash
$ gulp
```
