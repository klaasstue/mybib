<!doctype html>
<html class="no-js" lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foundation for Sites</title>
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/foundation.css') }}">
    <link rel="stylesheet" href="{{ url_for( 'static', filename = 'css/app.css') }}">
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
    <ul class="menu">
      <li><input type="search" placeholder="Search"></li>
      <li><button type="button" class="button">Search</button></li>
    </ul>
  </div>
</div>	 

<!--Ein Grid-Container Tabs   -->

		<div class="grid-container">
      <div class="grid-x grid-padding-x">
        <div class="large-12 cell">
          <h1>Welcome to Foundation</h1>

<!--Das Tab-Panel-->

					{% include 'panel.tpl' %}


        </div>
      </div>
    </div>

    <script src="{{ url_for( 'static', filename = 'js/vendor/jquery.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/what-input.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/vendor/foundation.js') }}"></script>
    <script src="{{ url_for( 'static', filename = 'js/app.js') }}"></script>
  </body>
</html>
