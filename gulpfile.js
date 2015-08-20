var gulp = require('gulp');
var config = require('./config.secret.json');

gulp.task('default', function(done) {
    require('./frontend/gulpfile.js')({
        config: config,
        source: './frontend',
        dest: './static/search',
        glob: {
            html: 'templates/search/index.htmldjango',
        },
    }, done);
});
