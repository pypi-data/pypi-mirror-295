
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def fstar():
  print("**********************************************************")
  print("Welcome to use fstar: a star financial analysis solution")
  print("**********************************************************")
  print()
  print("Contacts:")
  print()
  print("Dr Anna Sung - email: a.sung@chester.ac.uk")
  print("Prof Kelvin Leong - email: k.leong@chester.ac.uk")
  print("subpackage: liquidity, profitability, solvency")
  print("expected data input format is in Excel and from FAME")
  # print()
  # print()
  print("**********************************************************")

#SUBPACKAGE: liquidity---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions include:
# allow user to upload an excel file and then fstar will conduct liquidity ratio analysis 
#***********************************************************************************************************
def liquidity():
  import pandas as pd
  import matplotlib.pyplot as plt
  from google.colab import files
  import io

  # Upload Excel file
  print("Please upload the Excel file containing company information:")
  uploaded = files.upload()

  # Load the Excel file into a DataFrame
  for file_name in uploaded.keys():
      df = pd.read_excel(io.BytesIO(uploaded[file_name]))

  # Display the first few rows of the DataFrame to understand the structure
  print("Here are the first few rows of the uploaded data:")
  print(df.head())

  # Prepare a list to store missing columns and calculations
  missing_columns = []
  calculated_ratios = []

  # Conduct liquidity and solvency analysis by calculating key ratios
  if 'Current Assets' in df.columns and 'Current Liabilities' in df.columns:
      df['Current Ratio'] = df['Current Assets'] / df['Current Liabilities']
      calculated_ratios.append('Current Ratio')
  else:
      missing_columns.append('Current Ratio')

  if 'Current Assets' in df.columns and 'Inventory' in df.columns and 'Current Liabilities' in df.columns:
      df['Quick Ratio'] = (df['Current Assets'] - df['Inventory']) / df['Current Liabilities']
      calculated_ratios.append('Quick Ratio')
  else:
      missing_columns.append('Quick Ratio')

  if 'Cash and Cash Equivalents' in df.columns and 'Current Liabilities' in df.columns:
      df['Cash Ratio'] = df['Cash and Cash Equivalents'] / df['Current Liabilities']
      calculated_ratios.append('Cash Ratio')
  else:
      missing_columns.append('Cash Ratio')

  if 'Current Assets' in df.columns and 'Current Liabilities' in df.columns:
      df['Working Capital'] = df['Current Assets'] - df['Current Liabilities']
      calculated_ratios.append('Working Capital')
  else:
      missing_columns.append('Working Capital')

  if 'Total Liabilities' in df.columns and 'Equity' in df.columns:
      df['Debt to Equity Ratio'] = df['Total Liabilities'] / df['Equity']
      calculated_ratios.append('Debt to Equity Ratio')
  else:
      missing_columns.append('Debt to Equity Ratio')

  if 'EBIT' in df.columns and 'Interest Expense' in df.columns:
      df['Interest Coverage Ratio'] = df['EBIT'] / df['Interest Expense']
      calculated_ratios.append('Interest Coverage Ratio')
  else:
      missing_columns.append('Interest Coverage Ratio')

  if 'Operating Cash Flow' in df.columns and 'Current Liabilities' in df.columns:
      df['Operating Cash Flow Ratio'] = df['Operating Cash Flow'] / df['Current Liabilities']
      calculated_ratios.append('Operating Cash Flow Ratio')
  else:
      missing_columns.append('Operating Cash Flow Ratio')

  # Display a message for missing columns
  if missing_columns:
      print("\nThe following ratios could not be calculated due to missing columns:")
      for ratio in missing_columns:
          print(f"- {ratio}")

#SUBPACKAGE: profitability---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions include:
# allow user to upload an excel file and then fstar will conduct profitability ratio analysis 
#***********************************************************************************************************
def profitability():
  import pandas as pd
  import matplotlib.pyplot as plt
  from google.colab import files
  import io

  # Upload Excel file
  print("Please upload the Excel file containing company information:")
  uploaded = files.upload()

  # Load the Excel file into a DataFrame
  for file_name in uploaded.keys():
      df = pd.read_excel(io.BytesIO(uploaded[file_name]))

  # Display the first few rows of the DataFrame to understand the structure
  print("Here are the first few rows of the uploaded data:")
  print(df.head())

  # Prepare a list to store missing columns and calculations
  missing_columns = []
  calculated_ratios = []

  # Conduct profitability analysis by calculating key ratios
  if 'Revenue' in df.columns and 'Cost of Goods Sold' in df.columns:
      df['Gross Profit Margin'] = (df['Revenue'] - df['Cost of Goods Sold']) / df['Revenue']
      calculated_ratios.append('Gross Profit Margin')
  else:
      missing_columns.append('Gross Profit Margin')

  if 'Operating Income' in df.columns and 'Revenue' in df.columns:
      df['Operating Profit Margin'] = df['Operating Income'] / df['Revenue']
      calculated_ratios.append('Operating Profit Margin')
  else:
      missing_columns.append('Operating Profit Margin')

  if 'Net Income' in df.columns and 'Revenue' in df.columns:
      df['Net Profit Margin'] = df['Net Income'] / df['Revenue']
      calculated_ratios.append('Net Profit Margin')
  else:
      missing_columns.append('Net Profit Margin')

  if 'Net Income' in df.columns and 'Total Assets' in df.columns:
      df['Return on Assets (ROA)'] = df['Net Income'] / df['Total Assets']
      calculated_ratios.append('Return on Assets (ROA)')
  else:
      missing_columns.append('Return on Assets (ROA)')

  if 'Net Income' in df.columns and 'Equity' in df.columns:
      df['Return on Equity (ROE)'] = df['Net Income'] / df['Equity']
      calculated_ratios.append('Return on Equity (ROE)')
  else:
      missing_columns.append('Return on Equity (ROE)')

  # Display a message for missing columns
  if missing_columns:
      print("\nThe following ratios could not be calculated due to missing columns:")
      for ratio in missing_columns:
          print(f"- {ratio}")

  # Display the resulting DataFrame with the calculated ratios
  if calculated_ratios:
      print("\nRatios have been calculated. Here is the updated DataFrame with the key ratios:\n")
      print(df[['Company Name'] + calculated_ratios])

      # Plotting the ratios for each company
      for ratio in calculated_ratios:
          plt.figure(figsize=(10, 6))
          plt.bar(df['Company Name'], df[ratio], color='lightgreen')
          plt.title(f'{ratio} Analysis')
          plt.xlabel('Company Name')
          plt.ylabel(ratio)
          plt.grid(True, axis='y', linestyle='--', alpha=0.7)
          plt.show()

  # Print the ratio explanations for the calculated ratios
  if calculated_ratios:
      print("\n### Ratio Explanations ###\n")

  ratios_explanation = {
      "Gross Profit Margin": {
          "Formula": "(Revenue - Cost of Goods Sold) / Revenue",
          "Interpretation": "Measures the percentage of revenue that exceeds the cost of goods sold, indicating how efficiently a company produces and sells its products."
      },
      "Operating Profit Margin": {
          "Formula": "Operating Income / Revenue",
          "Interpretation": "Indicates the percentage of revenue left after deducting operating expenses, showing how well a company manages its core business operations."
      },
      "Net Profit Margin": {
          "Formula": "Net Income / Revenue",
          "Interpretation": "Represents the percentage of revenue that remains as profit after all expenses, taxes, and costs have been deducted. A higher margin indicates better profitability."
      },
      "Return on Assets (ROA)": {
          "Formula": "Net Income / Total Assets",
          "Interpretation": "Measures how efficiently a company uses its assets to generate profit. A higher ROA indicates more efficient asset use."
      },
      "Return on Equity (ROE)": {
          "Formula": "Net Income / Equity",
          "Interpretation": "Assesses the profitability relative to shareholders' equity. A higher ROE indicates better returns on investment for shareholders."
      }
  }

  for ratio in calculated_ratios:
      if ratio in ratios_explanation:
          details = ratios_explanation[ratio]
          print(f"{ratio}:\n  Formula: {details['Formula']}\n  Interpretation: {details['Interpretation']}\n")

  # Optionally, save the DataFrame with the new columns to a new Excel file
  if calculated_ratios:
      output_file = "profitability_analysis.xlsx"
      df.to_excel(output_file, index=False)
      print(f"Profitability analysis has been saved to {output_file}")

      # Allow the user to download the result file
      files.download(output_file)

#SUBPACKAGE: solvency---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions include:
# allow user to upload an excel file and then fstar will conduct solvency ratio analysis 
#***********************************************************************************************************
def solvency():
  import pandas as pd
  import matplotlib.pyplot as plt
  from google.colab import files
  import io
  # Upload Excel file
  print("Please upload the Excel file containing company information:")
  uploaded = files.upload()

  # Load the Excel file into a DataFrame
  for file_name in uploaded.keys():
      df = pd.read_excel(io.BytesIO(uploaded[file_name]))

  # Display the first few rows of the DataFrame to understand the structure
  print("Here are the first few rows of the uploaded data:")
  print(df.head())

  # Prepare a list to store missing columns and calculations
  missing_columns = []
  calculated_ratios = []

  # Conduct solvency analysis by calculating key ratios
  if 'Total Liabilities' in df.columns and 'Total Assets' in df.columns:
      df['Debt to Assets Ratio'] = df['Total Liabilities'] / df['Total Assets']
      calculated_ratios.append('Debt to Assets Ratio')
  else:
      missing_columns.append('Debt to Assets Ratio')

  if 'Total Liabilities' in df.columns and 'Equity' in df.columns:
      df['Debt to Equity Ratio'] = df['Total Liabilities'] / df['Equity']
      calculated_ratios.append('Debt to Equity Ratio')
  else:
      missing_columns.append('Debt to Equity Ratio')

  if 'Equity' in df.columns and 'Total Assets' in df.columns:
      df['Equity Ratio'] = df['Equity'] / df['Total Assets']
      calculated_ratios.append('Equity Ratio')
  else:
      missing_columns.append('Equity Ratio')

  if 'EBIT' in df.columns and 'Interest Expense' in df.columns:
      df['Interest Coverage Ratio'] = df['EBIT'] / df['Interest Expense']
      calculated_ratios.append('Interest Coverage Ratio')
  else:
      missing_columns.append('Interest Coverage Ratio')

  if 'Operating Cash Flow' in df.columns and 'Total Debt Service' in df.columns:
      df['Debt Service Coverage Ratio (DSCR)'] = df['Operating Cash Flow'] / df['Total Debt Service']
      calculated_ratios.append('Debt Service Coverage Ratio (DSCR)')
  else:
      missing_columns.append('Debt Service Coverage Ratio (DSCR)')

  # Display a message for missing columns
  if missing_columns:
      print("\nThe following ratios could not be calculated due to missing columns:")
      for ratio in missing_columns:
          print(f"- {ratio}")

  # Display the resulting DataFrame with the calculated ratios
  if calculated_ratios:
      print("\nRatios have been calculated. Here is the updated DataFrame with the key ratios:\n")
      print(df[['Company Name'] + calculated_ratios])

      # Plotting the ratios for each company
      for ratio in calculated_ratios:
          plt.figure(figsize=(10, 6))
          plt.bar(df['Company Name'], df[ratio], color='lightcoral')
          plt.title(f'{ratio} Analysis')
          plt.xlabel('Company Name')
          plt.ylabel(ratio)
          plt.grid(True, axis='y', linestyle='--', alpha=0.7)
          plt.show()

  # Print the ratio explanations for the calculated ratios
  if calculated_ratios:
      print("\n### Ratio Explanations ###\n")

  ratios_explanation = {
      "Debt to Assets Ratio": {
          "Formula": "Total Liabilities / Total Assets",
          "Interpretation": "Indicates the percentage of a company's assets that are financed by debt. A higher ratio suggests higher financial risk."
      },
      "Debt to Equity Ratio": {
          "Formula": "Total Liabilities / Equity",
          "Interpretation": "Measures the degree to which a company is financing its operations through debt versus wholly-owned funds. A higher ratio indicates higher leverage and potentially higher financial risk."
      },
      "Equity Ratio": {
          "Formula": "Equity / Total Assets",
          "Interpretation": "Shows the proportion of a company’s assets that are financed by shareholders’ equity. A higher ratio indicates more reliance on equity financing."
      },
      "Interest Coverage Ratio": {
          "Formula": "EBIT / Interest Expense",
          "Interpretation": "Indicates how easily a company can pay interest on its outstanding debt. A higher ratio suggests the company is more capable of meeting its interest obligations."
      },
      "Debt Service Coverage Ratio (DSCR)": {
          "Formula": "Operating Cash Flow / Total Debt Service",
          "Interpretation": "Measures the cash flow available to pay current debt obligations. A higher DSCR indicates better ability to service debt."
      }
  }

  for ratio in calculated_ratios:
      if ratio in ratios_explanation:
          details = ratios_explanation[ratio]
          print(f"{ratio}:\n  Formula: {details['Formula']}\n  Interpretation: {details['Interpretation']}\n")

  # Optionally, save the DataFrame with the new columns to a new Excel file
  if calculated_ratios:
      output_file = "solvency_analysis.xlsx"
      df.to_excel(output_file, index=False)
      print(f"Solvency analysis has been saved to {output_file}")

      # Allow the user to download the result file
      files.download(output_file)
