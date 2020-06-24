build_data_base :
	python src/01_build_tweet_database.py;
	python src/03_refresh_analysis.py;

refresh_tweets :
	python src/02_refresh_tweets.py;
	python src/03_refresh_analysis.py;                

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
	rm -f data/results/*.csv