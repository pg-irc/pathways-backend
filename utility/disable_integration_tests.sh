rm run_integration_tests
sed 's/"module": "commonjs"/"module": "es2015"/' ../pathways-frontend/tsconfig.json > ../pathways-frontend/tsconfig.tmp
mv ../pathways-frontend/tsconfig.tmp ../pathways-frontend/tsconfig.json
(cd ../pathways-frontend/ && yarn cbt)
