# {{ subsystem.scope | default("Global options", true) }}

---

{% if subsystem.is_goal%}

```
pants {{ subsystem.scope }} [args]
```

{% endif %}
{{ subsystem.description }}

Backend: <span style="color: purple"><code>{{ subsystem.provider }}</code></span>
<br>
Config section: <span style="color: purple"><code>[{{ subsystem.scope | default("GLOBAL", true) }}]</code></span>

## Basic options

{% for option in subsystem.basic %}

    {%- include 'option.md' %}

{% else -%}

    None

{% endfor %}

## Advanced options

{% for option in subsystem.advanced %}

    {%- include 'option.md' %}

{% else -%}

    None

{% endfor %}

## Deprecated options

{% for option in subsystem.deprecated %}

    {%- include 'option.md' %}

{% else -%}

    None

{% endfor %}

{% set related_subsystems = goal_info.consumed_scopes | filter_out("", subsystem.scope) | sort  %}

{% if related_subsystems %}

## Related subsystems

{% for subsystem in related_subsystems %}

{% if subsystem is goal_subsystem %}

- [{{ subsystem }}](../goals/{{ subsystem }}.md)

{% else %}

- [{{ subsystem }}](../subsystems/{{ subsystem }}.md)

{% endif %}

{% endfor %}

{% endif %}
