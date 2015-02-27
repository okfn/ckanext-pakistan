$(document).ready(function () {
	// Wrap each word in a span.
	$('.masthead .logo a').each(function(){ 
	 var text = $(this).text().split(' ');
	 for( var i = 0, len = text.length; i < len; i++ ) { 
		 text[i] = '<span class="word-' + i + '">' + text[i] + '</span>'; 
		} 
		$(this).html(text.join(' '));
	});
});

$(document).ready(function () {
    $('#facebook-count').each(function(){
        var currentdiv = $(this);
        var url = currentdiv.attr('rel');
        $.getJSON('http://graph.facebook.com/?id='+url+'&callback=?', function(data) {
           currentdiv.text((data.shares || 0));
        });
    });
    $('#twitter-count').each(function(){
        var currentdiv = $(this);
        var url = currentdiv.attr('rel');
        $.getJSON('http://cdn.api.twitter.com/1/urls/count.json?url='+url+'&callback=?', function(data) {
           currentdiv.text((data.count || 0));
        });
    });
    $('#gplus-count').each(function(){
        var currentdiv = $(this);
        var url = currentdiv.attr('rel');
        var count = $('#aggregateCount');
        console.log(count);
    });
});
