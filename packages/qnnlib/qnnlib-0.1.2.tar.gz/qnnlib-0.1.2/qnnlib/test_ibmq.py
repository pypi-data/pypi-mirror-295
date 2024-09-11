from qnnlib import qnnlib
from sklearn.preprocessing import MaxAbsScaler

from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token='895c52192b9808e59219bd934ba43af91d8dcfeb1324510b857ccf0b9ed00ecc1bd6ce21b517c3da2e5443b12cc96fd5e160b71d9e1c49ca4adaa0112682e1b2'
)
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=8)


qnn = qnnlib(nqubits=8, device_name="qiskit.remote", backend=backend)
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
    seed=1234
)


