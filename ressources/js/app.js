// Für das Lazy Loading
let images = document.querySelectorAll(".thumbnail");
lazyload(images);

// Für das Modal mit den Buch-Details
function fillTemplate(jObj){
  // Fill template for book details
  $('.modal img.large-image').attr('src',jObj.image);
  $('.modal h2').text( jObj.title);
  $('.modal h4').text( jObj.summary);
  $('.modal div.infotext').html( jObj.content);
  $('.modal p.caption a').attr( 'href', jObj.book );
  var string = $( '.modal p.caption' ).html().replace(/\| .*? \|/g, '| '+jObj.size+' |' );
  $('.modal p.caption').html( string );
}

function showDetails( pk ){
  // fetch details for book with bookId pk and show
  url = detail_prefix + pk
  $.getJSON(url, function(jsonObj){
    fillTemplate( jsonObj );
    $('.overlay').removeClass('is_hidden');
    $('.modal').removeClass('is_hidden');
  });
}

function hideDetails(){
    $('.overlay').addClass('is_hidden');
    $('.modal').addClass('is_hidden');
}

// Funktionen für das Nachladen 
function appendThumbnail( jObj ){
  // Ein Thumbnail hinzufügen
  var card = $('div.card:visible').last();
  var newCard = $( card ).clone();
  $( newCard ).find( 'img.thumbnail' ).attr('data-src', jObj.image).attr('src', jObj.image);
  $( newCard ).find( 'a' ).attr( 'href', jObj.book );
  var string = $( newCard ).find( 'p' ).html().replace(/\| .*? \|/g, '| '+jObj.size+' |' );
  console.log('Die Buchgroesse ist ' + jObj.size )
  $( newCard ).find('p').html( string );
  $( card ).after( newCard );
  console.log('Buch hinzugefügt: ' + jObj.image )
};

function getPageNo(label_index){
  // get next page number
  var next_page = pagq_list[ label_index ].shift();
  // Don't forget to hide the more button, if no further page to fetch
  if( pagq_list[ label_index ].length==0){
    $("#more_" + label_index).hide()
  };
  return next_page;
};

function loadJSONBooklist( label, label_index ){
  // load next page and add castlist
  var pageNo = getPageNo( label_index );
  var url = more_prefix + pageNo + "?q=" + label.replace('&','%26');
  
  $.getJSON(url, function(jsonObjList){
      $.each(jsonObjList, function(i, jsonObj){
        appendThumbnail(jsonObj)
      });
  });
}

// Die Tabs
$('.tabs-title').click(function(){
  $('.tabs-title').removeClass('is_active');
  $(this).addClass('is_active');
});

function openTab(label) {
  $('.tabs-panel').addClass('is_hidden');
  $('#label' + label).removeClass('is_hidden');
};

// Auto completion für die Volltextsuche
$('#Volltextsuche').autoComplete({
  source: function(term, response){
    $.getJSON("{{ url_for('suggest') }}", { q: term }, function(data){
    	response(data);
    });
  },
  
  renderItem: function (item, search){
      // escape special characters
      search = search.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      var re = new RegExp("(" + search.split(' ').join('|') + ")", "gi");
      return '<div class="autocomplete-suggestion" data-val="' + search + '" data-pk="' + item[0] + '">' + item[1].replace(re, "<b>$1</b>") + '</div>';
  },
  
  onSelect: function(e, term, item){
  	bookId 	= item.data('pk');
  	url 		= "{{ url_for('get_book',bookId='') }}" + bookId;
  	window.location.href = url ;
  }
});

// Auto Completion für die Schlagwortsuche. Gegenwärtig nicht im Einsatz
$('#Schlagwortsuche').autoComplete({
  source: function(term, response){
    $.getJSON("{{ url_for('schlagworte') }}", { q: term }, function(data){
    	response(data);
    });
  }
});

