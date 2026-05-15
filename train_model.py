import numpy as np
import tensorflow as tf

from keras.preprocessing.image import ImageDataGenerator
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau


# paths
train_dir = "dataset/train"
test_dir = "dataset/test"

IMG_SIZE = (160,160)
BATCH_SIZE = 32
EPOCHS_STAGE1 = 8
EPOCHS_STAGE2 = 10


# data generators
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=30,
    width_shift_range=0.15,
    height_shift_range=0.15,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=(0.7,1.3),
    fill_mode="nearest"
)

test_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=True
)

test_gen = test_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

num_classes = train_gen.num_classes
print("Classes:", train_gen.class_indices)


# handle imbalance
class_counts = np.bincount(train_gen.classes)

total = float(class_counts.sum())

class_weights = {
    i: total/(num_classes*count)
    for i,count in enumerate(class_counts)
    if count>0
}

print("class counts:", class_counts)
print("class weights:", class_weights)


# base model
base_model = MobileNetV2(
    input_shape=(IMG_SIZE[0],IMG_SIZE[1],3),
    include_top=False,
    weights="imagenet"
)

# stage 1 freeze
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)

x = Dense(256, activation="relu")(x)
x = Dropout(0.4)(x)

outputs = Dense(num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=outputs)


model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


# callbacks
checkpoint = ModelCheckpoint(
    "best_arecanut_model.h5",
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

early_stop = EarlyStopping(
    monitor="val_accuracy",
    patience=5,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=2,
    min_lr=1e-6,
    verbose=1
)


# training stage 1
print("\nStage 1 training...")

history1 = model.fit(
    train_gen,
    validation_data=test_gen,
    epochs=EPOCHS_STAGE1,
    class_weight=class_weights,
    callbacks=[checkpoint, early_stop, reduce_lr]
)


# stage 2 fine tuning
print("\nStage 2 fine tuning...")

for layer in base_model.layers[-60:]:
    layer.trainable = True


model.compile(
    optimizer=Adam(learning_rate=0.00001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history2 = model.fit(
    train_gen,
    validation_data=test_gen,
    epochs=EPOCHS_STAGE1 + EPOCHS_STAGE2,
    initial_epoch=len(history1.history["loss"]),
    class_weight=class_weights,
    callbacks=[checkpoint, early_stop, reduce_lr]
)

print("\nTraining finished")