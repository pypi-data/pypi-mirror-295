"""Module to help with parsing and generating configuration files."""

from __future__ import annotations

import asyncio
from collections import OrderedDict
from collections.abc import Callable, Hashable, Iterable, Sequence
from contextlib import suppress
from dataclasses import dataclass
from enum import StrEnum
from functools import partial, reduce
import logging
import operator
import os
from pathlib import Path
import re
import shutil
from types import ModuleType
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from awesomeversion import AwesomeVersion
import voluptuous as vol
from voluptuous.humanize import MAX_VALIDATION_ERROR_ITEM_LENGTH
from yaml.error import MarkedYAMLError

from . import auth
from .auth import mfa_modules as auth_mfa_modules, providers as auth_providers
from .const import (
    ATTR_ASSUMED_STATE,
    ATTR_FRIENDLY_NAME,
    ATTR_HIDDEN,
    CONF_ALLOWLIST_EXTERNAL_DIRS,
    CONF_ALLOWLIST_EXTERNAL_URLS,
    CONF_AUTH_MFA_MODULES,
    CONF_AUTH_PROVIDERS,
    CONF_COUNTRY,
    CONF_CURRENCY,
    CONF_CUSTOMIZE,
    CONF_CUSTOMIZE_DOMAIN,
    CONF_CUSTOMIZE_GLOB,
    CONF_DEBUG,
    CONF_ELEVATION,
    CONF_EXTERNAL_URL,
    CONF_ID,
    CONF_INTERNAL_URL,
    CONF_LANGUAGE,
    CONF_LATITUDE,
    CONF_LEGACY_TEMPLATES,
    CONF_LONGITUDE,
    CONF_MEDIA_DIRS,
    CONF_NAME,
    CONF_PACKAGES,
    CONF_PLATFORM,
    CONF_RADIUS,
    CONF_TEMPERATURE_UNIT,
    CONF_TIME_ZONE,
    CONF_TYPE,
    CONF_UNIT_SYSTEM,
    LEGACY_CONF_WHITELIST_EXTERNAL_DIRS,
    __version__,
)
from .core import DOMAIN as HOMEASSISTANT_DOMAIN, ConfigSource, HomeAssistant, callback
from .exceptions import ConfigValidationError, HomeAssistantError
from .generated.currencies import HISTORIC_CURRENCIES
from .helpers import config_validation as cv, issue_registry as ir
from .helpers.entity_values import EntityValues
from .helpers.translation import async_get_exception_message
from .helpers.typing import ConfigType
from .loader import ComponentProtocol, Integration, IntegrationNotFound
from .requirements import RequirementsNotFound, async_get_integration_with_requirements
from .util.async_ import create_eager_task
from .util.hass_dict import HassKey
from .util.package import is_docker_env
from .util.unit_system import get_unit_system, validate_unit_system
from .util.yaml import SECRET_YAML, Secrets, YamlTypeError, load_yaml_dict
from .util.yaml.objects import NodeStrClass

_LOGGER = logging.getLogger(__name__)

RE_YAML_ERROR = re.compile(r"homeassistant\.util\.yaml")
RE_ASCII = re.compile(r"\033\[[^m]*m")
YAML_CONFIG_FILE = "configuration.yaml"
VERSION_FILE = ".HA_VERSION"
CONFIG_DIR_NAME = ".homeassistant"
DATA_CUSTOMIZE: HassKey[EntityValues] = HassKey("hass_customize")

AUTOMATION_CONFIG_PATH = "automations.yaml"
SCRIPT_CONFIG_PATH = "scripts.yaml"
SCENE_CONFIG_PATH = "scenes.yaml"

LOAD_EXCEPTIONS = (ImportError, FileNotFoundError)
INTEGRATION_LOAD_EXCEPTIONS = (IntegrationNotFound, RequirementsNotFound)

SAFE_MODE_FILENAME = "safe-mode"

DEFAULT_CONFIG = f"""
# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
    themes:
        Latte Vioneta:
            modes:
                light:
                    # Colors
                    text: "#4c4f69"

                    subtext1: "#5c5f77"
                    subtext0: "#6c6f85"

                    overlay2: "#7c7f93"
                    overlay1: "#8c8fa1"
                    overlay0: "#9ca0b0"

                    surface2: "#acb0be"
                    surface1: "#bcc0cc"
                    surface0: "#ccd0da"

                    base: "#eff1f5"
                    mantle: "#e6e9ef"
                    crust: "#dce0e8"

                    rosewater: "#dc8a78"
                    flamingo: "#dd7878"
                    pink: "#ea76cb"
                    mauve: "#8839ef"
                    red: "#d20f39"
                    maroon: "#e64553"
                    peach: "#fe640b"
                    yellow: "#df8e1d"
                    green: "#40a02b"
                    teal: "#179299"
                    sky: "#04a5e5"
                    sapphire: "#209fb5"
                    blue: "#1e66f5"
                    lavender: "#7287fd"

                    ###########################

                    # Header
                    app-header-background-color: var(--mantle)
                    app-header-text-color: var(--text)

                    # Main Interface colors
                    primary-color: var(--blue)
                    light-primary-color: var(--primary-color)

                    primary-background-color: var(--mantle)
                    secondary-background-color: var(--mantle)
                    accent-color: var(--yellow)

                    # Text
                    primary-text-color: var(--text)
                    secondary-text-color: var(--subtext1)
                    text-primary-color: var(--text)
                    divider-color: var(--base)
                    disabled-text-color: var(--overlay0)
                    text-accent-color: var(--text)

                    # Sidebar
                    sidebar-background-color: var(--crust)
                    sidebar-selected-background-color: var(--primary-background-color)

                    sidebar-icon-color: var(--subtext0)
                    sidebar-text-color: var(--subtext0)
                    sidebar-selected-icon-color: var(--mauve)
                    sidebar-selected-text-color: var(--mauve)

                    # Buttons
                    paper-item-icon-color: var(--subtext0)
                    paper-item-icon-active-color: var(--primary-color)

                    # States and Badges
                    state-icon-color: var(--lavender)
                    state-icon-active-color: var(--primary-color)

                    state-icon-unavailable-color: var(--disabled-text-color)

                    # Sliders
                    paper-slider-knob-color: var(--blue)
                    paper-slider-knob-start-color: var(--paper-slider-knob-color)
                    paper-slider-pin-color: var(--paper-slider-knob-color)
                    paper-slider-active-color: var(--paper-slider-knob-color)
                    paper-slider-secondary-color: var(--blue)

                    # Labels
                    label-badge-background-color: var(--surface0)
                    label-badge-text-color: var(--text)
                    label-badge-red: var(--red)
                    label-badge-green: var(--green)
                    label-badge-blue: var(--blue)
                    label-badge-yellow: var(--yellow)
                    label-badge-gray: var(--overlay0)

                    # Cards
                    card-background-color: var(--base)
                    ha-card-background: var(--card-background-color)

                    ha-card-border-radius: "15px"
                    ha-card-box-shadow: none
                    paper-dialog-background-color: var(--overlay0)
                    paper-listbox-background-color: var(--overlay0)
                    paper-card-background-color: var(--card-background-color)

                    # Switches
                    switch-checked-button-color: var(--green)
                    switch-checked-track-color: var(--surface0)
                    switch-unchecked-button-color: rgb(--overlay0)
                    switch-unchecked-track-color: rgb(--surface0)
                    # Toggles
                    paper-toggle-button-checked-button-color: var(--switch-checked-button-color)
                    paper-toggle-button-checked-bar-color: var(--switch-checked-track-color)
                    paper-toggle-button-unchecked-button-color: var(--switch-unchecked-button-color)
                    paper-toggle-button-unchecked-bar-color: var(--switch-unchecked-track-color)

                    # Table
                    table-row-background-color: var(--primary-background-color)
                    table-row-alternative-background-color: var(--secondary-background-color)
                    data-table-background-color: var(--primary-background-color)
                    mdc-checkbox-unchecked-color: var(--overlay0)

                    # Dropdowns
                    material-background-color: var(--primary-background-color)
                    material-secondary-background-color: var(--primary-background-color)
                    mdc-theme-surface: var(--primary-background-color)

                    # Pre/Code
                    markdown-code-background-color: var(--surface0)

                    # Checkboxes
                    mdc-select-fill-color: var(--surface0)
                    mdc-select-ink-color: var(--primary-text-color)
                    mdc-select-label-ink-color: var(--subtext1)
                    mdc-select-idle-line-color: var(--primary-text-color)
                    mdc-select-dropdown-icon-color: var(--secondary-text-color)
                    mdc-select-hover-line-color: var(--accent-color)

                    # Input
                    input-fill-color: var(--secondary-background-color)
                    input-dropdown-icon-color: var(--secondary-text-color)
                    input-ink-color: var(--primary-text-color)
                    input-label-ink-color: var(--secondary-text-color)
                    input-idle-line-color: var(--primary-text-color)
                    input-hover-line-color: var(--accent-color)
                    input-disabled-ink-color: var(--disabled-text-color)
                    input-disabled-line-color: var(--disabled-text-color)
                    input-outlined-idle-border-color: var(--disabled-text-color)
                    input-outlined-hover-border-color: var(--disabled-text-color)
                    input-outlined-disabled-border-color: var(--disabled-text-color)
                    input-disabled-fill-color: rgba(0, 0, 0, 0)

                    # Toast
                    paper-toast-background-color: var(--overlay0)

                    # Colors
                    error-color: var(--red)
                    warning-color: var(--yellow)
                    success-color: var(--green)
                    info-color: var(--blue)

                    state-on-color: var(--green)
                    state-off-color: var(--red)

              

                dark:
                    # Colors
                    text: "#c6d0f5"
                    subtext1: "#b5bfe2"
                    subtext0: "#a5adce"

                    overlay2: "#949cbb"
                    overlay1: "#838ba7"
                    overlay0: "#737994"

                    surface2: "#626880"
                    surface1: "#51576d"
                    surface0: "#414559"

                    base: "#303446"
                    mantle: "#292c3c"
                    crust: "#232634"

                    rosewater: "#f2d5cf"
                    flamingo: "#eebebe"
                    pink: "#f4b8e4"
                    mauve: "#ca9ee6"
                    red: "#e78284"
                    maroon: "#ea999c"
                    peach: "#ef9f76"
                    yellow: "#e5c890"
                    green: "#a6d189"
                    teal: "#81c8be"
                    sky: "#99d1db"
                    sapphire: "#85c1dc"
                    blue: "#8caaee"
                    lavender: "#babbf1"

                    ###########################

                    # Header
                    app-header-background-color: var(--mantle)
                    app-header-text-color: var(--text)

                    # Main Interface colors
                    primary-color: var(--blue)
                    light-primary-color: var(--primary-color)
                    accent-color: var(--yellow)

                    primary-background-color: var(--base)
                    secondary-background-color: var(--base)

                    # Text
                    primary-text-color: var(--text)
                    secondary-text-color: var(--subtext1)
                    text-primary-color: var(--text)
                    divider-color: var(--base)
                    disabled-text-color: var(--overlay0)
                    text-accent-color: var(--base)

                    # Sidebar
                    sidebar-background-color: var(--crust)
                    sidebar-selected-background-color: var(--primary-background-color)

                    sidebar-icon-color: var(--subtext0)
                    sidebar-text-color: var(--subtext0)
                    sidebar-selected-icon-color: var(--mauve)
                    sidebar-selected-text-color: var(--mauve)

                    # Buttons
                    paper-item-icon-color: var(--subtext0)
                    paper-item-icon-active-color: var(--primary-color)

                    # States and Badges
                    state-icon-color: var(--lavender)
                    state-icon-active-color: var(--primary-color)

                    state-icon-unavailable-color: var(--disabled-text-color)

                    # Sliders
                    paper-slider-knob-color: var(--blue)
                    paper-slider-knob-start-color: var(--paper-slider-knob-color)
                    paper-slider-pin-color: var(--paper-slider-knob-color)
                    paper-slider-active-color: var(--paper-slider-knob-color)
                    paper-slider-secondary-color: var(--blue)

                    # Labels
                    label-badge-background-color: var(--surface0)
                    label-badge-text-color: var(--text)
                    label-badge-red: var(--red)
                    label-badge-green: var(--green)
                    label-badge-blue: var(--blue)
                    label-badge-yellow: var(--yellow)
                    label-badge-gray: var(--overlay0)

                    # Cards
                    card-background-color: var(--surface0)
                    ha-card-background: var(--card-background-color)

                    ha-card-border-radius: "15px"
                    ha-card-box-shadow: none
                    paper-dialog-background-color: var(--overlay0)
                    paper-listbox-background-color: var(--overlay0)
                    paper-card-background-color: var(--card-background-color)

                    # Switches
                    switch-checked-button-color: var(--green)
                    switch-checked-track-color: var(--surface2)
                    switch-unchecked-button-color: rgb(--overlay0)
                    switch-unchecked-track-color: rgb(--surface0)

                    # Toggles
                    paper-toggle-button-checked-button-color: var(--switch-checked-button-color)
                    paper-toggle-button-checked-bar-color: var(--switch-checked-track-color)
                    paper-toggle-button-unchecked-button-color: var(--switch-unchecked-button-color)
                    paper-toggle-button-unchecked-bar-color: var(--switch-unchecked-track-color)

                    # Table
                    table-row-background-color: var(--primary-background-color)
                    table-row-alternative-background-color: var(--secondary-background-color)
                    data-table-background-color: var(--primary-background-color)
                    mdc-checkbox-unchecked-color: var(--overlay0)

                    # Dropdowns
                    material-background-color: var(--primary-background-color)
                    material-secondary-background-color: var(--primary-background-color)
                    mdc-theme-surface: var(--primary-background-color)

                    # Pre/Code
                    markdown-code-background-color: var(--surface0)

                    # Checkboxes
                    mdc-select-fill-color: var(--surface0)
                    mdc-select-ink-color: var(--primary-text-color)
                    mdc-select-label-ink-color: var(--subtext1)
                    mdc-select-idle-line-color: var(--primary-text-color)
                    mdc-select-dropdown-icon-color: var(--secondary-text-color)
                    mdc-select-hover-line-color: var(--accent-color)

                    # Input
                    input-fill-color: var(--secondary-background-color)
                    input-dropdown-icon-color: var(--secondary-text-color)
                    input-ink-color: var(--primary-text-color)
                    input-label-ink-color: var(--secondary-text-color)
                    input-idle-line-color: var(--primary-text-color)
                    input-hover-line-color: var(--accent-color)
                    input-disabled-ink-color: var(--disabled-text-color)
                    input-disabled-line-color: var(--disabled-text-color)
                    input-outlined-idle-border-color: var(--disabled-text-color)
                    input-outlined-hover-border-color: var(--disabled-text-color)
                    input-outlined-disabled-border-color: var(--disabled-text-color)
                    input-disabled-fill-color: rgba(0, 0, 0, 0)

                    # Toast
                    paper-toast-background-color: var(--overlay0)

                    # Colors
                    error-color: var(--red)
                    warning-color: var(--yellow)
                    success-color: var(--green)
                    info-color: var(--blue)

                    state-on-color: var(--green)
                    state-off-color: var(--red)

        Dream Vioneta:
            modes:
                light:
                    # Header:
                    app-header-background-color: rgb(243, 245, 244)
                    app-header-text-color: var(--primary-text-color)
                    app-header-selection-bar-color: var(--primary-color)
                    # Main Interface Colors
                    primary-color: rgb(0, 122, 255)
                    primary-background-color: rgb(255, 255, 255)
                    secondary-background-color: rgb(243, 245, 244)
                    divider-color: rgb(210, 210, 210)
                    accent-color: var(--primary-color)
                    # Text
                    primary-text-color: rgb(39, 39, 39)
                    secondary-text-color: rgb(85, 85, 85)
                    text-primary-color: var(--primary-text-color)
                    disabled-text-color: rgb(85, 85, 85)
                    # Sidebar Menu
                    sidebar-icon-color: rgb(85, 85, 85)
                    sidebar-text-color: rgb(39, 39, 39)
                    sidebar-background-color: var(--app-header-background-color)
                    sidebar-selected-icon-color: var(--primary-color)
                    sidebar-selected-text-color: var(--sidebar-selected-icon-color)
                    # Buttons
                    paper-item-icon-color: rgb(70, 70, 70)
                    paper-item-icon-active-color: var(--primary-color)
                    # States and Badges
                    state-icon-color: var(--paper-item-icon-color)
                    state-icon-active-color: var(--paper-item-icon-active-color)
                    state-icon-unavailable-color: rgb(154, 153, 152)
                    # Sliders
                    paper-slider-knob-color: rgb(191, 191, 192)
                    paper-slider-knob-start-color: var(--paper-slider-knob-color)
                    paper-slider-pin-color: var(--paper-slider-active-color)
                    paper-slider-active-color: rgb(0, 122, 255)
                    paper-slider-secondary-color: var(--paper-slider-active-color)
                    slider-track-color: rgb(203, 203, 205)
                    # Labels
                    label-badge-background-color: var(--secondary-background-color)
                    label-badge-text-color: var(--primary-text-color)
                    label-badge-red: rgb(253, 73, 67)
                    label-badge-green: rgb(40, 205, 65)
                    label-badge-blue: rgb(0, 122, 255)
                    label-badge-yellow: rgb(255, 204, 0)
                    label-badge-gray: rgb(142, 142, 147)
                    # Cards
                    card-background-color: rgb(243, 243, 244)
                    ha-card-background, var: rgb(243, 243, 244)
                    ha-card-border-color: none
                    ha-card-border-width: 0px
                    paper-dialog-background-color: var(--card-background-color)
                    paper-listbox-background-color: var(--card-background-color)
                    paper-card-background-color: var(--card-background-color)
                    # Switches
                    switch-checked-button-color: rgb(255, 255, 255)
                    switch-checked-track-color: rgb(0, 122, 255)
                    switch-unchecked-button-color: var(--switch-checked-button-color)
                    switch-unchecked-track-color: rgb(175, 177, 182)
                    # Toggles
                    paper-toggle-button-checked-button-color: var(--switch-checked-button-color)
                    paper-toggle-button-checked-bar-color: var(--switch-checked-track-color)
                    paper-toggle-button-unchecked-button-color: var(--switch-unchecked-button-color)
                    paper-toggle-button-unchecked-bar-color: var(--switch-unchecked-track-color)
                    # Table
                    table-row-background-color: rgb(244, 244, 245)
                    table-row-alternative-background-color: rgb(255, 255, 255)
                    data-table-background-color: rgb(244, 244, 245)
                    # Dropdowns
                    material-background-color: var(--table-row-background-color)
                    material-secondary-background-color: var(--table-row-alternative-background-color)
                    mdc-theme-surface: var(--secondary-background-color)
                    # Pre/Code
                    markdown-code-background-color: rgb(255, 255, 255)
                    # Checkboxes
                    mdc-checkbox-unchecked-color: rgb(154, 152, 152)
                    mdc-checkbox-disable-color: var(--disabled-text-color)
                    mdc-select-fill-color: rgb(228, 228, 231)
                    mdc-select-ink-color: var(--primary-text-color)
                    mdc-select-label-ink-color: var(--secondary-text-color)
                    mdc-select-idle-line-color: var(--primary-text-color)
                    mdc-select-dropdown-icon-color: rgb(170, 170, 170)
                    mdc-select-hover-line-color: var(--accent-color)
                    mdc-text-field-fill-color: var(--mdc-select-fill-color)
                    # Input
                    input-fill-color: var(--secondary-background-color)
                    input-dropdown-icon-color: var(--secondary-text-color)
                    input-ink-color: var(--primary-text-color)
                    input-label-ink-color: var(--secondary-text-color)
                    input-idle-line-color: var(--primary-text-color)
                    input-hover-line-color: var(--accent-color)
                    # Error, Warning, Success and Info colors
                    error-color: rgb(253, 73, 67)
                    warning-color: rgb(255, 204, 0)
                    sucess-color: rgb(40, 205, 65)
                    info-color: rgb(0, 122, 255)
                    # Progress bar
                    ha-bar-background-color: var(--slider-track-color)
                    # Mushroom Custom cards
                    mush-rgb-state-entity: 1, 122, 255
                    mush-rgb-green: 40, 205, 65
                    mush-rgb-yellow: 255, 204, 0
                    mush-rgb-orange: 255, 149, 0
                    mush-rgb-cyan: 85, 190, 240
                    mush-rgb-purple: 175, 82, 222
                    mush-rgb-pink: 255, 45, 85
                    mush-rgb-red: 253, 73, 67
                    mush-rgb-gray: 142, 142, 147
                    mush-rgb-disabled: 70, 70, 70
                    mush-icon-border-radius: 30%
                    mush-rgb-state-media-player: 0, 122, 255
                    
                    #RGB
                    rgb-primary-text-color: 0, 0, 0
                    rgb-primary-color: 0, 0, 0
                    rgb-accent-color: 0, 122, 255
                    rgb-state-switch-color: var(--rgb-accent-color)
                    rgb-state-light-color: var(--rgb-accent-color)
                    rgb-state-fan-color: var(--rgb-accent-color)
                    rgb-state-script-color: var(--rgb-accent-color)
                    rgb-state-vacuum-color: var(--rgb-accent-color)
                    rgb-state-remote-color: var(--rgb-accent-color)
                    rgb-state-input-boolean-color: var(--rgb-accent-color)
                    rgb-state-humidifier-color: var(--rgb-accent-color)
                    rgb-state-cover-color: var(--rgb-accent-color)
                
                dark:
                    # Header:
                    app-header-background-color: rgb(48, 48, 49)
                    app-header-text-color: var(--primary-text-color)
                    app-header-selection-bar-color: var(--primary-color)
                    # Main Interface Colors
                    primary-color: rgb(0, 122, 255)
                    primary-background-color: rgb(28, 29, 31)
                    secondary-background-color: rgb(48, 48, 49)
                    divider-color: rgb(22, 23, 24)
                    accent-color: var(--primary-color)
                    # Text
                    primary-text-color: rgb(220, 221, 221)
                    secondary-text-color: rgb(170, 170, 170)
                    text-primary-color: var(--primary-text-color)
                    disabled-text-color: rgb(170, 170, 170)
                    # Sidebar Menu
                    sidebar-icon-color: rgb(170, 170, 170)
                    sidebar-text-color: rgb(220, 221, 221)
                    sidebar-background-color: var(--app-header-background-color)
                    sidebar-selected-icon-color: var(--primary-color)
                    sidebar-selected-text-color: var(--sidebar-selected-icon-color)
                    # Buttons
                    paper-item-icon-color: rgb(197, 197, 198)
                    paper-item-icon-active-color: var(--primary-color)
                    # States and Badges
                    state-icon-color: var(--paper-item-icon-color)
                    state-icon-active-color: var(--paper-item-icon-active-color)
                    state-icon-unavailable-color: rgb(90, 89, 88)
                    # Sliders
                    paper-slider-knob-color: rgb(141, 142, 143)
                    paper-slider-knob-start-color: var(--paper-slider-knob-color)
                    paper-slider-pin-color: var(--paper-slider-active-color)
                    paper-slider-active-color: rgb(0, 122, 255)
                    paper-slider-secondary-color: var(--paper-slider-active-color)
                    slider-track-color: rgb(85, 85, 87)
                    # Labels
                    label-badge-background-color: var(--secondary-background-color)
                    label-badge-text-color: var(--primary-text-color)
                    label-badge-red: rgb(255, 69, 58)
                    label-badge-green: rgb(50, 215, 75)
                    label-badge-blue: rgb(0, 122, 255)
                    label-badge-yellow: rgb(255, 214, 10)
                    label-badge-gray: rgb(90, 89, 88)
                    # Cards
                    card-background-color: rgb(50, 51, 53)
                    ha-card-background: rgb(50, 51, 53)
                    ha-card-border-color: none
                    ha-card-border-width: 0px
                    paper-dialog-background-color: var(--card-background-color)
                    paper-listbox-background-color: var(--card-background-color)
                    paper-card-background-color: var(--card-background-color)
                    # Switches
                    switch-checked-button-color: rgb(202, 203, 204)
                    switch-checked-track-color: rgb(22, 100, 218)
                    switch-unchecked-button-color: var(--switch-checked-button-color)
                    switch-unchecked-track-color: rgb(12, 13, 14)
                    # Toggles
                    paper-toggle-button-checked-button-color: var(--switch-checked-button-color)
                    paper-toggle-button-checked-bar-color: var(--switch-checked-track-color)
                    paper-toggle-button-unchecked-button-color: var(--switch-unchecked-button-color)
                    paper-toggle-button-unchecked-bar-color: var(--switch-unchecked-track-color)
                    # Table
                    table-row-background-color: rgb(27, 29, 30)
                    table-row-alternative-background-color: rgb(38, 40, 41)
                    data-table-background-color: rgb(27, 29, 30)
                    # Dropdowns
                    material-background-color: var(--table-row-background-color)
                    material-secondary-background-color: var(--table-row-alternative-background-color)
                    mdc-theme-surface: var(--secondary-background-color)
                    # Pre/Code
                    markdown-code-background-color: rgb(64, 64, 65)
                    # Checkboxes
                    mdc-checkbox-unchecked-color: rgb(204, 203, 203)
                    mdc-checkbox-disable-color: var(--disabled-text-color)
                    mdc-select-fill-color: rgb(43, 45, 46)
                    mdc-select-ink-color: var(--primary-text-color)
                    mdc-select-label-ink-color: var(--secondary-text-color)
                    mdc-select-idle-line-color: var(--primary-text-color)
                    mdc-select-dropdown-icon-color: rgb(170, 170, 170)
                    mdc-select-hover-line-color: var(--accent-color)
                    mdc-text-field-fill-color: var(--mdc-select-fill-color)
                    
                    # Input
                    input-fill-color: var(--secondary-background-color)
                    input-dropdown-icon-color: var(--secondary-text-color)
                    input-ink-color: var(--primary-text-color)
                    input-label-ink-color: var(--secondary-text-color)
                    input-idle-line-color: var(--primary-text-color)
                    input-hover-line-color: var(--accent-color)
                    
                    # Error, Warning, Success and Info colors
                    error-color: rgb(255, 69, 58)
                    warning-color: rgb(255, 214, 10)
                    sucess-color: rgb(50, 215, 75)
                    info-color: rgb(0, 122, 255)
                    
                    # Progress bar
                    ha-bar-background-color: var(--slider-track-color)
                    
                    # Mushroom Custom cards
                    mush-rgb-state-entity: 1, 122, 255
                    mush-rgb-green: 50, 215, 75
                    mush-rgb-yellow: 255, 214, 10
                    mush-rgb-orange: 255, 159, 10
                    mush-rgb-cyan: 90, 200, 245
                    mush-rgb-purple: 191, 90, 242
                    mush-rgb-pink: 255, 55, 95
                    mush-rgb-red: 255, 69, 58
                    mush-rgb-gray: 90, 89, 88
                    mush-rgb-disabled: 197, 197, 198
                    mush-icon-border-radius: 30%
                    mush-rgb-state-media-player: 0, 122, 255
                    
                    #RGB
                    rgb-primary-text-color: 255, 255, 255
                    rgb-primary-color: 255, 255, 255
                    rgb-accent-color: 0, 122, 255
                    rgb-state-switch-color: var(--rgb-accent-color)
                    rgb-state-light-color: var(--rgb-accent-color)
                    rgb-state-fan-color: var(--rgb-accent-color)
                    rgb-state-script-color: var(--rgb-accent-color)
                    rgb-state-vacuum-color: var(--rgb-accent-color)
                    rgb-state-remote-color: var(--rgb-accent-color)
                    rgb-state-input-boolean-color: var(--rgb-accent-color)
                    rgb-state-humidifier-color: var(--rgb-accent-color)
                    rgb-state-cover-color: var(--rgb-accent-color)



        Drakula Vioneta:
            modes:
                dark:

                    # Color tokens
                    token-rgb-primary: 229, 145, 9
                    token-color-primary: rgb(var(--token-rgb-primary))
                    token-color-accent: var(--token-color-primary)
                    token-color-feedback-info: rgb(138, 208, 248)
                    token-color-feedback-warning: rgb(244, 180, 0)
                    token-color-feedback-error: rgb(229, 97, 128)
                    token-color-feedback-success: rgb(93, 193, 145)
                    token-color-icon-primary: rgba(228, 228, 231, 1)
                    token-color-icon-secondary: rgb(138, 140, 153)
                    token-color-icon-sidebar: rgba(147, 149, 159, 1)
                    token-color-icon-sidebar-selected: rgba(174, 176, 183, 1)
                    token-color-text-primary: rgba(228, 228, 231, 1)
                    token-color-text-secondary: rgb(138, 140, 153)
                    token-color-text-disabled: rgba(255, 255, 255, 0.5)
                    token-color-text-sidebar-selected: rgba(214, 215, 219, 1)
                    token-color-text-sidebar: var(--token-color-text-secondary)
                    token-color-text-label-badge: rgb(198, 203, 210)
                    token-color-background-base: rgba(22, 24, 29, 1)
                    token-color-background-secondary: rgba(28, 29, 33, 1)
                    token-color-background-sidebar: var(--token-color-background-base)
                    token-color-background-input-base: rgba(46, 48, 56, 1)
                    token-color-background-input-disabled: rgba(37, 37, 40, 0.5)
                    token-color-background-label-badge: rgba(54, 55, 67, 1)
                    token-color-background-card: rgba(37, 38, 45, 1)
                    token-color-background-skrim: rgba(0, 0, 3, 0.9)
                    token-color-background-divider: var(--token-color-background-sidebar)
                    token-color-background-scrollbar-thumb: rgba(46, 48, 56, 1)
                    token-color-background-label-badge-red: var(--token-color-feedback-error)
                    token-color-background-label-badge-green: rgba(78, 183, 128, 1)
                    token-color-background-label-badge-blue: var(--token-color-feedback-info)
                    token-color-background-label-badge-yellow: var(--token-color-feedback-warning)
                    token-color-background-label-badge-grey: rgba(83, 90, 103, 1)
                    token-color-background-popup-scrim: rgba(4, 5, 7, 0.9)
                    token-color-border-card: rgba(0, 0, 0, 0)

                    # Opacity tokens
                    token-opacity-ripple-hover: 0.14

                    # Font tokens
                    token-font-family-primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"

                    # Size tokens
                    token-size-radius-small: 9px
                    token-size-radius-medium: 16px
                    token-size-radius-large: 18px
                    token-size-radius-card: var(--token-size-radius-large)
                    token-size-width-border-card: 0
                    token-size-height-slider: 4px
                    token-size-height-navbar: 56px
                    token-size-font-title: 28px

                    # Weight tokens
                    token-weight-font-title: 600

                    ##############################################################################
                    # Definitions

                    # Shapes
                    mdc-shape-small: var(--token-size-radius-small)
                    mdc-shape-medium: var(--token-size-radius-medium)
                    mdc-shape-large: var(--token-size-radius-large)

                    # Sizes
                    header-height: var(--token-size-height-navbar)
                    paper-slider-height: var(--token-size-height-slider)

                    # Typography
                    primary-font-family: var(--token-font-family-primary)
                    paper-font-common-base_-_font-family: var(--token-font-family-primary)
                    paper-font-common-code_-_font-family: var(--token-font-family-primary)
                    paper-font-body1_-_font-family: var(--token-font-family-primary)
                    paper-font-subhead_-_font-family: var(--token-font-family-primary)
                    paper-font-headline_-_font-family: var(--token-font-family-primary)
                    paper-font-caption_-_font-family: var(--token-font-family-primary)
                    paper-font-title_-_font-family: var(--token-font-family-primary)
                    ha-card-header-font-family: var(--token-font-family-primary)
                    mdc-typography-font-family: var(--token-font-family-primary)
                    mdc-typography-button-font-family: var(--token-font-family-primary)
                    mdc-typography-body1-font-family: var(--token-font-family-primary)
                    mdc-typography-button-font-weight: var(--token-weight-font-title)

                    title-font-weight: var(--token-weight-font-title)
                    title-font-size: var(--token-size-font-title)

                    # Text
                    primary-text-color: var(--token-color-text-primary)
                    secondary-text-color: var(--token-color-text-secondary)
                    text-primary-color: var(--token-color-text-primary)
                    text-light-primary-color: var(--token-color-text-primary)
                    disabled-text-color: var(--token-color-text-disabled)

                    # Main interface colors
                    primary-color: var(--token-color-primary)
                    dark-primary-color: var(--primary-color)
                    light-primary-color: var(--primary-color)
                    accent-color: var(--token-color-accent)
                    divider-color: var(--token-color-background-divider)
                    scrollbar-thumb-color: var(--token-color-background-scrollbar-thumb)

                    # Feedback colors
                    error-color: rgb(234, 114, 135)
                    warning-color: rgb(255, 219, 117)
                    success-color: rgb(118, 214, 152)
                    info-color: rgb(39, 209, 246)

                    # Background
                    lovelace-background: var(--token-color-background-base)
                    background-color: var(--token-color-background-base)
                    primary-background-color: var(--token-color-background-base)
                    secondary-background-color: var(--token-color-background-secondary)

                    # Navbar
                    app-header-background-color: var(--primary-background-color)
                    app-header-text-color: var(--token-color-icon-primary)
                    app-header-edit-background-color: var(--token-color-background-card)

                    # Sidebar
                    sidebar-icon-color: var(--token-color-icon-sidebar)
                    sidebar-text-color: var(--sidebar-icon-color)
                    sidebar-background-color: var(--token-color-background-sidebar)
                    sidebar-selected-icon-color: var(--token-color-icon-sidebar-selected)
                    sidebar-selected-text-color: var(--token-color-text-sidebar-selected)

                    # Cards
                    border-radius: var(--token-size-radius-card)
                    card-background-color: var(--token-color-background-card)
                    ha-card-background: var(--token-color-background-card)
                    ha-card-border-radius: var(--token-size-radius-card)
                    ha-card-border-color: var(--token-color-border-card)
                    ha-card-border-width: var(--token-size-width-border-card)
                    ha-card-border-style: none
                    ha-card-border: none
                    ha-card-box-shadow: none

                    # States
                    state-icon-color: var(--token-color-icon-primary)
                    state-on-color: var(--token-color-feedback-success)
                    state-off-color: var(--token-color-feedback-error)

                    # Label-badge
                    label-badge-text-color: var(--token-color-text-primary)
                    label-badge-red: var(--token-color-background-label-badge-red)
                    label-badge-blue: var(--token-color-background-label-badge-blue)
                    label-badge-green: var(--token-color-background-label-badge-green)
                    label-badge-yellow: var(--token-color-background-label-badge-yellow)
                    label-badge-grey: var(--token-color-background-label-badge-grey)

                    # Chip
                    ha-chip-text-color: rgb(255, 255, 255)

                    # Dialog
                    mdc-dialog-scrim-color: var(--token-color-background-popup-scrim)

                    # Slider
                    paper-slider-knob-color: var(--token-color-primary)
                    paper-slider-knob-start-color: var(--paper-slider-knob-color)
                    paper-slider-pin-color: var(--paper-slider-knob-color)
                    paper-slider-active-color: var(--paper-slider-knob-color)
                    paper-slider-secondary-color: var(--light-primary-color)

                    # Switch
                    switch-checked-button-color: var(--primary-color)
                    switch-checked-track-color: var(--switch-checked-button-color)
                    switch-unchecked-button-color: rgba(255, 255, 255, 0.7)
                    switch-unchecked-track-color: rgba(125, 128, 132, 0.4)

                    # Toggles
                    paper-toggle-button-checked-button-color: var(--switch-checked-button-color)
                    paper-toggle-button-checked-bar-color: var(--switch-checked-track-color)
                    paper-toggle-button-unchecked-button-color: var(--switch-unchecked-button-color)
                    paper-toggle-button-unchecked-bar-color: var(--switch-unchecked-track-color)
                    mdc-checkbox-unchecked-color: var(--token-color-icon-secondary)
                    mdc-radio-unchecked-color: var(--mdc-checkbox-unchecked-color)

                    # List items
                    mdc-ripple-hover-opacity: var(--token-opacity-ripple-hover)

                    # Text Fields an Dropdown
                    input-background-color: var(--token-color-background-input-base)
                    input-background-token-color-disabled: rgba(var(--input-background-color), 0.5)
                    input-fill-color: var(--input-background-color)
                    input-ink-color: var(--token-color-text-primary)
                    input-label-ink-color: var(--token-color-text-primary)
                    input-disabled-fill-color: var(--input-background-token-color-disabled)
                    input-disabled-ink-color: var(--disabled-text-color)
                    input-disabled-label-ink-color: var(--disabled-text-color)
                    input-idle-line-color: var(--background-color)
                    input-dropdown-icon-color: var(--secondary-text-color)
                    input-hover-line-color: var(--primary-color)
                    mdc-select-idle-line-color: var(--color-background-base)
                    mdc-text-field-idle-line-color: var(--mdc-select-idle-line-color)

                    # Editor
                    code-editor-background-color: var(--token-color-background-base)
                    codemirror-meta: var(--token-color-text-primary)
                    codemirror-property: var(--accent-color)
                    codemirror-atom: var(--codemirror-property)
                    codemirror-string: rgb(119, 196, 229)
                    codemirror-keyword: rgb(140, 169, 255)
                    codemirror-number: rgb(255, 91, 29)

                    # RGB colors
                    rgb-primary-color: var(--token-rgb-primary)
                    rgb-accent-color: var(--token-rgb-primary)
                    rgb-white-color: 240, 243, 255
                    rgb-purple-color: 189, 157, 255
                    rgb-pink-color: 255, 98, 192
                    rgb-red-color: 255, 97, 116
                    rgb-deep-purple-color: 166, 77, 255
                    rgb-indigo-color: 84, 132, 255
                    rgb-blue-color: 33, 150, 243
                    rgb-light-blue-color: 3, 169, 244
                    rgb-cyan-color: 0, 188, 212
                    rgb-teal-color: 107, 255, 237
                    rgb-green-color: 141, 253, 166
                    rgb-light-green-color: 156, 255, 166
                    rgb-lime-color: 205, 220, 57
                    rgb-yellow-color: 255, 235, 59
                    rgb-amber-color: 255, 211, 99
                    rgb-orange-color: var(--rgb-primary-color)
                    rgb-deep-orange-color: 255, 87, 34
                    rgb-brown-color: 121, 85, 72
                    rgb-grey-color: 158, 158, 158
                    rgb-blue-grey-color: 96, 125, 139
                    rgb-black-color: 0, 0, 0
                    rgb-disabled-color: 61, 65, 85
                    rgb-state-inactive-color: 123, 126, 139

                    ##############################################################################
                    # Extentions

                    # HACS
                    hacs-new-color: rgb(27, 153, 123)
                    hacs-error-color: rgb(182, 46, 95)

                    # Mini graph card
                    mcg-title-font-weight: 400

                    # Mushroom
                    mush-title-font-weight: var(--title-font-weight)
                    mush-title-font-size: var(--title-font-size)
                    mush-rgb-white: var(--rgb-white-color)
                    mush-rgb-purple: var(--rgb-purple-color)
                    mush-rgb-pink: var(--rgb-pink-color)
                    mush-rgb-red: var(--rgb-red-color)
                    mush-rgb-deep-purple: var(--rgb-deep-purple-color)
                    mush-rgb-indigo: var(--rgb-indigo-color)
                    mush-rgb-blue: var(--rgb-blue-color)
                    mush-rgb-light-blue: var(--rgb-light-blue-color)
                    mush-rgb-cyan: var(--rgb-cyan-color)
                    mush-rgb-teal: var(--rgb-teal-color)
                    mush-rgb-green: var(--rgb-green-color)
                    mush-rgb-light-green: var(--rgb-light-green-color)
                    mush-rgb-lime: var(--rgb-lime-color)
                    mush-rgb-yellow: var(--rgb-yellow-color)
                    mush-rgb-amber: var(--rgb-amber-color)
                    mush-rgb-orange: var(--rgb-orange-color)
                    mush-rgb-deep-orange: var(--rgb-deep-orange-color)
                    mush-rgb-brown: var(--rgb-brown-color)
                    mush-rgb-grey: var(--rgb-grey-color)
                    mush-rgb-blue-grey: var(--rgb-blue-grey-color)
                    mush-rgb-black: var(--rgb-black-color)
                    mush-rgb-disabled: var(--rgb-disabled-color)

                light:
                    # Graphite is a contemporary theme that offers both a calm dark color scheme and a clean light theme,
                    # featuring native device fonts and a cohesive design language. 
                    # Carefully crafted to be visually appealing and easy on the eyes, Graphite ensures a consistent user experience 
                    # throughout the entire Vioneta Agro interface, including the administration panel and code editors.
                    # https://github.com/TilmanGriesel/graphite

                    ##############################################################################
                    # Tokens

                    # Color tokens
                    token-rgb-primary: 255, 158, 0
                    token-color-primary: rgb(var(--token-rgb-primary))
                    token-color-accent: var(--token-color-primary)
                    token-color-feedback-info: rgb(29, 130, 193)
                    token-color-feedback-warning: rgb(204, 144, 0)
                    token-color-feedback-error: rgb(179, 57, 96)
                    token-color-feedback-success: rgb(29, 143, 95)
                    token-color-icon-primary: rgba(19, 21, 54, 0.87)
                    token-color-icon-secondary: rgba(19, 21, 54, 0.8)
                    token-color-icon-sidebar: rgba(19, 21, 54, 0.7)
                    token-color-icon-sidebar-selected: var(--token-color-icon-primary)
                    token-color-text-primary: rgba(19, 21, 54, 0.95)
                    token-color-text-secondary: rgba(19, 21, 54, 0.8)
                    token-color-text-disabled: rgba(19, 21, 54, 0.38)
                    token-color-text-sidebar-selected: var(--token-color-text-primary)
                    token-color-text-sidebar: var(--token-color-text-secondary)
                    token-color-text-label-badge: rgba(19, 21, 54, 0.7)
                    token-color-background-base: rgb(225, 226, 229)
                    token-color-background-secondary: rgba(245, 245, 245, 1)
                    token-color-background-sidebar: var(--token-color-background-base)
                    token-color-background-input-base: rgba(255, 255, 255, 1)
                    token-color-background-input-disabled: rgba(245, 245, 245, 1)
                    token-color-background-label-badge: rgba(230, 230, 230, 1)
                    token-color-background-card: rgba(255, 255, 255, 1)
                    token-color-background-skrim: rgba(0, 0, 0, 0.5)
                    token-color-background-divider: rgba(224, 224, 224, 1)
                    token-color-background-scrollbar-thumb: rgba(200, 200, 200, 1)
                    token-color-background-label-badge-red: var(--token-color-feedback-error)
                    token-color-background-label-badge-green: rgba(78, 183, 128, 1)
                    token-color-background-label-badge-blue: var(--token-color-feedback-info)
                    token-color-background-label-badge-yellow: var(--token-color-feedback-warning)
                    token-color-background-label-badge-grey: rgba(83, 90, 103, 1)
                    token-color-background-popup-scrim: rgba(0, 0, 0, 0.5)
                    token-color-border-card: rgba(224, 224, 224, 1)

                    # Opacity tokens
                    token-opacity-ripple-hover: 0.14

                    # Font tokens
                    token-font-family-primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"

                    # Size tokens
                    token-size-radius-small: 9px
                    token-size-radius-medium: 16px
                    token-size-radius-large: 18px
                    token-size-radius-card: var(--token-size-radius-large)
                    token-size-width-border-card: 0
                    token-size-height-slider: 4px
                    token-size-height-navbar: 56px
                    token-size-font-title: 28px

                    # Weight tokens
                    token-weight-font-title: 600

                    ##############################################################################
                    # Definitions

                    # Shapes
                    mdc-shape-small: var(--token-size-radius-small)
                    mdc-shape-medium: var(--token-size-radius-medium)
                    mdc-shape-large: var(--token-size-radius-large)

                    # Sizes
                    header-height: var(--token-size-height-navbar)
                    paper-slider-height: var(--token-size-height-slider)

                    # Typography
                    primary-font-family: var(--token-font-family-primary)
                    paper-font-common-base_-_font-family: var(--token-font-family-primary)
                    paper-font-common-code_-_font-family: var(--token-font-family-primary)
                    paper-font-body1_-_font-family: var(--token-font-family-primary)
                    paper-font-subhead_-_font-family: var(--token-font-family-primary)
                    paper-font-headline_-_font-family: var(--token-font-family-primary)
                    paper-font-caption_-_font-family: var(--token-font-family-primary)
                    paper-font-title_-_font-family: var(--token-font-family-primary)
                    ha-card-header-font-family: var(--token-font-family-primary)
                    mdc-typography-font-family: var(--token-font-family-primary)
                    mdc-typography-button-font-family: var(--token-font-family-primary)
                    mdc-typography-body1-font-family: var(--token-font-family-primary)
                    mdc-typography-button-font-weight: var(--token-weight-font-title)

                    title-font-weight: var(--token-weight-font-title)
                    title-font-size: var(--token-size-font-title)

                    # Text
                    primary-text-color: var(--token-color-text-primary)
                    secondary-text-color: var(--token-color-text-secondary)
                    text-primary-color: var(--token-color-text-primary)
                    text-light-primary-color: var(--token-color-text-primary)
                    disabled-text-color: var(--token-color-text-disabled)
                    app-header-edit-text-color: var(--token-color-text-primary)

                    # Main interface colors
                    primary-color: var(--token-color-primary)
                    dark-primary-color: var(--primary-color)
                    light-primary-color: var(--primary-color)
                    accent-color: var(--token-color-accent)
                    divider-color: var(--token-color-background-divider)
                    scrollbar-thumb-color: var(--token-color-background-scrollbar-thumb)

                    # Feedback colors
                    error-color: rgb(234, 114, 135)
                    warning-color: rgb(255, 219, 117)
                    success-color: rgb(118, 214, 152)
                    info-color: rgb(39, 209, 246)

                    # Background
                    lovelace-background: var(--token-color-background-base)
                    background-color: var(--token-color-background-base)
                    primary-background-color: var(--token-color-background-base)
                    secondary-background-color: var(--token-color-background-secondary)

                    # Navbar
                    app-header-background-color: var(--primary-background-color)
                    app-header-text-color: var(--token-color-icon-primary)
                    app-header-edit-background-color: var(--token-color-background-card)

                    # Sidebar
                    sidebar-icon-color: var(--token-color-icon-sidebar)
                    sidebar-text-color: var(--sidebar-icon-color)
                    sidebar-background-color: var(--token-color-background-sidebar)
                    sidebar-selected-icon-color: var(--token-color-icon-sidebar-selected)
                    sidebar-selected-text-color: var(--token-color-text-sidebar-selected)

                    # Cards
                    border-radius: var(--token-size-radius-card)
                    card-background-color: var(--token-color-background-card)
                    ha-card-background: var(--token-color-background-card)
                    ha-card-border-radius: var(--token-size-radius-card)
                    ha-card-border-color: var(--token-color-border-card)
                    ha-card-border-width: var(--token-size-width-border-card)
                    ha-card-border-style: none
                    ha-card-border: none
                    ha-card-box-shadow: none

                    # States
                    state-icon-color: var(--token-color-icon-primary)
                    state-on-color: var(--token-color-feedback-success)
                    state-off-color: var(--token-color-feedback-error)

                    # Label-badge
                    label-badge-text-color: var(--token-color-text-primary)
                    label-badge-red: var(--token-color-background-label-badge-red)
                    label-badge-blue: var(--token-color-background-label-badge-blue)
                    label-badge-green: var(--token-color-background-label-badge-green)
                    label-badge-yellow: var(--token-color-background-label-badge-yellow)
                    label-badge-grey: var(--token-color-background-label-badge-grey)

                    # Chip
                    ha-chip-text-color: rgb(0, 0, 0)

                    # Dialog
                    mdc-dialog-scrim-color: var(--token-color-background-popup-scrim)

                    # Slider
                    paper-slider-knob-color: var(--token-color-primary)
                    paper-slider-knob-start-color: var(--paper-slider-knob-color)
                    paper-slider-pin-color: var(--paper-slider-knob-color)
                    paper-slider-active-color: var(--paper-slider-knob-color)
                    paper-slider-secondary-color: var(--light-primary-color)

                    # Switch
                    switch-checked-button-color: var(--primary-color)
                    switch-checked-track-color: var(--switch-checked-button-color)
                    switch-unchecked-button-color: rgba(0, 0, 0, 0.5)
                    switch-unchecked-track-color: rgba(0, 0, 0, 0.25)

                    # Toggles
                    paper-toggle-button-checked-button-color: var(--switch-checked-button-color)
                    paper-toggle-button-checked-bar-color: var(--switch-checked-track-color)
                    paper-toggle-button-unchecked-button-color: var(--switch-unchecked-button-color)
                    paper-toggle-button-unchecked-bar-color: var(--switch-unchecked-track-color)
                    mdc-checkbox-unchecked-color: var(--token-color-icon-secondary)
                    mdc-radio-unchecked-color: var(--mdc-checkbox-unchecked-color)

                    # List items
                    mdc-ripple-hover-opacity: var(--token-opacity-ripple-hover)

                    # Text Fields an Dropdown
                    input-background-color: var(--token-color-background-input-base)
                    input-background-token-color-disabled: rgba(var(--input-background-color), 0.5)
                    input-fill-color: var(--input-background-color)
                    input-ink-color: var(--token-color-text-primary)
                    input-label-ink-color: var(--token-color-text-primary)
                    input-disabled-fill-color: var(--input-background-token-color-disabled)
                    input-disabled-ink-color: var(--disabled-text-color)
                    input-disabled-label-ink-color: var(--disabled-text-color)
                    input-idle-line-color: var(--background-color)
                    input-dropdown-icon-color: var(--secondary-text-color)
                    input-hover-line-color: var(--primary-color)
                    mdc-select-idle-line-color: var(--color-background-base)
                    mdc-text-field-idle-line-color: var(--mdc-select-idle-line-color)

                    # Editor
                    code-editor-background-color: var(--token-color-background-base)
                    codemirror-meta: var(--token-color-text-primary)
                    codemirror-property: var(--accent-color)
                    codemirror-atom: var(--codemirror-property)
                    codemirror-string: rgb(0, 77, 153)
                    codemirror-keyword: rgb(70, 112, 216)
                    codemirror-number: rgb(204, 85, 0)

                    # RGB colors
                    rgb-primary-color: var(--token-rgb-primary)
                    rgb-accent-color: var(--token-rgb-primary)
                    rgb-white-color: 255, 255, 255
                    rgb-purple-color: 129, 45, 250
                    rgb-pink-color: 204, 0, 136
                    rgb-red-color: 204, 0, 51
                    rgb-deep-purple-color: 98, 0, 234
                    rgb-indigo-color: 48, 63, 159
                    rgb-blue-color: 33, 150, 243
                    rgb-light-blue-color: 3, 169, 244
                    rgb-cyan-color: 0, 188, 212
                    rgb-teal-color: 0, 150, 136
                    rgb-green-color: 56, 142, 60
                    rgb-light-green-color: 139, 195, 74
                    rgb-lime-color: 205, 220, 57
                    rgb-yellow-color: 255, 235, 59
                    rgb-amber-color: 255, 193, 7
                    rgb-orange-color: var(--rgb-primary-color)
                    rgb-deep-orange-color: 255, 87, 34
                    rgb-brown-color: 121, 85, 72
                    rgb-grey-color: 158, 158, 158
                    rgb-blue-grey-color: 96, 125, 139
                    rgb-black-color: 0, 0, 0
                    rgb-disabled-color: 189, 189, 189
                    rgb-state-inactive-color: 176, 190, 197

                    ##############################################################################
                    # Extentions

                    # HACS
                    hacs-new-color: rgb(27, 153, 123)
                    hacs-error-color: rgb(182, 46, 95)

                    # Mini graph card
                    mcg-title-font-weight: 400

                    # Mushroom
                    mush-title-font-weight: var(--title-font-weight)
                    mush-title-font-size: var(--title-font-size)
                    mush-rgb-white: var(--rgb-white-color)
                    mush-rgb-purple: var(--rgb-purple-color)
                    mush-rgb-pink: var(--rgb-pink-color)
                    mush-rgb-red: var(--rgb-red-color)
                    mush-rgb-deep-purple: var(--rgb-deep-purple-color)
                    mush-rgb-indigo: var(--rgb-indigo-color)
                    mush-rgb-blue: var(--rgb-blue-color)
                    mush-rgb-light-blue: var(--rgb-light-blue-color)
                    mush-rgb-cyan: var(--rgb-cyan-color)
                    mush-rgb-teal: var(--rgb-teal-color)
                    mush-rgb-green: var(--rgb-green-color)
                    mush-rgb-light-green: var(--rgb-light-green-color)
                    mush-rgb-lime: var(--rgb-lime-color)
                    mush-rgb-yellow: var(--rgb-yellow-color)
                    mush-rgb-amber: var(--rgb-amber-color)
                    mush-rgb-orange: var(--rgb-orange-color)
                    mush-rgb-deep-orange: var(--rgb-deep-orange-color)
                    mush-rgb-brown: var(--rgb-brown-color)
                    mush-rgb-grey: var(--rgb-grey-color)
                    mush-rgb-blue-grey: var(--rgb-blue-grey-color)
                    mush-rgb-black: var(--rgb-black-color)
                    mush-rgb-disabled: var(--rgb-disabled-color)
automation: !include {AUTOMATION_CONFIG_PATH}
script: !include {SCRIPT_CONFIG_PATH}
scene: !include {SCENE_CONFIG_PATH}
"""
DEFAULT_SECRETS = """
# Use this file to store secrets like usernames and passwords.
# Learn more at https://www.home-assistant.io/docs/configuration/secrets/
some_password: welcome
"""
TTS_PRE_92 = """
tts:
  - platform: google
"""
TTS_92 = """
tts:
  - platform: google_translate
    service_name: google_say
"""


class ConfigErrorTranslationKey(StrEnum):
    """Config error translation keys for config errors."""

    # translation keys with a generated config related message text
    CONFIG_VALIDATION_ERR = "config_validation_err"
    PLATFORM_CONFIG_VALIDATION_ERR = "platform_config_validation_err"

    # translation keys with a general static message text
    COMPONENT_IMPORT_ERR = "component_import_err"
    CONFIG_PLATFORM_IMPORT_ERR = "config_platform_import_err"
    CONFIG_VALIDATOR_UNKNOWN_ERR = "config_validator_unknown_err"
    CONFIG_SCHEMA_UNKNOWN_ERR = "config_schema_unknown_err"
    PLATFORM_COMPONENT_LOAD_ERR = "platform_component_load_err"
    PLATFORM_COMPONENT_LOAD_EXC = "platform_component_load_exc"
    PLATFORM_SCHEMA_VALIDATOR_ERR = "platform_schema_validator_err"

    # translation key in case multiple errors occurred
    MULTIPLE_INTEGRATION_CONFIG_ERRORS = "multiple_integration_config_errors"


_CONFIG_LOG_SHOW_STACK_TRACE: dict[ConfigErrorTranslationKey, bool] = {
    ConfigErrorTranslationKey.COMPONENT_IMPORT_ERR: False,
    ConfigErrorTranslationKey.CONFIG_PLATFORM_IMPORT_ERR: False,
    ConfigErrorTranslationKey.CONFIG_VALIDATOR_UNKNOWN_ERR: True,
    ConfigErrorTranslationKey.CONFIG_SCHEMA_UNKNOWN_ERR: True,
    ConfigErrorTranslationKey.PLATFORM_COMPONENT_LOAD_ERR: False,
    ConfigErrorTranslationKey.PLATFORM_COMPONENT_LOAD_EXC: True,
    ConfigErrorTranslationKey.PLATFORM_SCHEMA_VALIDATOR_ERR: True,
}


@dataclass
class ConfigExceptionInfo:
    """Configuration exception info class."""

    exception: Exception
    translation_key: ConfigErrorTranslationKey
    platform_path: str
    config: ConfigType
    integration_link: str | None


@dataclass
class IntegrationConfigInfo:
    """Configuration for an integration and exception information."""

    config: ConfigType | None
    exception_info_list: list[ConfigExceptionInfo]


def _no_duplicate_auth_provider(
    configs: Sequence[dict[str, Any]],
) -> Sequence[dict[str, Any]]:
    """No duplicate auth provider config allowed in a list.

    Each type of auth provider can only have one config without optional id.
    Unique id is required if same type of auth provider used multiple times.
    """
    config_keys: set[tuple[str, str | None]] = set()
    for config in configs:
        key = (config[CONF_TYPE], config.get(CONF_ID))
        if key in config_keys:
            raise vol.Invalid(
                f"Duplicate auth provider {config[CONF_TYPE]} found. "
                "Please add unique IDs "
                "if you want to have the same auth provider twice"
            )
        config_keys.add(key)
    return configs


def _no_duplicate_auth_mfa_module(
    configs: Sequence[dict[str, Any]],
) -> Sequence[dict[str, Any]]:
    """No duplicate auth mfa module item allowed in a list.

    Each type of mfa module can only have one config without optional id.
    A global unique id is required if same type of mfa module used multiple
    times.
    Note: this is different than auth provider
    """
    config_keys: set[str] = set()
    for config in configs:
        key = config.get(CONF_ID, config[CONF_TYPE])
        if key in config_keys:
            raise vol.Invalid(
                f"Duplicate mfa module {config[CONF_TYPE]} found. "
                "Please add unique IDs "
                "if you want to have the same mfa module twice"
            )
        config_keys.add(key)
    return configs


def _filter_bad_internal_external_urls(conf: dict) -> dict:
    """Filter internal/external URL with a path."""
    for key in CONF_INTERNAL_URL, CONF_EXTERNAL_URL:
        if key in conf and urlparse(conf[key]).path not in ("", "/"):
            # We warn but do not fix, because if this was incorrectly configured,
            # adjusting this value might impact security.
            _LOGGER.warning(
                "Invalid %s set. It's not allowed to have a path (/bla)", key
            )

    return conf


# Schema for all packages element
PACKAGES_CONFIG_SCHEMA = vol.Schema({cv.string: vol.Any(dict, list)})

# Schema for individual package definition
PACKAGE_DEFINITION_SCHEMA = vol.Schema({cv.string: vol.Any(dict, list, None)})

CUSTOMIZE_DICT_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_FRIENDLY_NAME): cv.string,
        vol.Optional(ATTR_HIDDEN): cv.boolean,
        vol.Optional(ATTR_ASSUMED_STATE): cv.boolean,
    },
    extra=vol.ALLOW_EXTRA,
)

CUSTOMIZE_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_CUSTOMIZE, default={}): vol.Schema(
            {cv.entity_id: CUSTOMIZE_DICT_SCHEMA}
        ),
        vol.Optional(CONF_CUSTOMIZE_DOMAIN, default={}): vol.Schema(
            {cv.string: CUSTOMIZE_DICT_SCHEMA}
        ),
        vol.Optional(CONF_CUSTOMIZE_GLOB, default={}): vol.Schema(
            {cv.string: CUSTOMIZE_DICT_SCHEMA}
        ),
    }
)


def _raise_issue_if_historic_currency(hass: HomeAssistant, currency: str) -> None:
    if currency not in HISTORIC_CURRENCIES:
        ir.async_delete_issue(hass, HOMEASSISTANT_DOMAIN, "historic_currency")
        return

    ir.async_create_issue(
        hass,
        HOMEASSISTANT_DOMAIN,
        "historic_currency",
        is_fixable=False,
        learn_more_url="homeassistant://config/general",
        severity=ir.IssueSeverity.WARNING,
        translation_key="historic_currency",
        translation_placeholders={"currency": currency},
    )


def _raise_issue_if_no_country(hass: HomeAssistant, country: str | None) -> None:
    if country is not None:
        ir.async_delete_issue(hass, HOMEASSISTANT_DOMAIN, "country_not_configured")
        return

    ir.async_create_issue(
        hass,
        HOMEASSISTANT_DOMAIN,
        "country_not_configured",
        is_fixable=False,
        learn_more_url="homeassistant://config/general",
        severity=ir.IssueSeverity.WARNING,
        translation_key="country_not_configured",
    )


def _validate_currency(data: Any) -> Any:
    try:
        return cv.currency(data)
    except vol.InInvalid:
        with suppress(vol.InInvalid):
            return cv.historic_currency(data)
        raise


CORE_CONFIG_SCHEMA = vol.All(
    CUSTOMIZE_CONFIG_SCHEMA.extend(
        {
            CONF_NAME: vol.Coerce(str),
            CONF_LATITUDE: cv.latitude,
            CONF_LONGITUDE: cv.longitude,
            CONF_ELEVATION: vol.Coerce(int),
            CONF_RADIUS: cv.positive_int,
            vol.Remove(CONF_TEMPERATURE_UNIT): cv.temperature_unit,
            CONF_UNIT_SYSTEM: validate_unit_system,
            CONF_TIME_ZONE: cv.time_zone,
            vol.Optional(CONF_INTERNAL_URL): cv.url,
            vol.Optional(CONF_EXTERNAL_URL): cv.url,
            vol.Optional(CONF_ALLOWLIST_EXTERNAL_DIRS): vol.All(
                cv.ensure_list, [vol.IsDir()]
            ),
            vol.Optional(LEGACY_CONF_WHITELIST_EXTERNAL_DIRS): vol.All(
                cv.ensure_list, [vol.IsDir()]
            ),
            vol.Optional(CONF_ALLOWLIST_EXTERNAL_URLS): vol.All(
                cv.ensure_list, [cv.url]
            ),
            vol.Optional(CONF_PACKAGES, default={}): PACKAGES_CONFIG_SCHEMA,
            vol.Optional(CONF_AUTH_PROVIDERS): vol.All(
                cv.ensure_list,
                [
                    auth_providers.AUTH_PROVIDER_SCHEMA.extend(
                        {
                            CONF_TYPE: vol.NotIn(
                                ["insecure_example"],
                                (
                                    "The insecure_example auth provider"
                                    " is for testing only."
                                ),
                            )
                        }
                    )
                ],
                _no_duplicate_auth_provider,
            ),
            vol.Optional(CONF_AUTH_MFA_MODULES): vol.All(
                cv.ensure_list,
                [
                    auth_mfa_modules.MULTI_FACTOR_AUTH_MODULE_SCHEMA.extend(
                        {
                            CONF_TYPE: vol.NotIn(
                                ["insecure_example"],
                                "The insecure_example mfa module is for testing only.",
                            )
                        }
                    )
                ],
                _no_duplicate_auth_mfa_module,
            ),
            vol.Optional(CONF_MEDIA_DIRS): cv.schema_with_slug_keys(vol.IsDir()),
            vol.Remove(CONF_LEGACY_TEMPLATES): cv.boolean,
            vol.Optional(CONF_CURRENCY): _validate_currency,
            vol.Optional(CONF_COUNTRY): cv.country,
            vol.Optional(CONF_LANGUAGE): cv.language,
            vol.Optional(CONF_DEBUG): cv.boolean,
        }
    ),
    _filter_bad_internal_external_urls,
)


def get_default_config_dir() -> str:
    """Put together the default configuration directory based on the OS."""
    data_dir = os.path.expanduser("~")
    return os.path.join(data_dir, CONFIG_DIR_NAME)


async def async_ensure_config_exists(hass: HomeAssistant) -> bool:
    """Ensure a configuration file exists in given configuration directory.

    Creating a default one if needed.
    Return boolean if configuration dir is ready to go.
    """
    config_path = hass.config.path(YAML_CONFIG_FILE)

    if os.path.isfile(config_path):
        return True

    print(  # noqa: T201
        "Unable to find configuration. Creating default one in", hass.config.config_dir
    )
    return await async_create_default_config(hass)


async def async_create_default_config(hass: HomeAssistant) -> bool:
    """Create a default configuration file in given configuration directory.

    Return if creation was successful.
    """
    return await hass.async_add_executor_job(
        _write_default_config, hass.config.config_dir
    )


def _write_default_config(config_dir: str) -> bool:
    """Write the default config."""
    config_path = os.path.join(config_dir, YAML_CONFIG_FILE)
    secret_path = os.path.join(config_dir, SECRET_YAML)
    version_path = os.path.join(config_dir, VERSION_FILE)
    automation_yaml_path = os.path.join(config_dir, AUTOMATION_CONFIG_PATH)
    script_yaml_path = os.path.join(config_dir, SCRIPT_CONFIG_PATH)
    scene_yaml_path = os.path.join(config_dir, SCENE_CONFIG_PATH)

    # Writing files with YAML does not create the most human readable results
    # So we're hard coding a YAML template.
    try:
        with open(config_path, "w", encoding="utf8") as config_file:
            config_file.write(DEFAULT_CONFIG)

        if not os.path.isfile(secret_path):
            with open(secret_path, "w", encoding="utf8") as secret_file:
                secret_file.write(DEFAULT_SECRETS)

        with open(version_path, "w", encoding="utf8") as version_file:
            version_file.write(__version__)

        if not os.path.isfile(automation_yaml_path):
            with open(automation_yaml_path, "w", encoding="utf8") as automation_file:
                automation_file.write("[]")

        if not os.path.isfile(script_yaml_path):
            with open(script_yaml_path, "w", encoding="utf8"):
                pass

        if not os.path.isfile(scene_yaml_path):
            with open(scene_yaml_path, "w", encoding="utf8"):
                pass
    except OSError:
        print(  # noqa: T201
            f"Unable to create default configuration file {config_path}"
        )
        return False
    return True


async def async_hass_config_yaml(hass: HomeAssistant) -> dict:
    """Load YAML from a Vioneta Agro configuration file.

    This function allows a component inside the asyncio loop to reload its
    configuration by itself. Include package merge.
    """
    secrets = Secrets(Path(hass.config.config_dir))

    # Not using async_add_executor_job because this is an internal method.
    try:
        config = await hass.loop.run_in_executor(
            None,
            load_yaml_config_file,
            hass.config.path(YAML_CONFIG_FILE),
            secrets,
        )
    except HomeAssistantError as exc:
        if not (base_exc := exc.__cause__) or not isinstance(base_exc, MarkedYAMLError):
            raise

        # Rewrite path to offending YAML file to be relative the hass config dir
        if base_exc.context_mark and base_exc.context_mark.name:
            base_exc.context_mark.name = _relpath(hass, base_exc.context_mark.name)
        if base_exc.problem_mark and base_exc.problem_mark.name:
            base_exc.problem_mark.name = _relpath(hass, base_exc.problem_mark.name)
        raise

    invalid_domains = []
    for key in config:
        try:
            cv.domain_key(key)
        except vol.Invalid as exc:
            suffix = ""
            if annotation := find_annotation(config, exc.path):
                suffix = f" at {_relpath(hass, annotation[0])}, line {annotation[1]}"
            _LOGGER.error("Invalid domain '%s'%s", key, suffix)
            invalid_domains.append(key)
    for invalid_domain in invalid_domains:
        config.pop(invalid_domain)

    core_config = config.get(HOMEASSISTANT_DOMAIN, {})
    try:
        await merge_packages_config(hass, config, core_config.get(CONF_PACKAGES, {}))
    except vol.Invalid as exc:
        suffix = ""
        if annotation := find_annotation(
            config, [HOMEASSISTANT_DOMAIN, CONF_PACKAGES, *exc.path]
        ):
            suffix = f" at {_relpath(hass, annotation[0])}, line {annotation[1]}"
        _LOGGER.error(
            "Invalid package configuration '%s'%s: %s", CONF_PACKAGES, suffix, exc
        )
        core_config[CONF_PACKAGES] = {}

    return config


def load_yaml_config_file(
    config_path: str, secrets: Secrets | None = None
) -> dict[Any, Any]:
    """Parse a YAML configuration file.

    Raises FileNotFoundError or HomeAssistantError.

    This method needs to run in an executor.
    """
    try:
        conf_dict = load_yaml_dict(config_path, secrets)
    except YamlTypeError as exc:
        msg = (
            f"The configuration file {os.path.basename(config_path)} "
            "does not contain a dictionary"
        )
        _LOGGER.error(msg)
        raise HomeAssistantError(msg) from exc

    # Convert values to dictionaries if they are None
    for key, value in conf_dict.items():
        conf_dict[key] = value or {}
    return conf_dict


def process_ha_config_upgrade(hass: HomeAssistant) -> None:
    """Upgrade configuration if necessary.

    This method needs to run in an executor.
    """
    version_path = hass.config.path(VERSION_FILE)

    try:
        with open(version_path, encoding="utf8") as inp:
            conf_version = inp.readline().strip()
    except FileNotFoundError:
        # Last version to not have this file
        conf_version = "0.7.7"

    if conf_version == __version__:
        return

    _LOGGER.info(
        "Upgrading configuration directory from %s to %s", conf_version, __version__
    )

    version_obj = AwesomeVersion(conf_version)

    if version_obj < AwesomeVersion("0.50"):
        # 0.50 introduced persistent deps dir.
        lib_path = hass.config.path("deps")
        if os.path.isdir(lib_path):
            shutil.rmtree(lib_path)

    if version_obj < AwesomeVersion("0.92"):
        # 0.92 moved google/tts.py to google_translate/tts.py
        config_path = hass.config.path(YAML_CONFIG_FILE)

        with open(config_path, encoding="utf-8") as config_file:
            config_raw = config_file.read()

        if TTS_PRE_92 in config_raw:
            _LOGGER.info("Migrating google tts to google_translate tts")
            config_raw = config_raw.replace(TTS_PRE_92, TTS_92)
            try:
                with open(config_path, "w", encoding="utf-8") as config_file:
                    config_file.write(config_raw)
            except OSError:
                _LOGGER.exception("Migrating to google_translate tts failed")

    if version_obj < AwesomeVersion("0.94") and is_docker_env():
        # In 0.94 we no longer install packages inside the deps folder when
        # running inside a Docker container.
        lib_path = hass.config.path("deps")
        if os.path.isdir(lib_path):
            shutil.rmtree(lib_path)

    with open(version_path, "w", encoding="utf8") as outp:
        outp.write(__version__)


@callback
def async_log_schema_error(
    exc: vol.Invalid,
    domain: str,
    config: dict,
    hass: HomeAssistant,
    link: str | None = None,
) -> None:
    """Log a schema validation error."""
    message = format_schema_error(hass, exc, domain, config, link)
    _LOGGER.error(message)


@callback
def async_log_config_validator_error(
    exc: vol.Invalid | HomeAssistantError,
    domain: str,
    config: dict,
    hass: HomeAssistant,
    link: str | None = None,
) -> None:
    """Log an error from a custom config validator."""
    if isinstance(exc, vol.Invalid):
        async_log_schema_error(exc, domain, config, hass, link)
        return

    message = format_homeassistant_error(hass, exc, domain, config, link)
    _LOGGER.error(message, exc_info=exc)


def _get_annotation(item: Any) -> tuple[str, int | str] | None:
    if not hasattr(item, "__config_file__"):
        return None

    return (getattr(item, "__config_file__"), getattr(item, "__line__", "?"))


def _get_by_path(data: dict | list, items: list[Hashable]) -> Any:
    """Access a nested object in root by item sequence.

    Returns None in case of error.
    """
    try:
        return reduce(operator.getitem, items, data)  # type: ignore[arg-type]
    except (KeyError, IndexError, TypeError):
        return None


def find_annotation(
    config: dict | list, path: list[Hashable]
) -> tuple[str, int | str] | None:
    """Find file/line annotation for a node in config pointed to by path.

    If the node pointed to is a dict or list, prefer the annotation for the key in
    the key/value pair defining the dict or list.
    If the node is not annotated, try the parent node.
    """

    def find_annotation_for_key(
        item: dict, path: list[Hashable], tail: Hashable
    ) -> tuple[str, int | str] | None:
        for key in item:
            if key == tail:
                if annotation := _get_annotation(key):
                    return annotation
                break
        return None

    def find_annotation_rec(
        config: dict | list, path: list[Hashable], tail: Hashable | None
    ) -> tuple[str, int | str] | None:
        item = _get_by_path(config, path)
        if isinstance(item, dict) and tail is not None:
            if tail_annotation := find_annotation_for_key(item, path, tail):
                return tail_annotation

        if (
            isinstance(item, (dict, list))
            and path
            and (
                key_annotation := find_annotation_for_key(
                    _get_by_path(config, path[:-1]), path[:-1], path[-1]
                )
            )
        ):
            return key_annotation

        if annotation := _get_annotation(item):
            return annotation

        if not path:
            return None

        tail = path.pop()
        if annotation := find_annotation_rec(config, path, tail):
            return annotation
        return _get_annotation(item)

    return find_annotation_rec(config, list(path), None)


def _relpath(hass: HomeAssistant, path: str) -> str:
    """Return path relative to the Vioneta Agro config dir."""
    return os.path.relpath(path, hass.config.config_dir)


def stringify_invalid(
    hass: HomeAssistant,
    exc: vol.Invalid,
    domain: str,
    config: dict,
    link: str | None,
    max_sub_error_length: int,
) -> str:
    """Stringify voluptuous.Invalid.

    This is an alternative to the custom __str__ implemented in
    voluptuous.error.Invalid. The modifications are:
    - Format the path delimited by -> instead of @data[]
    - Prefix with domain, file and line of the error
    - Suffix with a link to the documentation
    - Give a more user friendly output for unknown options
    - Give a more user friendly output for missing options
    """
    if "." in domain:
        integration_domain, _, platform_domain = domain.partition(".")
        message_prefix = (
            f"Invalid config for '{platform_domain}' from integration "
            f"'{integration_domain}'"
        )
    else:
        message_prefix = f"Invalid config for '{domain}'"
    if domain != HOMEASSISTANT_DOMAIN and link:
        message_suffix = f", please check the docs at {link}"
    else:
        message_suffix = ""
    if annotation := find_annotation(config, exc.path):
        message_prefix += f" at {_relpath(hass, annotation[0])}, line {annotation[1]}"
    path = "->".join(str(m) for m in exc.path)
    if exc.error_message == "extra keys not allowed":
        return (
            f"{message_prefix}: '{exc.path[-1]}' is an invalid option for '{domain}', "
            f"check: {path}{message_suffix}"
        )
    if exc.error_message == "required key not provided":
        return (
            f"{message_prefix}: required key '{exc.path[-1]}' not provided"
            f"{message_suffix}"
        )
    # This function is an alternative to the stringification done by
    # vol.Invalid.__str__, so we need to call Exception.__str__ here
    # instead of str(exc)
    output = Exception.__str__(exc)
    if error_type := exc.error_type:
        output += " for " + error_type
    offending_item_summary = repr(_get_by_path(config, exc.path))
    if len(offending_item_summary) > max_sub_error_length:
        offending_item_summary = (
            f"{offending_item_summary[: max_sub_error_length - 3]}..."
        )
    return (
        f"{message_prefix}: {output} '{path}', got {offending_item_summary}"
        f"{message_suffix}"
    )


def humanize_error(
    hass: HomeAssistant,
    validation_error: vol.Invalid,
    domain: str,
    config: dict,
    link: str | None,
    max_sub_error_length: int = MAX_VALIDATION_ERROR_ITEM_LENGTH,
) -> str:
    """Provide a more helpful + complete validation error message.

    This is a modified version of voluptuous.error.Invalid.__str__,
    the modifications make some minor changes to the formatting.
    """
    if isinstance(validation_error, vol.MultipleInvalid):
        return "\n".join(
            sorted(
                humanize_error(
                    hass, sub_error, domain, config, link, max_sub_error_length
                )
                for sub_error in validation_error.errors
            )
        )
    return stringify_invalid(
        hass, validation_error, domain, config, link, max_sub_error_length
    )


@callback
def format_homeassistant_error(
    hass: HomeAssistant,
    exc: HomeAssistantError,
    domain: str,
    config: dict,
    link: str | None = None,
) -> str:
    """Format HomeAssistantError thrown by a custom config validator."""
    if "." in domain:
        integration_domain, _, platform_domain = domain.partition(".")
        message_prefix = (
            f"Invalid config for '{platform_domain}' from integration "
            f"'{integration_domain}'"
        )
    else:
        message_prefix = f"Invalid config for '{domain}'"
    # HomeAssistantError raised by custom config validator has no path to the
    # offending configuration key, use the domain key as path instead.
    if annotation := find_annotation(config, [domain]):
        message_prefix += f" at {_relpath(hass, annotation[0])}, line {annotation[1]}"
    message = f"{message_prefix}: {str(exc) or repr(exc)}"
    if domain != HOMEASSISTANT_DOMAIN and link:
        message += f", please check the docs at {link}"

    return message


@callback
def format_schema_error(
    hass: HomeAssistant,
    exc: vol.Invalid,
    domain: str,
    config: dict,
    link: str | None = None,
) -> str:
    """Format configuration validation error."""
    return humanize_error(hass, exc, domain, config, link)


async def async_process_ha_core_config(hass: HomeAssistant, config: dict) -> None:
    """Process the [homeassistant] section from the configuration.

    This method is a coroutine.
    """
    config = CORE_CONFIG_SCHEMA(config)

    # Only load auth during startup.
    if not hasattr(hass, "auth"):
        if (auth_conf := config.get(CONF_AUTH_PROVIDERS)) is None:
            auth_conf = [{"type": "homeassistant"}]

        mfa_conf = config.get(
            CONF_AUTH_MFA_MODULES,
            [{"type": "totp", "id": "totp", "name": "Authenticator app"}],
        )

        setattr(
            hass, "auth", await auth.auth_manager_from_config(hass, auth_conf, mfa_conf)
        )

    await hass.config.async_load()

    hac = hass.config

    if any(
        k in config
        for k in (
            CONF_LATITUDE,
            CONF_LONGITUDE,
            CONF_NAME,
            CONF_ELEVATION,
            CONF_TIME_ZONE,
            CONF_UNIT_SYSTEM,
            CONF_EXTERNAL_URL,
            CONF_INTERNAL_URL,
            CONF_CURRENCY,
            CONF_COUNTRY,
            CONF_LANGUAGE,
            CONF_RADIUS,
        )
    ):
        hac.config_source = ConfigSource.YAML

    for key, attr in (
        (CONF_LATITUDE, "latitude"),
        (CONF_LONGITUDE, "longitude"),
        (CONF_NAME, "location_name"),
        (CONF_ELEVATION, "elevation"),
        (CONF_INTERNAL_URL, "internal_url"),
        (CONF_EXTERNAL_URL, "external_url"),
        (CONF_MEDIA_DIRS, "media_dirs"),
        (CONF_CURRENCY, "currency"),
        (CONF_COUNTRY, "country"),
        (CONF_LANGUAGE, "language"),
        (CONF_RADIUS, "radius"),
    ):
        if key in config:
            setattr(hac, attr, config[key])

    if config.get(CONF_DEBUG):
        hac.debug = True

    _raise_issue_if_historic_currency(hass, hass.config.currency)
    _raise_issue_if_no_country(hass, hass.config.country)

    if CONF_TIME_ZONE in config:
        await hac.async_set_time_zone(config[CONF_TIME_ZONE])

    if CONF_MEDIA_DIRS not in config:
        if is_docker_env():
            hac.media_dirs = {"local": "/media"}
        else:
            hac.media_dirs = {"local": hass.config.path("media")}

    # Init whitelist external dir
    hac.allowlist_external_dirs = {hass.config.path("www"), *hac.media_dirs.values()}
    if CONF_ALLOWLIST_EXTERNAL_DIRS in config:
        hac.allowlist_external_dirs.update(set(config[CONF_ALLOWLIST_EXTERNAL_DIRS]))

    elif LEGACY_CONF_WHITELIST_EXTERNAL_DIRS in config:
        _LOGGER.warning(
            "Key %s has been replaced with %s. Please update your config",
            LEGACY_CONF_WHITELIST_EXTERNAL_DIRS,
            CONF_ALLOWLIST_EXTERNAL_DIRS,
        )
        hac.allowlist_external_dirs.update(
            set(config[LEGACY_CONF_WHITELIST_EXTERNAL_DIRS])
        )

    # Init whitelist external URL list – make sure to add / to every URL that doesn't
    # already have it so that we can properly test "path ownership"
    if CONF_ALLOWLIST_EXTERNAL_URLS in config:
        hac.allowlist_external_urls.update(
            url if url.endswith("/") else f"{url}/"
            for url in config[CONF_ALLOWLIST_EXTERNAL_URLS]
        )

    # Customize
    cust_exact = dict(config[CONF_CUSTOMIZE])
    cust_domain = dict(config[CONF_CUSTOMIZE_DOMAIN])
    cust_glob = OrderedDict(config[CONF_CUSTOMIZE_GLOB])

    for name, pkg in config[CONF_PACKAGES].items():
        if (pkg_cust := pkg.get(HOMEASSISTANT_DOMAIN)) is None:
            continue

        try:
            pkg_cust = CUSTOMIZE_CONFIG_SCHEMA(pkg_cust)
        except vol.Invalid:
            _LOGGER.warning("Package %s contains invalid customize", name)
            continue

        cust_exact.update(pkg_cust[CONF_CUSTOMIZE])
        cust_domain.update(pkg_cust[CONF_CUSTOMIZE_DOMAIN])
        cust_glob.update(pkg_cust[CONF_CUSTOMIZE_GLOB])

    hass.data[DATA_CUSTOMIZE] = EntityValues(cust_exact, cust_domain, cust_glob)

    if CONF_UNIT_SYSTEM in config:
        hac.units = get_unit_system(config[CONF_UNIT_SYSTEM])


def _log_pkg_error(
    hass: HomeAssistant, package: str, component: str | None, config: dict, message: str
) -> None:
    """Log an error while merging packages."""
    message_prefix = f"Setup of package '{package}'"
    if annotation := find_annotation(
        config, [HOMEASSISTANT_DOMAIN, CONF_PACKAGES, package]
    ):
        message_prefix += f" at {_relpath(hass, annotation[0])}, line {annotation[1]}"

    _LOGGER.error("%s failed: %s", message_prefix, message)


def _identify_config_schema(module: ComponentProtocol) -> str | None:
    """Extract the schema and identify list or dict based."""
    if not isinstance(module.CONFIG_SCHEMA, vol.Schema):
        return None  # type: ignore[unreachable]

    schema = module.CONFIG_SCHEMA.schema

    if isinstance(schema, vol.All):
        for subschema in schema.validators:
            if isinstance(subschema, dict):
                schema = subschema
                break
        else:
            return None

    try:
        key = next(k for k in schema if k == module.DOMAIN)
    except (TypeError, AttributeError, StopIteration):
        return None
    except Exception:
        _LOGGER.exception("Unexpected error identifying config schema")
        return None

    if hasattr(key, "default") and not isinstance(
        key.default, vol.schema_builder.Undefined
    ):
        default_value = module.CONFIG_SCHEMA({module.DOMAIN: key.default()})[
            module.DOMAIN
        ]

        if isinstance(default_value, dict):
            return "dict"

        if isinstance(default_value, list):
            return "list"

        return None

    domain_schema = schema[key]

    t_schema = str(domain_schema)
    if t_schema.startswith("{") or "schema_with_slug_keys" in t_schema:
        return "dict"
    if t_schema.startswith(("[", "All(<function ensure_list")):
        return "list"
    return None


def _validate_package_definition(name: str, conf: Any) -> None:
    """Validate basic package definition properties."""
    cv.slug(name)
    PACKAGE_DEFINITION_SCHEMA(conf)


def _recursive_merge(conf: dict[str, Any], package: dict[str, Any]) -> str | None:
    """Merge package into conf, recursively."""
    duplicate_key: str | None = None
    for key, pack_conf in package.items():
        if isinstance(pack_conf, dict):
            if not pack_conf:
                continue
            conf[key] = conf.get(key, OrderedDict())
            duplicate_key = _recursive_merge(conf=conf[key], package=pack_conf)

        elif isinstance(pack_conf, list):
            conf[key] = cv.remove_falsy(
                cv.ensure_list(conf.get(key)) + cv.ensure_list(pack_conf)
            )

        else:
            if conf.get(key) is not None:
                return key
            conf[key] = pack_conf
    return duplicate_key


async def merge_packages_config(
    hass: HomeAssistant,
    config: dict,
    packages: dict[str, Any],
    _log_pkg_error: Callable[
        [HomeAssistant, str, str | None, dict, str], None
    ] = _log_pkg_error,
) -> dict:
    """Merge packages into the top-level configuration.

    Ignores packages that cannot be setup. Mutates config. Raises
    vol.Invalid if whole package config is invalid.
    """

    PACKAGES_CONFIG_SCHEMA(packages)

    invalid_packages = []
    for pack_name, pack_conf in packages.items():
        try:
            _validate_package_definition(pack_name, pack_conf)
        except vol.Invalid as exc:
            _log_pkg_error(
                hass,
                pack_name,
                None,
                config,
                f"Invalid package definition '{pack_name}': {exc!s}. Package "
                f"will not be initialized",
            )
            invalid_packages.append(pack_name)
            continue

        for comp_name, comp_conf in pack_conf.items():
            if comp_name == HOMEASSISTANT_DOMAIN:
                continue
            try:
                domain = cv.domain_key(comp_name)
            except vol.Invalid:
                _log_pkg_error(
                    hass, pack_name, comp_name, config, f"Invalid domain '{comp_name}'"
                )
                continue

            try:
                integration = await async_get_integration_with_requirements(
                    hass, domain
                )
                component = await integration.async_get_component()
            except LOAD_EXCEPTIONS as exc:
                _log_pkg_error(
                    hass,
                    pack_name,
                    comp_name,
                    config,
                    f"Integration {comp_name} caused error: {exc!s}",
                )
                continue
            except INTEGRATION_LOAD_EXCEPTIONS as exc:
                _log_pkg_error(hass, pack_name, comp_name, config, str(exc))
                continue

            try:
                config_platform: (
                    ModuleType | None
                ) = await integration.async_get_platform("config")
                # Test if config platform has a config validator
                if not hasattr(config_platform, "async_validate_config"):
                    config_platform = None
            except ImportError:
                config_platform = None

            merge_list = False

            # If integration has a custom config validator, it needs to provide a hint.
            if config_platform is not None:
                merge_list = config_platform.PACKAGE_MERGE_HINT == "list"

            if not merge_list:
                merge_list = hasattr(component, "PLATFORM_SCHEMA")

            if not merge_list and hasattr(component, "CONFIG_SCHEMA"):
                merge_list = _identify_config_schema(component) == "list"

            if merge_list:
                config[comp_name] = cv.remove_falsy(
                    cv.ensure_list(config.get(comp_name)) + cv.ensure_list(comp_conf)
                )
                continue

            if comp_conf is None:
                comp_conf = OrderedDict()

            if not isinstance(comp_conf, dict):
                _log_pkg_error(
                    hass,
                    pack_name,
                    comp_name,
                    config,
                    f"integration '{comp_name}' cannot be merged, expected a dict",
                )
                continue

            if comp_name not in config or config[comp_name] is None:
                config[comp_name] = OrderedDict()

            if not isinstance(config[comp_name], dict):
                _log_pkg_error(
                    hass,
                    pack_name,
                    comp_name,
                    config,
                    (
                        f"integration '{comp_name}' cannot be merged, dict expected in "
                        "main config"
                    ),
                )
                continue

            duplicate_key = _recursive_merge(conf=config[comp_name], package=comp_conf)
            if duplicate_key:
                _log_pkg_error(
                    hass,
                    pack_name,
                    comp_name,
                    config,
                    f"integration '{comp_name}' has duplicate key '{duplicate_key}'",
                )

    for pack_name in invalid_packages:
        packages.pop(pack_name, {})

    return config


@callback
def _get_log_message_and_stack_print_pref(
    hass: HomeAssistant, domain: str, platform_exception: ConfigExceptionInfo
) -> tuple[str | None, bool, dict[str, str]]:
    """Get message to log and print stack trace preference."""
    exception = platform_exception.exception
    platform_path = platform_exception.platform_path
    platform_config = platform_exception.config
    link = platform_exception.integration_link

    placeholders: dict[str, str] = {
        "domain": domain,
        "error": str(exception),
        "p_name": platform_path,
    }

    show_stack_trace: bool | None = _CONFIG_LOG_SHOW_STACK_TRACE.get(
        platform_exception.translation_key
    )
    if show_stack_trace is None:
        # If no pre defined log_message is set, we generate an enriched error
        # message, so we can notify about it during setup
        show_stack_trace = False
        if isinstance(exception, vol.Invalid):
            log_message = format_schema_error(
                hass, exception, platform_path, platform_config, link
            )
            if annotation := find_annotation(platform_config, exception.path):
                placeholders["config_file"], line = annotation
                placeholders["line"] = str(line)
        else:
            if TYPE_CHECKING:
                assert isinstance(exception, HomeAssistantError)
            log_message = format_homeassistant_error(
                hass, exception, platform_path, platform_config, link
            )
            if annotation := find_annotation(platform_config, [platform_path]):
                placeholders["config_file"], line = annotation
                placeholders["line"] = str(line)
            show_stack_trace = True
        return (log_message, show_stack_trace, placeholders)

    # Generate the log message from the English translations
    log_message = async_get_exception_message(
        HOMEASSISTANT_DOMAIN,
        platform_exception.translation_key,
        translation_placeholders=placeholders,
    )

    return (log_message, show_stack_trace, placeholders)


async def async_process_component_and_handle_errors(
    hass: HomeAssistant,
    config: ConfigType,
    integration: Integration,
    raise_on_failure: bool = False,
) -> ConfigType | None:
    """Process and component configuration and handle errors.

    In case of errors:
    - Print the error messages to the log.
    - Raise a ConfigValidationError if raise_on_failure is set.

    Returns the integration config or `None`.
    """
    integration_config_info = await async_process_component_config(
        hass, config, integration
    )
    async_handle_component_errors(
        hass, integration_config_info, integration, raise_on_failure
    )
    return async_drop_config_annotations(integration_config_info, integration)


@callback
def async_drop_config_annotations(
    integration_config_info: IntegrationConfigInfo,
    integration: Integration,
) -> ConfigType | None:
    """Remove file and line annotations from str items in component configuration."""
    if (config := integration_config_info.config) is None:
        return None

    def drop_config_annotations_rec(node: Any) -> Any:
        if isinstance(node, dict):
            # Some integrations store metadata in custom dict classes, preserve those
            tmp = dict(node)
            node.clear()
            node.update(
                (drop_config_annotations_rec(k), drop_config_annotations_rec(v))
                for k, v in tmp.items()
            )
            return node

        if isinstance(node, list):
            return [drop_config_annotations_rec(v) for v in node]

        if isinstance(node, NodeStrClass):
            return str(node)

        return node

    # Don't drop annotations from the homeassistant integration because it may
    # have configuration for other integrations as packages.
    if integration.domain in config and integration.domain != HOMEASSISTANT_DOMAIN:
        drop_config_annotations_rec(config[integration.domain])
    return config


@callback
def async_handle_component_errors(
    hass: HomeAssistant,
    integration_config_info: IntegrationConfigInfo,
    integration: Integration,
    raise_on_failure: bool = False,
) -> None:
    """Handle component configuration errors from async_process_component_config.

    In case of errors:
    - Print the error messages to the log.
    - Raise a ConfigValidationError if raise_on_failure is set.
    """

    if not (config_exception_info := integration_config_info.exception_info_list):
        return

    platform_exception: ConfigExceptionInfo
    domain = integration.domain
    placeholders: dict[str, str]
    for platform_exception in config_exception_info:
        exception = platform_exception.exception
        (
            log_message,
            show_stack_trace,
            placeholders,
        ) = _get_log_message_and_stack_print_pref(hass, domain, platform_exception)
        _LOGGER.error(
            log_message,
            exc_info=exception if show_stack_trace else None,
        )

    if not raise_on_failure:
        return

    if len(config_exception_info) == 1:
        translation_key = platform_exception.translation_key
    else:
        translation_key = ConfigErrorTranslationKey.MULTIPLE_INTEGRATION_CONFIG_ERRORS
        errors = str(len(config_exception_info))
        placeholders = {
            "domain": domain,
            "errors": errors,
        }
    raise ConfigValidationError(
        translation_key,
        [platform_exception.exception for platform_exception in config_exception_info],
        translation_domain=HOMEASSISTANT_DOMAIN,
        translation_placeholders=placeholders,
    )


def config_per_platform(
    config: ConfigType, domain: str
) -> Iterable[tuple[str | None, ConfigType]]:
    """Break a component config into different platforms.

    For example, will find 'switch', 'switch 2', 'switch 3', .. etc
    Async friendly.
    """
    for config_key in extract_domain_configs(config, domain):
        if not (platform_config := config[config_key]):
            continue

        if not isinstance(platform_config, list):
            platform_config = [platform_config]

        item: ConfigType
        platform: str | None
        for item in platform_config:
            try:
                platform = item.get(CONF_PLATFORM)
            except AttributeError:
                platform = None

            yield platform, item


def extract_platform_integrations(
    config: ConfigType, domains: set[str]
) -> dict[str, set[str]]:
    """Find all the platforms in a configuration.

    Returns a dictionary with domain as key and a set of platforms as value.
    """
    platform_integrations: dict[str, set[str]] = {}
    for key, domain_config in config.items():
        try:
            domain = cv.domain_key(key)
        except vol.Invalid:
            continue
        if domain not in domains:
            continue

        if not isinstance(domain_config, list):
            domain_config = [domain_config]

        for item in domain_config:
            try:
                platform = item.get(CONF_PLATFORM)
            except AttributeError:
                continue
            if platform and isinstance(platform, Hashable):
                platform_integrations.setdefault(domain, set()).add(platform)
    return platform_integrations


def extract_domain_configs(config: ConfigType, domain: str) -> Sequence[str]:
    """Extract keys from config for given domain name.

    Async friendly.
    """
    domain_configs = []
    for key in config:
        with suppress(vol.Invalid):
            if cv.domain_key(key) != domain:
                continue
            domain_configs.append(key)
    return domain_configs


@dataclass(slots=True)
class _PlatformIntegration:
    """Class to hold platform integration information."""

    path: str  # integration.platform; ex: filter.sensor
    name: str  # integration; ex: filter
    integration: Integration  # <Integration filter>
    config: ConfigType  # un-validated config
    validated_config: ConfigType  # component validated config


async def _async_load_and_validate_platform_integration(
    domain: str,
    integration_docs: str | None,
    config_exceptions: list[ConfigExceptionInfo],
    p_integration: _PlatformIntegration,
) -> ConfigType | None:
    """Load a platform integration and validate its config."""
    try:
        platform = await p_integration.integration.async_get_platform(domain)
    except LOAD_EXCEPTIONS as exc:
        exc_info = ConfigExceptionInfo(
            exc,
            ConfigErrorTranslationKey.PLATFORM_COMPONENT_LOAD_EXC,
            p_integration.path,
            p_integration.config,
            integration_docs,
        )
        config_exceptions.append(exc_info)
        return None

    # If the platform does not have a config schema
    # the top level component validated schema will be used
    if not hasattr(platform, "PLATFORM_SCHEMA"):
        return p_integration.validated_config

    # Validate platform specific schema
    try:
        return platform.PLATFORM_SCHEMA(p_integration.config)  # type: ignore[no-any-return]
    except vol.Invalid as exc:
        exc_info = ConfigExceptionInfo(
            exc,
            ConfigErrorTranslationKey.PLATFORM_CONFIG_VALIDATION_ERR,
            p_integration.path,
            p_integration.config,
            p_integration.integration.documentation,
        )
        config_exceptions.append(exc_info)
    except Exception as exc:  # noqa: BLE001
        exc_info = ConfigExceptionInfo(
            exc,
            ConfigErrorTranslationKey.PLATFORM_SCHEMA_VALIDATOR_ERR,
            p_integration.name,
            p_integration.config,
            p_integration.integration.documentation,
        )
        config_exceptions.append(exc_info)

    return None


async def async_process_component_config(
    hass: HomeAssistant,
    config: ConfigType,
    integration: Integration,
    component: ComponentProtocol | None = None,
) -> IntegrationConfigInfo:
    """Check component configuration.

    Returns processed configuration and exception information.

    This method must be run in the event loop.
    """
    domain = integration.domain
    integration_docs = integration.documentation
    config_exceptions: list[ConfigExceptionInfo] = []

    if not component:
        try:
            component = await integration.async_get_component()
        except LOAD_EXCEPTIONS as exc:
            exc_info = ConfigExceptionInfo(
                exc,
                ConfigErrorTranslationKey.COMPONENT_IMPORT_ERR,
                domain,
                config,
                integration_docs,
            )
            config_exceptions.append(exc_info)
            return IntegrationConfigInfo(None, config_exceptions)

    # Check if the integration has a custom config validator
    config_validator = None
    # A successful call to async_get_component will prime
    # the cache for platforms_exists to ensure it does no
    # blocking I/O
    if integration.platforms_exists(("config",)):
        # If the config platform cannot possibly exist, don't try to load it.
        try:
            config_validator = await integration.async_get_platform("config")
        except ImportError as err:
            # Filter out import error of the config platform.
            # If the config platform contains bad imports, make sure
            # that still fails.
            if err.name != f"{integration.pkg_path}.config":
                exc_info = ConfigExceptionInfo(
                    err,
                    ConfigErrorTranslationKey.CONFIG_PLATFORM_IMPORT_ERR,
                    domain,
                    config,
                    integration_docs,
                )
                config_exceptions.append(exc_info)
                return IntegrationConfigInfo(None, config_exceptions)

    if config_validator is not None and hasattr(
        config_validator, "async_validate_config"
    ):
        try:
            return IntegrationConfigInfo(
                await config_validator.async_validate_config(hass, config), []
            )
        except (vol.Invalid, HomeAssistantError) as exc:
            exc_info = ConfigExceptionInfo(
                exc,
                ConfigErrorTranslationKey.CONFIG_VALIDATION_ERR,
                domain,
                config,
                integration_docs,
            )
            config_exceptions.append(exc_info)
            return IntegrationConfigInfo(None, config_exceptions)
        except Exception as exc:  # noqa: BLE001
            exc_info = ConfigExceptionInfo(
                exc,
                ConfigErrorTranslationKey.CONFIG_VALIDATOR_UNKNOWN_ERR,
                domain,
                config,
                integration_docs,
            )
            config_exceptions.append(exc_info)
            return IntegrationConfigInfo(None, config_exceptions)

    # No custom config validator, proceed with schema validation
    if hasattr(component, "CONFIG_SCHEMA"):
        try:
            return IntegrationConfigInfo(component.CONFIG_SCHEMA(config), [])
        except vol.Invalid as exc:
            exc_info = ConfigExceptionInfo(
                exc,
                ConfigErrorTranslationKey.CONFIG_VALIDATION_ERR,
                domain,
                config,
                integration_docs,
            )
            config_exceptions.append(exc_info)
            return IntegrationConfigInfo(None, config_exceptions)
        except Exception as exc:  # noqa: BLE001
            exc_info = ConfigExceptionInfo(
                exc,
                ConfigErrorTranslationKey.CONFIG_SCHEMA_UNKNOWN_ERR,
                domain,
                config,
                integration_docs,
            )
            config_exceptions.append(exc_info)
            return IntegrationConfigInfo(None, config_exceptions)

    component_platform_schema = getattr(
        component, "PLATFORM_SCHEMA_BASE", getattr(component, "PLATFORM_SCHEMA", None)
    )

    if component_platform_schema is None:
        return IntegrationConfigInfo(config, [])

    platform_integrations_to_load: list[_PlatformIntegration] = []
    platforms: list[ConfigType] = []
    for p_name, p_config in config_per_platform(config, domain):
        # Validate component specific platform schema
        platform_path = f"{p_name}.{domain}"
        try:
            p_validated = component_platform_schema(p_config)
        except vol.Invalid as exc:
            exc_info = ConfigExceptionInfo(
                exc,
                ConfigErrorTranslationKey.PLATFORM_CONFIG_VALIDATION_ERR,
                domain,
                p_config,
                integration_docs,
            )
            config_exceptions.append(exc_info)
            continue
        except Exception as exc:  # noqa: BLE001
            exc_info = ConfigExceptionInfo(
                exc,
                ConfigErrorTranslationKey.PLATFORM_SCHEMA_VALIDATOR_ERR,
                str(p_name),
                config,
                integration_docs,
            )
            config_exceptions.append(exc_info)
            continue

        # Not all platform components follow same pattern for platforms
        # So if p_name is None we are not going to validate platform
        # (the automation component is one of them)
        if p_name is None:
            platforms.append(p_validated)
            continue

        try:
            p_integration = await async_get_integration_with_requirements(hass, p_name)
        except (RequirementsNotFound, IntegrationNotFound) as exc:
            exc_info = ConfigExceptionInfo(
                exc,
                ConfigErrorTranslationKey.PLATFORM_COMPONENT_LOAD_ERR,
                platform_path,
                p_config,
                integration_docs,
            )
            config_exceptions.append(exc_info)
            continue

        platform_integration = _PlatformIntegration(
            platform_path, p_name, p_integration, p_config, p_validated
        )
        platform_integrations_to_load.append(platform_integration)

    #
    # Since bootstrap will order base platform (ie sensor) integrations
    # first, we eagerly gather importing the platforms that need to be
    # validated for the base platform since everything that uses the
    # base platform has to wait for it to finish.
    #
    # For example if `hue` where to load first and than called
    # `async_forward_entry_setup` for the `sensor` platform it would have to
    # wait for the sensor platform to finish loading before it could continue.
    # Since the base `sensor` platform must also import all of its platform
    # integrations to do validation before it can finish setup, its important
    # that the platform integrations are imported first so we do not waste
    # time importing `hue` first when we could have been importing the platforms
    # that the base `sensor` platform need to load to do validation and allow
    # all integrations that need the base `sensor` platform to proceed with setup.
    #
    if platform_integrations_to_load:
        async_load_and_validate = partial(
            _async_load_and_validate_platform_integration,
            domain,
            integration_docs,
            config_exceptions,
        )
        platforms.extend(
            validated_config
            for validated_config in await asyncio.gather(
                *(
                    create_eager_task(
                        async_load_and_validate(p_integration), loop=hass.loop
                    )
                    for p_integration in platform_integrations_to_load
                )
            )
            if validated_config is not None
        )

    # Create a copy of the configuration with all config for current
    # component removed and add validated config back in.
    config = config_without_domain(config, domain)
    config[domain] = platforms

    return IntegrationConfigInfo(config, config_exceptions)


@callback
def config_without_domain(config: ConfigType, domain: str) -> ConfigType:
    """Return a config with all configuration for a domain removed."""
    filter_keys = extract_domain_configs(config, domain)
    return {key: value for key, value in config.items() if key not in filter_keys}


async def async_check_ha_config_file(hass: HomeAssistant) -> str | None:
    """Check if Vioneta Agro configuration file is valid.

    This method is a coroutine.
    """
    # pylint: disable-next=import-outside-toplevel
    from .helpers import check_config

    res = await check_config.async_check_ha_config_file(hass)

    if not res.errors:
        return None
    return res.error_str


def safe_mode_enabled(config_dir: str) -> bool:
    """Return if safe mode is enabled.

    If safe mode is enabled, the safe mode file will be removed.
    """
    safe_mode_path = os.path.join(config_dir, SAFE_MODE_FILENAME)
    safe_mode = os.path.exists(safe_mode_path)
    if safe_mode:
        os.remove(safe_mode_path)
    return safe_mode


async def async_enable_safe_mode(hass: HomeAssistant) -> None:
    """Enable safe mode."""

    def _enable_safe_mode() -> None:
        Path(hass.config.path(SAFE_MODE_FILENAME)).touch()

    await hass.async_add_executor_job(_enable_safe_mode)
