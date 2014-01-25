PreHack-How2API
===============

Code for short workshop demonstrating basic API usage

#OAuth2

## Running the demos
### Step 0: Clone me!

Clone this repository to the local machine with `$ git clone https://github.com/cronin101/PreHack-How2API.git`

### Step 1: Requirements

First, we are going to set up a virtual python environment using **virtualenv**. [See how/why to use here](http://www.virtualenv.org/en/latest/virtualenv.html#usage).

`$ virtualenv ENV`
`$ source ENV/bin/activate`


Next, install the required packages for the python OAuth server with `$ pip install -r requirements.txt`.


### Step 2: Getting OAuth tokens

Run `./oauth_server.py` with `$ python ./oauth_server.py`. 

This starts the [Flask](http://flask.pocoo.org/) server, used to interact with OAuth providers, on port 8080.

You can now navigate to [the server's root page](http://127.0.0.1:8080) for further prompts.

Clicking on the OAuth-flow trigger for each provider will prompt you to sign in and give permissions to the Python application.

After permissions are granted, a `$provider_oauth.token` file will be created in the current directory, this can be used for authenticated request later.

### Step 3: Using the OAuth tokens

Once Facebook/GitHub OAuth tokens have been stored in a `.token` file, you can run the corresponding demo.

Eg `$ python ./facebook_demo.py`.

The Python application now has the ability to perform actions on the vendor API as the user that granted permissions without the need to store usernames/passwords. Magic!

To discover the full host of available actions, navigated to the linked API docs—commented within the oauth_server file.
