window.onload = function() {
  $.ajax({
    url: 'profile/',
    success: function(rest_data){
      console.log('All ok!');
      console.log(rest_data);
    }
    error: function(xhr, ajaxOptions, thrownError) {
  		console.log(xhr.status);
  		console.log(xhr.responseText);
  		console.log(thrownError);
  	},
  })
})
