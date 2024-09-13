

import cbr_static
import cbr_web_components

from fastapi                                                            import Request, FastAPI, Response
from fastapi.openapi.docs                                               import get_swagger_ui_html
from starlette.responses                                                import RedirectResponse, FileResponse, HTMLResponse
from starlette.staticfiles                                              import StaticFiles
from cbr_athena.athena__fastapi.FastAPI_Athena                          import FastAPI_Athena
from cbr_shared.aws.s3.server_requests.S3_DB__Server_Requests           import S3_DB__Server_Requests
from cbr_shared.aws.s3.server_requests.S3__Server_Request               import S3__Server_Request
from cbr_website_beta                                                   import global_vars
from cbr_website_beta.cbr__fastapi.routes.CBR__Site_Info__Routes        import CBR__Site_Info__Routes
from cbr_website_beta.cbr__fastapi__markdown.CBR__Fast_API__Markdown    import CBR__Fast_API__Markdown
from cbr_website_beta.cbr__flask.Flask_Site                             import Flask_Site
from cbr_website_beta.config.Server_Config__CBR_Website                 import server_config__cbr_website
from osbot_fast_api.api.Fast_API                                        import Fast_API
from osbot_utils.context_managers.capture_duration                      import print_duration
from osbot_utils.decorators.methods.cache_on_self                       import cache_on_self
from osbot_utils.utils.Files                                            import path_combine
from osbot_utils.utils.Http import current_host_online


class CBR__Fast_API(Fast_API):
    name: str = 'CBR__Fast_API'

    def add_athena(self):
        cbr_athena_app = self.cbr__athena().app()
        self.app().mount("/api", cbr_athena_app)

    def add_cbr_fastapi_markdown(self):
        cbr_fastapi_markdown = self.cbr__fastapi_markdown().app()
        self.app().mount("/markdown", cbr_fastapi_markdown)

    def add_cbr_static_routes(self):
        assets_path = path_combine(cbr_static.path, 'assets')
        self.app().mount("/assets", StaticFiles(directory=assets_path, html=True), name="assets")
        return self

    def add_cbr_static_web_components(self):
        target_folder = cbr_web_components.path
        self.app().mount("/web_components", StaticFiles(directory=target_folder, html=True), name="web_components")
        return self

    def add_flask__cbr_website(self):
        flask_site = self.cbr__flask()
        flask_app  = flask_site.app()
        path       = '/'
        self.add_flask_app(path, flask_app)
        return self

    @cache_on_self
    def cbr__athena(self):
        return FastAPI_Athena().setup()

    @cache_on_self
    def cbr__flask(self):
        return Flask_Site()

    @cache_on_self
    def cbr__fastapi_markdown(self):
        return CBR__Fast_API__Markdown().setup()

    @cache_on_self
    def app(self):
        kwargs = {'docs_url': None }
        return FastAPI(**kwargs)

    def config_http_events(self):
        S3_DB__Server_Requests().setup()  # step up tasks, including creating target bucket if it doesn't exist
        with self.http_events as _:
            _.trace_calls  = server_config__cbr_website.req_traces_enabled()
            _.trace_call_config.trace_capture_start_with = ["cbr"]
            _.background_tasks.append(self.background_task__log_request_data)


    def background_task__log_request_data(self,request: Request, response: Response):
        # todo add check to see if the aws is enabled and if the aws_creds are correctly set
        try:                                                                                        # we need to capture this error since an execption here will bring the server down
            from osbot_fast_api.api.Fast_API__Request_Data import Fast_API__Request_Data
            request_data: Fast_API__Request_Data
            request_data       = request.state.request_data
            server             = 'cbr_fast_api'                             # todo: make this specific
            s3_server_requests = S3__Server_Request(server=server)
            s3_server_requests.create_from_request_data(request_data)
        except Exception as error:                                                                  # todo: find a better way to capture this instead of the console out
            print(f"[ERROR][background_task__log_request_data]: {error}")

    # todo: fix problem with this workflow which is currently pausing execution in lambda (i.e. it needs the next request to be executed)
    # todo: refactor this to separate class that use a class that overloads S3_DB_Base
    # def background_task(self, request: Request, response: Response):
    #     if server_config__cbr_website.aws_disabled():
    #         return
    #     from osbot_fast_api.api.Fast_API__Request_Data     import Fast_API__Request_Data
    #     from cbr_shared.aws.s3.S3_DB_Base                  import S3_DB_Base
    #     request_data : Fast_API__Request_Data = request.state.request_data
    #     request_id  = request_data.request_id
    #     host_name   = request_data.request_host_name
    #
    #     s3_db_base = S3_DB_Base()
    #     with capture_duration() as duration:
    #         s3_key     = f'server-requests/2024-08-30/{host_name}/{request_id}.json'
    #         s3_bucket  = s3_db_base.s3_bucket()
    #         data       = request_data.json()
    #         s3_db_base.s3_save_data(data, s3_key)
    #     message = f"Saved {request.url.path} request data: {s3_bucket}{s3_key} in {duration.seconds} secs"
    #
    #     request_data.add_log_message(message)



    #@cbr_trace_calls(duration_bigger_than=0, include=['osbot_fast_api', 'cbr'])
    def setup(self):
        with print_duration(action_name='setup'):
            self.setup_global_vars              ()
            self.config_http_events             ()
            self.load_secrets_from_s3           ()
            super().setup()
            self.add_athena                     ()
            self.add_cbr_fastapi_markdown       ()
            self.add_cbr_static_routes          ()
            self.add_cbr_static_web_components  ()
            self.add_flask__cbr_website         ()             # this has to be last since it any non-resolved routes will be passed to the flask app
            return self

    def setup_global_vars(self):
        global_vars.fast_api_http_events = self.http_events

    def setup_routes(self):
        self.add_routes(CBR__Site_Info__Routes)
        pass

    def setup_add_root_route(self):
        app = self.app()

        @app.get("/")                                # todo: move this to a separate method
        def read_root():
            return RedirectResponse(url="/web/home")

        @app.get('/favicon.ico')                    # todo: convert the png below to .ico file (also see what are the side effects of returning a png instead of an ico)
        def favicon_ico():
            file_path = path_combine(cbr_static.path, "/assets/cbr/tcb-favicon.png")
            return FileResponse(file_path, media_type="image/png")

        @app.get('/docs', include_in_schema=False)
        async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
            return self.custom_swagger_ui_html(request)

    def load_secrets_from_s3(self):
        with server_config__cbr_website as _:
            server_online = current_host_online()               # can't use _.server_online() due to a circular dependency on cbr_site_info__data
            if _.s3_load_secrets() and  _.aws_enabled() and server_online:          # todo refactor out this load of env vars into separate method/class
                print()
                print("####### Setting up AWS Server Secrets #######")
                print("#######")
                try:
                    import boto3
                    from osbot_utils.utils.Env import load_dotenv
                    from osbot_utils.utils.Files import file_exists
                    from osbot_utils.utils.Files import file_contents
                    session = boto3.Session()
                    s3_client = session.client('s3')
                    s3_bucket = '654654216424--cbr-deploy--eu-west-1'
                    s3_key = 'cbr-custom-websites/dotenv_files/cbr-site-live-qa.env'
                    local_dotenv = '/tmp/cbr-site-live-qa.env'
                    s3_client.download_file(s3_bucket, s3_key, local_dotenv)
                    if file_exists(local_dotenv):
                        load_dotenv(local_dotenv)
                        print("####### OK: Dotenv file loaded from S3")
                    else:
                        print("####### Warning: Dotenv file NOT loaded from S3")
                except Exception as error:
                    print(f"####### Warning: Dotenv file NOT loaded from S3: {error}")
                print("#######")
                print("####### Setting up AWS QA Server #######")
                print()
            # else:
            #     print("data not loaded")
            #     with server_config__cbr_website as _:
            #         load_secrets = _.s3_load_secrets()
            #         aws_enabled  = _.aws_enabled()
            #     print(dict(load_secrets=load_secrets, aws_enabled=aws_enabled, server_online=server_online))

    # todo: refactor to separate class
    def custom_swagger_ui_html(self, request: Request):
        #root       = request.scope.get("root_path")
        app         = self.app()
        title       = 'CBR' + " - Swagger UI"
        openapi_url = '/openapi.json'  # '/api/openapi.json'
        static_url  = '/assets/plugins/swagger'
        favicon     = f"{static_url}/favicon.png"

        return get_swagger_ui_html(openapi_url          = f"{openapi_url}"                     ,
                                   title                = title                                ,
                                   swagger_js_url       = f"{static_url}/swagger-ui-bundle.js" ,
                                   swagger_css_url      = f"{static_url}/swagger-ui.css"       ,
                                   swagger_favicon_url  = favicon                              ,
                                   swagger_ui_parameters = app.swagger_ui_parameters           )

cbr_fast_api = CBR__Fast_API().setup()