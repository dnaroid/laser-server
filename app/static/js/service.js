$(document).ready(function () {
    init();
});

var frame = 'news_list';
// var frame = 'news_edit';

function init() {
    $.cookie('author', 'author=0');
    $.cookie('tags', '');
    $.cookie('pages', '0');

    $('#button_login').on('click', function () {
        frame = 'login';
        drawFrame();
    });

    drawFrame();
}

function setFilter(data) {
    author = $('#select_author').multiselect('getSelected').serialize();
    tags = $('#select_tags').multiselect('getSelected').serialize();
    $.cookie('author', author);
    $.cookie('tags', tags);
    showNews();
}

function resetFilter() {
    $.cookie('author', 'author=0');
    $.cookie('tags', '');
    $('#select_author').multiselect('select', [0]);
    $('#select_author').multiselect('refresh');
    $('#select_tags').multiselect('clearSelection');
    showNews();
}

function createTagSelect() {
    $('#div_form_filter').append($('<select id="select_tags" name="t" style="display: none" multiple>'));
    $.getJSON(
        '/_get_all_tags',
        function (data) {
            var opt = $('<option>');
            opt.attr('value', '0');
            opt.attr('disabled', 'true');
            $('#select_tags').append(opt.text('Select tags'));
            $.each(data, function (key, val) {
                var opt = $('<option>').text(val);
                opt.attr('value', key);
                $('#select_tags').append(opt);
            });
            $('#select_tags').multiselect();
            return false;
        }
    );
}

function createAuthorSelect() {
    $('#div_form_filter').append($('<select id="select_author" name="author">'));
    $.getJSON(
        '/_get_all_authors',
        function (data) {
            var opt = $('<option>');
            opt.attr('label', 'All authors');
            opt.attr('value', '0');
            $('#select_author').append(opt);

            $.each(data, function (key, val) {
                var opt = $('<option>');
                opt.attr('label', val);
                opt.attr('value', key);
                $('#select_author').append(opt);
            });
            $('#select_author').multiselect();
            return false;
        }
    );
}

function drawFrame() {
    $('#div_content').empty();
    switch (frame) {
        case 'news_list':
            drawNewsList();
            break;
        case 'news_view':
            drawNewsView();
            break;
        case 'login':
            drawLogin();
            break;
    }
}

function drawLogin() {
    $('#div_content').append('<div align="center"><form class="login-form">');
    $('#div_content').append($('<table>')
        .append(
            row(
                col('Login:'),
                col($('<input type="text">'))
            ))
        .append(
            row(
                col('Password:'),
                col($('<input type="password">'))
            ))
        .append(
            row(
                col(),
                col($('<input type="button" onclick="login()">'))
            ))
    );
}

function login() {
}

function drawNewsView() {

}

function drawNewsList() {

    $('#div_content').append('<div id="div_form_filter" align="center">');
    $('#div_content').append('<div id="div_news_list"><table id="news_table">');
    $('#div_content').append('<div id="div_pagination" align="center">');

    createAuthorSelect();
    createTagSelect();

    $('#div_form_filter').append($('<input id="button_filter" type="button" value="Filter">'));
    $('#div_form_filter').append($('<input id="button_reset" type="button" value="Reset">'));

    showNews();

    $('#button_filter').on('click', function () {
        setFilter();
    });

    $('#button_reset').on('click', function () {
        resetFilter();
    });
}

function showNews(page) {
    if (page == undefined) {
        page = 1;
    }
    $.getJSON(
        '/_get_news/' + page,
        function (data) {

            var table = $('#news_table');
            table.empty();
            var pages;
            var page;

            $.each(data, function (id, dic) {

                if (id == 'pagination') {
                    pages = dic.pages;
                    page = dic.page;
                }
                else {

                    table.append(
                        row(
                            col($('<strong>').text(dic.title), ' (by ', dic.author, ')'),
                            col(dic.date).addClass('right-align').attr('colspan', 2)
                        )
                    );

                    table.append(
                        row(
                            col(dic.short).attr('colspan', 3)
                        )
                    );

                    table.append(
                        row(
                            col(
                                $('<span>').text(dic.tags).addClass('tags-text'),
                                $('<span>').text('Comments(' + dic.comments + ')').addClass('comments-count'),
                                $('<span>').text('View').addClass('right-align')).attr('colspan', 3).addClass('right-align')
                        )
                    );
                }

            });

            var pagin = $('#div_pagination');
            pagin.empty();
            for (var i = 1; i <= pages; i++) {
                var a = $('<input>');
                a.attr('type', 'button');
                a.addClass('btn btn-default btn-xs');
                a.attr('value', i);
                if (i == page) {
                    a.addClass('btn btn-default btn-xs current');
                } else {
                    a.attr('onclick', 'showNews(' + i + ')');
                }
                pagin.append(a);
            }
        }
    );
}

function row() {
    var res = $('<tr>');
    for (var i = 0; i < arguments.length; i++) {
        res.append(arguments[i]);
    }
    return res;
}

function col() {
    var res = $('<td>');
    for (var i = 0; i < arguments.length; i++) {
        res.append(arguments[i]);
    }
    return res;
}

