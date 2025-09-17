import pandas as pd
from openai import OpenAI
import matplotlib.pyplot as plt

df = pd.read_csv("expense_data_1.csv")
#print(df.head())

data = df[["Date", "Category", "Note", "Amount", "Income/Expense"]]
#print(data.head())

def add_expense(date, category, note, amount, exp_type="Expense"):
    global data # This ensures the new expense is added to the main dataset (data) instead of a temp copy
    new_entry = {
        "Date": date,
        "Category": category,
        "Note": note,
        "Amount": amount,
        "Income/Expense": exp_type
    }
    data = date.append(new_entry, ignore_index=True) 
    # ignore_index ignores index when appending - so no 01234... instead of 010101 for example
    
def view_expenses(n=5):
    return data.tail(n) # Returns the bottom n rows of the DataFrame
#print(view_expenses(5))

def summarize_expenses(by="Category"):
    summary = data[data["Income/Expense"]=="Expense"].groupby(by)["Amount"].sum()
    # data[data["Income/Expense"]=="Expense"] filters the dataset to include only expenses (ignores income)
    
    # .gorupby(by)["Amount"].sum() groups by "Category" in this case as it is the default value, and adds up all amounts in each group,
    ## e.g. food expenses are summed together etc...
    return summary.sort_values(ascending=False) # Sorts categories by total spending from highest to lowest
print(summarize_expenses())

client = OpenAI(api_key=
                "")

def auto_categorize(note):
    prompt = f"""
    Categorize this expense note into one of these categories:
    Food, Transportation, Entertainment, Other.
    Note: {note}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Other"
    
data['Category'] = data.apply(
    lambda row: auto_categorize(row['Note']) if pd.isna(row['Category']) else row['Category'],
    axis=1
)

print(data[['Note', 'Category']].head(10))

expense_summary = data[data['Category'] != 'Income'].groupby("Category")['Amount'].sum()

# Pie Chart
plt.figure(figsize=(6,6))
expense_summary.plot.pie(autopct='%1.1f%%', startangle=90, shadow=True)
plt.title("Expenses Breakdown by Category")
plt.ylabel("")
plt.show()

# Bar Chart
plt.figure(figsize=(8.5))
expense_summary.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Expenses by Category")
plt.xlabel("Category")
plt.ylabl("Amount Spent")
plt.show()