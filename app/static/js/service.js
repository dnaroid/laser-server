$(document).ready(function () {
    init();
});



function init() {
    user = getCookie('user');
    authorFilter = '0'
    tagsFilter = ''
    allAuthors = []
    activeAuthors = []
    allTags = []
    comments = []
    loginCont = '#loginCont';
    menuCont = '#menuCont';
    navigationCont = '#navigationCont';
    paginateCont = '#paginateCont';
    filterCont = '#filterCont';
    newsListCont = '#newsListCont';
    newsListBlock = '#newsListBlock';
    filterCont = '#filterCont';
    selectorCont = '#selectorCont';
    newsViewCont = '#newsViewCont';
    tmpMultiSelect = $.templates('#tmpMultiSelect');
    tmpNewsListPage = $.templates('#tmpNewsListPage');
    tmpNavigation = $.templates('#tmpNavigation');
    tmpNewsList = $.templates('#tmpNewsList');
    tmpFilter = $.templates('#tmpFilter');
    tmpPaginBtn = $.templates('#tmpPaginBtn');
    tmpLoginPage = $.templates('#tmpLoginPage');
    tmpSideMenu = $.templates('#tmpSideMenu');
    tmpAddNews = $.templates('#tmpAddNews');
    tmpShowNews = $.templates('#tmpShowNews');
    tmpSelector = $.templates('#tmpSelector');
    tmpAddComment = $.templates('#tmpAddComment');
    tmpEditAuthors = $.templates('#tmpEditAuthors');
    tmpEditTags = $.templates('#tmpEditTags');

    loadFilterData();
    drawNavigation();
    drawNewsList();
}

function scrollOff() {
    var x = window.scrollX;
    var y = window.scrollY;
    window.onscroll = function () {
        window.scrollTo(x, y);
    };
}

function scrollOn() {
    setTimeout(function () {
        window.onscroll = function () {
        };
    }, 200);
}

function switchPage(page) {
    switch (page) {
        case 'newsList':
            $(newsViewCont).css('display', 'none');
            $(newsListBlock).css('display', 'block');
            $(loginCont).css('display', 'none');
            break;
        case 'newsEdit':
        case 'newsAdd':
        case 'newsView':
            $(newsViewCont).css('display', 'block');
            $(newsListBlock).css('display', 'none');
            $(loginCont).css('display', 'none');
            break;
        case 'loginPage':
            $(newsViewCont).css('display', 'none');
            $(newsListBlock).css('display', 'none');
            $(loginCont).css('display', 'block');
            break;
        case 'newsList':
            break;

    }

}

function setFilter() {
    if ($('#authorFilter option:selected').val() > 0
        || $('#tagsSelect input:checked').length) {
        authorFilter = $('#authorFilter option:selected').val();
        var tags = []
        $('#tagsSelect input:checked').each(
            function () {
                tags.push($(this).val());
            }
        );
        tagsFilter = tags;
        drawNewsList();
    }
}

function resetFilter() {
    if ($('#authorFilter option:selected').val() > 0
        || $('#tagsSelect input:checked').length) {
        authorFilter = '0'
        tagsFilter = ''
        $('#authorFilter').val(0);
        $("#ms1 input:checked").prop({'checked': false});
        $('#ms1 .dropDown').trigger('change');
        drawNewsList();
    }
}

function loadFilterData() {
    $.getJSON(
        '/_get_all_tags',
        function (data) {
            allTags = data;
            if (allAuthors != []) {
                drawFilter();
            }
        }
    );
    $.getJSON(
        '/_get_all_authors',
        function (data) {
            allAuthors = data;
            // if (allTags != []) {
            //     drawFilter();
            // }
        }
    );
    $.getJSON(
        '/_get_active_authors',
        function (data) {
            activeAuthors = data;
            if (allTags != []) {
                drawFilter();
            }
        }
    );
}

function drawFilter() {
    $(filterCont).css('display', 'none');
    $(filterCont).html(tmpFilter.render({authors: activeAuthors, tags: allTags}));
    $(filterCont).css('display', 'block');
}

function drawNavigation() {
    $(navigationCont).html(tmpNavigation.render({user: user}));
    if (user != undefined) {
        drawSideMenu();
    } else {
        $('#menuCol').width(0);
        $(menuCont).empty();
    }

    $('#loginBtn').on('click', function () {
        drawLoginPage();
    });

    $('#logoutBtn').on('click', function () {
        doLogout();
    });

    $('#bannerBtn').on('click', function () {
        drawNewsList();
    });
}

function drawSideMenu() {
    $('#menuCol').width('10em');
    $(menuCont).html(tmpSideMenu.render());
}

function drawEditAuthors() {
    scrollOff();
    $(newsViewCont).html(tmpEditAuthors.render({authors: allAuthors}));
    switchPage('newsView');
    scrollOn();
}

function drawEditTags() {
    scrollOff();
    $(newsViewCont).html(tmpEditTags.render({tags: allTags}));
    switchPage('newsView');
    scrollOn();
}

function drawAddNews() {
    $(newsViewCont).html(tmpAddNews.render({authors: allAuthors, tags: allTags}));
    $('#addNewsDate').val(getToday());
    switchPage('newsView');

    $('#addNewsSaveBtn').on('click', function () {
        var title = $('#addNewsTitle').val();
        var short = $('#addNewsBrief').val();
        var full = $('#addNewsContent').val();
        var date = $('#addNewsDate').val();
        var author = $('#addNewsAuthorSelect option:selected').val();
        var tags = []
        $('#addNewsTagsSelect input:checked').each(
            function () {
                tags.push($(this).val());
            }
        );
        var data = JSON.stringify({
            title: title,
            creation_date: date,
            short_text: short,
            full_text: full,
            author_id: author,
            tags: tags
        });
        if (author > 0) {
            $.post('/_add_news', data, function (resp) {
                console.log(resp);
                drawNewsList()
            })
        }
    })
}

function updateAuthor(id) {
    var newName = $('#editAuthorsTable textarea[idx=' + id + ']').val();
    var data = JSON.stringify({
        id: id,
        new_name: newName
    });
    $.post('/_update_author', data);
    allAuthors[id] = newName;
    drawFilter();
    drawEditAuthors();
}

function updateTag(id) {
    var newName = $('#editTagsTable textarea[idx=' + id + ']').val();
    var data = JSON.stringify({
        id: id,
        new_name: newName
    });
    $.post('/_update_tag', data);
    allTags[id] = newName;
    drawFilter();
    drawEditTags();
}

function deleteTag(id) {
    var data = JSON.stringify({
        id: id
    });
    $.post('/_del_tag', data);
    delete allTags[id];
    drawFilter();
    drawEditTags();
}

function expireAuthor(id) {
    var data = JSON.stringify({
        id: id
    });
    var name = allAuthors[id];
    $.post('/_expire_author', data);
    delete allAuthors[id];
    drawFilter();
    drawEditAuthors();
}

function addTag() {
    var name = $('.newTagName').val();
    var data = JSON.stringify({
        name: name
    });

    $.post('/_add_tag', data, function (resp) {
            var json = $.parseJSON(resp);
            var new_id = json.new_id;
            allTags[new_id] = name;
            drawFilter();
            drawEditTags();
        }
    );
}

function addAuthor() {
    var name = $('.newAuthorName').val();
    var data = JSON.stringify({
        name: name
    });

    $.post('/_add_author', data, function (resp) {
            var json = $.parseJSON(resp);
            if (resp == 'ok') {
                var new_id = json.new_id;
                allAuthors[new_id] = name;
                drawFilter();
                drawEditAuthors();
            }
        }
    );
}


function drawNewsView(id) {
    $.getJSON('/_get_news?id=' + id, function (data) {
        var comments = [];
        var len = data.comments.length;

        for (var i = 0; i < len; i++) {
            var arr = data.comments[i];
            comments.push({
                id: arr[0],
                date: arr[1],
                text: arr[2],
                news_id: arr[3]
            });
        }
        $(newsViewCont).html(tmpShowNews.render({user: user, data: data, comments: comments}));
        switchPage('newsView');
        $('#sendCommentButton').on('click', function () {
            addComment(data.id, $('#commentText').val());
        });
        $('#prevBtn').on('click', function () {
            drawNewsView(data.id - 1);//todo
        });
        $('#nextBtn').on('click', function () {
            drawNewsView(data.id + 1);//todo
        });
    });
}

function deleteComment(id, newsId) {
    $.get('/_del_comment', 'id=' + id);

    $('#newsTable .comments').each(function () {
        if ($(this).attr('idx') == id) {
            $(this).remove();
        }
    });

    // decrement comments counter in news list
    $('.commentsCounter span').each(function () {
        if ($(this).attr('idx') == newsId) {
            $(this).text($(this).text() - 1);
        }
    });
}

function drawNewsList(page) {
    $(paginateCont).css('display', 'none');
    switchPage('newsList');
    var page2 = page;
    if (page2 == undefined) {
        page2 = '1';
    }
    var filter = JSON.stringify({
        author: authorFilter,
        tags: tagsFilter
    });
    var request = '';
    if (authorFilter != '0' && tagsFilter != '') {
        request = '/_get_news_list_by_author_and_tags/';
    }
    else if (authorFilter != '0') {
        request = '/_get_news_list_by_author/';
    }
    else if (tagsFilter != '') {
        request = '/_get_news_list_by_tags/';
    } else {
        request = '/_get_news_list/';
    }
    $.post(request + page2, filter,
        function (data) {
            $(newsListCont).html(tmpNewsList.render({user: user, list: data.news_list}));
            var current_page = data.current_page;
            $('#newsListTable a').each(function (i) {
                $(this).on('click', function () {
                    drawNewsView($(this).prop('id'), current_page);
                });
            });
            paginate(data.num_pages, current_page);
            $(paginateCont).css('display', 'block');
        }
    );
}

function deleteNews() {
    var ids = [];
    $('#newsListTable input:checked').each(
        function () {
            ids.push($(this).val());
        }
    );
    var data = JSON.stringify({
        id: ids
    });
    console.log(data);
    $.post('/_del_news', data, function () {
        drawNewsList();
    })
}

function paginate(numPages, curPage) {
    var pagin = $('#paginateCont');
    pagin.empty();
    if (numPages > 1) {
        for (var i = 1; i <= numPages; i++) {
            if (i == curPage) {
                pagin.append(tmpPaginBtn.render({id: i, cls: ' current'}));
            } else {
                pagin.append(tmpPaginBtn.render({id: i}));
                $('#paginateCont a').on('click', function () {
                    var page = $(this).text();
                    if (page == undefined) {
                        page = '1';
                    }
                    var filter = JSON.stringify({
                        author: authorFilter,
                        tags: tagsFilter
                    });
                    var request = '';
                    if (authorFilter != '0' && tagsFilter != '') {
                        request = '/_get_news_list_by_author_and_tags/';
                    }
                    else if (authorFilter != '0') {
                        request = '/_get_news_list_by_author/';
                    }
                    else if (tagsFilter != '') {
                        request = '/_get_news_list_by_tags/';
                    } else {
                        request = '/_get_news_list/';
                    }
                    $.post(request + page, filter,
                        function (data) {
                            $(newsListCont).html(tmpNewsList.render({user: user, list: data.news_list}));
                            var curPg = data.current_page;
                            $('#newsListTable a').each(function (i) {
                                $(this).on('click', function () {
                                    drawNewsView($(this).prop('id'), curPg);
                                });
                            });
                            paginate(data.num_pages, curPg);
                        }
                    );
                });
            }
        }
    }
}

function drawLoginPage() {
    switchPage('loginPage');
    $(loginCont).html(tmpLoginPage.render());
    $('#loginForm').removeClass('loginError');
    $('#loginSubmit').on('click', function () {
        var form = $('#loginForm').serialize();
        $.post('/_login', form, function (data) {
            if (data.login == 'ok') {
                user = data.user;
                setCookie('user', user);
                $(loginCont).css('display', 'none');
                drawNavigation();
                drawNewsList();
            } else {
                $('#loginForm').addClass('loginError');
            }
        });
    });
}

function doLogout() {
    $.get('/_logout', function () {
        user = undefined;
        deleteCookie('user');
        drawNavigation();
        drawNewsList();
    });
}

function addComment(newsId, text) {
    if (text.length > 1) {
        var data = JSON.stringify({
            news_id: newsId,
            text: text
        });

        var new_id = '$$new$$';

        $('#commentText').val('');

        $.post('/_add_comment', data, function (resp) {
                var json = $.parseJSON(resp);
                new_id = json.new_id;
                // update new comment id
                $("#newsTable").html($("#newsTable").html().replace(/\$\$new\$\$/g, new_id));

            }
        );

        var $newComm = tmpAddComment.render({
            date: getToday(1),
            text: text,
            user: user,
            id: new_id,
            newsId: newsId
        });

        $('#newsTable tr.comments').last().after($($newComm));

        // increment comments counter in news list
        $('.commentsCounter span').each(function () {
            if ($(this).attr('idx') == newsId) {
                $(this).text(parseInt($(this).text()) + 1);
            }
        });

    }
}

function getToday(time) {

    var CurrentDate = new Date();
    var day = CurrentDate.getDate();
    var month = CurrentDate.getMonth() + 1;
    var year = CurrentDate.getFullYear();
    var hrs = CurrentDate.getHours();
    var min = CurrentDate.getMinutes();
    var sec = CurrentDate.getSeconds();
    if (month < 10)
        month = "0" + month;
    if (day < 10)
        day = "0" + day;
    if (time == undefined) {
        var today = day + "/" + month + "/" + year;
    } else {
        var today = day + "/" + month + "/" + year + ' ' + hrs + ':' + min;
    }
    return today;
}

function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options) {
    options = options || {};

    var expires = options.expires;

    if (typeof expires == "number" && expires) {
        var d = new Date();
        d.setTime(d.getTime() + expires * 1000);
        expires = options.expires = d;
    }
    if (expires && expires.toUTCString) {
        options.expires = expires.toUTCString();
    }

    value = encodeURIComponent(value);

    var updatedCookie = name + "=" + value;

    for (var propName in options) {
        updatedCookie += "; " + propName;
        var propValue = options[propName];
        if (propValue !== true) {
            updatedCookie += "=" + propValue;
        }
    }

    document.cookie = updatedCookie;
}

function deleteCookie(name) {
    setCookie(name, "", {
        expires: -1
    })
}
