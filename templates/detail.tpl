<!--  Ein Pop-up für die Details-->

  <div class="overlay is_hidden">
  </div>
  <div class="modal is_hidden">
    <a class="close" onclick="hideDetails()">&times;</a>
    <img class="large-image">
    <div class="content">
      <h2></h2>
      <h4></h4>
      <p class="authors"> 
        <a href=""></a>
      </p>
      <div class="infotext">
      </div>
      <p class="caption"><a href="">
        <img class="icon" src="{{ url_for('static', filename='download.png') }}"></a>
         |  | 
        <img class="icon" src="{{ url_for('static', filename='EPUB_logo.svg') }}"> 
      </p>
    </div>
  </div>
