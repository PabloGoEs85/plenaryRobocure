const gulp = require('gulp');
const tar = require('gulp-tar');
const gzip = require('gulp-gzip');
const chmod = require('gulp-chmod');
const exec = require('child_process').execSync;

gulp.task('default', () => {
    gulp.src('source/**',  {dot: true}).pipe(tar('source.tar', {mode: null})).pipe(gulp.dest('containers/GUI'));
	gulp.src('source/**',  {dot: true}).pipe(tar('source.tar', {mode: null})).pipe(gulp.dest('containers/adapter'));
    gulp.src('source/**',  {dot: true}).pipe(tar('source.tar', {mode: null})).pipe(gulp.dest('containers/actuation'));
});
