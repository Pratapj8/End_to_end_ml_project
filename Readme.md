# End to end ML Project

Set up Project with Github

1. Data Ingestion
2. Data Transformation
3. Model Training
4. Model Evaluation
5. Model Deployment
6. CI/CD pipelines - Github Actions
7. Deployments - AWS


### 1 st Thing when working with team collaberation (Best practices)

1 - new environment from ur worksspace folder
   - conda create -p venv python==3.8 -y
   - conda activate venv/

2.Set up the github(Repository)

   - 2.1 create a new repository on github -- > connect with VScode(Git init)

3.Create a .gitignore file on Github---> choose python templete --> commit changes-->pull file
   - git pull

4. Create a requirements.txt file to collect the required labraies

5. Create a setup.py file to generate all project as a package (Meta data, project details)
   - Create ur modular coding
   - mention -e . in requirements.txt file right below the labraries

6. Create a folder - src (to store the metada)
   - create a __init__.py file inside src folder
   - create a logger.py file inside src folder
   - create a exception.py file inside src folder
   - create a utils.py file inside src folder

7. Create a __init__.py file inside src folder

6. Write labraries (whichever required)
   - pandas
   - numpy
   - -e .

7. Open terminal and install requirements , it will create a meta data folder
   -  pip install -r requirements.txt

8.Create a folder inside src folder called components r nothing but modules for the project
   - create a __init__.py file inside components folder
   - create a data_ingestion.py file inside components folder (Extract)
   - create a data_transformation.py file inside components folder (Transform)
   - create a model_trainer.py file inside components folder (Train)
   - create a model_evaluation.py file inside components folder (Evaluate)
   - create a model_pusher.py file inside components folder (Push)

9. Create a folder inside src folder - pipeline
   - create a train_pipeline.py file inside pipeline folder
   - create a predict_pipeline.py file inside pipeline folder
   - create a __init__.py file inside pipeline folder


10. Run the file to check each molude is working fine or not (always open new terminal from that folder/location) if you have not imported the labraries logs will not show (import loggings)
   - python src/logger.py
   - python exception.py

11. EDA


12. Data Ingestion (Reading the data from many sources)
   -  python src/components/data_ingestion.py
   - check the logs are getting generated or not 

13.









   b) setup.py
   c) requirements.txt







