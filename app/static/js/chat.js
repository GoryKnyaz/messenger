// запрос на сообщение
function whatNews()
{
    var chat_window_html = $(".messageTable");
    var last_tbody_html = chat_window_html.last()[0].children;
    var last_tr_html = last_tbody_html[0].children;
    var last_td_html = last_tr_html[0].children;
    var last_td_last_html = last_td_html[1].children;

    var user_name = last_td_last_html[0].innerText;
    var timestamp = last_td_last_html[1].children[0].dataset["timestamp"];
    var text_str = last_td_html[1].innerText;
    var text = text_str.slice(text_str.indexOf('\n') + 1);
    $.ajax({
      url: "/whatNews",
      type: "get",
      data: {user: user_name.slice(0, user_name.length-1), time: timestamp, body: text},
      success: function(response) {
        $("#chat_window").append(response);
        flask_moment_render_all();
        var div = $("#chat_window");
        //div.scrollTop($("#chat_window").prop('scrollHeight')); прокрутки, нужно поставить какое-то условие, что чел
        //div.animate({scrollTop: div.prop('scrollHeight')}, 600); прокручен до конца и тогда прокрутить вниз
      },
      error: function(xhr) {
        alert(xhr)
      }
    });
}
window.setInterval(whatNews, 5000);


function picture() {
    var picture = "picture"
}

//прокрутка окна чата
$(document).ready(function() {
    var div = $("#chat_window");
    div.scrollTop(div.prop('scrollHeight')); // резкая
    //div.animate({scrollTop: div.prop('scrollHeight')}, 600); // плавная
});

//прокрутка по кнопке
$(function(){
    $('#scroll_down').click(function(){
        var div = $("#chat_window");
        div.animate({scrollTop: div.prop('scrollHeight')}, 600);
    });
});

//авторастворение кнопки в пространстве
$(document).ready(function() {
    var button = $('#scroll_down');
    $('#chat_window').scroll(function () {
        var scrl = this.scrollHeight - $(this).scrollTop() - $(this).height();
        if (scrl > 150) {
            button.fadeIn();
        } else {
            button.fadeOut();
        }
    });
});
