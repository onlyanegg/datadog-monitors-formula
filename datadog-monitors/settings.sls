{%- import_yaml 'datadog-monitors/defaults.yaml' as datadog_monitors_defaults -%}
{%- set datadog_monitors_pillar = salt.pillar.get('datadog_monitors', {}) %}
{%- set datadog_monitors_grains = salt.grains.get('datadog_monitors', {}) %}

{%- set datadog_monitors = datadog_monitors_defaults.datadog_monitors %}
{%- do salt.slsutil.update(datadog_monitors, datadog_monitors_pillar) %}
{%- do salt.slsutil.update(datadog_monitors, datadog_monitors_grains) %}
