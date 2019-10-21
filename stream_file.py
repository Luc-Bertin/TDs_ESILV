import streamlit as st
import pandas as pd
import github_command as gitcmd
import matplotlib.pyplot as plt
from ENV import dico_mapping

@st.cache
def load_metadata():
	""" I know the code could be enhanced, but it is for the sake of clarity """
	## urls
	url_vehicules2017		 = "https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20180927-111247/vehicules-2017.csv"
	url_usagers2017		  	 = "https://www.data.gouv.fr/fr/datasets/r/07bfe612-0ad9-48ef-92d3-f5466f8465fe"
	url_caracteristiques2017 = "https://www.data.gouv.fr/fr/datasets/r/9a7d408b-dd72-4959-ae7d-c854ec505354"
	
	## Opening
	df_vehicules2017		 = pd.read_csv(url_vehicules2017, sep=',', encoding='utf8') # regardez le séparateur au desus
	df_usagers2017			 = pd.read_csv(url_usagers2017, sep=',', encoding='utf8')
	df_caracteristiques2017	 = pd.read_csv(url_caracteristiques2017, sep=',', encoding='latin-1')

	# Merging
	df_all = df_vehicules2017.merge(df_caracteristiques2017, on=['Num_Acc'], how='inner').merge(df_usagers2017, on=['Num_Acc'], how='inner')
	return df_all

@st.cache
def replacement(df, dicoRemplacement):
	df_new = df.replace(dicoRemplacement)
	return df_new

def init_groupings(df):
	## Select categorical columns as columns having less than 20 different levels
	categorical_columns = df.nunique()[df.nunique() < 20].index
	## Create a selectbox (On the side using .sidebar. ) to suggest to the user the different attributes
	grouping  = st.sidebar.selectbox("Grouper par :", categorical_columns)

	## We can't groupby again with the same column as the chosen one so we drop it from further list option
	## We could also choose not to further groupby : selecting '-' option will be used for that
	remaining_options = ["—"] + list( set(categorical_columns)-set([grouping]) )
	grouping2 = st.sidebar.selectbox("et par :", remaining_options)

	## The final list of keys to groupby is stored in final_group_keys
	final_group_keys = [grouping, grouping2] if grouping2 != '—' else [grouping]
	return final_group_keys

def init_SelectionsLabels(df, grouping_keys):
	""" Let the user choose only some levels for each grouping variable """
	for element in grouping_keys:
		## List all levels one can use from the corresponding grouping variable
		level_options = list(pd.value_counts(df[element]).index)
		## Multiselect user interaction. 
		## globals()[etc.] to store as a global variable the corresponding choice made by the user 
		globals()["SelectedLabelsFor"+element] = st.sidebar.multiselect(label='Choice of levels for '+element, options=level_options)

def displayMe(df, grouping_keys, departement = 750):
	""" 	
	Display, in Paris area, a caracteristic, geographically by keys for a given department
		df : dataframe
		grouping_keys : a list of keys to groupby (defined in multiselects)	"""
	
	## Withdrawing the global variables "'SelectedLabelsFor'+element" from the previous multiselects
	## we could do it another better way imo, but still...
	import sys
	thismodule = sys.modules[__name__]
	
	## for Parisian departement, 
	## take the Selected Labels from the MultiSelect(s) widgets and filter on them.
	df_mini = df[df['dep']==departement]
	for element in grouping_keys:
		st.write(globals()['SelectedLabelsFor'+element])
		df_mini = df_mini[  df_mini[element].isin(getattr(thismodule, 'SelectedLabelsFor'+element)) ]

	## Create a plot to display the Map.
	fig, ax = plt.subplots(figsize=(14,7), nrows=1, ncols=1)
	for dataset_name, dataset in df_mini.groupby(grouping_keys):
		ax.plot(dataset.long, dataset.lat, marker='o', linestyle='', ms=6, label=dataset_name)
		ax.legend()
		## important: to display in the Streamlit app a matplotlib.pyplot figure, 
		## we will create later on a placeholder the_plot_map = st.pyplot(plt)
		## This plot will be filled upon execution of the following line
		the_plot_map.pyplot(plt)

	## Create a plot to display other stuff...
	fig, (ax1,ax2) = plt.subplots(figsize=(14,3), nrows=1, ncols=2)
	df_mini.groupby(grouping_keys).size().unstack().plot(kind='bar', stacked=True, ax=ax1, title="In Paris")	
	df.groupby(grouping_keys).size().unstack().plot(kind='bar', stacked=True, ax=ax2, title="In France")
	the_plot_bar.pyplot(plt) ## important: to display in the Streamlit app


'''
# Parisian accidents...

Below is a display for Paris department of different caracteristics which can be settled by the user.
Feel free to play with it !

**Statistiques gouvernementales 2017**

#### Documentation: https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20180927-112352/description-des-bases-de-donnees-onisr-annees-2005-a-2017.pdf

———

''' 

df_all = load_metadata() 					# load all datasets and merge them
df_all = replacement(df_all, dico_mapping)	# values mapping from an external dictionnary
final_group_keys = init_groupings(df_all)	# propose 1 or 2 grouping to be done
init_SelectionsLabels(df_all, final_group_keys)		# init the corresponding multiselect levels

# A simple button, if True / activated => display the plots 
if st.button('Show Map & other infos'):
	the_plot_map = st.pyplot(plt)
	the_plot_bar = st.pyplot(plt)
	displayMe(df_all, grouping_keys=final_group_keys)

