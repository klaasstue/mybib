<!doctype html>
<html class="no-js" lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meine kleine Bücherei</title>
<!-- <link href='http://fonts.googleapis.com/css?family=Lato:400,700' rel='stylesheet' type='text/css'>-->
<!--    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/slick.css') }}">-->
<!--    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/slick-theme.css') }}">-->
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/jquery.auto-complete.css') }}">
<!--    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/slick-style.css') }}">-->
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/app.css') }}">
    <script>
      // store queue list with page numbers to fetch
      var pagq_list = {{ page_queues }};
      var prefix = "{{ url_for( 'get_label', topic = topic, page='') }}";
    </script>
  </head>
  <body style="background-image:url({{ url_for('static',filename='my_library_logo.svgz') }}); background-size:120%; background-repeat: no-repeat;background-attachment:fixed;">
  
	<!--Die Navbar mit Suchfenster -->

	<div class="top-bar" id="example-menu">
		<div class="top-bar-left">
			
      <ul class="dropdown menu" data-dropdown-menu>
        <li>
          <a class="dropbtn" href="{{url_for('home')}}">HOME</a>
          <div class="dropdown-content">
	          {% for topic in topics %}
	              <a href="{{ url_for('get_topic', topic = topic ) }}">
	                {{ topic }}
	              </a>
	          {% endfor %}
          </div>
        </li>
      </ul>

		</div>
		<div class="top-bar-right">
      <form id="search" action="{{ url_for('search') }}">
				<ul class="menu">
				  <li><input id="Volltextsuche" name="q" style="max-width:100%;width:400px;" type="search" placeholder="Volltextsuche"></li>
				  <li><button type="submit" class="button">Search</button></li>
				</ul>
			</form>
		</div>
	</div>	 

	<!--Die Navbar mit Suchfenster -->

<!--Grid-Container mit Tabs   -->

	<div class="page">
	  <div class="text">
      <h1>{{ topic }}</h1>
    </div>
<!--Tab-Panel-->

					{% include template %}

<!--Ende Tab-Panel-->

  </div>
<button >
<!-- Ende Grid-Container mit Tabs   -->

    <script src="{{ url_for( 'static', filename = 'js/vendor/jquery.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/jquery.auto-complete.min.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/lazyload.min.js') }}"></script>
<!--    <script src="{{ url_for( 'static', filename = 'js/vendor/slick.min.js') }}"></script>-->
    <script src="{{ url_for( 'static', filename = 'js/app.js') }}"></script>
  </body>
</html>
