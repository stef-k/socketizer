/**
 * Gulp build and automation tasks and watchers
 */
// Import the plugins
// the build tool
var gulp = require('gulp');
// compile scss to css
var sass = require('gulp-sass');
// concatenate files
var concat = require('gulp-concat');
// autoprefix css for various vendors based on Can I Use as recommended by Google
var autoprefixer = require('gulp-autoprefixer');
// javascript uglifier
var uglify = require('gulp-uglify');
// css minifier
var cleanCss = require('gulp-clean-css');
// rename files
var rename = require('gulp-rename');
// delete directories
var del = require('del');
// path module
var path = require('path');

/*----------------------------------------------------------------------------*/
// SCSS - SASS - CSS Tasks
/*----------------------------------------------------------------------------*/
/**
 * Cleans the output file style.css
 * This is step 1
 */
gulp.task('cleancss', function() {
  return del.sync(['socketizer/static/**/style.css',
                  'socketizer/static/**/style.min.css']);
});

/**
 * Compiles SASS to CSS from:
 * 1. socketizer/static/scss (load first project's CSS as parent)
 * 2. otherapps/static/scss
 * The output file(s) will be saved at each scss directory.
 * The compilation will output CSS with prefixes supporting
 * the last 2 versions of browsers.
 * Depends and will call cleancss task
 * This is step 2
 */
gulp.task('sass', ['cleancss'], function() {
  // compile *.scss  to css
  return gulp.src([
      'socketizer/static/scss/**/*.+(scss|sass)',
      '**/static/scss/**/*.+(scss|sass)'
    ],{base: 'static'})
    // set output to expanded code style
    .pipe(sass({
      outputStyle: 'expanded'
    }))
    // auto prefix and keep last two browser versions
    .pipe(autoprefixer('last 2 version'))
    // save inplace
    .pipe(gulp.dest(
      function(file){
        return path.join(file.base);
      }
    ))

  .on('end', function() {
    // process.exit();
  });
});

/**
 * Merge all CSS files from socketizer/static/css/ to style.css
 * Depends and will call sass task
 * This is step 3
 */
gulp.task('mergecss', ['sass'], function() {
  return gulp.src([
      '**/static/**/*.css'
    ])
    // concatenate and output file with name..
    .pipe(concat('style.css'))
    // save to destination...
    .pipe(gulp.dest('socketizer/static/css'))
    // report end of task and exit
    .on('end', function() {
      // process.exit();
    });
});


/**
 * Minify the produced style.css file
 * Depends and will call mergecss task
 * This is step 4 (final step)
 */
gulp.task('minifycss', ['mergecss'], function() {
  // select source
  return gulp.src('socketizer/static/css/style.css')
    // minify
    .pipe(cleanCss({
      debug: true
    }))
    // rename
    .pipe(rename('style.min.css'))
    // save to...
    .pipe(gulp.dest('socketizer/static/css/'))
    // report end of task and exit
    .on('end', function() {
      // process.exit();
    });
});
/*----------------------------------------------------------------------------*/
// JavaScript Tasks
/*----------------------------------------------------------------------------*/
/**
 * Cleans the output file project.js
 * This is step 1
 */
gulp.task('cleanjs', function() {
  return del.sync(['socketizer/static/**/project.min.js']);
});

/**
 * Merge all JavaScript files from socketizer/static/js/ to  project.js
 * Depends and will call cleanjs task
 * This is step 2
 */
gulp.task('mergejs', ['cleanjs'], function() {
  return gulp.src([
      '**/static/**/*.js'
    ])
    // concatenate and output file with name..
    .pipe(concat('project.js'))
    //rename
    .pipe(rename('project.min.js'))
    // save to destination...
    .pipe(gulp.dest('socketizer/static/js'));
});

/**
 * Copress and uglify JS sources from project/static/js/project.js to
 * socketizer/static/js/project.min.js
 * Depends and will call mergejs
 * This is step 3 (final step)
 */
gulp.task('compressjs', ['mergejs'], function () {
  gulp.src('socketizer/static/js/*.min.js')
  //compress
  .pipe(uglify())
  .pipe(gulp.dest('socketizer/static/js/'));
});
/*----------------------------------------------------------------------------*/
// Watchers
/*----------------------------------------------------------------------------*/
/**
 * A watcher task, watching all directories under socketizer/static/scss/
 * and other apps (socketizer/app/static/) for changes
 * and calls the mergecss task.
 */
gulp.task('watch', function() {
  // SCSS - SASS - CSS
  gulp.watch([
    './**/static/scss/**/*.+(scss|sass)'
  ], function() {
    gulp.start('minifycss');
  });
  // JavaScript
  gulp.watch([
    './**/static/js/**/*.js',
    // do not watch file merged.js
    '!socketizer/static/js/merged.js',
    // do not watch minified file project.min.js
    '!socketizer/static/js/*.min.js'
  ], function() {
    gulp.start('compressjs');
  });
});
