"""Provide an apps controller."""
import asyncio
import json
import logging
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.request import urlopen

import base58
import multihash
from aiobotocore.session import get_session
from jinja2 import Environment, PackageLoader, select_autoescape

from hypha import main_version
from hypha.core import Card, UserInfo, ServiceInfo, UserPermission
from hypha.core.store import RedisStore
from hypha.plugin_parser import convert_config_to_card, parse_imjoy_plugin
from hypha.runner.browser import BrowserAppRunner
from hypha.utils import (
    PLUGIN_CONFIG_FIELDS,
    list_objects_async,
    remove_objects_async,
    random_id,
    safe_join,
)

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger("apps")
logger.setLevel(logging.INFO)

multihash.CodecReg.register("base58", base58.b58encode, base58.b58decode)


class ServerAppController:
    """Server App Controller."""

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        store: RedisStore,
        port: int,
        in_docker: bool = False,
        endpoint_url=None,
        access_key_id=None,
        secret_access_key=None,
        region_name=None,
        workspace_bucket="hypha-workspaces",
        workspace_etc_dir="etc",
    ):  # pylint: disable=too-many-arguments
        """Initialize the class."""
        self._sessions = {}
        self.port = int(port)
        self.in_docker = in_docker
        self.endpoint_url = endpoint_url
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name
        self.s3_enabled = endpoint_url is not None
        self.workspace_bucket = workspace_bucket
        self.workspace_etc_dir = workspace_etc_dir
        self.local_base_url = store.local_base_url
        self.public_base_url = store.public_base_url
        self.event_bus = store.get_event_bus()
        self.store = store
        store.register_public_service(self.get_service_api())
        self.jinja_env = Environment(
            loader=PackageLoader("hypha"), autoescape=select_autoescape()
        )
        self.templates_dir = Path(__file__).parent / "templates"
        # start the browser runner
        self._runner = [
            BrowserAppRunner(self.store, in_docker=self.in_docker),
            BrowserAppRunner(self.store, in_docker=self.in_docker),
        ]

        def close(_) -> None:
            asyncio.ensure_future(self.close())

        self.event_bus.on_local("shutdown", close)

    def create_client_async(self):
        """Create client async."""
        assert self.s3_enabled, "S3 is not enabled."
        return get_session().create_client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region_name,
        )

    async def list_saved_workspaces(
        self,
    ):
        """List saved workspaces."""
        async with self.create_client_async() as s3_client:
            items = await list_objects_async(s3_client, self.workspace_bucket, "/")
        return [item["Key"] for item in items]

    async def list_apps(
        self,
        workspace: str = None,
        context: Optional[dict] = None,
    ):
        """List applications in the workspace."""
        if not workspace:
            workspace = context["ws"]

        workspace = await self.store.get_workspace_info(workspace, load=True)
        assert workspace, f"Workspace {workspace} not found."
        return [app_info.model_dump() for app_info in workspace.applications.values()]

    async def save_application(
        self,
        workspace: str,
        app_id: str,
        card: Card,
        source: str,
        entry_point: str,
        attachments: Optional[Dict[str, Any]] = None,
    ):
        """Save an application to the workspace."""
        mhash = app_id
        async with self.create_client_async() as s3_client:
            app_dir = f"{self.workspace_etc_dir}/{workspace}/{mhash}"

            async def save_file(key, content):
                if isinstance(content, str):
                    content = content.encode("utf-8")
                response = await s3_client.put_object(
                    Body=content,
                    Bucket=self.workspace_bucket,
                    Key=key,
                    ContentLength=len(content),
                )

                if (
                    "ResponseMetadata" in response
                    and "HTTPStatusCode" in response["ResponseMetadata"]
                ):
                    response_code = response["ResponseMetadata"]["HTTPStatusCode"]
                    assert (
                        response_code == 200
                    ), f"Failed to save file: {key}, status code: {response_code}"
                assert "ETag" in response

            # Upload the source code
            await save_file(f"{app_dir}/{entry_point}", source)

            if attachments:
                card.attachments = card.attachments or {}
                card.attachments["files"] = card.attachments.get("files", [])
                files = card.attachments["files"]
                for att in attachments:
                    assert (
                        "name" in att and "source" in att
                    ), "Attachment should contain `name` and `source`"
                    if att["source"].startswith("http") and "\n" not in att["source"]:
                        if not att["source"].startswith("https://"):
                            raise Exception(
                                "Only https sources are allowed: " + att["source"]
                            )
                        with urlopen(att["source"]) as stream:
                            output = stream.read()
                        att["source"] = output
                    await save_file(f"{app_dir}/{att['name']}", att["source"])
                    files.append(att["name"])

            content = json.dumps(card.model_dump(), indent=4)
            await save_file(f"{app_dir}/manifest.json", content)
        logger.info("Saved application (%s)to workspace: %s", mhash, workspace)

    async def close(self) -> None:
        """Close the app controller."""
        logger.info("Closing the server app controller...")
        for app in self._sessions.values():
            await self.stop(app["id"])

    def get_service_api(self) -> Dict[str, Any]:
        """Get a list of service api."""
        # TODO: check permission for each function
        controller = {
            "name": "Server Apps",
            "id": "server-apps",
            "type": "server-apps",
            "config": {"visibility": "public", "require_context": True},
            "install": self.install,
            "uninstall": self.uninstall,
            "launch": self.launch,
            "start": self.start,
            "stop": self.stop,
            "list_apps": self.list_apps,
            "list_running": self.list_running,
            "get_log": self.get_log,
        }
        return controller

    # pylint: disable=too-many-statements,too-many-locals
    async def install(
        self,
        source: str = None,
        source_hash: str = None,
        config: Optional[Dict[str, Any]] = None,
        template: Optional[str] = None,
        attachments: List[dict] = None,
        workspace: Optional[str] = None,
        timeout: float = 60,
        force: bool = False,
        context: Optional[dict] = None,
    ) -> str:
        """Save a server app."""
        if template is None:
            if config:
                config["entry_point"] = config.get("entry_point", "index.html")
                template = config.get("type") + "." + config["entry_point"]
            else:
                template = "hypha"
        if not workspace:
            workspace = context["ws"]

        user_info = UserInfo.model_validate(context["user"])
        workspace_info = await self.store.get_workspace_info(workspace, load=True)
        assert workspace_info, f"Workspace {workspace} not found."
        if not user_info.check_permission(
            workspace_info.name, UserPermission.read_write
        ):
            raise Exception(
                f"User {user_info.id} does not have permission"
                f" to install apps in workspace {workspace_info.name}"
            )

        if source.startswith("http"):
            if not source.startswith("https://"):
                raise Exception("Only https sources are allowed: " + source)
            with urlopen(source) as stream:
                output = stream.read()
            source = output.decode("utf-8")
        # Compute multihash of the source code
        mhash = multihash.digest(source.encode("utf-8"), "sha2-256")
        mhash = mhash.encode("base58").decode("ascii")
        # Verify the source code, useful for downloading from the web
        if source_hash is not None:
            target_mhash = multihash.decode(source_hash.encode("ascii"), "base58")
            assert target_mhash.verify(
                source.encode("utf-8")
            ), f"App source code verification failed (source_hash: {source_hash})."
        if template == "hypha":
            if not source:
                raise Exception("Source should be provided for hypha app.")
            assert config is None, "Config should not be provided for hypha app."

            try:
                config = parse_imjoy_plugin(source)
                config["source_hash"] = mhash
                entry_point = config.get("entry_point", "index.html")
                config["entry_point"] = entry_point
                temp = self.jinja_env.get_template(
                    safe_join("apps", config["type"] + "." + entry_point)
                )

                source = temp.render(
                    hypha_main_version=main_version,
                    hypha_rpc_websocket_mjs=self.public_base_url
                    + "/assets/hypha-rpc-websocket.mjs",
                    config={k: config[k] for k in config if k in PLUGIN_CONFIG_FIELDS},
                    script=config["script"],
                    requirements=config["requirements"],
                    local_base_url=self.local_base_url,
                )
            except Exception as err:
                raise Exception(
                    f"Failed to parse or compile the hypha app {mhash}: {source[:100]}...",
                ) from err
        elif template:
            assert (
                "." in template
            ), f"Invalid template name: {template}, should be a file name with extension."
            # extract the last dash separated part as the file name
            temp = self.jinja_env.get_template(safe_join("apps", template))
            default_config = {
                "name": "Untitled App",
                "version": "0.1.0",
                "local_base_url": self.local_base_url,
            }
            default_config.update(config or {})
            config = default_config
            entry_point = config.get("entry_point", template)
            config["entry_point"] = entry_point
            source = temp.render(
                hypha_main_version=main_version,
                hypha_rpc_websocket_mjs=self.public_base_url
                + "//assets/hypha-rpc-websocket.mjs",
                script=source,
                source_hash=mhash,
                config=config,
                requirements=config.get("requirements", []),
            )
        elif not source:
            raise Exception("Source or template should be provided.")

        app_id = f"{mhash}"

        public_url = f"{self.public_base_url}/{workspace_info.name}/server-apps/{app_id}/{entry_point}"
        card_obj = convert_config_to_card(config, app_id, public_url)
        card_obj.update(
            {
                "local_url": f"{self.local_base_url}/{workspace_info.name}/server-apps/{app_id}/{entry_point}",
                "public_url": public_url,
            }
        )
        card = Card.model_validate(card_obj)
        assert card.entry_point, "Entry point not found in the card."
        await self.save_application(
            workspace_info.name, app_id, card, source, card.entry_point, attachments
        )
        async with self.store.get_workspace_interface(
            workspace_info.name, user_info
        ) as ws:
            await ws.install_application(card.model_dump(), force=force)
        try:
            info = await self.start(
                app_id,
                timeout=timeout,
                wait_for_service="default",
                context=context,
            )
            await self.stop(info["id"], context=context)
        except asyncio.TimeoutError:
            logger.error("Failed to start the app: %s during installation", app_id)
            await self.uninstall(app_id, context=context)
            raise TimeoutError(
                "Failed to start the app: %s during installation" % app_id
            )
        except Exception as exp:
            logger.exception("Failed to start the app: %s during installation", app_id)
            await self.uninstall(app_id, context=context)
            raise Exception(
                f"Failed to start the app: {app_id} during installation, error: {exp}"
            )

        return card_obj

    async def uninstall(self, app_id: str, context: Optional[dict] = None) -> None:
        """Uninstall a server app."""
        assert "/" not in app_id, (
            "Invalid app id: " + app_id + ", should not contain '/'"
        )
        workspace_name = context["ws"]
        mhash = app_id
        workspace = await self.store.get_workspace_info(workspace_name, load=True)
        assert workspace, f"Workspace {workspace} not found."
        user_info = UserInfo.model_validate(context["user"])
        if not user_info.check_permission(workspace.name, UserPermission.read_write):
            raise Exception(
                f"User {user_info.id} does not have permission"
                f" to uninstall apps in workspace {workspace.name}"
            )
        async with self.store.get_workspace_interface(workspace.name, user_info) as ws:
            await ws.uninstall_application(app_id)

        async with self.create_client_async() as s3_client:
            app_dir = f"{self.workspace_etc_dir}/{workspace.name}/{mhash}/"
            await remove_objects_async(s3_client, self.workspace_bucket, app_dir)

    async def launch(
        self,
        source: str,
        timeout: float = 60,
        config: Optional[Dict[str, Any]] = None,
        attachments: List[dict] = None,
        wait_for_service: str = None,
        context: Optional[dict] = None,
    ) -> dict:
        """Start a server app instance."""
        workspace = context["ws"]
        app_info = await self.install(
            source,
            attachments=attachments,
            config=config,
            workspace=workspace,
            context=context,
        )
        app_id = app_info["id"]
        return await self.start(
            app_id,
            timeout=timeout,
            wait_for_service=wait_for_service,
            context=context,
        )

    # pylint: disable=too-many-statements,too-many-locals
    async def start(
        self,
        app_id,
        client_id=None,
        timeout: float = 60,
        wait_for_service: Union[str, bool] = None,
        context: Optional[dict] = None,
    ):
        """Start the app and keep it alive."""
        if wait_for_service is True:
            wait_for_service = "default"
        if wait_for_service and ":" in wait_for_service:
            wait_for_service = wait_for_service.split(":")[1]

        workspace = context["ws"]
        user_info = UserInfo.model_validate(context["user"])

        async with self.store.get_workspace_interface(workspace, user_info) as ws:
            token = await ws.generate_token()

        if not user_info.check_permission(workspace, UserPermission.read):
            raise Exception(
                f"User {user_info.id} does not have permission"
                f" to run app {app_id} in workspace {workspace}."
            )

        if client_id is None:
            client_id = random_id(readable=True)

        workspace_info = await self.store.get_workspace_info(workspace, load=True)
        assert workspace, f"Workspace {workspace} not found."
        assert (
            app_id in workspace_info.applications
        ), f"App {app_id} not found in workspace {workspace}, please install it first."
        card = workspace_info.applications[app_id]
        entry_point = card.entry_point
        assert entry_point, f"Entry point not found for app {app_id}."
        server_url = self.local_base_url
        local_url = (
            f"{self.local_base_url}/{workspace}/server-apps/{app_id}/{entry_point}?"
            + f"client_id={client_id}&workspace={workspace}"
            + f"&app_id={app_id}"
            + f"&server_url={server_url}"
            + f"&token={token}"
            if token
            else ""
        )
        server_url = self.public_base_url
        public_url = (
            f"{self.public_base_url}/{workspace}/server-apps/{app_id}/{entry_point}?"
            + f"client_id={client_id}&workspace={workspace}"
            + f"&app_id={app_id}"
            + f"&server_url={server_url}"
            + f"&token={token}"
            if token
            else ""
        )

        runner = random.choice(self._runner)

        full_client_id = workspace + "/" + client_id
        await runner.start(url=local_url, session_id=full_client_id)
        self._sessions[full_client_id] = {
            "id": full_client_id,
            "app_id": app_id,
            "workspace": workspace,
            "local_url": local_url,
            "public_url": public_url,
            "_runner": runner,
        }
        # collecting services registered during the startup of the script
        collected_services: List[ServiceInfo] = []
        app_info = {
            "id": full_client_id,
            "app_id": app_id,
            "workspace": workspace,
            "config": {},
        }

        def service_added(info: dict):
            if info["id"].startswith(full_client_id + ":"):
                collected_services.append(ServiceInfo.model_validate(info))
            if info["id"] == full_client_id + ":default":
                for key in ["config", "name", "description"]:
                    if info.get(key):
                        app_info[key] = info[key]

        self.event_bus.on_local("service_added", service_added)

        try:
            if wait_for_service:
                logger.info(f"Waiting for service: {full_client_id}:{wait_for_service}")
                await self.event_bus.wait_for_local(
                    "service_added",
                    match={"id": full_client_id + ":" + wait_for_service},
                    timeout=timeout,
                )
            else:
                await self.event_bus.wait_for_local(
                    "client_connected", match={"id": full_client_id}, timeout=timeout
                )

            # save the services
            workspace_info.applications[app_id].services = collected_services
            Card.model_validate(workspace_info.applications[app_id])
            await self.store.set_workspace(workspace_info, user_info)
        except asyncio.TimeoutError:
            raise Exception(
                f"Failed to start the app: {workspace}/{app_id}, timeout reached ({timeout}s)."
            )
        except Exception as exp:
            raise Exception(
                f"Failed to start the app: {workspace}/{app_id}, error: {exp}"
            ) from exp
        finally:
            self.event_bus.off_local("service_added", service_added)

        if wait_for_service:
            app_info["service_id"] = (
                full_client_id + ":" + wait_for_service + "@" + app_id
            )
        return app_info

    async def stop(
        self,
        session_id: str,
        raise_exception=True,
        context: Optional[dict] = None,
    ) -> None:
        """Stop a server app instance."""
        if session_id in self._sessions:
            logger.info("Stopping app: %s...", session_id)

            app_info = self._sessions[session_id]
            if session_id in self._sessions:
                del self._sessions[session_id]
            try:
                await app_info["_runner"].stop(session_id)
            except Exception as exp:
                if raise_exception:
                    raise
                else:
                    logger.warning("Failed to stop browser tab: %s", exp)
        elif raise_exception:
            raise Exception(f"Server app instance not found: {session_id}")

    async def get_log(
        self,
        session_id: str,
        type: str = None,  # pylint: disable=redefined-builtin
        offset: int = 0,
        limit: Optional[int] = None,
        context: Optional[dict] = None,
    ) -> Union[Dict[str, List[str]], List[str]]:
        """Get server app instance log."""
        if session_id in self._sessions:
            return await self._sessions[session_id]["_runner"].get_log(
                session_id, type=type, offset=offset, limit=limit
            )
        else:
            raise Exception(f"Server app instance not found: {session_id}")

    async def list_running(self, context: Optional[dict] = None) -> List[str]:
        """List the running sessions for the current workspace."""
        workspace = context["ws"]
        sessions = [
            {k: v for k, v in session_info.items() if not k.startswith("_")}
            for session_id, session_info in self._sessions.items()
            if session_id.startswith(workspace + "/")
        ]
        return sessions
