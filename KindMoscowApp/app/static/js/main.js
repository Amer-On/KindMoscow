$(document).ready(function () {
    var sections = $('section');
    var navElem = $('.header-nav__elem');
    var profileContainer = $('.header-profile'), profile = $('.header-profile__icon'), headerDrop = $('.header-profile__dropmenu');
    
    $(document).mouseover(function(e){
        e.preventDefault();
        if(profileContainer.has(e.target).length == 1){
            profile.addClass('header-profile__icon_active');
            headerDrop.addClass('header-profile__dropmenu_active');
        }
        else{
            profile.removeClass('header-profile__icon_active');
            headerDrop.removeClass('header-profile__dropmenu_active');
        }
    });

    $(window).scroll(function(e){
        e.preventDefault();
        var cur_pos = $(this).scrollTop();
        var scroll = getCurrentScroll();
        if(scroll > $('.header').height() * 3){
           $('.header').addClass('header_active');
        }
        else if(scroll <= $('.header').height()){
           $('.header').removeClass('header_active');
        }
  
        function getCurrentScroll() {
           return window.pageYOffset || document.documentElement.scrollTop;
        }
     });

    navElem.each(function(){
        if($(this).attr('id') == sections.attr('class')){
            $(this).addClass('header-nav__elem_active');
        }
    });
    if(sections.hasClass('profile')){
        var password = $('#password'), passwordRepeat = $('#passwordrepeat'), formSubmit = $('.profile-safety__submit'), formWrapper = $('.profile-safety__password');
        $('.header-sign__btn').addClass('header-sign__btn_active');
        passwordRepeat.on('input', function(){
            if(password.val()){
                if($(this).val() != password.val()){
                    formWrapper.addClass('profile-safety__password_wrong');
                    formSubmit.prop('disabled', true);
                }
                else{
                    formWrapper.removeClass('profile-safety__password_wrong');
                    formSubmit.prop('disabled', false);
                }
            }
            if(!passwordRepeat.val() && !password.val()){
                formWrapper.removeClass('profile-safety__password_wrong');
            }
        });
        password.on('input', function(){
            if(passwordRepeat.val()){
                if($(this).val() != passwordRepeat.val()){
                    formWrapper.addClass('profile-safety__password_wrong');
                    formSubmit.prop('disabled', true);
                }
                else{
                    formWrapper.removeClass('profile-safety__password_wrong');
                    formSubmit.prop('disabled', false);
                }
            }
            if(!passwordRepeat.val() && !password.val()){
                formWrapper.removeClass('profile-safety__password_wrong');
            }
        });
    }
    if(sections.hasClass('forAuthorization')){
        var password = $('#password'), passwordRepeat = $('#passwordrepeat'), formSubmit = $('input[type=submit]'), formWrapper = $('.form-wrapper');
        $('.header-sign__btn').addClass('header-sign__btn_active');
        passwordRepeat.on('input', function(){
            if(password.val()){
                if($(this).val() != password.val()){
                    formWrapper.addClass('password_wrong');
                    formSubmit.prop('disabled', true);
                }
                else{
                    formWrapper.removeClass('password_wrong');
                    formSubmit.prop('disabled', false);
                }
            }
            if(!passwordRepeat.val() && !password.val()){
                formWrapper.removeClass('password_wrong');
            }
        });
        password.on('input', function(){
            if(passwordRepeat.val()){
                if($(this).val() != passwordRepeat.val()){
                    formWrapper.addClass('password_wrong');
                    formSubmit.prop('disabled', true);
                }
                else{
                    formWrapper.removeClass('password_wrong');
                    formSubmit.prop('disabled', false);
                }
            }
            if(!passwordRepeat.val() && !password.val()){
                formWrapper.removeClass('password_wrong');
            }
        });
    }
    if(sections.hasClass('hero')){
        var date = $('input#date');
        $('.event-wrapper').slick({
            speed: 1000
        });
        $('.news-wrapper').slick({
            speed: 1000
        });
        date.on('focus', function(){
            date.attr('type', 'date');
            date.css({'padding':'8px 0'});
        });
        date.on('blur', function(){
            if(!$(this).val()){
                date.attr('type', 'text');
                date.css({'padding':'10px 0'});
            }
        });
    }
    if(sections.hasClass('events')){
        var date = $('input#date');
        date.on('focus', function(){
            date.attr('type', 'date');
            date.css({'padding':'8px 0'});
        });
        date.on('blur', function(){
            if(!$(this).val()){
                date.attr('type', 'text');
                date.css({'padding':'10px 0'});
            }
        });
        $('.evlist-filter__btn').click(function(e){
            e.preventDefault();
            if($('.evlist-filter__form').hasClass('evlist-filter__form_active')){
                $('.evlist-filter__form').removeClass('evlist-filter__form_active');
            }
            else{
                $('.evlist-filter__form').addClass('evlist-filter__form_active');
            }
        });
        $(document).click(function(e){
            if($(e.target).closest('.evlist-filter__form').length || $(e.target).closest('.evlist-filter__btn').length){
                return;
            }
            $('.evlist-filter__form').removeClass('evlist-filter__form_active');
        });
    }
    if(sections.hasClass('addEvent')){
        var date = $('input#date'), dateContainer = $('.form-group__date');
        date.on('focus', function(){
            date.attr('type', 'date');
            dateContainer.css({'padding':'1.75rem 1.9rem'});
        });
        date.on('blur', function(){
            if(!$(this).val()){
                date.attr('type', 'text');
                dateContainer.css({'padding':'1.9rem'});
            }
        });
        $(function() {
            $( "#slider-range" ).slider({
              range: true,
              min: 14,
              max: 90,
              values: [ 18, 35 ],
              slide: function(event, ui){
                $('#from').val(ui.values[0]);
                $('#until').val(ui.values[1]);
                }
            });
        });
        $('#from').val(18);
        $('#until').val(35);
        $('#from').on('input', function(){
            var val1 = $(this).val(), val2 = $('#until').val();
            if(val1>=$('#until').val()){
                val1 = $('#until').val();
                $(this).val($('#until').val());
            }
            $( "#slider-range" ).slider({
                range: true,
                min: 14,
                max: 90,
                values: [ val1, val2 ],
              });
        });
        $('#until').on('input', function(){
            var val2 = $(this).val(), val1 = $('#from').val();
            if(val2<=$('#from').val()){
                val2 = $('#from').val();
                $(this).val($('#from').val());
            }
            $( "#slider-range" ).slider({
                range: true,
                min: 14,
                max: 90,
                values: [ val1, val2 ],
              });
        });
    }
    if(sections.hasClass('profile')){
        var labels = $('.checks-label'), inputs = $('.checks-input'), forms = $('.profile-form'), sidebar = $('.profile-sidebar'), date = $('#birthday'), dateContainer = $('.profile-form__date');
        inputs.on('input', function(){
            inputs.each(function(index){
                if($(inputs[index]).is(':checked')){
                    $(labels[index]).addClass('checks-label_active');
                }
                else{
                    $(labels[index]).removeClass('checks-label_active');
                }
            });
        });
        $(window).scroll(function(e){
            e.preventDefault();
            var cur_pos = $(this).scrollTop(), scroll = getCurrentScroll();
            forms.each(function(){
                var top = $(this).offset().top - sidebar.height(), bottom = top + $(this).height();
                if(cur_pos >= top && cur_pos <= bottom){
                    sidebar.find('a').removeClass('profile-sidebar__elem_active');
                    sidebar.find('a[href="#'+$(this).attr('id')+'"]').addClass('profile-sidebar__elem_active');
                }
            });
            function getCurrentScroll(){
                return window.pageYOffset || document.documentElement.scrollTop;
            }
        });
        $('a[href^="#"').on('click', function(e){
            e.preventDefault();
            var id = $(this).attr('href'), top = $(id).offset().top;
            $('html, body').animate({scrollTop: top - sidebar.height()/2}, 600);
        });
        date.on('focus', function(){
            date.attr('type', 'date');
        });
        date.on('blur', function(){
            if(!$(this).val()){
                date.attr('type', 'text');
            }
        });
    }
    if(sections.hasClass('fororg')){
        var statusGrade = $('.fororg-status__grade'), statusProgress = $('.fororg-status__progress'),
        tabButton = $('.fororg-tabs__item'), tabItem = $('.fororg-wrapper__item');
        statusGrade.each(function(index){
            $(statusProgress[index]).val($(statusGrade[index]).text());
        });
        tabButton.click(function(){
            var id = $(this).attr('data-tab'), content = $('.fororg-wrapper__item[data-tab="' + id + '"]');
            $('.fororg-tabs__item_active').removeClass('fororg-tabs__item_active');
            $(this).addClass('fororg-tabs__item_active');
            tabItem.each(function(index){
                $(this).removeClass('fororg-wrapper__item_active');
            });
            content.addClass('fororg-wrapper__item_active');
        });
    }
    if(sections.hasClass('aboutev')){
        var tabButton = $('.aboutev-tabs__item'), tabItem = $('.aboutev-content');
        tabButton.click(function(){
            var id = $(this).attr('data-tab'), content = $('.aboutev-content[data-tab="' + id + '"]');
            $('.aboutev-tabs__item_active').removeClass('aboutev-tabs__item_active');
            $(this).addClass('aboutev-tabs__item_active');
            tabItem.each(function(index){
                $(this).removeClass('aboutev-content_active');
            });
            content.addClass('aboutev-content_active');
        });
    }
    if(sections.hasClass('volev')){
        var statusGrade = $('.volev-status__grade'), statusProgress = $('.volev-status__progress'),
        tabButton = $('.volev-tabs__item'), tabItem = $('.volev-wrapper__item');
        statusGrade.each(function(index){
            $(statusProgress[index]).val($(statusGrade[index]).text());
        });
        tabButton.click(function(){
            var id = $(this).attr('data-tab'), content = $('.volev-wrapper__item[data-tab="' + id + '"]');
            $('.volev-tabs__item_active').removeClass('volev-tabs__item_active');
            $(this).addClass('volev-tabs__item_active');
            tabItem.each(function(index){
                $(this).removeClass('volev-wrapper__item_active');
            });
            content.addClass('volev-wrapper__item_active');
        });
    }
    if(sections.hasClass('forvol')){
        tabButton = $('.forvol-tabs__item'), tabItem = $('.forvol-content__item');
        tabButton.click(function(){
            var id = $(this).attr('data-tab'), content = $('.forvol-content__item[data-tab="' + id + '"]');
            $('.forvol-tabs__item_active').removeClass('forvol-tabs__item_active');
            $(this).addClass('forvol-tabs__item_active');
            tabItem.each(function(index){
                $(this).removeClass('forvol-content__item_active');
            });
            content.addClass('forvol-content__item_active');
        });
    }
    if(sections.hasClass('courses')){
        var items = $('.courses-card');
        items.click(function(){
            items.each(function(index){
                $(items[index]).removeClass('courses-card_active');
            });
            $(this).addClass('courses-card_active');
        });
    }
});