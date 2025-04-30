import pandas as pd
import pyreadstat

# Replace with your actual file path
file_path = r"D:\SFU\CMPT 733 Big Data2\final project\ADULT SAS\adult.sas7bdat"

# Load SAS file into a Pandas DataFrame
df, meta = pyreadstat.read_sas7bdat(file_path)

# Example: List of feature columns to include
selected_features = [
    "AC117V2", "AC118V2", "AC174", "AC207", "AC208","AB150", "AC209", "AC212", "AC81C",
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

for disease in disease_columns:

    print(f"disease:{disease}")
    # Filter dataset with selected columns
    df_filtered = df[selected_features + [disease]]

    # Compute correlation matrix
    correlation_matrix = df_filtered.corr()

    # Extract correlation with disease columns
    disease_corr = correlation_matrix[[disease]]

    # Drop disease columns themselves (if present)
    disease_corr = disease_corr.drop(index=disease, errors="ignore")

    # Compute mean absolute correlation for ranking
    top_features = disease_corr.abs().mean(axis=1).sort_values(ascending=False)

    print(top_features)
    print("")
















