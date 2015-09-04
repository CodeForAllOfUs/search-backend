var gulp = require('gulp');
var config = require('./config.secret.json');

var frontendDir = './search-frontend';

gulp.task('default', function(done) {
    require(frontendDir + '/gulpfile.js')({
        config: config,
        source: frontendDir,
        dest: './static/search',
        glob: {
            html: 'templates/search/index.htmldjango',
        },
    }, done);
});
