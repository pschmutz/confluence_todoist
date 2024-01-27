Confluence Todoist
==================

A small script to transfer Confluence Tasks to Todoist.

Installation
++++++++++++

It is a regular Python package, so you can install it with pip.
I recommend to use pipx to install it in a virtual environment.

.. code-block:: bash

    pipx install git+https://github.com/pschmutz/confluence_todoist.git


Usage
+++++
You can run the script with the following command:

.. code-block:: bash

    confluence_todoist

In case you have a lot of task it might make sense to limit the age of the tasks you get with

.. code-block:: bash

    confluence_todoist --since yyyy-mm-dd

On the first run the script will ask you for the following information:
 * atlassian_url (e.g. 'https://your-confluence-instance.company.com')
 * atlassian_username (usually your email)
 * atlassian_api_token (see https://id.atlassian.com/manage-profile/security/api-tokens)
 * atlassian_user_id (you can extract this from the URL when you open your profile in Confluence)
 * todoist_api_token (see https://todoist.com/prefs/integrations)

After that, the script will remember when you ran it the last time and only fetch tasks that were created since then.