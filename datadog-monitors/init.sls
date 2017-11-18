{% from 'datadog-monitors/settings.sls' import datadog_monitors with context -%}

{%- if datadog_monitors.manage_completely | lower() == 'true' %}
  {%- set goal_monitor_list = datadog_monitors.monitors.keys() %}
  {%- set current_monitor_list = salt['datadog.get_all_monitors'](
      api_key=datadog_monitors.api_key,
      app_key=datadog_monitors.app_key
    )
  %}

  {%- set remove_monitor_list = [] %}
  {%- for monitor in current_monitor_list %}
    {%- if monitor not in goal_monitor_list %}
      {%- do remove_monitor_list.update(monitor) %}
    {%- endif %}
  {%- endfor %}

  {%- for monitor in remove_monitor_list %}
{{ monitor }}_monitor_absent:
  datadog.monitor_absent:
    - name: {{ monitor }}
    - api_key: {{ datadog_monitors.api_key }}
    - app_key: {{ datadog_monitors.app_key }}
  {%- endfor %}
{%- endif %}

{%- for monitor, attributes in datadog_monitors.monitors.iteritems() %}
{{ monitor }}_monitor_managed:
  datadog.monitor_managed:
    - name: '{{ monitor }}'
    - api_key: {{ datadog_monitors.api_key }}
    - app_key: {{ datadog_monitors.app_key }}
    - type: '{{ attributes.type }}'
    - query: {{ attributes.query }}
    - message: '{{ attributes.message | default('') }}'
    - options: {{ attributes.options | default({}) }}
    - tags: {{ attributes.tags | default([]) }}
{%- endfor %}
