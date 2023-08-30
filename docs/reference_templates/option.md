### `{{ option.config_key }}` ### {: .purple .mb-0 }

`{{ option.comma_separated_display_args }}`
{: .purple .my-0 }

`{{ option.env_var }}`
{: .purple .mt-0}

{% if option.comma_separated_choices %}
one of: `{{ option.comma_separated_choices }}`
{: .green .pl-2 .mb-0 }
{% endif %}

{% set default_value = option.default | help_str %}
{% if "\n" in default_value %}

default:
{: .green .pl-2 .my-0 }

{#
The first class is supposed to be the language,
but this isn't really associated with a lang,
so `.unused` it is!
#}

```{ .unused .pl-2 .my-0 .green .no-copy }
{{ option.default | help_str }}
```

{% else %}

default: `{{ default_value }}`
{: .green .pl-2 .my-0 }

{% endif %}

{% if option.deprecated_message %}

{{ option.deprecated_message }}
{: .red .pl-2 .my-0 }

{{ option.removal_hint }}
{: .red .pl-2 .my-0 }

{% endif %}

{{ option.help | replace("\n", "<br>") }}
{: .pl-2 }

{% if option.target_field_name %}
Can be overridden by field `{{ option.target_field_name }}` on `local_environment`, `docker_environment`, or `remote_environment` targets.
{: .blue .pl-2 }

{% endif %}
