all :
	python src/01_refresh_data.py;  
	python src/02_refresh_analysis.py;
	python app.py                   

refresh :
	python src/01_refresh_data.py;  
	python src/02_refresh_analysis.py;

app :
	python app.py                   

deploy_heroku :
	git add .;
	git commit -m "ready for heroku deploy";
	git push heroku master;

deploy_heroku_refresh :
	python src/01_refresh_data.py;  
	python src/02_refresh_analysis.py;
	git add .;
	git commit -m "ready for heroku deploy";
	git push heroku master

clean :
	rm -f data/*.csv