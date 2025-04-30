import pandas as pd
import pyreadstat
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import classification_report

# 1. 读取数据
file_path = r"ADULT SAS\adult.sas7bdat"
df, meta = pyreadstat.read_sas7bdat(file_path)

selected_features = [
    "AC117V2", "AC118V2", "AC174", "AC207", "AC208", "AC209", "AC212", "AC81C",
    "AD13V2", "AD32_P1", "AE15", "AE15A", "AE2V2", "AE7V2", "AE_FRUITV2", "AE_VEGIV2", "AF81",
    "AJ169V3", "AJ235", "AJ236", "AJ241", "AJ29", "AJ30", "AJ31", "AJ32", "AJ33", "AJ34",
    "AK1", "AK139_1", "AK139_2", "AK139_3", "AK139_4", "AK20_P1", "AK7_P1V2", "AKWKLNG", "AM1",
    "AM194", "AM199", "AM2", "AM20", "AM21", "AM3", "AM39", "AM5", "ASTCUR", "DISTRESS",
    "DSTRS12", "DSTRS30", "DSTRSYR", "DISABILITY", "DMC8", "DMC9", "BINGE30",
    "FLAVTOB", "FLAVTOB2", "ESMKCUR", "HOUSETYPE", "HEALTHHARM", "AQ1", "AQ12", "AQ13", "AQ14",
    "AQ15", "AQ25V2", "AQ28", "LATIN2TP", "MARCUR", "MAREXPOSE", "MARIT", "MARIT2", "MARIT_45",
    "MARTYPEV2", "MAR_BLUNTV2", "MAR_DABV2", "MAR_DRINKV2", "MAR_EATV2", "MAR_SMKV2", "MAR_VAPV2",
    "MASK_VAX", "MENA", "MJMETHOD_P1", "MORE_VAX", "MORE_VAX2", "NONCIGPRO", "NONFLAVTOB",
    "NUMCIG", "OCCMAIN2", "OCC_FLAG3", "OMBSRR_P1", "OVRWT", "POVGWD_P1", "POVLL",
    "POVLL2_P1V2", "RACECN_P1", "RBMI", "SCND_SMK", "SMKCUR", "SMKCUR30", "SMKEXPOSE",
    "SMOKING", "SOCIAL2", "SRAGE_P1", "SREDUC", "SRSEX", "SRTENR", "STABLEHOUSE",
    "STABLEHOUSE2", "TOBCUR", "TRANSGEND2", "UR_BG4", "UR_CLRT4", "UR_TRACT4", "WGHTK_P",
    "WHOBMI", "WRKST_P1"
]

# Example: List of disease columns
disease_columns = ["AB154", "AB17", "AB22V2", "AB29V2", "AB34"]

df = df.drop(df[df.AJ31 == -2].index)

for disease in disease_columns:
    df[disease] = df[disease] - 1
    df.drop(df[df[disease] == 2].index, inplace=True)

# 2. 保留目标列和特征列
target_col = "AB154"
all_columns = selected_features + [target_col]
df = df[all_columns]

# 3. 删除目标为缺失值的行
df = df[df[target_col].notna()]

# 4. 简单处理：将类别变量用LabelEncoder编码，将缺失值填充为mode/median
for col in selected_features:
    if df[col].dtype == "object" or df[col].dtype.name == "category":
        df[col] = df[col].astype(str)  # Convert to string in case of mixed types
        df[col] = df[col].fillna("MISSING")
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    else:
        df[col] = df[col].fillna(df[col].median())  # 用中位数填充缺失值

# 5. 处理目标变量（分类标签）
df[target_col] = df[target_col].astype(int)  # 确保是整数标签（如0/1）

# 6. 切分训练集和测试集
X = df[selected_features]
y = df[target_col]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. 训练随机森林模型
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. 评估模型
y_pred = model.predict(X_test)
print("混淆矩阵:")
print(confusion_matrix(y_test, y_pred))
print("\n分类报告:")
print(classification_report(y_test, y_pred))
