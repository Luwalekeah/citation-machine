# import streamlit as st
import pandas as pd
from datetime import date
import streamlit as st

PAGE_TITLE = "Luwahs Citation Machine"
PAGE_ICON = "📚"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# App Title and other informaiton
# Create an empty DataFrame for citations if it doesn't exist
if 'citations_df' not in st.session_state:
    st.session_state.citations_df = pd.DataFrame(columns=['Citations Generated'])

# Check if it's the user's first time
if 'first_time' not in st.session_state:
    # Display the welcome message with background color and wrapping
    welcome_message = """
    <div style="background-color: #87CEEB; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: center;">
    Coming soon: A faster way to cite websites and other sources, including books.
    </div>
    """
    st.markdown(welcome_message, unsafe_allow_html=True)

    # Split the layout into columns
    columns = st.columns(5)

    # Add dummy columns if needed (skip if not required)
    for _ in range(3):
        columns[0].text("")  # Add empty content to the first two columns

    # Add a button to close the message in the middle column
    close_button = columns[2].button("Close")

    # Check if the button is clicked
    if close_button:
        # Mark that the user has seen the popup
        st.session_state.first_time = True
        # Close the expander immediately
        st.rerun()

st.markdown("<h1 style='text-align: center;'>MLA9 Citation Machine for Websites</h1>", unsafe_allow_html=True)

# adding some spacing
st.write("\n")
st.write("<p style='text-align:center;'>Provide as much information as you can to ensure a thorough citation.</p>", unsafe_allow_html=True)

# App begins here:
article_title = st.text_input('Article Title', '')

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
        if first_author and not middle_name:
            author_format = f"{last_name}, {first_name}"
            first_author = False
        elif first_author:
            author_format = f"{last_name}, {first_name} {middle_name}"
            first_author = False
        else:
            author_format = f", and {first_name} {middle_name} {last_name}"
        authors.append(author_format)
    elif contributor_role == "Editor" and not edited_by_shown:
        editor_count += 1
        if not first_editor:
            first_editor = False
        elif first_editor:
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

# Concatenate the lists in the desired order
editors_format = " ".join(editors)
translators_format = " ".join(translators)
authors_format = " ".join(authors)

# Add a comma or period after the last editor based on the presence of translators
if not editors_format and not translators_format:
    editors_format = ''
elif not translators_format:
    editors_format += ","
elif not editors_format:
    translators_format += ","
else:
    editors_format += ","
    translators_format += ","

# Order the contributors as needed
ordered_contributors = authors + [f'"{article_title}"'] + [editors_format] + [translators_format]

st.button('Add Contributor', on_click=increase_rows)

# Display the ordered contributors
st.write(f"Contributors: {' '.join(ordered_contributors)}")

# Adding space between the sections
st.write('\n')

# Order the contributors as needed
ordered_contributors = authors + [f'"{article_title}"'] + [editors_format] + [translators_format]

# Online Publication Info
website_title = st.text_input('Website Title', '')
publisher_sponsor = st.text_input('Publisher/Sponsor', '')
website_URL = st.text_input('URL', '')

# Add radio buttons to include or remove the url from the list
include_url = st.radio('Include URL in Contributors', ('Yes', 'No'))

# Dates
published_date = st.date_input("Published Date")

# getting today's date as default
date_accessed = st.date_input("Date Accessed", date.today())

# More Options Expander
with st.expander("More Options"):
    annotation = st.text_area('Add Annotation', '')

if website_title:
    ordered_contributors += [f'{website_title}, ']
    if publisher_sponsor and publisher_sponsor != website_title:
        ordered_contributors += [f'{publisher_sponsor}, ']

if published_date:
    ordered_contributors += [f' {published_date}']

# Check if URL should be included
if include_url == 'Yes':
    ordered_contributors += [f'{website_URL}.']
elif include_url == 'No':
    ordered_contributors += [f'']

# look at dates
if date_accessed:
    ordered_contributors += [f'{date_accessed}.']
    
# Add annotation if it is not empty
if annotation:
    ordered_contributors += [f' {annotation}.']

# st.write(f"Contributors: {' '.join(ordered_contributors)}")

# Create an empty DataFrame
df = pd.DataFrame(columns=['Citations Generated'])


# Button to add final ordered contributor to the DataFrame
if st.button('Cite'):
    # Initialize the DataFrame if it doesn't exist
    if 'citations_df' not in st.session_state:
        st.session_state.citations_df = pd.DataFrame(columns=['Citations Generated'])

    # Append the final ordered contributor to the DataFrame
    new_row = pd.DataFrame({'Citations Generated': [''.join(ordered_contributors)]})
    st.session_state.citations_df = pd.concat([st.session_state.citations_df, new_row], ignore_index=True)
    st.toast('Hooray!', icon='🎉')


    # Display the DataFrame with the "Copy" buttons
    st.table(st.session_state.citations_df)

# Button to clear sources cited
if st.button('Clear Sources Cited'):
    # Clear the DataFrame
    df = pd.DataFrame(columns=['Citations Generated'])

    # Display the message
    st.warning('Nothing cited yet', icon="⚠️")
    
#----------------------------------------------------------------
# ---------------------------------------------------------------

# Add empty space above and below the copyright notice
st.empty()

# Centered copyright notice and link to GitHub
st.markdown("""
    <div style="display: flex; justify-content: center; text-align: center;">
        <p>Copyright © 2024 Luwalekeah. 
        <a href="https://github.com/Luwalekeah" target="_blank">GitHub</a></p>
    </div>
""", unsafe_allow_html=True)

# Add empty space below the copyright notice
st.empty()