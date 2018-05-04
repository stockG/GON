/* 将数组内容进行随机 */
function randomSort(a) {
  var arr = a, random = [], len = arr.length;
  for (var i = 0; i < len; i++) {
    var index = Math.floor(Math.random()*(len - i));
    random.push(arr[index]);
    arr.splice(index,1);
  }
  return random;
};
/* end randomSort*/

function playMusic() {
        var player = $("#player")[0]; /*jquery对象转换成js对象*/
        if (player.paused){ /*如果已经暂停*/
            player.play(); /*播放*/
        }
    };

var us = ["eli", "umi", "hanayo", "honoka", "kotori", "maki", "nico", "nozomi", "rin",
          "eli2", "umi2", "hanayo2", "honoka2", "kotori2", "maki2", "nico2", "nozomi2", "rin2"];

var us_random = randomSort(us); //重新排序

var i = 0;
var image_id = new Array();
var score = 0;
var n = t = 0, count, bef = 0; //轮播参数

// 自动轮播
function showAuto() {
    n = n >= (count - 1) ? 0 : ++n;
    $(".carosel li").eq(n).trigger('click');
}

$(document).ready(function() {
  $('.back-lovelive').each(function(index) {
    var pictureName = us_random[index];
    var link = "<img src=\"../static/images/";
    link += pictureName;
    link += ".jpg\" alt=\"";
    link += pictureName;
    link += "\" height=\"175px\" width=\"175px\">";
    $(this).append(link);
  }); //end
  /* 计时器 */
  var j = 0;
  var timer = null;
  //补零
  function toDuble(n) {
    return (n < 10)?"0"+n:""+n;
  };
  // 开始计时
  $('#timestart').on("click",function() {
    clearInterval(timer);
    playMusic();
    timer = setInterval(function() {
      j++;
      var sec = Math.floor(j/60);
      var ms = j%60;
      var time_value = toDuble(sec) + ":" + toDuble(ms);
      $('#time').text(time_value);
    },1000/60);
    /* loveelive Game */
    $('.flipper-lovelive').on("click",function() {
      $this = $(this);
      $this.addClass('filpper-add');
       image_id[i] = $(this).find('img').attr('alt');
       // alert(image_id);
       if ((i > 0) && (i%2 != 0)) {
         if ( ((image_id[i] + "2") == image_id[i-1]) || (image_id[i].substring(0,image_id[i].length-1) == image_id[i-1]) ) {
           // $('.filpper-add').css('visibility','hidden');
           $('img[alt = "'+image_id[i]+'"]').closest('.flipper-lovelive').css('visibility','hidden');
           $('img[alt = "'+image_id[i-1]+'"]').closest('.flipper-lovelive').css('visibility','hidden');
           score = score + 12;
           $('#score').text(score);
         }
         else if (score>0) {
           score = score - 2;
           $('#score').text(score);
         }
         setTimeout(function(){$('.filpper-add').removeClass('filpper-add')}, 1000);
       };
       i++;
    }); //end click
  });
  // 暂停
  $('#timeend').on("click",function() {
    clearInterval(timer);
    $('.flipper-lovelive').unbind();
    player.pause(); //音乐暂停
  });
  // 重新开始
  $('#restart').on("click",function() {
    clearInterval(timer);
    $('#time').text("00:00");
    $('#score').text("0");
    j = 0;
    $('.flipper-lovelive').unbind().css('visibility','visible');
  });
  /* end timer */


  /* 新番动画js */
  $('#tabContainer').tabs({
		show: 'fadeIn',
  	hide: 'fadeOut'
  });
  var hash = location.hash;
	if (hash) {
		$('#tabContainer').tabs("load", hash)
	}
  /* end Animate*/

  /* 轮播 */
  count = $('.carosel_list a').length //获取图片标签长度
  $('.carosel_list a:not(:first-child)').hide(); //不是当前显示的图片隐藏
  $('.carosel_info div:not(:first-child)').hide(); 
  //点击下面的1234按钮，切换图片
  $('.carosel li').click(function() {
      var k = $(this).text() - 1;
      n = k;
      if ((k>=count) || (k == bef)) return;
      $('.carosel_list a').filter(':visible').fadeOut(500).parent().children().eq(k).fadeIn(1000); //淡入淡出效果
      $('.carosel_info div').filter(':visible').fadeOut(100).parent().children().eq(k).fadeIn(300);
      $(this).toggleClass('on'); //响应点击
      $(this).siblings().removeAttr('class'); //切换按钮的时候让上一个按钮回归原来的样式
      bef = k;
  })
  t = setInterval("showAuto()", 4000);
  $('.carosel').hover(function() { clearInterval(t) }, function() { t = setInterval("showAuto()", 4000); });
  /* end Animate*/
});


// var link = "<img src=\"{% static \"images/";
// link += pictureName;
// link += ".jpg\" %}\" alt=\"";
// link += pictureName;
// link += "\" height=\"175px\" width=\"175px\">";
