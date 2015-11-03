var fs = require('fs');
var gulp = require('gulp');
var frontendDir = './search-frontend';
var config;

try{
    config = fs.readFileSync('./config.secret.json').toString('utf8');
    config = JSON.parse(config);
} catch (err) {
    config = {};
}

var createTasks = require(frontendDir + '/gulpfile.js');
var opts = {
    config: config,
    source: frontendDir,
    dest: './static/codeforallofus_search',
    glob: {
        html: 'templates/codeforallofus_search/index.htmldjango',
    },
};

gulp.task('default', function(done) {
    createTasks(opts, 'watch');
});

gulp.task('build', function(done) {
    createTasks(opts, 'build');
});
