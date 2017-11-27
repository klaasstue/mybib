{% for label in panel['labels'] %}

<h1>{{ label['label'] }}</h1>

<!-- Das Carousel-->

<div class="orbit" role="region" aria-label="Favorite Space Pictures" data-orbit data-options="animOutToLeft:fade-out; animOutToRight:fade-out;autoPlay:false">

  <div class="orbit-wrapper">

    <div class="orbit-controls">
      <button class="orbit-previous"><span class="show-for-sr">Previous Slide</span>&#9664;&#xFE0E;</button>
      <button class="orbit-next"><span class="show-for-sr">Next Slide</span>&#9654;&#xFE0E;</button>
    </div>

    <ul class="orbit-container" style="overflow:visible">

    	{% for index in label['groups'] %}

      <li class="{% if label['ind'] == 1 %}is-active {% endif %}orbit-slide">
        <figure class="orbit-figure">

					{% include 'slides.tpl' %}

        </figure>
      </li>

      {% endfor %}

    </ul>

  </div>

  <nav class="orbit-bullets">

 	{% for index in label['groups'] %}

    <button {% if index == 0 %}class="is-active" {% endif %}data-slide="{{ index }}"><span class="show-for-sr">First slide details.</span><span class="show-for-sr">Current Slide</span></button>

	{% endfor %}

  </nav>

</div>

<!--Ende Carousel-->

{% endfor %}
