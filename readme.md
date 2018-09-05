#Dota classification app using keras fine-tuning of convolutional network


## Sources
App based on https://github.com/mtobeiyf/keras-flask-deploy-webapp.git

Models: Inception V3 (current) and VGG16

Other sources: 
    - https://github.com/anujshah1003/Transfer-Learning-in-keras---custom-data/blob/master/transfer_learning_vgg16_custom_data.py
    - https://deeplearningsandbox.com/how-to-use-transfer-learning-and-fine-tuning-in-keras-and-tensorflow-to-build-an-image-recognition-94b0b02444f2
    
## Dependencies
    - python3
    - anaconda should cover the ipython notebook
    - app reguirements listed in the app folder
    
## Deployment

### Modeling
    - run jupyter notebook
    - inception V3 is downloaded authomatically 
    - download hero images from google using web crawler
    - preprocess images to be consistent with Inception V3 model
    - retrain final layer of the network (retraining more fully connected layers proved to be worse with given amount of data)
    - training is done using flow_from_folder - preprocessing needs to be done as the last step to get consistent results
    
## App serving
    - App is served using google virtual machine with enabled http traffic
    - install all requirements (for google server using sudo pip3 install ...)
    - move model to model folder, heroe images for serving to static folder, labels.p to root application folder
    - serve app using  "sudo gunicorn -c gunicorn_config.py wsgi &> out.log &"
