$("document").ready(function() {
  loadGroup('/groups/testproj.json', 'testproj');

  $("#tree").click(function() {
    alert("test");
  });
});

function loadGroup(url, id) {
  $.getJSON(url, function(data) {
    var items = [];
    $.each(data, function(idx, val) {
      items.push('<li id="'+id+'_'+val["name"]+'"><a href="#" onClick="loadAsset(\'/assets/'+id+'/'+val["name"]+'.json\', \''+id+'_'+val["name"]+'\')">'+val["name"]+'</a></li>');
    });
    $('<ul/>', {
      'class': 'my-new-list',
      html: items.join('')
    }).appendTo("#"+id);
  });
}

function loadAsset(url, id) {
  $.getJSON(url, function(data) {
    var items = [];
    $.each(data, function(idx, val) {
      items.push('<li id="'+id+'_'+val["name"]+'"><a href="#" onClick="loadElement(\'/elements/'+id+'/'+val["name"]+'.json\', \''+id+'_'+val["name"]+'\')">'+val["name"]+'</a></li>');
    });
    $('<ul/>', {
      'class': 'my-new-list',
      html: items.join('')
    }).appendTo("#"+id);
  });
}

