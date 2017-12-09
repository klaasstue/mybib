{% from 'render_gallery.macro' import render_gallery %}

{{ render_gallery( entries ) }}

{% if pagination %}

  {% from 'render_pagination.macro' import render_pagination %}

  {{ render_pagination( pagination ) }}

{% endif %}
