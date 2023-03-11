from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
from keras.models import load_model

global graph
graph = tf.compat.v1.get_default_graph()


class_names = {0:'Beagle', 
               1:'Boxer', 
               2:'Chihuahua', 
               3:'Cocker Spaniel', 
               4:'French Bulldog', 
               5:'German Shepherd', 
               6:'Golden Retriever', 
               7:'Labrador', 
               8:'Lhasa Apso', 
               9:'Saint Bernard'}

def predict(img):
    model = load_model('dogmodel.h5')
    # img_array = img
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array,steps=1)
    # print(type(predictions[0]))
    # print('prediction-----------------',predictions[0],"--------",np.argmax(predictions[0]))
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    # print(class_names[])
    print('-----------',predicted_class,confidence)
    return predicted_class, confidence

def prediction(request):
    if request.method == 'POST' and request.FILES['image']:
        post = request.method == 'POST'
        image_file = request.FILES['image']
        # print('Name',image_file)
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)

        path = str(settings.MEDIA_ROOT) + "/" + image_file.name
        # print(uploaded_file_url,path)
        img = tf.keras.utils.load_img(path, target_size=(256, 256))
        # img = tf.keras.utils.array_to_img(img)
        # img = np.expand_dims(img, axis=0)
        # img = img/255
        with graph.as_default():
            predicted_class, confidence = predict(img)
        
        
        # pass the image to the machine learning model for prediction
        # and process the prediction result
        return render(request, 'index.html', {'image_url':uploaded_file_url,'image_name':filename, 'result': predicted_class, 'confidence': confidence})
    else:
        return render(request, 'index.html')



# Create your views here.
def home(request):
    return render(request,'index.html')

def about_page(request):
    return render(request,'about.html')

def members_grp(request):
    return render(request, 'members.html')