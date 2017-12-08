<!-- Slide Content -->

<div class="wrapper">

	  {% for item in entries %}
			
		    <div class="card">
		      <img class="thumbnail" src="{{ url_for('download', filename=item['path'], imgId=item['pk']) }}">

          <p class="caption"><a href="{{url_for( 'download', filename=item['file'], bookId=item['pk'])}}">
            <img class="icon" src="{{ url_for('static', filename='download.png') }}"></a>
             | {{ format_size(item['size']) }} | 
            <img class="icon" src="{{ url_for('static', filename='EPUB_logo.svg') }}"> 
          </p>

		    </div>

		{% endfor %}

</div>

<!-- End Slide Content -->

      {% if pagination %}

        {% from 'render_pagination.macro' import render_pagination %}
        {{ render_pagination(pagination) }}
        
      {% endif %}

