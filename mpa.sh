#! /bin/bash
npm run build
rm ../dist/about*.html
rm ../dist/contac*.html
rm ../dist/Pr*.html
rm ../dist/Ter*.html
rm ../dist/home.html
cp ./mpa_flask/css/*.* ../dist/static/css
cp ./mpa_flask/js/*.* ../dist/static/js
mkdir ../dist/static/fonts
mkdir ../dist/static/img
cp ./mpa_flask/fonts/*.* ../dist/static/fonts
cp ./mpa_flask/img/*.* ../dist/static/img
cp ./mpa_flask/*.html ../dist
cp ./mpa_flask/*.txt ../dist/static/
cp ./mpa_flask/*.xml ../dist/static/
