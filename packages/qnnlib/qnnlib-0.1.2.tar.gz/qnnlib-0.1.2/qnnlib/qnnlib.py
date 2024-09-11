import pennylane as qml
import numpy as np
import tensorflow as tf
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
import csv

class qnnlib:
    """
    qnnlib is a quantum neural network library that provides functionality for constructing 
    quantum circuits, training models, and performing experiments with various quantum devices. 
    The library supports custom optimization, scaling, and loss functions.
    
    Attributes:
        SUPPORTED_DEVICES (list): List of supported quantum devices.
        nqubits (int): The number of qubits used in the quantum circuits.
        device_name (str): The name of the quantum device to be used in computations.
    """
    
    SUPPORTED_DEVICES = [
        "default.qubit",
        "default.mixed",
        "lightning.qubit",
        "lightning.gpu",
        "lightning.kokkos",
        "qiskit.aer",
        "qiskit.remote"
    ]
    
    def __init__(self, nqubits=4, device_name="default.qubit", backend=None):
        """
        Initializes the qnnlib class with the specified number of qubits and quantum device.

        Args:
            nqubits (int): Number of qubits to use in the circuit.
            device_name (str): Name of the quantum device to be used.
            backend (None) : Physical quantum machine backend for using with qiskit.remote (refer to : https://docs.pennylane.ai/projects/qiskit/en/latest/)
        
        Raises:
            ValueError: If an unsupported device name is provided.
        """
        if device_name not in self.SUPPORTED_DEVICES:
            raise ValueError(f"Unsupported device: {device_name}. Supported devices are: {self.SUPPORTED_DEVICES}")
        self.nqubits = nqubits
        self.device_name = device_name
        self.backend=backend    

    def ZZFeatureMap(self, data):
        """
        Applies a ZZFeatureMap to encode classical data into quantum states.

        Args:
            data (np.ndarray): The input classical data to be encoded.
        """
        nload = min(len(data), self.nqubits)
        for i in range(nload):
            qml.Hadamard(i)
            qml.RZ(2.0 * data[:, i], wires=i)
        for pair in list(combinations(range(nload), 2)):
            q0, q1 = pair
            qml.CZ(wires=[q0, q1])
            qml.RZ(2.0 * (np.pi - data[:, q0]) * (np.pi - data[:, q1]), wires=q1)
            qml.CZ(wires=[q0, q1])

    def TwoLocal(self, theta, reps=3):
        """
        Constructs a parameterized quantum circuit (ansatz) using the TwoLocal structure.

        Args:
            theta (np.ndarray): The input parameters for the rotations.
            reps (int): The number of repetitions of the ansatz.
        """
        for r in range(reps):
            for i in range(self.nqubits):
                qml.RY(theta[r * self.nqubits + i], wires=i)
            for i in range(self.nqubits - 1):
                qml.CNOT(wires=[i, i + 1])

        for i in range(self.nqubits):
            qml.RY(theta[reps * self.nqubits + i], wires=i)

    def qnn_circuit(self, inputs, theta, M=None, reps=3):
        """
        Defines the full quantum neural network circuit using ZZFeatureMap and TwoLocal ansatz.

        Args:
            inputs (np.ndarray): The input data to be encoded.
            theta (np.ndarray): Parameters for the TwoLocal circuit.
            M (np.ndarray): Hermitian matrix used for measurement.
            reps (int): Number of repetitions for the ansatz.

        Returns:
            float: The expected value of the Hermitian observable.
        """
        self.ZZFeatureMap(inputs)
        self.TwoLocal(theta=theta, reps=reps)
        return qml.expval(qml.Hermitian(M, wires=[0]))

    def create_qnn_model(self, reps=3, optimizer=None, loss_fn=None, metrics=None):
        """
        Creates and compiles a quantum neural network model using TensorFlow and PennyLane.

        Args:
            reps (int): Number of repetitions for the TwoLocal ansatz.
            optimizer (tf.keras.optimizers.Optimizer): Optimizer for model training.
            loss_fn (tf.keras.losses.Loss): Loss function for model training.
            metrics (list): List of metrics to evaluate the model.

        Returns:
            tf.keras.models.Model: The compiled quantum neural network model.
        """
        # Use default values if not provided
        if optimizer is None:
            optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.01)
        if loss_fn is None:
            loss_fn = tf.keras.losses.CategoricalCrossentropy()
        if metrics is None:
            metrics = [tf.keras.metrics.BinaryAccuracy()]

        dev = None
        if self.device_name == "qiskit.remote":
            dev = qml.device(self.device_name, wires=self.nqubits, backend=self.backend)
        else:
            dev = qml.device(self.device_name, wires=self.nqubits)

        state_0 = np.array([[1], [0]])
        M = state_0 @ np.conj(state_0).T

        # Dynamically determine the number of parameters needed for theta
        total_params = self.nqubits * reps
        qnn = qml.QNode(lambda inputs, theta: self.qnn_circuit(inputs, theta, M=M), dev, interface="tf")
        weights = {"theta": total_params}

        qlayer = qml.qnn.KerasLayer(qnn, weights, output_dim=1)

        model = tf.keras.models.Sequential([qlayer])
        model.compile(optimizer=optimizer, loss=loss_fn, metrics=metrics)

        return model

    def train_qnn_model(self, model, xs_tr, y_tr, xs_val, y_val, epochs=50, batch_size=20):
        """
        Trains the quantum neural network model.

        Args:
            model (tf.keras.models.Model): The compiled QNN model.
            xs_tr (np.ndarray): Training data features.
            y_tr (np.ndarray): Training data labels.
            xs_val (np.ndarray): Validation data features.
            y_val (np.ndarray): Validation data labels.
            epochs (int): Number of training epochs.
            batch_size (int): Size of each training batch.

        Returns:
            tf.keras.callbacks.History: Training history containing loss and accuracy information.
        """
        history = model.fit(xs_tr, y_tr, epochs=epochs, shuffle=True, validation_data=(xs_val, y_val), batch_size=batch_size)
        return history

    def plot_losses(self, history):
        """
        Plots the training and validation losses over epochs.

        Args:
            history (tf.keras.callbacks.History): The history object from model training.
        """
        tr_loss = history.history["loss"]
        val_loss = history.history["val_loss"]
        epochs = np.array(range(len(tr_loss))) + 1
        plt.plot(epochs, tr_loss, label="Training loss")
        plt.plot(epochs, val_loss, label="Validation loss")
        plt.xlabel("Epoch")
        plt.legend()
        plt.show()

    def plot_accuracy(self, history):
        """
        Plots the training and validation accuracy over epochs.

        Args:
            history (tf.keras.callbacks.History): The history object from model training.
        """
        tr_acc = history.history["binary_accuracy"]
        val_acc = history.history["val_binary_accuracy"]
        epochs = np.array(range(len(tr_acc))) + 1
        plt.plot(epochs, tr_acc, label="Training accuracy")
        plt.plot(epochs, val_acc, label="Validation accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.legend()
        plt.show()

    def dump_training_progress(self, history, csv_filename):
        """
        Dumps the training progress (epoch, training accuracy, training loss, 
        validation accuracy, validation loss) into a CSV file.

        Args:
            history (tf.keras.callbacks.History): The history object from model training.
            csv_filename (str): The name of the CSV file where training progress will be saved.
        """
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Epoch", "Train Accuracy", "Train Loss", "Validation Accuracy", "Validation Loss"])
            epochs = len(history.history["loss"])
            for epoch in range(epochs):
                writer.writerow([
                    epoch + 1,
                    history.history["binary_accuracy"][epoch],
                    history.history["loss"][epoch],
                    history.history["val_binary_accuracy"][epoch],
                    history.history["val_loss"][epoch]
                ])

    def prepare_data_pca(self, filepath, target, test_size=0.2, val_size=0.5, seed=4321, scaler=None):
        """
        Prepares data for training by loading it, splitting into train, validation, and test sets,
        scaling, and applying PCA for dimensionality reduction.

        Args:
            filepath (str): The path to the CSV file containing the dataset.
            target (str): The name of the target column to predict.
            test_size (float): Proportion of data to use as test set.
            val_size (float): Proportion of the test data to use as validation set.
            seed (int): Seed for reproducibility.
            scaler (object): Optional scaler to apply (e.g., MinMaxScaler). If None, no scaling is applied.

        Returns:
            tuple: Training, validation, and test datasets with their labels.
        """
        data = pd.read_csv(filepath)
        features = [col for col in data.columns if col != target]
        X = data[features].values
        y = data[[target]].values

        xs_tr, xs_test, y_tr, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
        xs_val, xs_test, y_val, y_test = train_test_split(xs_test, y_test, test_size=val_size, random_state=seed)

        # Apply scaling if scaler is provided
        if scaler:
            xs_tr = scaler.fit_transform(xs_tr)
            xs_val = scaler.transform(xs_val)
            xs_test = scaler.transform(xs_test)

        # Apply PCA for dimensionality reduction
        pca = PCA(n_components=self.nqubits)
        xs_tr = pca.fit_transform(xs_tr)
        xs_val = pca.transform(xs_val)
        xs_test = pca.transform(xs_test)

        return xs_tr, y_tr, xs_val, y_val, xs_test, y_test

    def run_experiment(self, data_path, target, model_output_path="model.h5", csv_output_path="progress.csv", test_size=0.2, val_size=0.5, scaler=MinMaxScaler(), reps=3, epochs=50, batch_size=20, optimizer=None, loss_fn=None, metrics=None, seed=4321):
        """
        Runs a full quantum neural network experiment, including data preparation, model training, 
        and saving results to files.

        Args:
            data_path (str): Path to the CSV dataset.
            target (str): Target column name.
            model_output_path (str): File path to save the trained model.
            csv_output_path (str): File path to save training progress.
            test_size (float): Proportion of data to use as the test set.
            val_size (float): Proportion of test data used as validation set.
            scaler (object): Optional scaler for feature scaling.
            reps (int): Number of repetitions for the TwoLocal ansatz.
            epochs (int): Number of training epochs.
            batch_size (int): Batch size for training.
            optimizer (tf.keras.optimizers.Optimizer): Optional optimizer.
            loss_fn (tf.keras.losses.Loss): Optional loss function.
            metrics (list): Optional list of metrics for model evaluation.
            seed (int): Seed for reproducibility.
        """
        xs_tr, y_tr, xs_val, y_val, xs_test, y_test = self.prepare_data_pca(
            filepath=data_path, target=target, test_size=test_size, val_size=val_size, scaler=scaler,seed=seed
        )

        model = self.create_qnn_model(reps=reps, optimizer=optimizer, loss_fn=loss_fn, metrics=metrics)
        history = self.train_qnn_model(model, xs_tr, y_tr, xs_val, y_val, epochs=epochs, batch_size=batch_size)

        # Save the entire model
        model.save(model_output_path)
        
        # Dump training progress into a CSV file
        self.dump_training_progress(history, csv_output_path)

        # Plot losses and accuracy
        self.plot_losses(history)
        self.plot_accuracy(history)



if __name__ == '__main__':
    qnn = qnnlib(nqubits=8, device_name="lightning.qubit")
    qnn.run_experiment(
        data_path='diabetes.csv', 
        target='Outcome', 
        test_size=0.3,
        model_output_path='qnn_model.keras', 
        csv_output_path='training_progress.csv',
        batch_size=10,
        epochs=2,
        reps=2048,
        scaler=MinMaxScaler(),
        seed=1234
    )