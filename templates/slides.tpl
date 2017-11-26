<!-- Row of Cards in einem Carousel -->

<div class="grid-container">
  <div class="grid-x grid-padding-x small-up-2 medium-up-3 large-up-6">

			{% for item in label['items'][6*index:6*(index + 1)] %}
			
    <div class="cell">
		    <div class="card container">
		      <img src="{{ url_for('download', filename=item['path'], imgId=item['pk']) }}">
		      <div class="overlay">
			      <img class="image" src="{{ url_for('download', filename=item['path'], imgId=item['pk']) }}">
		        <div class="text">
		          <h4>{{ item['title'] }}</h4>
		          <p>{{ item['description'] }}</p>
		        </div>
		      </div>
		    </div>
    </div>

			{% endfor %}

  </div>
</div>
<!-- End of Row of Cards in einem Tab -->

