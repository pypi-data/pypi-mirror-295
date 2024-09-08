<style>h2 { text-align: center; }</style>

## Overview

AuthBase is good if you want to ship something quickly to test out a concept
and don't want to spend any time on an authentication system.

It is designed to provide boilerplate FastAPI code for a webapp.

It doesn't use passwords for authentication, instead it relies on users
clicking a link that was sent to their email address. The logic behind this is
that usually there is a reset password option that sends an email anyway, so in
theory it is a system that has the same or a similar level of security.

AuthBase also provides some basic utility functions for emailing the users, and
getting user information from the database.

## Features

 - Email confirmation upon user sign up to verify the user's email address.
 - Sign in link emailed to users upon sign in.
 - Plans for security fingerprint that displays browser, ip address, and where
   possible, approximate location, of the person trying to log in.
 - Plans for an unsubscribe link at the bottom of all emails sent through the
   gateway.

## Setup

    pip install authbase

Then in your FastAPI webapp:

    from fastapi import FastAPI
    from authbase import install_auth_routes

    app = FastAPI()
    install_auth_routes(app)

    # ... the rest of your code goes here ...

Then edit config.py in the root directory of your project to contain:

    # Name of your webapp.
    WEBAPP_NAME='My Example App'

    # Email settings.
    SMTP_HOST='smtp.example.org'
    SMTP_PORT=587
    SMTP_USERNAME='username'
    SMTP_PASSWORDD='password'
    SENDER_ADDRESS='My Example App <no-reply@example.org>'

    # Redirct URL where users are sent after they successfully confirm their email
    # address or sign up.
    REDIRECT_URL='https://example.org/signed-in'

## API

### POST /auth

Signs up a new user or initiates the sign in process.

This endpoint takes a single parameter, **email_address**, which should be the
email address of the user signing up or signing in.

The response is HTML with a message instructing the user to check their email
for a confirmation link or a link to sign in.

This response sets a session_id cookie.

Here's an example JS snippet that you can attach to a form submit event:

    const form = document.getElementById("my-sign-in-form")
    form.addEventListener("submit", event => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        fetch("https://api.example.org/auth", {
            method: "POST",
            body: formData,
            credentials: "include",
        }).then(... handle response ...);
    });


### POST /sign_out

This endpoint takes no parameters and signs out the user associated with the
session_id cookie.

Here's an example JS snippet that makes this request:

    await fetch('https://api.example.org/sign_out', {
        method: 'POST',
        credentials: 'include',
    }); 

### GET /me

Gets information about the currently signed in user.

The request should send the session_id cookie.

The response is A JSON object with two fields, **id**, and **email_address**.

This response returns error 401 UNAUTHENTICATED if the user has not signed in.

Here's an example JS snippet that makes this request:

    fetch('https://api.example.org/me', {
        method: 'GET',
        credentials: 'include',
    }).then(... handle response ...);

### GET /sign_in/{session_secret}

This endpoint is for internal use only.

### get_user(user_id)

This function gets a specific user.

Returns a dictionary containing **id** and **email_address**.

### get_users()

This function gets all users.

Returns a list of dictionaries containing **id** and **email_address**.
