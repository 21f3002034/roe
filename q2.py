import pandas as pd

# Load the CSV files
students = pd.read_csv('q2/students.csv')
subjects = pd.read_csv('q2/subjects.csv')

# Merge the students and subjects data on 'studentId'
merged_data = pd.merge(students, subjects, on='studentId')
# excel_writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")
# merged_data.to_excel(excel_writer, sheet_name="1", index=False)
# excel_writer.close()
# Group by 'class' and find the unique subjects in each class
unique_subjects_per_class = merged_data.groupby('class')['subject'].nunique()

# Get the 3 lowest counts of unique subjects in ascending order
lowest_counts = unique_subjects_per_class.nsmallest(5)

# Format the output as required
result = ','.join(map(str, lowest_counts))
print(result)
