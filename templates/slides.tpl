<!-- Slide Content -->

<div class="grid-container">
  <div class="grid-x grid-padding-x small-up-2 medium-up-3 large-up-6">

		{% for item in label['items'][6*index:6*(index + 1)] %}
			
    <div class="cell">
		    <div class="card container">
		      <img src="{{ url_for('download', filename=item['path'], imgId=item['pk']) }}">
		      <div class="overlay">

            {{ item['content'] }}
          
		      </div>
		    </div>

        <p><a href="{{url_for( 'download', filename=item['file'], bookId=item['pk'])}}">
          <img src="{{ url_for('static', filename='download.png') }}"
               width="12px"></a>
           | {{ format_size(item['size']) }} | <img src="{{ url_for('static', filename='EPUB_logo.svg') }}" width="12px"> 
        </p>

    </div>

		{% endfor %}

  </div>
</div>

<!-- End Slide Content -->

