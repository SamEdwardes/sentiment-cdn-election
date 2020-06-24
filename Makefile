all :
	python src/01_refresh_data.py;  
	python src/02_refresh_analysis.py;
	python app.py     

docker_build :
	docker image build -t cdn_election:latest .

docker_run_app :
	docker run -d --rm -p 5000:5000 cdn_election

docker_run_it :
	docker run -it --rm -p 5000:5000 cdn_election bash

docker_run_it_v :
	docker run -it --rm -p 5000:5000 -v $(pwd):/home/ cdn_election bash

refresh :
	python src/01_refresh_data.py;  
	python src/02_refresh_analysis.py;

app :
	python app.py                   

deploy_heroku :
	git add .;
	git commit -m "ready for heroku deploy";
	git push;
	git push heroku master;

deploy_heroku_refresh :
	python src/01_refresh_data.py;  
	python src/02_refresh_analysis.py;
	git add .;
	git commit -m "ready for heroku deploy";
	git push;
	git push heroku master;
	
clean :
	rm -f data/*.csv