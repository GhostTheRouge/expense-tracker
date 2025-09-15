import pandas as pd

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