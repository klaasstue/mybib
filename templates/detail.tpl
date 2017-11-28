	<div class="row">
				<img 	src="{{ url_for('download', filename=item['path'], imgId=item['pk']) }}" 
							class="detail-img"  style="max-width: 1440px;"/>

	</div>

	<div class="row detail">

		<div class="callout">	
	    <div class="grid-x grid-padding-x">

				<div class="medium-8 large-8 cell">	
 				  <h4>{{ item['title'] }}</h4>
					<b>{{ item['summary'] }}</b>
					{{ item['content'] }}
				</div>

				<div class="medium-4 large-4 cell">
          <p>
          	<a href="{{url_for( 'download', filename=item['file'], bookId=item['pk'])}}">
            	Download <img src="{{ url_for('static', filename='download.png') }}"
                 width="18px">
            </a>
          </p>
          <p>Größe: {{ format_size(item['size']) }}</p>
 
          {% if item['mimetype'] == 'application/pdf' %}
 
          <p>Format: PDF <img src="{{ url_for('static', filename='pdf-icon.png') }}" width="18px"> 
          
          {% else %}
          
          <p>Format: ePub <img src="{{ url_for('static', filename='EPUB_logo.svg') }}" width="18px"> 
          
          {% endif %}
          
          </p>
					<h4>Autor(en)</h4>
					<p style="color: grey;font-weight:bold"> 
						<a href="{{url_for('get_author', author=item['authors'][0] )}}">
						  {{ format_author(item['authors'][0]) }}
						</a>
						{% for author in item['authors'][1:] %}
							<br/>
						  <a href="{{url_for('get_author', author=author )}}">
						    {{ format_author( author ) }}
						  </a>
						{% endfor %}
					</p>
				</div>

			</div>
    </div>

	</div>

