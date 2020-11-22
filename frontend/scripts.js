//SOME JS FOR SETTING THE DEMO VALUES
$('document').ready(function() {
    randomize();
    var timer = setInterval(function() {
      randomize()
    }, 3000);
  });
  
  function randomize() {
    $('.progress .bar').each(function() {
      var val = Math.floor((Math.random() * 100));
      $(this).attr('style', 'width:' + val + '%;background-position:0 ' + val + '%');
    });
  }