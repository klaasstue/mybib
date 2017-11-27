<ul class="tabs" data-tabs id="example-tabs">

{% for panel in panels %}

 {% if panel['ind'] == 1 %}

  <li class="tabs-title is-active"><a href="#panel1" aria-selected="true">{{ panel['panel'] }}</a></li>

 {% else %} 

  <li class="tabs-title"><a href="#panel{{ panel['ind'] }}">{{ panel['panel'] }}</a></li>

 {% endif %}

{% endfor %}

</ul>

<div class="tabs-content" data-tabs-content="example-tabs">

	{% for panel in panels %}
 
  <div class="tabs-panel{% if panel['ind'] == 1 %} is-active {% endif %}" id="panel{{ panel['ind'] }}">
    
    {% include 'carousel.tpl' %}
    
  </div>
  
	{% endfor %}

</div>

