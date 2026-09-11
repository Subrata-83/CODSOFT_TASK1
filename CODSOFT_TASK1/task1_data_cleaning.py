import pandas as pd
from tkinter import Tk, filedialog
import os


# ============================================================
# STEP 1: SELECT AND LOAD DATASET
# ============================================================

root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select Student Dataset",
    filetypes=[("Excel Files", "*.xlsx")]
)

if not file_path:
    print("No file selected. Program stopped.")
    exit()

df = pd.read_excel(file_path)

print("\n========== DATASET LOADED SUCCESSFULLY ==========\n")

print("First 5 rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
df.info()


# ============================================================
# STEP 2: IDENTIFY MISSING VALUES
# ============================================================

print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())


# ============================================================
# STEP 3: HANDLE MISSING VALUES
# ============================================================

print("\n========== HANDLING MISSING VALUES ==========")

# Fill missing categorical values with the most frequent value
df["Gender"] = df["Gender"].fillna(df["Gender"].mode()[0])
df["Department"] = df["Department"].fillna(df["Department"].mode()[0])


# Convert Study Hours to numeric
df["Study_Hours"] = pd.to_numeric(
    df["Study_Hours"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
    errors="coerce"
)


# Convert Attendance to numeric
df["Attendance"] = pd.to_numeric(
    df["Attendance"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
    errors="coerce"
)


# Convert Math Score to numeric
df["Math_Score"] = pd.to_numeric(
    df["Math_Score"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
    errors="coerce"
)


# Numeric columns
numeric_columns = [
    "Study_Hours",
    "Attendance",
    "Math_Score",
    "Reading_Score",
    "Writing_Score"
]


# Fill missing numeric values with median
for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())


print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nTotal missing values:")
print(df.isnull().sum().sum())


# ============================================================
# STEP 4: IDENTIFY AND REMOVE DUPLICATE RECORDS
# ============================================================

print("\n========== DUPLICATE RECORDS ==========")

duplicate_count = df.duplicated().sum()

print("Number of duplicate rows:", duplicate_count)


# Remove duplicate records
df = df.drop_duplicates()


print("\nDuplicate records after cleaning:")
print(df.duplicated().sum())


# ============================================================
# STEP 5: IDENTIFY INCONSISTENT DATA
# ============================================================

print("\n========== INCONSISTENT VALUES BEFORE CLEANING ==========")

print("\nGender values before cleaning:")
print(df["Gender"].value_counts(dropna=False))

print("\nDepartment values before cleaning:")
print(df["Department"].value_counts(dropna=False))


# ============================================================
# STEP 6: CLEAN INCONSISTENT DATA
# ============================================================

print("\n========== CLEANING INCONSISTENT DATA ==========")


# Clean Gender values
df["Gender"] = df["Gender"].replace({
    "female": "Female",
    "male": "Male",
    "M": "Male",
    "F": "Female"
})


# Remove extra spaces from Department
df["Department"] = df["Department"].astype(str).str.strip()


# Standardize Department names
df["Department"] = df["Department"].replace({
    "cse": "CSE",
    "Computer Science": "CSE",
    "civil": "Civil"
})


# ============================================================
# STEP 7: VERIFY CLEANED CATEGORICAL DATA
# ============================================================

print("\nGender values after cleaning:")
print(df["Gender"].value_counts())

print("\nDepartment values after cleaning:")
print(df["Department"].value_counts())


# ============================================================
# STEP 8: CORRECT DATA TYPES
# ============================================================

print("\n========== DATA TYPES AFTER CLEANING ==========")

print(df.dtypes)


# ============================================================
# STEP 9: FINAL VERIFICATION
# ============================================================

print("\n========== FINAL DATA VERIFICATION ==========")

print("Total missing values:", df.isnull().sum().sum())
print("Total duplicate rows:", df.duplicated().sum())
print("Final dataset shape:", df.shape)


# ============================================================
# STEP 10: SAVE CLEANED DATASET
# ============================================================

print("\n========== SAVING CLEANED DATASET ==========")

# Save cleaned CSV in the same folder as the original Excel file
output_folder = os.path.dirname(file_path)

output_file = os.path.join(
    output_folder,
    "cleaned_StudentsPerformance.csv"
)

df.to_csv(output_file, index=False)

print("Cleaned dataset saved successfully!")
print("File name: cleaned_StudentsPerformance.csv")
print("Saved location:", output_file)


# ============================================================
# PROJECT COMPLETION MESSAGE
# ============================================================

print("\n========== TASK 1 COMPLETED SUCCESSFULLY ==========")
print("Data cleaning and preprocessing completed.")