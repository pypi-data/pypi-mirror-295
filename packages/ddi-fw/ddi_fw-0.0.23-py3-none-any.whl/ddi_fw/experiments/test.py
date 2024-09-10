# # https://github.com/kashif/tf-keras-tutorial/blob/tf2/3-imdb.ipynb
# # TensorFlow and tf.keras
# import tensorflow as tf

# # Helper libraries
# import numpy as np
# import matplotlib.pyplot as plt
# from tensorflow_helper import CustomCallback

# print(tf.__version__)


# imdb = tf.keras.datasets.imdb

# (train_data, train_labels), (test_data, test_labels) = tf.keras.datasets.imdb.load_data(num_words=10000)


# class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
#                'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

  
# # Create a model
# model = tf.keras.Sequential()
# custom_callback = CustomCallback()

#  # input shape here is the length of our movie review vector
# model.add(tf.keras.layers.Dense(16, activation=tf.nn.relu, input_shape=(10000,)))
# model.add(tf.keras.layers.Dense(16, activation=tf.nn.relu))
# model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))

# optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.001)

# model.compile(loss='binary_crossentropy',
#               optimizer=optimizer,
#               metrics=['binary_accuracy'])

# model.summary()
 
# VAL_SIZE = 10000
# x  = np.array(train_data[:VAL_SIZE].tolist())

# val_data = np.asarray(train_data[:VAL_SIZE])
# partial_train_data = np.asarray(train_data[VAL_SIZE:])


# val_labels = train_labels[:VAL_SIZE]
# partial_train_labels = train_labels[VAL_SIZE:]

# BATCH_SIZE = 512
# SHUFFLE_SIZE = 1000

# # training_set = tf.data.Dataset.from_tensor_slices((partial_train_data, partial_train_labels))
# # training_set = training_set.shuffle(SHUFFLE_SIZE).batch(BATCH_SIZE)

# model.fit(partial_train_data , partial_train_labels , batch_size=128, epochs=20, validation_data=(val_data , val_labels ),
#                           callbacks=[custom_callback])

# loss, accuracy = model.evaluate(test_data, test_labels,callbacks=[custom_callback])
# print('Test accuracy: %.2f' % (accuracy))