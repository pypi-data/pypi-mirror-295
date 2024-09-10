import base64
import hashlib
import os
import random
import secrets
import urllib
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO, StringIO
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from typing import Dict, Iterator, List,Union
from urllib.parse import urlparse, parse_qs

import httpx
import pandas as pd
try:
    import pyarrow
except ImportError:
    pyarrow = None


from .schemas import ActivityDetail, ActivitySummary, Metric, PermissionType, Sport, User
from .plotting import PlottingMixin


AUTH_SUCCESSFUL_RESPONSE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Authorization Successful</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tachyons/4.11.1/tachyons.min.css">
</head>
<body class="bg-light-gray vh-100 flex items-center justify-center">
    <article class="mw6 center bg-white br3 pa3 pa4-ns mv3 ba b--black-10">
        <div class="tc">
            <div class="flex justify-center items-center">
                <img src="https://sweatstack.no/images/favicon-white-bg-small.png" alt="Sweat Stack Logo" class="h4 w4 dib pa2 ml2">
                <div class="f1 b black ph3">❤️</div>
                <img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png" alt="Python Logo" class="h4 w4 dib pa2 ml2">
            </div>
            <h1 class="f2 mb2">Sweat Stack Python login successful</h1>
        </div>
        <p class="lh-copy measure center f4 black-70">
            You can now close this window and return to your Python code.
        </p>
    </article>
    <script>
        setTimeout(function() {
            window.close();
        }, 5000);
    </script>
</body>
</html>
"""


SWEAT_STACK_CLIENT_ID = "j0mX9SQQAJXHmf6jUsbX"


if "SWEAT_STACK_URL" not in os.environ:
    os.environ["SWEAT_STACK_URL"] = "https://app.sweatstack.no"


class SweatStack(PlottingMixin):
    def __init__(self):
        self.jwt = os.environ.get("SWEAT_STACK_API_KEY")
        self.root_jwt = self.jwt
    
    def _get_url(self):
        """
        This method enables easy switching between Sweat Stack instances after module import.
        """
        return os.environ.get("SWEAT_STACK_URL")
    
    def login(self):
        class AuthHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                # Override to disable logging
                pass

            def do_GET(self):
                query = urlparse(self.path).query
                params = parse_qs(query)
                
                self.server.code = params.get("code", [None])[0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(AUTH_SUCCESSFUL_RESPONSE.encode())
                self.server.server_close()

        code_verifier = secrets.token_urlsafe(32)
        code_challenge = hashlib.sha256(code_verifier.encode("ascii")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).rstrip(b"=").decode("ascii")

        while True:
            port = random.randint(8000, 9000)
            try:
                server = HTTPServer(("localhost", port), AuthHandler)
                break
            except OSError:
                continue

        redirect_uri = f"http://localhost:{port}"
        params = {
            "client_id": SWEAT_STACK_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "code_challenge": code_challenge,
        }
        base_url = self._get_url()
        path = "/oauth/authorize"
        authorization_url = urllib.parse.urljoin(base_url, path + "?" + urllib.parse.urlencode(params))
        webbrowser.open(authorization_url)

        print(f"Waiting for authorization... (listening on port {port})")
        print(f"If not redirected, open the following URL in your browser: {authorization_url}")
        print("")

        server.timeout = 30
        try:
            server.handle_request()
        except TimeoutError:
            raise Exception("Sweat Stack Python login timed out after 30 seconds. Please try again.")

        if hasattr(server, "code"):
            token_data = {
                "grant_type": "authorization_code",
                "client_id": SWEAT_STACK_CLIENT_ID,
                "code": server.code,
                "code_verifier": code_verifier
            }
            response = httpx.post(
                f"{self._get_url()}/oauth/token",
                data=token_data,
            )
            response.raise_for_status()
            token_response = response.json()

            self.jwt = token_response.get("access_token")
            os.environ["SWEAT_STACK_API_KEY"] = self.jwt  # This env variable is for example used by the JupyterLab extension.
            print(f"Sweat Stack Python login successful.")
        else:
            raise Exception("Sweat Stack Python login failed. Please try again.")
    
    @contextmanager
    def _httpx_client(self):
        headers = {
            "authorization": f"Bearer {self.jwt}"
        }
        with httpx.Client(
            base_url=self._get_url(),
            headers=headers,
            timeout=30,
        ) as client:
            yield client

    def list_users(self, permission_type: Union[PermissionType, str] = None) -> List[User]:
        if permission_type is not None:
            params = {"type": permission_type.value if isinstance(permission_type, PermissionType) else permission_type}
        else:
            params = {}

        with self._httpx_client() as client:
            response = client.get("/api/users/", params=params)
            users = response.json()

        return [User.model_validate(user) for user in users]
    
    def list_accessible_users(self) -> List[User]:
        return self.list_users(permission_type=PermissionType.received)
    
    def whoami(self) -> User:
        with self._httpx_client() as client:
            response = client.get("/api/users/me")
            return User.model_validate(response.json())
    
    def get_delegated_token(self, user: Union[User, str]):
        if isinstance(user, str):
            user_id = user
        else:
            user_id = user.id

        with self._httpx_client() as client:
            response = client.get(
                f"/api/users/{user_id}/delegated-token",
            )
            response.raise_for_status()
            return response.json()["jwt"]
    
    def switch_user(self, user: Union[User, str]):
        self.root_jwt = self.jwt
        self.jwt = self.get_delegated_token(user)
    
    def switch_to_root_user(self):
        """
        Switch back to the root user by setting the JWT to the root JWT.
        """
        self.jwt = self.root_jwt
    
    def _check_timezone_aware(self, date_obj: Union[date, datetime]):
        if not isinstance(date_obj, date) and date_obj.tzinfo is None and date_obj.tzinfo.utcoffset(date_obj) is None:
            return date_obj.replace(tzinfo=timezone.utc)
        else:
            return date_obj

    def _fetch_activities(
            self,
            sport: Union[Sport, str] = None,
            start: Union[date, datetime] = None,
            end: Union[date, datetime] = None,
            limit: int = None,
            as_pydantic: bool = False,
        ) -> Iterator[Union[Dict, ActivitySummary]]:
        activities_count = 0

        params = {}
        if sport is not None:
            if isinstance(sport, Sport):
                sport = sport.value
            params["sport"] = sport

        if start is not None:
            params["start"] = self._check_timezone_aware(start).isoformat()

        if end is not None:
            params["end"] = self._check_timezone_aware(end).isoformat()

        with self._httpx_client() as client:
            step_size = 1000
            offset = 0

            while True:
                params["limit"] = step_size
                params["offset"] = offset
                response = client.get("/api/activities/", params=params)
                activities = response.json()

                for activity in activities:
                    activities_count += 1
                    if limit is not None and activities_count > limit:
                        break
                    yield ActivitySummary.model_validate(activity) if as_pydantic else activity

                if limit is not None and activities_count > limit or len(activities) < step_size:
                    break

                offset += step_size


    def list_activities(self, sport: Union[Sport, str] = None, start: Union[date, datetime] = None, end: Union[date, datetime] = None, limit: int = None, as_dataframe: bool = True) -> Union[Iterator[Dict], pd.DataFrame]:
        if as_dataframe:
            return pd.DataFrame(self._fetch_activities(limit=limit))
        else:
            return self._fetch_activities(
                sport=sport,
                start=start,
                end=end,
                limit=limit,
                as_pydantic=True,
            )
    
    def get_longitudinal_data(
            self,
            sport: Union[Sport, str],
            metrics: List[Union[Metric, str]],
            start: Union[date, datetime] = None,
            end: Union[date, datetime] = None,
        ) -> pd.DataFrame:

        params = {}
        if sport is not None:
            if isinstance(sport, Sport):
                sport = sport.value
            params["sport"] = sport

        if metrics is not None:
            new_metrics = []
            for metric in metrics:
                if isinstance(metric, Metric):
                    new_metrics.append(metric.value)
                else:
                    new_metrics.append(metric)
            params["metrics"] = new_metrics
        
        if start is not None:
            params["start"] = self._check_timezone_aware(start).isoformat()
        else:
            params["start"] = (date.today() - timedelta(days=30)).isoformat()
        
        if end is not None:
            params["end"] = self._check_timezone_aware(end).isoformat()
        

        with self._httpx_client() as client:
            response = client.get(f"/api/activities/timeseries", params=params)
            buffer = BytesIO(response.content)
            data = pd.read_parquet(buffer, engine="pyarrow")
            return data

    def get_activity(self, activity_id: str) -> ActivityDetail:
        with self._httpx_client() as client:
            response = client.get(f"/api/activities/{activity_id}")
            return ActivityDetail(**response.json())

    def get_latest_activity(self) -> ActivityDetail:
        activity = next(self._fetch_activities(limit=1, as_pydantic=True))
        return self.get_activity(activity.id)
    
    def get_activity_data(self, activity_id: str) -> pd.DataFrame:
        with self._httpx_client() as client:
            response = client.get(f"/api/activities/{activity_id}/timeseries")
            data = pd.read_json(StringIO(response.json()), orient="split")
            data.index = pd.to_datetime(data.index)
            return data
        
    def get_latest_activity_data(self) -> pd.DataFrame:
        activity = self.get_latest_activity()
        return self.get_activity_data(activity.id)

    def get_accumulated_work_duration(self, start: date, sport: Union[Sport, str], metric: Union[Metric, str], end: date=None) -> pd.DataFrame:
        if not isinstance(start, date):
            start = date.fromisoformat(start)

        if end is None:
            end = date.today()
        if not isinstance(end, date):
            end = date.fromisoformat(end)

        if not isinstance(metric, Metric):
            metric = Metric(metric)
        if not isinstance(sport, Sport):
            sport = Sport(sport)

        with self._httpx_client() as client:
            response = client.get(
                "/api/activities/accumulated-work-duration",
                params={
                    "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "sport": sport.value,
                    "metric": metric.value,
                }
            )

            awd = pd.read_json(
                StringIO(response.json()),
                orient="split",
                date_unit="s",
                typ="series",
            )
            awd = pd.to_timedelta(awd, unit="seconds")
            awd.name = "duration"
            awd.index.name = metric.value
            return awd

    def get_mean_max(self, start: date, sport: Union[Sport, str], metric: Union[Metric, str], end: date=None) -> pd.DataFrame:
        if not isinstance(start, date):
            start = date.fromisoformat(start)

        if end is None:
            end = date.today()
        if not isinstance(end, date):
            end = date.fromisoformat(end)

        if not isinstance(metric, Metric):
            metric = Metric(metric)
        if not isinstance(sport, Sport):
            sport = Sport(sport)

        with self._httpx_client() as client:
            response = client.get(
                "/api/activities/mean-max",
                params={
                    "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "sport": sport.value,
                    "metric": metric.value,
                }
            )

            mean_max = pd.read_json(
                StringIO(response.json()),
                orient="split",
                date_unit="s",
                typ="series",
            )
            mean_max = pd.to_timedelta(mean_max, unit="seconds")
            mean_max.name = "duration"
            mean_max.index.name = metric.value
            return mean_max
        

_instance = SweatStack()


login = _instance.login
list_users = _instance.list_users
list_accessible_users = _instance.list_accessible_users
switch_user = _instance.switch_user
switch_to_root_user = _instance.switch_to_root_user
whoami = _instance.whoami

list_activities = _instance.list_activities
get_activity = _instance.get_activity
get_latest_activity = _instance.get_latest_activity
get_activity_data = _instance.get_activity_data
get_latest_activity_data = _instance.get_latest_activity_data

get_accumulated_work_duration = _instance.get_accumulated_work_duration
get_mean_max = _instance.get_mean_max
get_longitudinal_data = _instance.get_longitudinal_data
plot_activity_data = _instance.plot_activity_data
plot_latest_activity_data = _instance.plot_latest_activity_data
plot_scatter = _instance.plot_scatter