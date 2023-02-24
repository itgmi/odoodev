odoo.define('custom_stock_view.stock_view', function (require) {
'use strict';
        var ajax = require('web.ajax');
        $("#search_input").on("keyup", function() {
          var value = $(this).val().toLowerCase();
          ajax.jsonRpc("/search/stock", 'call',{'value': value}).then(function (result){
            $('#search_stock').html(result)
            $('#selected_stock_div').css({'display': 'none'});
        })
        });
        $("#portal_stock_search").on("keyup", function() {
          var value = $(this).val().toLowerCase();
          ajax.jsonRpc("/search/portal/stock", 'call',{'value': value}).then(function (result){
            $('#stock_portal_search').html(result)
        })
        });
        $(document).on('click', '.stock_row', function () {
             $('.stock_row').removeClass('custom_selected')
             $(this).addClass('custom_selected');
             var id = this.dataset.value
             ajax.jsonRpc("/selected/stock", 'call',{'selected_id': id}).then(function (result){
                $('#selected_stock_div').css({'display': 'block'});
                $('#selected_stock_div').html(result)
            })
        });
        $(document).on('click', '#hide_display', function () {
                $('#selected_stock_div').css({'display': 'none'});
                $('.stock_row').removeClass('custom_selected')
        });
});