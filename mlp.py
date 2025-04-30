import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.metrics import AUC, Recall

file = "save_file/AB22V2_df.csv"
df = pd.read_csv(file)

target_col = df.columns[-1]
X = df.drop(columns=[target_col]).values
y = df[target_col].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

mlp_model = Sequential()
mlp_model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
mlp_model.add(Dropout(0.2))
mlp_model.add(Dense(48, activation='relu'))
mlp_model.add(Dropout(0.2))
mlp_model.add(Dense(32, activation='relu'))
mlp_model.add(Dropout(0.2))
mlp_model.add(Dense(16, activation='relu'))
mlp_model.add(Dropout(0.2))
mlp_model.add(Dense(1, activation='sigmoid'))

mlp_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', Recall(name="recall"), AUC(name='auc')])

class_weights = compute_class_weight('balanced', classes=np.array([0, 1]), y=y_train)
class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

history = mlp_model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=32,
    batch_size=32,
    class_weight=class_weight_dict,
    verbose=1
)

y_proba = mlp_model.predict(X_test).flatten()
y_pred = (y_proba >= 0.5).astype(int)

print({
    "target": target_col,
    "accuracy": round(accuracy_score(y_test, y_pred), 4),
    "auc": round(roc_auc_score(y_test, y_proba), 4),
    "f1_score": round(f1_score(y_test, y_pred), 4),
    "precision": round(precision_score(y_test, y_pred), 4),
    "recall": round(recall_score(y_test, y_pred), 4)
})

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
# plt.plot(history.history['accuracy'], label='Train Acc')
# plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.plot(history.history['auc'], label='Train AUC')
plt.plot(history.history['val_auc'], label='Val AUC')
plt.plot(history.history['recall'], label='Train Recall')
plt.plot(history.history['val_recall'], label='Val Recall')
plt.legend()
plt.show()

test = X_test[0:1].copy()
test[0][0] = 60
test[0][1] = 2
test[0][3] = 70
test[0][4] = 3
print(mlp_model.predict(test))

mlp_model.save('save_file/AB22V2_model.h5')
