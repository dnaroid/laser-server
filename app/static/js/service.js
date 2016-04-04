// var myTmpl = $.templates("<label>Name:</label> {{:name}}");
// var html = myTmpl.render(person);
var CONTENT = '#div_content';
var DIV_FORM_FILTER = $.templates('<div id="div_form_filter" align="center">');
var DIV_NEWS_LIST = $.templates('<div id="div_news_list"><table id="news_table">');
var DIV_PAGINATION = $.templates('<div id="div_pagination" align="center">');

var PAGE_NEWS_LIST = $.templates('' +
    '<div id="div_form_filter" align="center">' +
    '<select id="select_author" name="author" >' +
    '<option value="0" label="All authors"></option>' +
    '</select>' +
    '<select id="select_tags" name="t"  multiple>' +
    '<option value="0" label="Select tags" disabled></option>' +
    '</select>' +
    '<input id="button_filter" type="button" value="Filter">' +
    '<input id="button_reset" type="button" value="Reset">' +
    '</div>' +
    '<div id="div_news_list">' +
    '<table id="news_table">' +
    '</table>' +
    '</div>' +
    '<div id="div_pagination" align="center">' +
    '</div>'
);
var tags, authors;

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

function loadTagFilter() {
    $.getJSON(
        '/_get_all_tags',
        function (data) {
            $.each(data, function (key, val) {
                var opt = $('<option>').text(val);
                opt.attr('value', key);
                $('#select_tags').append(opt);
            });
            $('#select_tags').multiselect('rebuild');
        }
    );
}

function loadAuthorFilter() {
    $.getJSON(
        '/_get_all_authors',
        function (data) {
            $.each(data, function (key, val) {
                var opt = $('<option>');
                opt.attr('label', val);
                opt.attr('value', key);
                $('#select_author').append(opt);
            });
            $('#select_author').multiselect('refresh');
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

function createFilter() {
    loadAuthorFilter();
    loadTagFilter();
}

function drawNewsList() {

    $(CONTENT).html(PAGE_NEWS_LIST.render());

    $('#select_tags').multiselect();
    $('#select_authors').multiselect();
    createFilter();
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

