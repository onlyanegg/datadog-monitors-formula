{%- import_yaml 'datadog-monitors/defaults.yaml' as datadog-monitors_defaults -%}
{%- set datadog-monitors_pillar = salt.pillar.get('datadog-monitors', {}) %}
{%- set datadog-monitors_grains = salt.grains.get('datadog-monitors', {}) %}

{%- set datadog-monitors = datadog-monitors_defaults.datadog-monitors %}
{%- do salt.slsutil.update(datadog-monitors, datadog-monitors_pillar) %}
{%- do salt.slsutil.update(datadog-monitors, datadog-monitors_grains) %}
