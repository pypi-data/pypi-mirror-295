
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def datastar():
#  pip install mlxtend pandas openpyxl
#  pip install pandas scikit-learn openpyxl matplotlib
  print("**********************************************************")
  print("Welcome to use datastar *: a star data analytics solution")
  print("**********************************************************")
  print()
  print("Contacts:")
  print()
  print("Dr Anna Sung - email: a.sung@chester.ac.uk")
  print("Prof Kelvin Leong - email: k.leong@chester.ac.uk")
  print("subpackage: ar01, artext, clusternum, clustertext, dtree")
  # print()
  # print()
  print("**********************************************************")

#SUBPACKAGE: ar01---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: association tree will be created for data input as 0 1 format
#***********************************************************************************************************
def ar01():
  import pandas as pd
  from mlxtend.frequent_patterns import apriori, association_rules
  from google.colab import files

  # Allow the user to upload the file
  uploaded = files.upload()

  # Assume only one file is uploaded, get the file name
  file_name = list(uploaded.keys())[0]

  # Load the dataset from the uploaded file
  df = pd.read_excel(file_name)

  # Display the dataset
  print("Dataset:")
  print(df)

  # Remove 'Transaction' column if it exists
  if 'Transaction' in df.columns:
      df = df.drop(columns=['Transaction'])

  # Prompt the user to input the minimum support value
  while True:
      try:
          min_support = float(input("Please enter the minimum support value (less than 1): "))
          if min_support <= 0 or min_support >= 1:
              raise ValueError("The value must be between 0 and 1 (exclusive).")
          break
      except ValueError as e:
          print(e)

  # Perform Apriori algorithm to find frequent itemsets
  frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

  # Display the frequent itemsets
  print("\nFrequent Itemsets:")
  print(frequent_itemsets)

  # Generate the association rules
  rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

  # Display the association rules
  print("\nAssociation Rules:")
  print(rules)

#SUBPACKAGE: artext---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: association tree will be created for data input as text (e.g. milk, chips, cake)
#***********************************************************************************************************
def artext():
  import pandas as pd
  from mlxtend.frequent_patterns import apriori, association_rules
  from google.colab import files

  # Allow the user to upload the file
  uploaded = files.upload()

  # Assume only one file is uploaded, get the file name
  file_name = list(uploaded.keys())[0]

  # Load the dataset from the uploaded file
  df = pd.read_excel(file_name)

  # Display the dataset
  print("Original Dataset:")
  print(df)

  # Split the items into lists and create a one-hot encoded DataFrame
  df['Items'] = df['Items'].str.split(', ')

  # One-hot encode the items
  df_onehot = df['Items'].str.join('|').str.get_dummies()

  # Display the one-hot encoded DataFrame
  print("\nOne-Hot Encoded Dataset:")
  print(df_onehot)

  # Prompt the user to input the minimum support value
  while True:
      try:
          min_support = float(input("Please enter the minimum support value (less than 1): "))
          if min_support <= 0 or min_support >= 1:
              raise ValueError("The value must be between 0 and 1 (exclusive).")
          break
      except ValueError as e:
          print(e)

  # Perform Apriori algorithm to find frequent itemsets
  frequent_itemsets = apriori(df_onehot, min_support=min_support, use_colnames=True)

  # Display the frequent itemsets
  print("\nFrequent Itemsets:")
  print(frequent_itemsets)

  # Generate the association rules
  rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

  # Display the association rules
  print("\nAssociation Rules:")
  print(rules)

#SUBPACKAGE: clusternum---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct clustering analysis for data input as number type
#***********************************************************************************************************
def clusternum():
  import pandas as pd
  from sklearn.cluster import KMeans
  import matplotlib.pyplot as plt
  from google.colab import files

  # Step 1: Upload the Excel file
  print("Please upload your Excel file:")
  uploaded = files.upload()

  # Step 2: Load the Excel file into a Pandas DataFrame
  df = pd.read_excel(list(uploaded.keys())[0])

  # Display the first few rows of the dataset
  print("\nHere is a preview of your dataset:")
  print(df.head())

  # Step 3: Allow users to choose the number of clusters
  print("\nHow many clusters would you like to create?")
  num_clusters = int(input("> "))  # User input on the next line

  # Step 4: Allow users to select columns for clustering
  print("\nAvailable columns in the dataset:")
  print(df.columns)
  print("\nEnter the column names to use for clustering (separated by commas):")
  columns = input("> ").split(',')  # User input on the next line

  # Step 5: Prepare the selected data for clustering
  X = df[columns]

  # Step 6: Apply KMeans clustering
  kmeans = KMeans(n_clusters=num_clusters)
  kmeans.fit(X)

  # Step 7: Add the cluster labels to the DataFrame
  df['Cluster'] = kmeans.labels_

  # Display the DataFrame with the cluster labels
  print("\nHere is your dataset with the assigned cluster labels:")
  print(df.head())

  # Step 8: Visualize the Clusters (optional: if you selected two numeric columns)
  if len(columns) == 2:
      plt.scatter(df[columns[0]], df[columns[1]], c=df['Cluster'], cmap='viridis')
      plt.xlabel(columns[0])
      plt.ylabel(columns[1])
      plt.title(f'K-Means Clustering with {num_clusters} clusters')
      plt.show()

  # Step 9: Save the DataFrame with the cluster labels into a new Excel file
  output_file = "clustered_data.xlsx"
  df.to_excel(output_file, index=False)

  # Step 10: Allow the user to download the new Excel file
  print(f"\nThe file '{output_file}' has been created and is ready for download.")
  files.download(output_file)

#SUBPACKAGE: clustertext---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct clustering analysis for data input as text type
#***********************************************************************************************************
def clustertext():
  import pandas as pd
  from sklearn.cluster import KMeans
  from sklearn.preprocessing import OneHotEncoder
  import matplotlib.pyplot as plt
  from google.colab import files

  # Step 1: Upload the Excel file
  print("Please upload your Excel file:")
  uploaded = files.upload()

  # Step 2: Load the Excel file into a Pandas DataFrame
  df = pd.read_excel(list(uploaded.keys())[0])

  # Display the first few rows of the dataset
  print("\nHere is a preview of your dataset:")
  print(df.head())

  # Step 3: Allow users to choose the number of clusters
  print("\nHow many clusters would you like to create?")
  num_clusters = int(input("> "))  # User input on the next line

  # Step 4: Allow users to select columns for clustering
  print("\nAvailable columns in the dataset:")
  print(df.columns)
  print("\nEnter the column names to use for clustering (separated by commas):")
  columns = input("> ").split(',')  # User input on the next line

  # Step 5: Prepare the selected data for clustering
  # Apply one-hot encoding to handle categorical text data
  X = df[columns]

  # Identify categorical columns (object dtype usually means text data)
  categorical_cols = X.select_dtypes(include=['object']).columns

  # Use OneHotEncoder to transform categorical columns into numerical format
  encoder = OneHotEncoder(sparse=False, drop='first')
  X_encoded = X.copy()

  if len(categorical_cols) > 0:
      print(f"Categorical columns detected: {list(categorical_cols)}. Applying one-hot encoding...")
      encoded_data = encoder.fit_transform(X[categorical_cols])
      # Create DataFrame with the encoded categorical columns
      encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_cols))
      # Concatenate with the original DataFrame (drop original categorical columns)
      X_encoded = X_encoded.drop(columns=categorical_cols).reset_index(drop=True)
      X_encoded = pd.concat([X_encoded.reset_index(drop=True), encoded_df], axis=1)

  # Step 6: Apply KMeans clustering
  kmeans = KMeans(n_clusters=num_clusters, random_state=0)
  kmeans.fit(X_encoded)

  # Step 7: Add the cluster labels to the DataFrame
  df['Cluster'] = kmeans.labels_

  # Display the DataFrame with the cluster labels
  print("\nHere is your dataset with the assigned cluster labels:")
  print(df.head())

  # Step 8: Visualize the Clusters (optional: if you selected two numeric columns)
  if len(columns) == 2:
      plt.scatter(df[columns[0]], df[columns[1]], c=df['Cluster'], cmap='viridis')
      plt.xlabel(columns[0])
      plt.ylabel(columns[1])
      plt.title(f'K-Means Clustering with {num_clusters} clusters')
      plt.show()

  # Step 9: Save the DataFrame with the cluster labels into a new Excel file
  output_file = "clustered_data.xlsx"
  df.to_excel(output_file, index=False)

  # Step 10: Allow the user to download the new Excel file
  print(f"\nThe file '{output_file}' has been created and is ready for download.")
  files.download(output_file)

#SUBPACKAGE: dtree---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct clustering analysis for data input as text type
#***********************************************************************************************************
def dtree():
  import pandas as pd
  from sklearn.model_selection import train_test_split
  from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
  from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
  from sklearn.preprocessing import LabelEncoder, OneHotEncoder
  import matplotlib.pyplot as plt
  from google.colab import files

  # Upload the Excel file
  uploaded = files.upload()

  # Load the uploaded Excel file into a pandas DataFrame
  file_name = list(uploaded.keys())[0]
  data = pd.read_excel(file_name)

  # Display the first few rows of the dataset
  print("Dataset Preview:")
  print(data.head())

  # Ask user to input feature columns and target column
  print("\nFeature (X) and Target (y) Selection:")
  print("***********************************************************************")
  print("***********************************************************************")
  print("Features (X) are the independent variables used to predict the target.")
  print("Target (y) is the dependent variable that we are trying to predict. It can be continuous or categorical.")
  print("***********************************************************************")
  print("***********************************************************************")

  # Display column names to help user choose
  print("\nAvailable columns in the dataset:")
  print(data.columns)

  # Ask user for input on which columns to use as features (X)
  features = input("\nEnter the column names for features (X) separated by commas: \n").split(',')
  # Strip extra spaces and display the user-selected features
  features = [feature.strip() for feature in features]
  print(f"\nYou selected features: {features}")

  # Ask user to input target column
  target = input("\nEnter the column name for the target (y): \n")
  target = target.strip()  # Strip any extra spaces
  print(f"\nYou selected target: {target}")

  # Split data into features (X) and target (y)
  X = data[features]
  y = data[target]

  # Explanation of test size
  print("\nTest Size Selection:")
  print("The test size is the proportion of the dataset that will be used for testing the model. The rest will be used for training. A typical test size is between 20% and 30% of the data.")

  # Ask user to input the test size
  test_size = float(input("\nEnter the test size as a fraction (e.g., 0.3 for 30% test size): \n"))
  print(f"\nYou selected a test size of: {test_size}")

  # Handle categorical features in X (if any)
  categorical_features = X.select_dtypes(include=['object', 'category']).columns
  if len(categorical_features) > 0:
      X = pd.get_dummies(X, columns=categorical_features)
      print(f"\nCategorical features found and one-hot encoded: {list(categorical_features)}")

  # Detect if the target is categorical or continuous
  if pd.api.types.is_numeric_dtype(y):
      # Continuous target -> Regression
      print("\nThe target is continuous. Performing regression analysis.")
      model = DecisionTreeRegressor(random_state=42)
      is_classification = False
  else:
      # Categorical target -> Classification
      print("\nThe target is categorical. Performing classification analysis.")
      le = LabelEncoder()
      y = le.fit_transform(y)  # Encode target labels as numbers for classification
      model = DecisionTreeClassifier(random_state=42)
      is_classification = True

  # Split the dataset into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

  # Train the model
  model.fit(X_train, y_train)

  # Predict on the test set
  y_pred = model.predict(X_test)

  # Evaluate the model based on the type of task (classification or regression)
  if is_classification:
      accuracy = accuracy_score(y_test, y_pred)
      print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
  else:
      mse = mean_squared_error(y_test, y_pred)
      r2 = r2_score(y_test, y_pred)
      print(f"\nModel Evaluation Metrics:")
      print(f"Mean Squared Error: {mse}")
      print(f"R-squared: {r2}")

  # Plot the Decision Tree
  plt.figure(figsize=(12, 8))
  tree.plot_tree(model, feature_names=X.columns, filled=True)
  plt.show()

  # Provide description of the Decision Tree
  n_nodes = model.tree_.node_count
  max_depth = model.tree_.max_depth
  print(f"\nThe decision tree has {n_nodes} nodes and a maximum depth of {max_depth}.")

  # Short conclusion based on model evaluation
  if is_classification:
      if accuracy > 0.8:
          print("\nConclusion: The model has a high accuracy, indicating that it performs well on this dataset.")
      elif accuracy > 0.6:
          print("\nConclusion: The model has moderate accuracy. It performs decently, but there is room for improvement.")
      else:
          print("\nConclusion: The model has low accuracy, and its predictions may not be reliable. Consider tuning the model or providing more data.")
  else:
      if r2 > 0.8:
          print("\nConclusion: The model explains most of the variance in the data and performs well.")
      elif r2 > 0.6:
          print("\nConclusion: The model explains a decent amount of variance, but there is room for improvement.")
      else:
          print("\nConclusion: The model does not explain much of the variance, and its predictions may not be very accurate. Consider tuning the model or providing more data.")
