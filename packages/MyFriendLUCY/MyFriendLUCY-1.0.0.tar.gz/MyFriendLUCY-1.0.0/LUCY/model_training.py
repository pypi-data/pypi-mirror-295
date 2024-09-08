import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore

# Load the preprocessed datasets
X = np.load('X.npy')
Y = np.load('Y.npy')

# Ensure Y matches the time step prediction (1 hour ahead)
Y_lstm = Y  # Directly using Y since it's already structured for 1 hour ahead

# Adjust X to match the length of Y
X_lstm = X[:len(Y_lstm)]

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=100, return_sequences=True, input_shape=(X_lstm.shape[1], X_lstm.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=25))
model.add(Dense(units=1))  # Predicting 1 future price

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_lstm, Y_lstm, epochs=10, batch_size=64, validation_split=0.2)

# Save the model
model.save('eth_lstm_model.h5')

print("Model training complete and saved to eth_lstm_model.h5")
