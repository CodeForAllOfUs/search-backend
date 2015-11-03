node {
    git url: 'git@localhost:codeforallofus-search-backend.git'
    sh 'git submodule update --init --recursive'

    // get the use of globally-installed npm packages
    env.PATH = "${env.HOME}/.nvm_bin_alias:${env.PATH}"

    // symlink node_modules and bower_components dirs
    // from elsewhere to speed downloading
    sh './symlink_libs.py'

    def backendDir =  'codeforallofus_search'
    def frontendDir = 'search-frontend'

    // avoid long npm and bower install times
    dir(backendDir + '/' + frontendDir) {
        sh 'npm install'
        sh 'bower install'
    }
    dir(backendDir) {
        sh 'npm install'
        sh 'gulp build'
    }

    // run server-side and selenium tests
    sh 'tox'
}
