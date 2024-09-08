from mistletoe import markdown as render_markdown
from typing import Optional, Union
from starlette.status import HTTP_302_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from base64 import b64encode
from textwrap import dedent
from fastapi import FastAPI, Form, UploadFile, File, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from re import match, sub
from sqlite3 import connect
from secrets import randbits
from smtp_emailer import send
from urllib.parse import unquote
from email.mime.application import MIMEApplication
try:
    from config import (
        WEBAPP_NAME,
        SMTP_HOST,
        SMTP_PORT,
        SMTP_USERNAME,
        SMTP_PASSWORD,
        SENDER_ADDRESS,
        REDIRECT_URL,
    )
except:
    print("Error: invalid or missing config.py")
    exit(1)


EMAIL_REGEX = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"

Object = type('', (), {})
app = FastAPI()

def normalize_webapp_name(name):
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Convert to lowercase
    name = name.lower()
    # Remove non-alphanumeric characters except underscores
    name = sub(r'[^a-z0-9_]', '', name)
    return name

def get_db_name():
    return normalize_webapp_name(WEBAPP_NAME) + ".db"

def send_email(recipient, subject, html, attachments=[]):
    mail_attachments = []
    if attachments:
        for attachment in attachments:
            if attachment.size > 0:
                mail_attachment = MIMEApplication(
                    attachment.file.read(),
                    name=attachment.filename,
                )
                mail_attachment['Content-Disposition'] = 'attachment; filename="%s"' % attachment.filename
                mail_attachments.append(mail_attachment)
    send(SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_ADDRESS, recipient, subject, html, mail_attachments)

def email_user(
    user_id: str,
    subject: str,
    html: str,
    # Weird typing here from https://github.com/fastapi/fastapi/discussions/10280
    attachments: list[UploadFile],
):
    connection, cursor = db()
    try:
        (user_email_address,) = cursor.execute("SELECT users.email_address FROM users WHERE id = ? AND users.confirmed = TRUE", (user_id,)).fetchone()
    except:
        connection.close()
        return None
    send_email(user_email_address, subject, html, attachments)
    return True

def db():
    connection = connect(get_db_name())
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id VARCHAR PRIMARY KEY, email_address VARCHAR, confirmed BOOLEAN)")
    cursor.execute("CREATE TABLE IF NOT EXISTS sessions (id VARCHAR PRIMARY KEY, user_id VARCHAR, secret VARCHAR, confirmed BOOLEAN)")
    connection.commit()
    return connection, cursor

def random_128_bit_string():
    number = randbits(128)
    binary_data = number.to_bytes(16, 'big')
    base64_encoded = b64encode(binary_data)
    return base64_encoded.decode('utf-8').replace("==","").replace("/","A").replace("+", "B")

def get_session(cursor, session_id):
    try:
        (secret, confirmed) = cursor.execute("SELECT secret, confirmed FROM sessions WHERE id = ?", (session_id,)).fetchone()
        session = Object()
        session.id = session_id
        session.secret = secret
        session.confirmed = confirmed
        return session
    except:
        return None

def send_sign_in_email(host, secret, email_address):
    # Put together the sign-in HTML
    sign_in_url = f"https://{host}/sign_in/{secret}"
    html = render_markdown(dedent(f"""
        Hi,

        To complete the sign in process and start using {WEBAPP_NAME}, please
        click the link below:

        <a clicktracking="off" href="SIGN_IN_URL">SIGN_IN_URL</a>

        If you didn't sign in to {WEBAPP_NAME}, please ignore this email.

        Thank you!<br>
        &mdash; The {WEBAPP_NAME} Team
    """))
    html = html.replace("SIGN_IN_URL", sign_in_url)
 
    # Set the subject.
    subject = f"{WEBAPP_NAME}: Sign in link."

    # Send it all
    send_email(email_address, subject, html)

    response_html = render_markdown(dedent(f"""
        ## Check your email.

        A sign-in link has been sent to EMAIL_ADDRESS.

        Please check your email and click on the link to sign in.

        If you don't see the email within a few minutes, please check your spam or junk folder.
    """))

    response_html = response_html.replace("EMAIL_ADDRESS", email_address)

    # Return HTML for the user.
    return response_html

def check_email_html(email_address):
    html = render_markdown(dedent(f"""
        ## Check your email.

        A confirmation link has been sent to EMAIL_ADDRESS.

        Please check your email and click on the link to confirm your details.

        If you don't see the email within a few minutes, please check your spam or junk folder.
    """))

    html = html.replace("EMAIL_ADDRESS", email_address)

    return html

def send_confirmation_email(host, secret, email_address):
    # Put together the confirmation HTML
    confirmation_url = f"https://{host}/sign_in/{secret}"

    html = render_markdown(dedent(f"""
        Hi,

        To complete the sign up process and start using {WEBAPP_NAME},
        please confirm your email address by clicking the link below:

        <a clicktracking="off" href="CONFIRMATION_URL">CONFIRMATION_URL</a>

        If you didn't sign up for {WEBAPP_NAME}, please ignore this email.

        Thank you!<br>
        &mdash; The {WEBAPP_NAME} Team
    """))

    html = html.replace("CONFIRMATION_URL", confirmation_url)
    subject = f"{WEBAPP_NAME}: Please confirm your email address."

    # Send it all
    send_email(email_address, subject, html)

    return check_email_html(email_address)

def get_user(user_id):
    return users(user_id)

def get_users():
    return users()

def users(user_id: Optional[str] = None):
    connection, cursor = db()

    if user_id:
        row = cursor.execute("""
                SELECT users.email_address FROM users
                WHERE  users.id = ? AND users.confirmed = TRUE
            """,
           (user_id,),
        ).fetchone()
        if not row:
            return None
        (email_address,) = row
        return {"id": user_id, "email_address": email_address}
    results = []
    for (id, email_address) in (
        cursor.execute("""
                SELECT users.id, users.email_address FROM users
                WHERE users.confirmed = TRUE
            """),
    ):
        results.append({"id": id, "email_address": email_address})
    connection.close()
    return results

def install_auth_routes(app):
    @app.post("/auth", response_class=HTMLResponse)
    async def auth(request: Request, response: Response, email_address: str = Form()):

        domain = "." + ".".join(request.headers.get("host").split(".")[-2:])

        email_address = email_address.lower()

        if not match(EMAIL_REGEX, email_address):
            return HTMLResponse("Invalid email address.", status_code=HTTP_400_BAD_REQUEST)

        connection, cursor = db()

        # Existing session doesn't exist.
        # First check if the user has already signed up and is confirmed.
        row = cursor.execute("SELECT users.id FROM users WHERE email_address = ? AND confirmed = TRUE", (email_address,)).fetchone()
        if row:
            (user_id,) = row
            # This user has sign up and is confirmed. Need to generate a session then send sign_in email.
            session = Object()
            session.id = f"session_{random_128_bit_string()}"
            session.user_id = user_id
            session.secret = f"session_secret_{random_128_bit_string()}"
            session.confirmed = False
            cursor.execute("INSERT INTO sessions (id, user_id, secret, confirmed) VALUES (?, ?, ?, ?)",
                           (session.id, session.user_id, session.secret, session.confirmed))
            connection.commit()
            connection.close()
            response.set_cookie(
                key=f"session_id",
                value=session.id,
                domain=domain,  # Allows the cookie to be accessible across all subdomains
                httponly=True,  # Prevents JavaScript access to the cookie
                secure=True,  # Ensures the cookie is only sent over HTTPS
                samesite="None",  # Allows the cookie to be sent with cross-origin requests
                path="/",  # Makes the cookie available on all paths
            )
            return send_sign_in_email(request.headers.get("host"), session.secret, email_address)

        # Existing confirmed user does not exist
        # First check if user account exists, but is unconfirmed.
        row = cursor.execute("SELECT users.id FROM users WHERE email_address = ?", (email_address,)).fetchone()
        if row:
            # User account exists, but is unconfirmed.
            # In this case, tell them to check their email again.
            connection.close()
            return check_email_html(email_address)

        # Haven't already signed up. Need to generate user id and session secret.
        user_id = f"user_id_{random_128_bit_string()}"
        session_id = f"session_{random_128_bit_string()}"
        session_secret = f"session_secret_{random_128_bit_string()}"

        # Create the new user in the sign ups table.
        cursor.execute("INSERT INTO users (id, email_address, confirmed) VALUES (?, ?, FALSE)", (user_id, email_address))
        cursor.execute("INSERT INTO sessions (id, user_id, secret, confirmed) VALUES (?, ?, ?, FALSE)", (session_id, user_id, session_secret))
        connection.commit()

        # Close connection and send off an email
        connection.close()

        response.set_cookie(
            key=f"session_id",
            value=session_id,
            domain=domain,  # Allows the cookie to be accessible across all subdomains
            httponly=True,  # Prevents JavaScript access to the cookie
            secure=True,  # Ensures the cookie is only sent over HTTPS
            samesite="None",  # Allows the cookie to be sent with cross-origin requests
            path="/",  # Makes the cookie available on all paths
        )

        return send_confirmation_email(request.headers.get("host"), session_secret, email_address)

    @app.get("/sign_in/{session_secret}", response_class=HTMLResponse)
    async def sign_in(session_secret: str):
        connection, cursor = db()
        try:
            (user_id, session_id) = cursor.execute("""
                    SELECT users.id, sessions.id
                    FROM users, sessions
                    WHERE
                        users.id = sessions.user_id AND
                        sessions.secret = ?
                """, (session_secret,)).fetchone()
        except:
            connection.close()
            return HTMLResponse("Invalid session secret.", status_code=HTTP_400_BAD_REQUEST)
        cursor.execute("UPDATE users SET confirmed = TRUE WHERE id = ?", (user_id,))
        cursor.execute("UPDATE sessions SET confirmed = TRUE WHERE id = ?", (session_id,))
        connection.commit()
        connection.close()
        return RedirectResponse(REDIRECT_URL)

    @app.get("/me")
    async def me(request: Request):
        session_id = request.cookies.get(f"session_id")
        connection, cursor = db()
        try:
            (id, email_address) = cursor.execute("SELECT users.id, users.email_address FROM sessions, users WHERE sessions.confirmed AND sessions.id = ? AND users.id = sessions.user_id", (session_id,)).fetchone()
        except:
            connection.close()
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        connection.close()
        return {"id": id, "email_address": email_address}

    @app.post("/sign_out")
    async def sign_out(request: Request):
        session_id = request.cookies.get(f"session_id")
        connection, cursor = db()
        row = cursor.execute("SELECT 1 FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not row:
            connection.close()
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        connection.commit()
        connection.close()
        return Response()

