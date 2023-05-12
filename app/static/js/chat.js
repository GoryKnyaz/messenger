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
        if (Math.abs(div[0].scrollHeight - div.scrollTop() - div[0].clientHeight) < 100)
        {
        //div.scrollTop($("#chat_window").prop('scrollHeight'));
            div.animate({scrollTop: div.prop('scrollHeight')}, 600);
        }
      },
      error: function(xhr) {
        //alert(xhr)
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
    //div.scrollTop(div.prop('scrollHeight')); // резкая
    div.animate({scrollTop: div.prop('scrollHeight')}, 600); // плавная
});

//прокрутка по кнопке
function scrollToDown()
{
    var div = $("#chat_window");
    div.animate({scrollTop: div.prop('scrollHeight')}, 600);
}

//авторастворение кнопки в пространстве
$(document).ready(function() {
    var button = $('#scroll_down');
    $('#chat_window').scroll(function () {
        var scrl = this.scrollHeight - $(this).scrollTop() - $(this).height();
        if (scrl > 100) {
            button.fadeIn();
        } else {
            button.fadeOut();
        }
    });
});
