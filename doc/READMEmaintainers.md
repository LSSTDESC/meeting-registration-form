# For Maintainers
## Overview
The meeting-registration-form repo is an application running on the free platform Heroku which handles/includes web forms, a PostgreSQL database, a Python program, and some ancillary files needed to describe the app to Heroku.

### Web pages
The main one is `index.html`, which is the form people use to register. `success.html` is displayed after a successful registration. `participants.html` describes the table used to display minimal participant information for public viewing: first name, last name and affiliation.

### Python program
`registration_server.py` describes the database structure (a single table named participants), creates the table when invoked with `--create`  (see `app.json` for such an invocation) and defines some other functions not used within the repo.

### Dependencies
Dependencies are described in `Pipfile` in a general way; `Pipfile.lock` contains detailed information about exactly which versions of everything were used.  Under normal circumstances, the ones in the repo can be used as is, with no changes. In the unlikely event you do have to change something, see the section **Updating Dependencies** below.


## Updating the meeting-registration-form Repo

### Use a fork
Since it’s very unlikely you’ll get everything right the first time (or even that you’ll know exactly what you want initially), fork the production repository, e.g. under your personal github space, and work on the fork until everything is ready for production.

In order to be able to test everything thoroughly on your fork, you should set up github.io:
1. If you don't already have it, create a repository in your space named your-github-name.github.io. My github name is JoanneBogart so the full path to mine is `JoanneBogart/JoanneBogart.github.io`. This repo needs a README.md file but nothing else.
2. In the github web interface
* go to your fork of meeting-registration-form
* click **Settings** (along the top)
* click **Pages** (in the list to the left, under **Options**)
* the drop-down menu under **Source** should say **None**. Choose the branch (either master or main) which will be the source. And you’re done.

### First deploy
The old instructions in the README are obsolete.  There have been many
changes to the way Heroku operates since then.  For one, they no longer
provide free access to their database services. As a result, several operations
which used to be handled for you by the README must now be done manually.

The following instructions were last verified to work as of May, 2025.

SLAC has an account managed by Seth Digel.  In order to use it you must
* create a personal Heroku account
* have that account added to the group __desc-meeting__.

For everything that follows, you should log into heroku using your account,
then select __desc-meeting__

Then do the following:

1. __Create your app__
   It can be called something like desc-july2025-collab or
   desc_july2025-collab-dev if this is a development deploy associated
   with your fork.   You do this by clicking the __New__ button.

2. __Connect to GitHub__ by specifying the repo:
   YourGitHubUser/meeting-registration-form for your fork, or
   LSSTDESC/meeting-registration-form for production.  You will
   then be able to deploy or redeploy directly from the repo.

   NOTE: It is also possible to deploy or redeploy using the Heroku CLI (see
   instructions below) but, under normal circumstances, connecting to
   GitHub will be simpler.

3. __Discover SERVER_URL__
   Deploy, then click "view".  You'll get an error,
   but save the URL in the tab or window that pops up because you will
   need it later.

4. __Attach a database__
   Click on "Resources" in the upper menu bar, then on
   "Add-on Services".   Select Heroku Postgres

5. __Create database table__
   Click on the "More" button and select the "Run console" option.
   Your run command should be "bash"
   Then at the prompt type
       python registration_server.py --create

6. __Config variables__
   Go to "Settings" in upper menu bar. Scroll down if
   necessary and click on "Reveal Config Vars".  Make a note of the value
   of DATABASE_URL; you'll need it later.  Also create a variable called
   SECRET_KEY.   The value should be some random string of numbers, letters
   and other URL-friendly characters like underscore (_). Make a note of
   what you used.

### Useful URLs
   * The URL used to display registered participants is just SERVER_URL from
     step 3
   * The URL used to register for the meeting looks like
     https://lsstdesc.github.io/meeting-registration-from/index.html?backend=SERVER_URL&secret=SECRET_KEY_VALUE

     SERVER_URL is the value from step 3
     SECRET_KEY_VALUE is the value you chose for the SECRET_KEY config
     variable in step 5

**NOTE:** For your fork the registration URL will be a little different. `lsstdesc.github.io` will instead be `your-github-user.github.io`.   If your forked repo is not named meeting-registration-form, that part of the URL will also have to change.

### Handling payment
Typically payment is involved for in-person registrants. The Heroku app does not itself process payment, but it must interact to some degree with a system that does.  Since that system is up to the host institution, the form of the interaction varies somewhat.   At the least, when the in-person registrant clicks "register" the pop-up which results should include a link to the payment form.  The link may or may not include arguments (such as participant name, email address, fee,..). That will depend on how the payment form has been implemented.  For examples of how this has been handled, see the file `registration_server.py` and various files in the `templates` folder with "payment" in the filename.  The following commits (among others) have the relevant code enabled:

- [July 2023 Collaboration Meeting](https://github.com/LSSTDESC/meeting-registration-form/tree/3f1f6d49e9d56bbf03dcd20a4b205279b5489208)

- [August 2022 Collaboration Meeting](https://github.com/LSSTDESC/meeting-registration-form/tree/e46a5f4771696a336faf00bc412648f7ad98f438)

### Redeploying from the Heroku web dashboard
One can redeploy the app from the Heroku dashboard if the app is connected to the meeting-registration-form repository on GitHub.  To make that connection, go to the "Deploy" tab for the app instance and select the "GitHub" deployment method.  Once the app is connected to the GitHub repository, you will see options to enable automatic deployment based on pushes to the GitHub repo or to trigger deployments from specific branches.  Note that with the GitHub connection enabled, the Heroku app will appear as an active "Environment" in the GitHub repository, so you may wish to disconnect that app from the GitHub repository after the meeting is over.


### Redeploy Using Heroku CLI
1. Install the Heroku CLI.   There are various ways to do this.  For my (mac) laptop I downloaded the tarball, unpacked, and set my path to include the bin directory so that the heroku command could be found.

2. Do
    `$ heroku login`
This will open a browser window so you can log in to your Heroku account.  You may be asked to set up 2-factor authentication.

3. There are many useful commands.  See the [doc](https://devcenter.heroku.com/articles/heroku-cli-commands)

For example, list all your apps with
  `$ heroku apps`

To find out more about a particular app called “my-app-name”
  `$ heroku apps:info -a my-app-name`

4. If there isn’t already a copy of the git repo on the machine where the CLI is installed, clone one.

5. From within your clone, do
  `$ heroku git:remote -a my-app-name`
Your repo now has a new remote named heroku.

6. To redeploy at any time, just do
`$ git push heroku master`
(or push main if that is the production branch of the repo.) You can only push _to_ master or (main), but the source can be a different branch. For example, if you want to push a development branch, say my-dev-branch, for testing, do
`$ git push heroku my-dev-branch:master`

Note that redeploying will not change SERVER_URL, SECRET_KEY, or DATABASE_URL. It also will not touch the database. If the database structure has changed either
* do not redeploy; instead delete the app and start over. This is fine if you’re not yet in production.
* fix the database by hand somehow. There are various Heroku commands starting with the string `heroku pg:` which might be useful. For example you can create backups, restore them, and open a psql session.


## Querying the database
Connect to the database using DATABASE_URL.   It’s in this format:

    `postgres://user:password@host:port/dbname`

If you use sqlalchemy to connect, depending on version you might need to change the initial `postgres` to `postgresql`.   Then make a file, e.g. `database.ini`, consisting just of that string. Change protection on the file so only you can read it. See the Jupyter notebook DatabaseQueries in this repo for an example.

Alternatively, you can put the database access credentials in a `.pgpass` file in your home directory with the following format
```
hostname:port:database:username:password
```
Set the permissions of the `.pgpass` file with `chmod 600 ~/.pgpass`, and you can then use client programs such as `pgsql` or `pgcli` to access the tables.

