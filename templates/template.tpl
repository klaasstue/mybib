<!doctype html>
<html class="no-js" lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/foundation.css') }}">
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/app.css') }}">
    <script src="https://code.jquery.com/jquery-1.10.2.js"></script>
    <script>
      function toggle_content( cid ){
        $( "#short-"+cid ).toggle();
        $( "#long-"+cid ).toggle();
      }
    </script>
  </head>
  <body>
  <div class="row" style="max-width:100%">
    <div class="large-12 columns">
      <div style="margin: 15px 0 0 0;	
                  width: 520px;	
                  height: 150px;	
                  overflow: hidden;
                  vertical-align: middle;
                  margin-right: 3em;">
        <a data-tooltip aria-haspopup="true" class="has-tip" 
                title="Klicke für weitere Ausgaben!"data-toggle="offCanvasLeft">
          <img src="{{ url_for('static',filename='my_library_logo.svgz') }}" 
                style="height: 150px;"/>
        </a>
      </div>
      <div class="callout" style="box-shadow:0 10px 20px rgba(0,0,0,0.3)">
        <div class="row" style="max-width:100%">
          <div class="off-canvas-wrapper">

            <div class="off-canvas-wrapper-inner" data-off-canvas-wrapper>

          <!--  Die linke Spalte zum aufschieben  -->

              <div class="off-canvas position-left" id="offCanvasLeft" data-off-canvas>
                <ul>
                 {% if topics %}
                  {% for topic in topics %}
                    <li><a href="{{ url_for( 'get_topic', topic=topic)}}">
                    {{ topic }}
                    </a></li>
                  {% endfor %}
                 {% else %}
                  {% for author in authors %}
                    <li><a href="{{ url_for( 'get_author', author=author)}}">
                    {{ author }}
                    </a></li>
                  {% endfor %}
                 {% endif %}
                </ul>
              </div>

  <!--Der eigentliche Inhalt    -->
              {% for entry in entries %}
              <div class="large-4 medium-6 columns" style="float: left">
                <div class="callout">
                  <div class="media-object" style="padding: 20px 20px 20px 20px;"> 
                    <div class="media-object-section" style="height:16em;width: 30%">
                      <img src="{{ url_for('download', filename=entry['path'], imgId=entry['pk']) }}" style="max-width: 100%;max-height: 15em;box-shadow:0 10px 20px rgba(0,0,0,0.3)">
                      <p><a href="{{url_for( 'download', filename=entry['file'], bookId=entry['pk'])}}">
                        <img src="{{ url_for('static', filename='download.png') }}"
                             width="12px"></a>
                         | {{ format_size(entry['size']) }} | <img src="{{ url_for('static', filename='EPUB_logo.svg') }}" width="12px"> 
                      </p>
                    </div>
                    <div class="media-object-section">
                      <h4>{{ entry['title'] }}</h4>
                      <b>{{ entry['summary'] }}</b>
                      <p style="color: grey;font-weight:bold"> 
                        <a href="{{url_for('get_author', author=entry['authors'][0] )}}">
                          {{ format_author(entry['authors'][0]) }}
                        </a>
                        {% for author in entry['authors'][1:] %}
                          <a href="{{url_for('get_author', author=author )}}">
                            , {{ format_author( author ) }}
                          </a>
                        {% endfor %}
                      </p>
                      {% if is_short( entry['content']) %}
                        {{ entry['content'] }}
                      {% else %}
                        <p id="short-{{entry['isbn']}}">
                          {{ shorten( entry['content'] ) }}... 
                          <a id="{{entry['isbn']}}" onclick="toggle_content('{{entry['isbn']}}')">mehr</a> 
                        </p>
                        <div id="long-{{entry['isbn']}}" style="display: none">
                          {{ entry['content'] }}
                          <a id="{{entry['isbn']}}" onclick="toggle_content('{{entry['isbn']}}')"> 
                            <img src="{{ url_for('static', filename='drop-up-arrow.svg') }}" width="12px">
                          </a>
                        </div>
                      {% endif %}
                    </div>
                  </div>
                </div>
              </div>
              {% endfor %}
           </div>
      {% if pagination %}

        {% from 'render_pagination.macro' import render_pagination %}
        {{ render_pagination(pagination) }}
        
      {% endif %}
           </div>
        </div>
      </div>
    </div>
  </div>

    <script src="{{ url_for( 'static', filename = 'js/vendor/jquery.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/what-input.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/foundation.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/jquery.loadTemplate.min.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/app.js') }}"></script>
  </body>
</html>
