from importlib import import_module

from django.conf import settings

from allianceauth.services.hooks import get_extension_logger
from allianceauth.hooks import get_hooks

from .utils import AppImport

logger = get_extension_logger(__name__)

_supported_apps = {}

_duplicated_apps = set()

_imported = False


def import_apps():
    global _imported
    if not _imported:
        # hooks
        charlink_hooks = get_hooks('charlink')

        for hook_f in charlink_hooks:
            hook_mod = hook_f()
            try:
                assert isinstance(hook_mod, str)
                app_import: AppImport = import_module(hook_mod).app_import
                assert type(app_import) == AppImport
                app_import.validate_import()
            except AssertionError:
                logger.debug(f"Loading of {hook_mod} link via hook: failed to validate")
            except ModuleNotFoundError:
                logger.debug(f"Loading of {hook_mod} link via hook: failed to import")
            except:
                logger.debug(f"Loading of {hook_mod} link via hook: failed")
            else:
                if app_import.app_label in _supported_apps:
                    _supported_apps.pop(app_import.app_label)
                    _duplicated_apps.add(app_import.app_label)

                if app_import.app_label in _duplicated_apps:
                    logger.debug(f"Loading of {hook_mod} link via hook: failed, duplicate {app_import.app_label}")
                else:
                    _supported_apps[app_import.app_label] = app_import
                    logger.debug(f"Loading of {hook_mod} link via hook: success")

        # defaults
        for app in settings.INSTALLED_APPS:
            if app != 'allianceauth' and app not in _supported_apps:
                try:
                    module = import_module(f'charlink.imports.{app}')
                except ModuleNotFoundError:
                    logger.debug(f"Loading of {app} link: failed")
                else:
                    _supported_apps[app] = module.app_import
                    logger.debug(f"Loading of {app} link: success")

        _imported = True

    return _supported_apps


def get_duplicated_apps():
    if not _imported:
        import_apps()

    return _duplicated_apps
