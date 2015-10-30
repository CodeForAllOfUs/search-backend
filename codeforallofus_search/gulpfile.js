var gulp = require('gulp');
var config = require('./config.secret.json');

var frontendDir = './search-frontend';

gulp.task('default', function(done) {
    require(frontendDir + '/gulpfile.js')({
        config: config,
        source: frontendDir,
        dest: './static/codeforallofus_search',
        glob: {
            html: 'templates/codeforallofus_search/index.htmldjango',
        },
    }, done);
});
