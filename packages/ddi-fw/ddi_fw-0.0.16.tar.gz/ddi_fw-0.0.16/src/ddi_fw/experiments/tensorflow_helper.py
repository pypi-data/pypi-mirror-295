from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, Input, Activation, BatchNormalization
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
import numpy as np

import mlflow
from mlflow.utils.autologging_utils import batch_metrics_logger
import time

from mlflow.models import infer_signature
from ddi_fw.experiments.evaluation_helper import evaluate

import tf2onnx
import onnx

import itertools
import ddi_fw.utils

# https://github.com/YifanDengWHU/DDIMDL/blob/master/newTask.py
# from numpy.random import seed
# seed(1)
# from tensorflow import set_random_seed
# set_random_seed(2)
tf.random.set_seed(1)
np.random.seed(2)
np.set_printoptions(precision=4)


class TFMultiModal:
    # todo model related parameters to config
    def __init__(self, model_func, batch_size=128, epochs=100):
        self.model_func = model_func
        self.batch_size = batch_size
        self.epochs = epochs

    def set_data(self, items, train_idx_arr, val_idx_arr, y_test_label):
        self.items = items
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr
        self.y_test_label = y_test_label

    def predict(self, combinations: list = [], generate_combinations=False):
        self.prefix = utils.utc_time_as_string()
        self.date = utils.utc_time_as_string_simple_format
        sum = np.zeros(
            (self.y_test_label.shape[0], self.y_test_label.shape[1]))
        single_results = dict()

        if generate_combinations:
            l = [item[0] for item in self.items]
            combinations = []
            for i in range(2, len(l) + 1):
                combinations.extend(list(itertools.combinations(l, i)))  # all

        with mlflow.start_run(run_name=self.prefix, description="***") as run:
            self.level_0_run_id = run.info.run_id
            for item in self.items:
                print(item[0])
                single_modal = TFSingleModal(
                    self.date, item[0], self.model_func, self.batch_size, self.epochs)
                single_modal.set_data(
                    self.train_idx_arr, self.val_idx_arr, item[1], item[2], item[3], item[4])
                r = single_modal.predict()
                single_results[item[0]] = r
                sum = sum + r

            if combinations:
                self.evaluate_combinations(single_results, combinations)
        # TODO: sum'a gerek yok
        return sum, single_results

    def evaluate_combinations(self, single_results, combinations):
        for combination in combinations:
            combination_descriptor = '-'.join(combination)
            with mlflow.start_run(run_name=combination_descriptor, description="***", nested=True) as combination_run:
                prediction = np.zeros(
                    (self.y_test_label.shape[0], self.y_test_label.shape[1]))
                for item in combination:
                    prediction = prediction + single_results[item]
                logs, metrics = evaluate(
                    actual=self.y_test_label, pred=prediction, info=combination_descriptor)
                mlflow.log_metrics(logs)
                metrics.format_float()
                # TODO path bulunamadı hatası aldık
                print(
                    f'combination_artifact_uri:{combination_run.info.artifact_uri}')
                utils.compress_and_save_data(
                    metrics.__dict__, combination_run.info.artifact_uri, f'{self.date}_metrics.gzip')


class TFSingleModal:
    def __init__(self, date, descriptor, model_func, batch_size=128, epochs=100):
        self.date = date
        self.descriptor = descriptor
        self.model_func = model_func
        self.batch_size = batch_size
        self.epochs = epochs

    def set_data(self, train_idx_arr, val_idx_arr, train_data, train_label, test_data, test_label):
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr
        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label

# https://github.com/mlflow/mlflow/blob/master/examples/tensorflow/train.py
    def predict(self):
        print(self.train_data.shape)

        # Failed to convert a NumPy array to a Tensor
        with mlflow.start_run(run_name=self.descriptor, description="***", nested=True) as run:
            models = dict()
            histories = dict()
            models_val_acc = dict()
            # with batch_metrics_logger(run_id) as metrics_logger:
            for i, (train_idx, val_idx) in enumerate(zip(self.train_idx_arr, self.val_idx_arr)):
                print(f"Validation {i}")

                with mlflow.start_run(run_name=f'Validation {i}', description='CV models', nested=True) as cv_fit:
                    model = self.model_func(self.train_data.shape[1])
                    models[f'validation_{i}'] = model
                    X_train_cv = self.train_data[train_idx]
                    y_train_cv = self.train_label[train_idx]
                    X_valid_cv = self.train_data[val_idx]
                    y_valid_cv = self.train_label[val_idx]

                    early_stopping = EarlyStopping(
                        monitor='val_loss', patience=10, verbose=0, mode='auto')
                    custom_callback = CustomCallback()
                    history = model.fit(X_train_cv, y_train_cv,
                                        batch_size=self.batch_size,
                                        epochs=self.epochs,
                                        validation_data=(
                                            X_valid_cv, y_valid_cv),
                                        callbacks=[early_stopping, custom_callback])
                    # histories[f'validation_{i}'] = history
                    models_val_acc[f'validation_{i}'] = history.history['val_accuracy'][-1]
                    # Saving each CV model

            best_model_key = max(models_val_acc, key=models_val_acc.get)
            best_model = models[best_model_key]
            best_model.evaluate(self.test_data, self.test_label,
                                callbacks=[custom_callback])
            pred = best_model.predict(self.test_data)

            logs, metrics = evaluate(
                actual=self.test_label, pred=pred, info=self.descriptor)
            metrics.format_float()
            mlflow.log_metrics(logs)
            mlflow.log_param('best_cv', best_model_key)
            signature = infer_signature(
                self.train_data,
                # generate_signature_output(model,X_valid_cv)
                # params=params,
            )

            mlflow.tensorflow.save_model(
                best_model,
                path=run.info.artifact_uri + '/model',
                signature=signature,
            )
            print(run.info.artifact_uri)
            onnx_model, _ = tf2onnx.convert.from_keras(
                best_model, input_signature=None, opset=13)
            onnx.save(onnx_model, run.info.artifact_uri +
                      '/model/model.onnx')
            utils.compress_and_save_data(
                metrics.__dict__, run.info.artifact_uri, f'{self.date}metrics.gzip')
            # mlflow.log_dict(metrics.__dict__, "metrics.json")

            # Plot Precision-Recall curves for each class and micro-average
            # fig = plt.figure()
            # plt.step(metrics.recall['micro_event'], metrics.precision['micro_event'],
            #          color='b', alpha=0.2, where='post')
            # plt.fill_between(
            #     metrics.recall["micro_event"], metrics.precision["micro_event"], step='post', alpha=0.2, color='b')

            # for i in range(pred.shape[1]):
            #     plt.step(metrics.recall[i], metrics.precision[i], where='post',
            #              label='Class {0} (AUC={1:0.2f})'.format(i, metrics.roc_aupr[i]))

            # plt.xlabel('Recall')
            # plt.ylabel('Precision')
            # plt.ylim([0.0, 1.05])
            # plt.xlim([0.0, 1.0])
            # plt.title(
            #     'Micro-average Precision-Recall curve: AUC={0:0.2f}'.format(metrics.roc_aupr["micro"]))
            # plt.legend(loc='best')
            # # plt.savefig(run.info.artifact_uri + '/auprc.png')
            # mlflow.log_figure(fig, 'auprc.png')

            # mlflow.log_model(
            #         model,
            #         artifact_path=run.info.artifact_uri + '/model',
            #         signature=signature,
            #     )
            # mlflow.log_artifact(run.info.artifact_uri + '/model')

            # mlflow.MlflowClient().log_artifact(run.info.run_id,
            #                                    run.info.artifact_uri, None)
        return pred


class CustomCallback(keras.callbacks.Callback):
    def on_train_begin(self, logs=None):
        keys = list(logs.keys())
        mlflow.log_param("train_begin_keys", keys)
        config = self.model.optimizer.get_config()
        for attribute in config:
            mlflow.log_param("opt_" + attribute, config[attribute])

        sum_list = []
        self.model.summary(print_fn=sum_list.append)
        summary = "\n".join(sum_list)
        mlflow.log_text(summary, artifact_file="model_summary.txt")

    def on_train_end(self, logs=None):
        print(logs)
        mlflow.log_metrics(logs)

    def on_epoch_begin(self, epoch, logs=None):
        keys = list(logs.keys())

    def on_epoch_end(self, epoch, logs=None):
        keys = list(logs.keys())

    def on_test_begin(self, logs=None):
        keys = list(logs.keys())

    def on_test_end(self, logs=None):
        mlflow.log_metrics(logs)
        print(logs)

    def on_predict_begin(self, logs=None):
        keys = list(logs.keys())

    def on_predict_end(self, logs=None):
        keys = list(logs.keys())
        mlflow.log_metrics(logs)

    def on_train_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

    def on_train_batch_end(self, batch, logs=None):
        keys = list(logs.keys())

    def on_test_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

    def on_test_batch_end(self, batch, logs=None):
        keys = list(logs.keys())

    def on_predict_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

    def on_predict_batch_end(self, batch, logs=None):
        keys = list(logs.keys())
    # def on_train_begin(self, logs=None):  # pylint: disable=unused-argument
    #     config = self.model.optimizer.get_config()
    #     for attribute in config:
    #         mlflow.log_param("opt_" + attribute, config[attribute])

    #     sum_list = []
    #     self.model.summary(print_fn=sum_list.append)
    #     summary = "\n".join(sum_list)
    #     mlflow.log_text(summary, artifact_file="model_summary.txt")

    # def on_epoch_end(self, epoch, logs=None):
    #     # NB: tf.Keras uses zero-indexing for epochs, while other TensorFlow Estimator
    #     # APIs (e.g., tf.Estimator) use one-indexing. Accordingly, the modular arithmetic
    #     # used here is slightly different from the arithmetic used in `_log_event`, which
    #     # provides  metric logging hooks for TensorFlow Estimator & other TensorFlow APIs
    #     if epoch % self.log_every_n_steps == 0:
    #         self.metrics_logger.record_metrics(logs, epoch)

    # def predict(self):
    #     model = self.model_func()
    #     # Failed to convert a NumPy array to a Tensor
    #     for i, (train_idx, val_idx) in enumerate(zip(self.train_idx_arr, self.val_idx_arr)):
    #         print(f"Validation {i}")
    #         X_train_cv = self.train_data[train_idx]
    #         y_train_cv = self.train_label[train_idx]
    #         X_valid_cv = self.train_data[val_idx]
    #         y_valid_cv = self.train_label[val_idx]

    #         early_stopping = EarlyStopping(
    #             monitor='val_loss', patience=10, verbose=0, mode='auto')
    #         model.fit(X_train_cv, y_train_cv, batch_size=128, epochs=20, validation_data=(X_valid_cv, y_valid_cv),
    #                   callbacks=[early_stopping])
    #     pred = model.predict(self.test_data)
    #     return pred
