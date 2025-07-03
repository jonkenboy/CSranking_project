import pandas as pd

   # Load your data and CSRankings affiliations
   df = pd.read_csv('C:\\Users\\jjonk\\output.csv')
   affiliations = pd.read_csv('path_to_csrankings_csv.csv')  # Replace with actual path

   def map_departments(authors):
       depts = set()
       for author in authors.split(', '):
           dept = affiliations[affiliations['name'].str.contains(author.strip(), case=False)]['affiliation'].values
           if len(dept) > 0:
               depts.add(dept[0])
       return ', '.join(depts) if depts else 'Unknown'

   df['departments'] = df['authors'].apply(map_departments)
   df.to_csv('C:\\Users\\jjonk\\output_with_depts.csv', index=False)
   print("Department mapping complete. Check output_with_depts.csv.")