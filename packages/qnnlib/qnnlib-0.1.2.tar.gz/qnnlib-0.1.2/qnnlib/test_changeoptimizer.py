from qnnlib import qnnlib
from sklearn.preprocessing import MaxAbsScaler
import tensorflow as tf

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
    scaler=MaxAbsScaler(),
    optimizer=tf.keras.optimizers.Adamax(learning_rate=0.001),
    seed=1234
)


