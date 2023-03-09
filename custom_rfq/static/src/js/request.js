odoo.define('custom_rfq.request', function (require) {
       "use strict";
       var rpc = require('web.rpc')
       var clipboard_toast = $('.request_toast')
       var clipboard_toast_cart = $('.request_toast_cart')
       $(document).ready(function() {
       $(document).on('click', '.request_quote_request_user', function(){
            var product = $(".product_id_request_user").val();
            var website = $(".website_request_user").val();
            rpc.query({
                       route: '/request/quote/user',
                       params: {product: product, website: website},
                   })
            clipboard_toast.addClass('show')
        });
       $(document).on('click', '.request_quote_request', function(){
            $('#hidden_box_request').css('display', 'flex');
        });
        $(document).on('click', '#cancel_request', function(cancel){
            cancel.preventDefault();
            $('#hidden_box_request').css('display', 'none');
        });
        $(document).on('click', '.request_toast_close', function(){
            clipboard_toast.removeClass('show')
        });
       $(document).on('click', '#submit_request', function(submission){
            submission.preventDefault();
            var website = $(".website_request").val();
            var product = $(".product_id_request").val();
            var name = $("#name_request").val();
            var email = $("#email_request").val();
            var phone = $("#phone_request").val();
            var price_list_id = $(".price_list_id").val();
            var price_list_name = $(".price_list_name").val();
            if (name && email && phone){
            var val = []
            val.push({
                'website': website,
                'product': product,
                'name': name,
                'email': email,
                'phone': phone,
                'price_list_id': price_list_id,
                'price_list_name': price_list_name,
            })
            rpc.query({
                       route: '/request/quote',
                       params: {vals: val},
                   })
            $('#hidden_box_request').css('display', 'none');
            clipboard_toast.addClass('show')
            }
        else{
            alert("Fill All Details");
        }
        });
        $(document).on('click', '.request_quote_request_cart_user', function(){
            var lines = $(".product_id_request_cart_user").val();
            var website = $(".website_request_cart_user").val();
            rpc.query({
                       route: '/request/quote/cart/user',
                       params: {lines: lines, website: website},
                   })
            clipboard_toast_cart.addClass('show')
        });
        $(document).on('click', '.request_quote_request_cart', function(){
            $('#hidden_box_request_cart').css('display', 'flex');
        });
        $(document).on('click', '#cancel_request_cart', function(cancel){
            cancel.preventDefault();
            $('#hidden_box_request_cart').css('display', 'none');
        });
        $(document).on('click', '.request_toast_close_cart', function(){
            clipboard_toast_cart.removeClass('show')
        });
        $(document).on('click', '#submit_request_cart', function(submission){
            submission.preventDefault();
            var website = $(".website_request_cart").val();
            var product = $(".product_id_request_cart").val();
            var name = $("#name_request_cart").val();
            var email = $("#email_request_cart").val();
            var phone = $("#phone_request_cart").val();
            var price_list_id = $(".price_list_id_cart").val();
            var price_list_name = $(".price_list_name_cart").val();
            if (name && email && phone){
            var val = []
            val.push({
                'website': website,
                'product': product,
                'name': name,
                'email': email,
                'phone': phone,
                'price_list_id': price_list_id,
                'price_list_name': price_list_name,
            })
            rpc.query({
                       route: '/request/quote/cart',
                       params: {vals: val},
                   })
            $('#hidden_box_request_cart').css('display', 'none');
            clipboard_toast_cart.addClass('show')
            }
        else{
            alert("Fill All Details");
        }
        });
        });
});
