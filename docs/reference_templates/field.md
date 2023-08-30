## `{{ field.alias }}` ### {: .purple .mb-0 }

{% if field.provider %}

backend: `{{ field.provider }}`
{: .purple .mb-0 }

{% endif %}

type: `{{ field.type_hint }}`
{: .purple .my-0 }

{% if field.required %}

required
{: .green .my-0 }

{% else %}

default: `{{ field.default }}`
{: .green .mt-0 }

{% endif %}

{{ field.description | replace("\n", "<br>") }}
{: .pl-2 }
