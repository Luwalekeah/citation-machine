"""
Wieczner, Jen, and Daniel L Cooke. 
“Commanders in Chief: The Women Building America’s Military Machine.” 
Fortune, Fortune, 7 June 2021, 
fortune.com/longform/lockheed-martin-boeing-women-defense-ceos-trump/. 
Highly recommend this place
"""

# import streamlit as st
import pandas as pd
from datetime import date
import streamlit as st

st.divider()
st.write('Contributors')

wastebin_index = 0

if 'rows' not in st.session_state:
    st.session_state['rows'] = 1
    wastebin_index = 1  # Initialize wastebin_index

# Flags to check if "Edited by" and "Translated by" have been shown
edited_by_shown = False
translated_by_shown = False

# Counter to track the number of "Author" contributors
author_count = 0
translator_count = 0
editor_count = 0

# Flag to check if it's the first author
first_translator = True
first_editor = True
first_author = True

# Global dictionary to store additional contributor counts
additional_counts = {}

def increase_rows():
    st.session_state['rows'] += 1
    global wastebin_index  # Declare wastebin_index as global
    wastebin_index += 1  # Increment wastebin_index

def delete_rows(index):
    # Mark the row for deletion by setting a flag in the session state
    st.session_state[f'delete_row_{index}'] = True

def display_input_row(index):
    role, left, middle, right, suffix, trash = st.columns([1, 1, 1, 1, 1, 1])

    # Empty title for the ":wastebasket:" icon
    trash.text("")  # Empty title
    trash.text("")  # Empty title

    # Check if the row should be deleted
    if not st.session_state.get(f'delete_row_{index}', False):
        with role:
            selected_role = st.selectbox(
                "Role",
                ("Author", "Editor", "Translator"),
                placeholder="Author", key=f'role_{index}'
            )

        first_name = st.session_state.get(f'first_{index}', "")
        middle_name = st.session_state.get(f'middle_{index}', "")
        last_name = st.session_state.get(f'last_{index}', "")
        suffix_value = st.session_state.get(f'suffix_{index}', "")

        first_name = left.text_input('First', key=f'first_{index}', value=first_name)
        middle_name = middle.text_input('Middle', key=f'middle_{index}', value=middle_name)
        last_name = right.text_input('Last', key=f'last_{index}', value=last_name)

        suffix_value = suffix.text_input('Suffix', key=f'suffix_{index}', value=suffix_value)

        # Add a delete button with ":wastebasket:" icon
        if trash.button(":wastebasket:", key=f'trash_{index}', on_click=lambda i=index: delete_rows(i)):
            # This is necessary to ensure the button is rendered properly
            pass

        return selected_role, first_name, middle_name, last_name

# Display all rows except those marked for deletion
contributors = [display_input_row(i) for i in range(st.session_state['rows']) if not st.session_state.get(f'delete_row_{i}', False)]

# Concatenate the lists in the desired order
authors = []
editors = []
translators = []

for contributor_role, first_name, middle_name, last_name in contributors:
    if contributor_role == "Author":
        author_count += 1
        if first_author:
            author_format = f"{last_name}, {first_name} {middle_name}"
            first_author = False
        else:
            author_format = f", and {first_name} {middle_name} {last_name}"
        authors.append(author_format)
    elif contributor_role == "Editor" and not edited_by_shown:
        editor_count += 1
        if first_editor:
            editor_format = f"Edited by {first_name} {middle_name} {last_name}"
            first_editor = False
        else:
            editor_format = f" and {first_name} {middle_name} {last_name}"
        editors.append(editor_format)
    elif contributor_role == "Translator" and not translated_by_shown:
        translator_count += 1
        if first_translator:
            translator_format = f"Translated by {first_name} {middle_name} {last_name}"
            first_translator = False
        else:
            translator_format = f" and {first_name} {middle_name} {last_name}"
        translators.append(translator_format)

# Concatenate the lists in the desired order
if author_count > 0:
    authors[-1] += "."  # Add period only to the last "Author" contributor

# Add 'and' between multiple editors and translators
editors_format = " ".join(editors)
translators_format = " ".join(translators)

# Add a comma or period after the last editor based on the presence of translators
if editors_format and not translators_format:
    editors_format += ","
elif translators_format and not editors_format:
    translators_format += ","
else:
    editors_format += "."
    translators_format += ","

# Order the contributors as needed
ordered_contributors = authors + [f'"{article_title}"'] + [editors_format] + [translators_format]

st.button('Add Contributor', on_click=increase_rows)

# Display the ordered contributors
st.write(f"Contributors: {' '.join(ordered_contributors)}")


#-------------

# Adding space between the sections
st.write('\n')
st.divider()

st.write('Online Publication Info')
website_title = st.text_input('Website Title', '')
publisher_sponsor = st.text_input('Publisher/Sponsor', '')
website_URL = st.text_input('URL', '')

# Add a button to include or remove the url from the list

# Dates
published_date = st.date_input("Published Date")

# getting todays date as default
date_accessed = st.date_input("Date Accessed", date.today())

st.write('You accessed this site on: ', date_accessed)

# add another divider
st.divider()

st.expander("")
    

# citation_string = 
# cite = st.text(f'{middle_name} {last_name},{first_name} {name_suffix}."{article_title}"{website_title},{publisher_sponsor},{published_date},{website_URL}.{date_accessed}')



