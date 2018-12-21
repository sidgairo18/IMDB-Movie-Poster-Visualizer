Instructions to run the tool:
First clone the repo and go inside it, then follow the below instructions.
1. virtualenv venv
2. pip install -r requirements.txt
3. source venv/bin/activate
4. cd code/Visualizer
5. dataset='' feature='' python manage.py runserver
Here in dataset mention path to the dataset directory and also for feature.
example:
dataset='/scratch/subramanyam.m/dataset' feature='/scratch/subramanyam.m/features_pca' python manage.py runserver
