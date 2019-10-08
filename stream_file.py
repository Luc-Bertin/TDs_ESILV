import streamlit as st
import pandas as pd
import github_command as gitcmd
import matplotlib.pyplot as plt
from ENV import dico_mapping

@st.cache
def load_metadata():
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

def toList(x):
	if isinstance(x, str):
		return [x]
	elif isinstance(x, list):
		return x
	else:
		raise('Error : ' + str(x) + ' should be a string or a list')

def init_groupings(df):
	categorical_columns = df.nunique()[df.nunique() < 20].index
	grouping  = st.selectbox("Grouper par :", categorical_columns)
	options_restantes = ["—"] + list(set(categorical_columns)-set([grouping]))
	grouping2 = st.selectbox("et par :", options_restantes)
	final_group_keys = [grouping, grouping2] if grouping2 != '—' else grouping
	return final_group_keys

def init_slider(df, grouping_keys):
	for element in toList(grouping_keys):
		options = list(pd.value_counts(df[element]).index)
		globals()["slider_Of_"+element] = st.multiselect(label='choix '+element, options=options)

def affichage(df, grouping_keys, departement = 750):
	"""
	Une petite définition de ce que fait la fonction (docstring) pour qui veut l'utiliser...
	Display a caracteristic geographically by keys for given department
		df : dataframe
		grouping_keys : a list of keys to groupby		
	"""
	import sys
	thismodule = sys.modules[__name__]
	
	df_mini = df[df['dep']==departement]
	for element in toList(grouping_keys):
		st.write(globals()['slider_Of_'+element])
		df_mini = df_mini[  df_mini[element].isin(getattr(thismodule, 'slider_Of_'+element)) ]

	fig, ax = plt.subplots(figsize=(12,7), nrows=1, ncols=1)
	for dataset_name, dataset in df_mini.groupby(grouping_keys):
		ax.plot(dataset.long, dataset.lat, marker='o', linestyle='', ms=6, label=dataset_name)
		ax.legend()
		the_plot.pyplot(plt)

st.title("Accidents Parisiens...")
st.write("""Below is a display for Paris department of
 different caracteristics which can be settled by the user.
 Feel free to play with it !""")
st.write("**Statistiques gouvernementales 2017**", "Lien de la documentation: https://static.data.gouv.fr/resources/base-de-donnees-accidents-corporels-de-la-circulation/20180927-112352/description-des-bases-de-donnees-onisr-annees-2005-a-2017.pdf")
df_all = load_metadata()
df_all = replacement(df_all, dico_mapping)

final_group_keys = init_groupings(df_all)
init_slider(df_all, final_group_keys)

if st.button('Show Map'):
	the_plot = st.pyplot(plt)
	affichage(df_all, grouping_keys=final_group_keys)


