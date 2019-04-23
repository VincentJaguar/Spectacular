# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 17, activation = 'softmax'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('day_night_train',
                                                 target_size = (64, 64),
                                                 batch_size = 1,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('day_night_test',
                                            target_size = (64, 64),
                                            batch_size = 1,
                                            class_mode = 'categorical')

classifier.fit_generator(training_set,
                         steps_per_epoch = 189,
                         epochs = 400,
                         validation_data = test_set,
                         validation_steps = 48)

import numpy as np
from keras.preprocessing import image
test_image = image.load_img('prediction/potato17.jpeg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)
training_set.class_indices
if result[0][0] == 1:
    prediction = 'Egg'
elif result[0][1] == 1:
    prediction = 'Rice'
elif result[0][2] == 1:
    prediction='almonds'
elif result[0][3] == 1:
    prediction='chicken' 
elif result[0][4] == 1:
    prediction='chilli'
elif result[0][5] == 1:
    prediction = 'drumstick'
elif result[0][6] == 1:
    prediction='flour'
elif result[0][7] == 1:
    prediction='jeera' 
elif result[0][8] == 1:
    prediction='lemon'
elif result[0][9] == 1:
    prediction='milk'
elif result[0][10] == 1:
    prediction='mutton'
elif result[0][11] == 1:
    prediction='onion' 
elif result[0][12] == 1:
    prediction='paneer'
elif result[0][13] == 1:
    prediction='peas'
elif result[0][14] == 1:
    prediction='potato'
elif result[0][15] == 1:
    prediction='tamarind'   
else:
    prediction='tomato'

print(prediction)
