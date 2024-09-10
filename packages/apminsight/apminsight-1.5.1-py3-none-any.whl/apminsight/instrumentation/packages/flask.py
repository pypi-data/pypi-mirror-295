import asyncio
from apminsight import constants
from apminsight.instrumentation.wrapper import wsgi_wrapper, handle_dt_headers, async_default_wrapper, default_wrapper
from apminsight.context import get_cur_txn, is_no_active_txn
from apminsight.logger import agentlogger


def wrap_wsgi_app(original, module, method_info):
    def wrapper(*args, **kwargs):
        if is_no_active_txn():
            return original(*args, **kwargs)
        try:
            if args:
                request = args[0].request_context(args[1]).request
                s247_license_key_from_req = request.headers.get(constants.LICENSE_KEY_FOR_DT_REQUEST)
                handle_dt_headers(s247_license_key_from_req)
        except:
            agentlogger.exception("while extracting request headers for distributed trace")

        return original(*args, **kwargs)

    # special handling for flask route decorator
    wrapper.__name__ = original.__name__
    return wrapper


def wrap_finalize_request(original, module, method_info):
    def wrapper(*args, **kwargs):
        if is_no_active_txn() or not get_cur_txn().get_dt_response_headers():
            return original(*args, **kwargs)
        cur_txn = get_cur_txn()
        res = None
        try:
            res = original(*args, **kwargs)
        except Exception as exc:
            raise exc
        if res is not None:
            try:
                res.headers[constants.DTDATA] = cur_txn.get_dt_response_headers()
            except:
                agentlogger.exception("while adding response headers for distributed trace")
        return res

    # special handling for flask route decorator
    wrapper.__name__ = original.__name__
    return wrapper


def get_status_code(original, module, method_info):
    def wrapper(*args, **kwargs):
        if is_no_active_txn():
            return original(*args, **kwargs)
        try:
            res = original(*args, **kwargs)
        except Exception as exc:
            raise exc
        try:
            cur_txn = get_cur_txn()
            from werkzeug.exceptions import HTTPException

            if isinstance(res, HTTPException):
                cur_txn.set_status_code(int(res.code))
        except:
            agentlogger.exception("Exception occured while getting Status Code")
        return res

    return wrapper

view_function_mapping = {}


def view_function_wrapper(original, module, method_info):

    def bind_params(instance, rule, endpoint=None, view_func=None, **options):
        return instance, rule, endpoint, view_func, options

    def wrapper(*args, **kwargs):
        try:
            global view_function_mapping
            instance, rule, endpoint, view_func, options = bind_params(*args, **kwargs)
            view_wrapper = view_function_mapping.get(view_func, None)
            module_name = view_func.__module__
            args_method_info = {"method": view_func.__name__}
            if view_wrapper is None:
                view_wrapper = (
                    async_default_wrapper(view_func, module_name, args_method_info)
                    if asyncio.iscoroutinefunction(view_func)
                    else default_wrapper(view_func, module_name, args_method_info)
                )
                view_function_mapping[view_func] = view_wrapper

            try:
                for att in view_func.__dict__:
                    setattr(view_wrapper, att, getattr(view_func, att))

            except Exception:
                agentlogger.exception("copying attribute")
        except Exception as exc:
            agentlogger.info("Exception while wrapping flask routes")
            return original(*args, **kwargs)
        return original(instance, rule, endpoint, view_wrapper, **options)


    return wrapper

module_info = {
    "flask": [
        {
            constants.class_str: "Flask",
            constants.method_str: "__call__",
            constants.wrapper_str: wsgi_wrapper,
            constants.component_str: constants.flask_comp,
        },
        {
            constants.class_str: "Flask",
            constants.method_str: "add_url_rule",
            constants.component_str: constants.flask_comp,
            constants.wrapper_str: view_function_wrapper,
        },
        {
            constants.class_str: "Flask",
            constants.method_str: "handle_user_exception",
            constants.wrapper_str: get_status_code,
            constants.component_str: constants.flask_comp,
        },
        {
            constants.class_str: "Flask",
            constants.method_str: "wsgi_app",
            constants.wrapper_str: wrap_wsgi_app,
            constants.component_str: constants.flask_comp,
        },
        {
            constants.class_str: "Flask",
            constants.method_str: "finalize_request",
            constants.wrapper_str: wrap_finalize_request,
            constants.component_str: constants.flask_comp,
        },
    ]
}
