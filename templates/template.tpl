<!doctype html>
<html class="no-js" lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foundation for Sites</title>
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/foundation.css') }}">
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/app.css') }}">
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/jquery.auto-complete.css') }}">
  </head>
  <body>
  
	<!--Die Navbar mit Suchfenster -->

	<div class="top-bar" id="example-menu">
		<div class="top-bar-left">
		  <ul class="dropdown menu" data-dropdown-menu>
		    <li class="menu-text">Site Title</li>
		    <li class="has-submenu">
		      <a href="#0">One</a>
		      <ul class="submenu menu vertical" data-submenu>
		        <li><a href="#0">One</a></li>
		        <li><a href="#0">Two</a></li>
		        <li><a href="#0">Three</a></li>
		      </ul>
		    </li>
		    <li><a href="#0">Two</a></li>
		    <li><a href="#0">Three</a></li>
		  </ul>
		</div>
		<div class="top-bar-right">
      <form id="search" action="{{ url_for('search') }}">
				<ul class="menu">
				  <li><input name="q" style="max-width:100%;width:400px;" type="search" placeholder="Volltextsuche"></li>
				  <li><button type="button" class="button">Search</button></li>
				</ul>
			</form>
		</div>
	</div>	 

<!--Grid-Container mit Tabs   -->

		<div class="grid-container">
      <div class="grid-x grid-padding-x">
        <div class="large-12 cell">
          <h1>Welcome to Foundation</h1>

<!--Tab-Panel-->

					{% include template %}

<!--Ende Tab-Panel-->

        </div>
      </div>
    </div>

<!-- Ende Grid-Container mit Tabs   -->

    <script src="{{ url_for( 'static', filename = 'js/vendor/jquery.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/what-input.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/foundation.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/jquery.auto-complete.min.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/app.js') }}"></script>
    <script>
      $('input[name="q"]').autoComplete({
        source: function(term, response){
          $.getJSON("{{ url_for('suggest') }}", { q: term }, function(data){
          	response(data);
          });
        }
      });
    </script>
  </body>
</html>
