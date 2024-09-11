
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def prota():
  print("**********************************************************")
  print("Welcome to use datastar *: professional data analytic package")
  print("**********************************************************")
  print()
  print("Contacts:")
  print()
  print("Dr Anna Sung - email: a.sung@chester.ac.uk")
  print("Prof Kelvin Leong - email: k.leong@chester.ac.uk")
  print("subpackage: tc, functions: tcexp01, tcexp02, tcfb, extract, combine, edit")
  # print()
  # print("porta includes following subpackages")
  # print("tc: text classification")
  # print()
  print("**********************************************************")

#SUBPACKAGE: tc---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions include:
# tcexp01 (allows user to experience zero shot classification)
# tcexp02 (allows user to experience zero shot classification and assign own selected labels)
# tcfb (allows user to upload a csv, specify the column to analyse, provide label set, generate result to csv)
#      (using zero-shot classification, model: facebook/bart-large-mnli)
#
#***********************************************************************************************************
def tcexp01():
  from transformers import pipeline
  from tabulate import tabulate  # Import tabulate library
  
  classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

  # Allow the user to enter the text for classification
  text = input("Enter the text to classify: \n")
  candidate_labels = ["positive", "negative", "neutral"]

  # Perform classification
  output = classifier(text, candidate_labels, multi_label=False)

  # Create a table from the output
  table_data = []
  for label, score in zip(output['labels'], output['scores']):
      table_data.append([label, score])

  # Print the table
  print(tabulate(table_data, headers=["Label", "Score"], tablefmt="grid"))
  print("*Notes: The 'score' in the code represents a numerical value that indicates how confident the classifier is that a given label is the correct classification for the input text. Higher scores suggest a higher level of confidence in the classification choice, while lower scores suggest less confidence.")
  print("for more detail, contacts: Dr Anna Sung / Prof Kelvin Leong")
  
#***********************************************************************************************************
def tcexp02():
  from transformers import pipeline
  from tabulate import tabulate  # Import tabulate library

  # ------- Select label
  input_labels = input("Suggest your label set - using the format: label 1, label 2... label n \n")
  print(f'You suggested the following labels: {input_labels}')

  # ------- Start running and enter text
  classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

  # Allow the user to enter the text for classification
  text = input("Enter the text to classify: \n")
  candidate_labels = input_labels

  # Perform classification
  output = classifier(text, candidate_labels, multi_label=False)

  # Create a table from the output
  table_data = []
  for label, score in zip(output['labels'], output['scores']):
      table_data.append([label, score])

  # Print the table
  print(tabulate(table_data, headers=["Label", "Score"], tablefmt="grid"))
  print(f'You selected the model: facebook/bart-large-mnli')
  print("*Notes: The 'score' in the code represents a numerical value that indicates how confident the classifier is that a given label is the correct classification for the input text. Higher scores suggest a higher level of confidence in the classification choice, while lower scores suggest less confidence.")
  print("for more detail, contacts: Dr Anna Sung / Prof Kelvin Leong")

#***********************************************************************************************************
def tcfb():
  from transformers import pipeline
  from tabulate import tabulate
  import pandas as pd
  from google.colab import files

  # Use Colab file upload to upload the CSV file
  uploaded = files.upload()

  # Check if a file was uploaded
  if len(uploaded) == 0:
     print("No CSV file uploaded. Exiting.")
     exit(0)

  # Assuming you uploaded a single CSV file, get its name
  csv_file_name = list(uploaded.keys())[0]

  # Read the uploaded CSV file
  try:
     df = pd.read_csv(csv_file_name)
  except FileNotFoundError:
     print("File not found. Please provide a valid CSV file.")
     exit(1)

  # Ask the user to input the name of the column to analyze
  column_name = input("Enter the name of the column to analyze: \n")

  # Check if the specified column exists in the DataFrame
  if column_name not in df.columns:
     print(f"Column '{column_name}' not found in the CSV file.")
     exit(1)

  # Ask the user to specify the labels
  input_labels = input('Suggest your label set - using the format "label 1", "label 2", ... "label n": \n')
  print(f'You suggested the following labels: {input_labels}')

  # Initialize the text classifier
  classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

  # Create an empty DataFrame to store the classification results
  output_df = pd.DataFrame(columns=["Content", "Label", "Score"])

  # Iterate through each cell in the specified column
  for index, row in df.iterrows():
     text = row[column_name]
     # Perform classification
     output = classifier(text, input_labels, multi_label=False)
     # Append the classification results to the output DataFrame
     for label, score in zip(output['labels'], output['scores']):
         output_df = output_df.append({"Content": text, "Label": label, "Score": score}, ignore_index=True)

  # Specify the output CSV file path
  output_csv_path = "output_classification.csv"
   
  # Save the output DataFrame to a CSV file
  output_df.to_csv(output_csv_path, index=False)

  # Print the table of classification results
  print(tabulate(output_df, headers=["Content", "Label", "Score"], tablefmt="grid"))
  print(f'Classification results saved to {output_csv_path}')
  print("Notes: The 'Score' represents a numerical value that indicates the confidence of the classification for each label.")
  print("for more detail, contacts: Dr Anna Sung / Prof Kelvin Leong")

#***********************************************************************************************************

def extract():

  import requests
  from lxml import html
  import pandas as pd

  # Ask the user to input the url link, first page and last page to be extracted
  theurlink = input("Paste the URL link of Trustpilot to be extracted: \n")
  thefirstpage = int(input("What is the first page you want to start with? [Hints: enter 0 for the first page]: \n"))
  thelastpage = int(input("What is the last page you want to end the extraction? : \n"))
  

  # Define the base URL and XPaths
  base_url = theurlink
  review_xpath_prefix = "//html/body/div[1]/div/div/main/div/div[4]/section/div["
  review_xpath_suffix = "]/article/div/section/div[2]/p[1]"
  title_xpath_suffix = "]/article/div/section/div[2]/a/h2"
  date_xpath_suffix = "]/article/div/section/div[2]/p[2]"
  rating_xpath_suffix = "]/article/div/section/div[1]/div[1]/img"
  # Create lists to store the extracted data
  all_titles = []
  all_dates = []
  all_ratings = []
  all_reviews = []
  all_links = []
  # Iterate through pages from first to last page (you can adjust this as needed)
  for n in range(thefirstpage, thelastpage):
      url = f"{base_url}?page={n}"
      for i in range(1, 26):  # Variable number from 1 to 20
          review_xpath = f"{review_xpath_prefix}{i}{review_xpath_suffix}"
          title_xpath = f"{review_xpath_prefix}{i}{title_xpath_suffix}"
          date_xpath = f"{review_xpath_prefix}{i}{date_xpath_suffix}"
          rating_xpath = f"{review_xpath_prefix}{i}{rating_xpath_suffix}"
          # Send a GET request to the URL
          response = requests.get(url)
          if response.status_code == 200:
              # Parse the HTML content
              tree = html.fromstring(response.content)
              # Extract the review, title, and date using the provided XPaths
              review_elements = tree.xpath(review_xpath)
              title_elements = tree.xpath(title_xpath)
              date_elements = tree.xpath(date_xpath)
              rating_elements = tree.xpath(rating_xpath)
              # Check if the elements exist before extracting data
              if title_elements:
                  titles = [title_element.text_content() for title_element in title_elements]
              else:
                  titles = ["*** EMPTY ***"]
              if date_elements:
                  dates = [date_element.text_content() for date_element in date_elements]
              else:
                  dates = ["*** READ THE REVIEW FIELD ***"]
              if rating_elements:
                  ratings = [rating_element.get('alt') for rating_element in rating_elements]
              else:
                  ratings = ["*** EMPTY ***"]
              if review_elements:
                  reviews = [review_element.text_content() for review_element in review_elements]
              else:
                  reviews = ["*** EMPTY ***"]  # Use None if the element is not found
              links = [base_url]
              
              # Extend the lists with the extracted data
              all_titles.extend(titles)
              all_dates.extend(dates)
              all_ratings.extend(ratings)
              all_reviews.extend(reviews)
              all_links.extend(links)
          else:
              print(f"Failed to retrieve data for part {i}. Status code:", response.status_code)
  # Create a DataFrame to store the data
  data = {
      'Title': all_titles,
      'Date': all_dates,
      'Rating': all_ratings,
      'Review': all_reviews,
      'URL' : all_links,
  }
  df = pd.DataFrame(data)
  csv_filename = f"trustpilot_data_page_ended_{n}.csv"
  # Save the data to a CSV file
  df.to_csv(csv_filename, index=False)
  print("Data extracted and saved")
  
#***********************************************************************************************************
def combine():

  import pandas as pd
  from google.colab import files
  def process_csv_files():
      # Prompt the user to upload CSV files
      uploaded_files = files.upload()
      # Create an empty DataFrame to store the combined data
      combined_df = pd.DataFrame()
      # Iterate through each uploaded file
      for file_name in uploaded_files.keys():
          try:
              # Try reading the CSV file with UTF-8 encoding
              df = pd.read_csv(file_name)
          except UnicodeDecodeError:
              # If there's a decoding error, try reading with 'latin1' encoding
              df = pd.read_csv(file_name, encoding='latin1')
            # Append the DataFrame to the combined DataFrame
          combined_df = combined_df.append(df, ignore_index=True, sort=False)
      # i) Keep only one heading at the first row, remove other headings from other files
      combined_df = combined_df[combined_df['Title'].notnull()]
      # ii) Remove duplicate rows
      combined_df = combined_df.drop_duplicates()
      # Save the edited DataFrame to a new CSV file
      output_file = 'combined_and_deduplicated.csv'
      combined_df.to_csv(output_file, index=False)
      print(f"Processing complete. Combined and deduplicated file saved as: {output_file}")
      # Call the function to process the CSV files
  process_csv_files()
  
#***********************************************************************************************************

def edit():
  import pandas as pd
  from google.colab import files
  # Function to process the CSV file
  def process_csv(df):
      # i) Delete rows with (*** EMPTY ***) under the column "Title"
      df = df[df['Title'] != '*** EMPTY ***']
      # ii) Copy "Review" to "Date" where "Date" is (*** READ THE REVIEW FIELD ***)
      mask = df['Date'] == '*** READ THE REVIEW FIELD ***'
      df.loc[mask, 'Date'] = df.loc[mask, 'Review']
      df.loc[mask, 'Review'] = ''
      # iii) Keep only the 7th character from the left in the "Rating" column
      df['Rating'] = df['Rating'].str[6]
      return df
  # Upload CSV file
  uploaded = files.upload()
  # Check if a file was uploaded
  if uploaded:
      # Assuming only one file is uploaded, get the first file name
      input_file_name = list(uploaded.keys())[0]
      # Read the CSV file into a DataFrame
      df = pd.read_csv(input_file_name)
      # Call the function to process the DataFrame
      df_processed = process_csv(df)
      # Save the edited DataFrame to a new CSV file
      output_file_name = input_file_name.replace('.csv', '-edited.csv')
      df_processed.to_csv(output_file_name, index=False)
      print(f"File '{output_file_name}' has been created with the edited data.")
  else:
      print("No file uploaded.")



#***********************************************************************************************************
