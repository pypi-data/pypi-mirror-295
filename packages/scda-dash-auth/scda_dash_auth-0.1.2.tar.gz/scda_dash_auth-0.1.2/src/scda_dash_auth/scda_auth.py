import logging
import os
import re
from typing import Optional, Tuple, Union
from urllib.parse import urlencode, urljoin

import dash
import dash_auth
import dash_auth.auth
import requests
from flask import Response, redirect, request, session


class SCDAAuth(dash_auth.auth.Auth):
    """Implements auth via SCDA/QDT OpenID."""

    def __init__(
        self,
        app: dash.Dash,
        secret_key: str,
        auth_url: str,
        login_route: str = "/login",
        logout_route: str = "/logout",
        callback_route: str = "/callback",
        log_signin: bool = False,
        public_routes: Optional[list] = None,
        logout_page: Union[str, Response] = None,
        secure_session: bool = False,
    ):
        """
        Secure a Dash app through SCDA/QDT Auth service.

        Parameters
        ----------
        app : dash.Dash
            Dash app to secure
        secret_key : str
            Secret key used to sign the session for the app
        auth_url : str
            URL to the SCDA/QDT Auth service
        login_route : str, optional
            Route to login, by default "/login"
        logout_route : str, optional
            Route to logout, by default "/logout"
        callback_route : str, optional
            Route to callback for the current service. By default "/callback"
        log_signin : bool, optional
            Log sign-ins, by default False
        public_routes : Optional[list], optional
            List of public routes, by default None
        logout_page : Union[str, Response], optional
            Page to redirect to after logout, by default None
        secure_session : bool, optional
            Whether to ensure the session is secure, setting the flasck config
            SESSION_COOKIE_SECURE and SESSION_COOKIE_HTTPONLY to True,
            by default False

        """
        super().__init__(app, public_routes = public_routes)

        self.auth_url = auth_url
        self.login_route = login_route
        self.logout_route = logout_route
        self.callback_route = callback_route
        self.log_signin = log_signin
        self.logout_page = logout_page

        if secret_key is not None:
            app.server.secret_key = secret_key

        if app.server.secret_key is None:
            raise RuntimeError(
                """
                app.server.secret_key is missing.
                Generate a secret key in your Python session
                with the following commands:
                >>> import os
                >>> import base64
                >>> base64.b64encode(os.urandom(30)).decode('utf-8')
                and assign it to the property app.server.secret_key
                (where app is your dash app instance), or pass is as
                the secret_key argument to SCDAAuth.__init__.
                Note that you should not do this dynamically:
                you should create a key and then assign the value of
                that key in your code/via a secret.
                """
            )
        if secure_session:
            app.server.config["SESSION_COOKIE_SECURE"] = True
            app.server.config["SESSION_COOKIE_HTTPONLY"] = True

        app.server.add_url_rule(
            login_route,
            endpoint = "scda_login",
            view_func = self.login_request,
            methods = ["GET"],
        )
        app.server.add_url_rule(
            logout_route,
            endpoint = "scda_logout",
            view_func = self.logout,
            methods = ["GET"],
        )
        app.server.add_url_rule(
            callback_route,
            endpoint = "callback",
            view_func = self.callback,
            methods = ["GET"],
        )

    def is_authorized(self) -> bool:
        authorized = False

        if "user" in session:
            authorized = True
            return authorized

        access_token_cookie = request.cookies.get("access_token", None)
        access_token_header = request.headers.get("Authorization", None)

        if not access_token_cookie:
            if not access_token_header:
                return authorized
            else:
                access_token = re.sub("Bearer ", "", access_token_header)
        else:
            access_token = access_token_cookie

        try:
            authorized, token_payload = self.verify_token(access_token)
        except Exception as e:
            logging.exception(f"Error verifying token: {e}")
            return False

        if authorized:
            try:
                session["user"] = token_payload["user_info"]
            except RuntimeError:
                logging.warning("Session is unavailable. Cannot store user info.")

        return authorized

    def verify_token(self, token: str) -> Tuple[bool, dict]:
        try:
            response = requests.post(
                self.auth_url + "/verify_token",
                json = {
                    "access_token": token,
                    "token_type": "bearer",
                }
            )
            response.raise_for_status()
            is_verified = response.json()["is_verified"]
            return is_verified, response.json()["token_payload"]
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error verifying token: {e}")
            return False, None

    def login_request(self):
        next_url = request.base_url
        auth_url_with_next = urljoin(self.auth_url, '/login')
        query_params = urlencode({'next': next_url})
        full_url = f"{auth_url_with_next}?{query_params}"
        return redirect(full_url)

    def logout(self):
        session.clear()
        base_url = self.app.config.get("url_base_pathname") or "/"
        page = self.logout_page or f"""
        <div style="display: flex; flex-direction: column;
        gap: 0.75rem; padding: 3rem 5rem;">
            <div>Logged out successfully</div>
            <div><a href="{base_url}">Go back</a></div>
        </div>
        """
        return page

    def callback(self):
        token = request.args.get("token")
        next_url = request.args.get("next", self.app.config["routes_pathname_prefix"])

        if token:
            response = redirect(next_url)
            response.set_cookie("access_token", token, httponly = True)
            return response

        return redirect(self.login_request())
